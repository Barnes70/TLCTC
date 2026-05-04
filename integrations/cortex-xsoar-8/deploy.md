# Deployment Runbook — XSOAR 8.x + XSIAM

End-to-end install via `demisto-sdk`. Total time: ~20 minutes (most spent on
first-run Docker image pulls during `lint`).

---

## 0. Prerequisites

- Workstation with Python 3.10+ and Docker.
- A target tenant: **Cortex XSOAR 8.x** (cloud or on-prem) **or** **Cortex XSIAM**.
- API key with `Admin` role on the tenant.
- This repo cloned locally.

## 1. Install demisto-sdk

```bash
pip install demisto-sdk
demisto-sdk --version    # confirm it runs
```

## 2. Configure environment

Set these env vars for the tenant you're targeting:

```bash
# XSOAR 8.x
export DEMISTO_BASE_URL=https://<tenant>.crtx.us.paloaltonetworks.com
export DEMISTO_API_KEY=<api-key>
export DEMISTO_API_KEY_ID=<key-id>     # required on 8.x; not used on 6.x
export XSIAM_AUTH_ID=<auth-id>         # XSIAM only

# Verify connectivity
demisto-sdk auth-validate
```

## 3. Validate the pack (offline)

```bash
cd integrations/cortex-xsoar-8

# Lint Python automations (pulls demisto/python3:3.11.10 if not cached)
demisto-sdk lint -i Scripts/script-TLCTCClassify
demisto-sdk lint -i Scripts/script-TLCTCEmitLayer3

# Validate every object against pack rules
demisto-sdk validate --no-conf-json -i .

# Auto-format any nits the linter wants fixed
demisto-sdk format -i .
```

Expected: zero validation errors. Warnings about test playbooks are acceptable
for community packs.

## 4. Build a zipped Content Pack

```bash
demisto-sdk zip-packs -i . -o ./dist
ls dist/   # -> TLCTC.zip
```

## 5. Install on the tenant

### Option A — Marketplace upload (UI)

1. Open the tenant.
2. **Marketplace → Manage → Upload** → select `dist/TLCTC.zip` → Upload.
3. Open the `TLCTC` pack page and click **Install**.

### Option B — `demisto-sdk upload` (CLI)

```bash
demisto-sdk upload -i .
```

This pushes every object to the tenant in the correct order. Use for fast
iteration during dev; for production prefer the zip + Marketplace path because
it produces an audit record.

## 6. Smoke test (matches `test-cases.md` TC-1)

1. Tenant UI → **Incidents → New** → Type: `TLCTC Threat`.
2. Set `ATT&CK Techniques: T1566.001`. Save.
3. Within 5 s confirm:
   - `TLCTC Cluster` = `#9`
   - `TLCTC Operational ID` = `TLCTC-09.00`
   - `TLCTC FEC Executed` = `true`
   - Investigation timeline shows: `TLCTC-Dispatch → TLCTC-09-SocialEngineering → TLCTC-07-Malware`.
4. Set `TLCTC DRE Outcomes = C`, add tag `pii`, set severity `High`. Close.
5. Re-open and verify the **Attack Path (Layer 3)** tab contains a JSON
   instance with two steps (`#9` then `#7`), `fec_executed: true` on step 2,
   `outcomes: ["C"]`.
6. Validate the emitted JSON externally:
   ```bash
   ajv validate \
     -s json-schemas/layer-3/tlctc-attack-path.schema.json \
     -d /tmp/emitted-path.json
   ```

If all 6 checks pass, run the remaining cases in `test-cases.md`.

## 7. Wire up your alert source

The `attck-tlctc-mapper` expects inbound alerts to expose
`alert.attack.technique[].id` (T-numbers). For Cortex XDR / XSIAM-native
alerts, this is already populated. For 3rd-party SIEM/EDR feeders, edit the
mapper's `internalMapping` to point to the correct source path.

## 8. Rollback

```bash
demisto-sdk delete-pack -i TLCTC --force
```

Or via UI: **Marketplace → Manage → TLCTC → Uninstall**. All custom fields,
incident type, layout, classifier, automations, and playbooks are removed.

## 9. Maintenance

- The lookup list (`Lists/list-attck-tlctc-lookup.json`) is the only object
  with a maintenance cadence. Regenerate from
  `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json` when ATT&CK
  ships an upstream update.
- Bump `currentVersion` in `pack_metadata.json` and add a `ReleaseNotes/` entry
  for every published change.
- Custom field `cliName` values are baked into playbooks and automations.
  **Do not** rename them after install — it will break existing incidents.
