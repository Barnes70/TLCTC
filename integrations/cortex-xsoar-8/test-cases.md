# Test Cases — XSOAR 8.x + XSIAM

Five canonical scenarios. Each verifies a specific TLCTC classification rule.
Behaviour is identical to the 6.2 build; only the install path differs. Run
these in order after a successful smoke test (see `deploy.md` step 6).

For each test:

1. Inject a synthetic alert with the listed `attack.technique.id` value(s).
2. Confirm `TLCTC Cluster` is set to **Expected Cluster** within 5 s.
3. Confirm the `TLCTCSequence` label matches **Expected Sequence**.
4. Confirm the listed playbooks fire in order.
5. On close, confirm the emitted `TLCTC Attack Path (Layer 3)` validates
   against `json-schemas/layer-3/tlctc-attack-path.schema.json`.

---

## TC-1 — T1566.001 Spearphishing Attachment (Axiom VI + R-EXEC)

| | |
|---|---|
| Input techniques | `T1566.001` |
| Expected cluster | `#9` |
| Expected sequence | `#9, #7` |
| Playbooks fired | `TLCTC-Dispatch` → `TLCTC-09-SocialEngineering` → `TLCTC-07-Malware` |
| `tlctcfecexecuted` | `true` |
| Boundary required | Yes — `||[human][@External→@Org]||` |

**Why this matters:** ATT&CK conflates the lure and execution into one
technique. TLCTC requires two steps. The integration must split them and fire
both playbooks; the FEC execution (#7) records `fec_executed: true`.

---

## TC-2 — T1078 Valid Accounts (R-CRED)

| | |
|---|---|
| Input techniques | `T1078` |
| Expected cluster | `#4` |
| Expected sequence | `#4` |
| Playbooks fired | `TLCTC-Dispatch` → `TLCTC-04-IdentityTheft` |
| Boundary required | No |

**Why this matters:** Credential APPLICATION is always #4 regardless of how
the credential was obtained. If a separate alert with T1003 (credential
dumping) also exists, that fires #1 separately — different steps.

---

## TC-3 — T1190 Public-Facing Application Exploit (R-ROLE)

| | |
|---|---|
| Input techniques | `T1190` |
| Expected cluster | `#2` |
| Expected sequence | `#2` |
| Playbooks fired | `TLCTC-Dispatch` → `TLCTC-02-ExploitingServer` |

**Why this matters:** R-ROLE classifies by the role of the flawed component
relative to the attacker. A public-facing app is server-role → #2. The same
flaw class in a browser would be #3. The integration must not collapse to
"web attack" or similar outcome label.

---

## TC-4 — T1195.002 Software Supply Chain Compromise (R-SUPPLY)

| | |
|---|---|
| Input techniques | `T1195.002` |
| Expected cluster | `#10` |
| Expected sequence | `#10` |
| Playbooks fired | `TLCTC-Dispatch` → `TLCTC-10-SupplyChain` |
| Boundary required | Yes — `||[update][@Vendor→@Org]||` or `||[dev][@Vendor→@Org]||` |

**Why this matters:** #10 is placed at the Trust Acceptance Event. The
boundary field MUST be populated. The RS Container's regulatory branches
fire if DRE includes Confidentiality on PII (GDPR) or severity ≥ 3 (NIS2).

---

## TC-5 — T1059.001 PowerShell (R-EXEC + Axiom VI split)

| | |
|---|---|
| Input techniques | `T1059.001` |
| Expected cluster | `#1` (primary, since #1 precedes) |
| Expected sequence | `#1, #7` |
| Playbooks fired | `TLCTC-Dispatch` → `TLCTC-01-AbuseOfFunctions` → `TLCTC-07-Malware` |
| `tlctcfecexecuted` | `true` |

**Why this matters:** PowerShell.exe is a designed Windows tool (#1). The
encoded script it runs is FEC (#7). Per Axiom VI both steps must be recorded;
per R-EXEC the #7 step records `fec_executed: true`. ATT&CK gives one
technique; TLCTC gives two steps.

---

## Acceptance criteria

All five test cases must pass before the pack is promoted to production.
Failures indicate either the lookup list is stale or one of the classification
rules in `Scripts/script-TLCTCClassify/TLCTCClassify.py` is incorrectly
implemented.

The Layer 3 emit step on close must produce a JSON instance that passes:

```bash
ajv validate \
  -s json-schemas/layer-3/tlctc-attack-path.schema.json \
  -d <emitted-path>.json
```
