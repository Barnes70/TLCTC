# TLCTC Cortex XSOAR 6.2 — Deployment Runbook

End-to-end install for a fresh XSOAR 6.2 tenant. Total time: ~45 minutes.

---

## 0. Prerequisites

- XSOAR 6.2.x tenant (on-prem or cloud).
- Account with **Administrator** role (needed to create custom fields, scripts,
  and incident types).
- Python 3 on a workstation for local validation (`pip install ajv-cli` or
  `npm install -g ajv-cli` for schema validation in test step).
- Network reachable to `demisto/python3:3.10` Docker image.
- This integration directory cloned to your workstation.

## 1. Roles and permissions

Create or confirm the following roles exist:

| Role | Required for |
|---|---|
| Administrator | Steps 2–5 (create fields, types, scripts) |
| `DBotWeakRole` | Runtime for `TLCTCClassify` and `TLCTCEmitLayer3` automations |
| `Analyst` | Investigates incidents; can edit Layer 3 path before close |

If `DBotWeakRole` does not exist, create it with read-only access plus
`setIncident` permission.

## 2. Import order — strict

Each step depends on the previous. Do not reorder.

### Step 2.1 — Lookup list

`Settings → Advanced → Lists → New`
- Name: `attck-tlctc-lookup`
- Type: `JSON`
- Content: paste contents of `lists/attck-tlctc-lookup.json`
- Save.

### Step 2.2 — Custom incident fields

`Settings → Advanced → Fields → Upload`
- Upload `incident-fields/tlctc-fields.json`
- Verify all 10 fields appear with `tlctc...` cliName prefix.

### Step 2.3 — Incident type

`Settings → Object Setup → Incidents → Types → Upload`
- Upload `incident-types/tlctc-threat.json`
- Open the new type and verify `preProcessingScript = TLCTCClassify`,
  `closureScript = TLCTCEmitLayer3` (these scripts don't exist yet — XSOAR will
  show a warning; resolved in step 2.5).

### Step 2.4 — Layout

`Settings → Object Setup → Incidents → Layouts → Upload`
- Upload `layouts/tlctc-threat-layout.json`
- Open the layout and verify both tabs render.

### Step 2.5 — Automations

`Settings → Advanced → Scripts → Upload`
- Upload `automations/TLCTCClassify.yml`
- Upload `automations/TLCTCEmitLayer3.yml`
- Re-open the incident type from 2.3 — warnings should clear.

### Step 2.6 — Classifier and mapper

`Settings → Object Setup → Classification & Mapping`
- New classifier → Upload `classifiers/attck-tlctc-classifier.json`
- New mapper → Upload `classifiers/attck-tlctc-mapper.json`
- Attach both to your inbound integration instance (XDR/SIEM/EDR feeder).

### Step 2.7 — Sub-playbooks (must precede master playbooks)

`Playbooks → Upload`
1. `playbooks/sub-velocity-router.yml`
2. `playbooks/sub-rs-container.yml`

### Step 2.8 — Dispatch playbook

`Playbooks → Upload`
- `playbooks/TLCTC-Dispatch.yml`
- This is the default playbook for the `TLCTC Threat` incident type.

### Step 2.9 — 10 master playbooks

`Playbooks → Upload` (one at a time):
- `playbooks/TLCTC-01-AbuseOfFunctions.yml` … `playbooks/TLCTC-10-SupplyChain.yml`

After upload, run `Playbooks → Validate` against each — all must pass.

## 3. Smoke test

1. Manually create a new incident: `Incidents → New → Type: TLCTC Threat`.
2. In the incident form, set:
   - `ATT&CK Techniques`: `T1566.001`
3. Save.
4. Within 5 seconds confirm:
   - `TLCTC Cluster` shows `#9`.
   - `TLCTC Operational ID` shows `TLCTC-09.00`.
   - `TLCTC FEC Executed` is `true`.
   - The investigation timeline shows `TLCTC-Dispatch → TLCTC-09-SocialEngineering`.
   - A second cluster fires: `TLCTC-07-Malware` (the FEC follow-on step).
5. Set `TLCTC DRE Outcomes = C`, add tag `pii`, set severity to `High`, then close the incident.
6. Re-open the incident and inspect `TLCTC Attack Path (Layer 3)` — must contain a valid Layer 3 JSON instance with two steps (`#9` then `#7`), `fec_executed: true` on step 2, and `outcomes: ["C"]`.

If all 6 checks pass, proceed to full test cases (`test-cases.md`).

## 4. Production wire-up

Connect your inbound feeders (XDR, EDR, SIEM) to use the `attck-tlctc-classifier`
+ `attck-tlctc-mapper` pair. Verify their outbound payload includes
`alert.attack.technique[].id` (or remap inside the mapper if your feed uses a
different field name).

## 5. Rollback

If anything misbehaves and you need to revert:

1. Disable the classifier on each inbound integration instance (Object Setup →
   Classification & Mapping → unlink from instance).
2. Switch the `TLCTC Threat` incident type's `Default Playbook` to "None".
3. Existing incidents remain readable; no new ones will auto-route.

To fully remove: delete in **reverse** of step 2 order — playbooks → mapper /
classifier → automations → layout → incident type → incident fields → list.

## 6. Maintenance

- The lookup list is the only file that needs periodic regeneration. Source of
  truth: `mappings/mitre-attack-enterprise/tlctc-enterprise-attack.json`.
  Re-export and re-upload the list whenever ATT&CK is updated upstream
  (typically twice yearly).
- TLCTC framework JSON (`json-schemas/layer-1/tlctc-framework.v2.3.json`) is
  immutable per project policy. Cluster IDs and operational IDs in the
  integration map 1:1 to that file — no maintenance needed unless the framework
  version changes.
- Custom field IDs are baked into the playbooks and automations. Do **not**
  rename them after install.
