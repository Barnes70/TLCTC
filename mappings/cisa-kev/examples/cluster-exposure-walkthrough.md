# Walkthrough: Vendor-Stack → TLCTC Exposure Profile

**Scenario.** An organisation runs Microsoft, Cisco, and Fortinet products. Leadership asks: *"Given what CISA says is under active attack in 2026-Q1, where is our exposure concentrated?"*

This walkthrough shows how to read the answer out of `tlctc-kev.json`.

---

## Step 1 — Filter

```python
import json
kev = json.load(open("tlctc-kev.json"))

vendors = {"Microsoft", "Cisco", "Fortinet"}
q1_2026 = [
    e for e in kev["entries"]
    if e["dateAdded"] >= "2026-01-01"
    and e["dateAdded"] <  "2026-04-01"
    and e["vendorProject"] in vendors
]
# 17 entries
```

17 CVEs landed in the KEV catalog during 2026-Q1 across these three vendors.

## Step 2 — Check derivation coverage FIRST

Always check `derivationStatus` before reading cluster counts — aggregates hide missing data.

| Status | Count | What it means |
|--------|-------|---------------|
| `ok` | 11 | Cluster confidently derived |
| `cwe-too-abstract` | 4 | CWE-20 class; no cluster derivable without CVE-level analysis |
| `cwe-missing` | 1 | KEV entry carries no CWE |
| `cwe-unmapped-in-tlctc` | 1 | CWE not in the TLCTC mapping |

**6 out of 17 (35%) need manual follow-up.** This is normal — recent/high-profile CVEs disproportionately enter KEV before NVD finishes its CWE analysis, and vendor-specific CWEs are often overly abstract. Record the 6 as "derivation-pending" rather than treating them as zero exposure.

## Step 3 — Cluster breakdown (OK records only)

| Cluster | Count | Typical examples |
|---------|-------|------------------|
| **`#2` Exploiting Server** | 7 | Cisco FMC deserialization, SharePoint input validation, Cisco SD-WAN RCE |
| **`#1` Abuse of Functions** | 3 | Windows privilege features being used as designed in unintended ways |
| **`#3` Exploiting Client** | 1 | Office/Edge document-triggered RCE |

The exposure concentrates in `#2`. Two things this tells you:

1. **Your patch cadence for internet-facing appliances and server software is the dominant risk lever this quarter.** Edge devices (FMC, SD-WAN controllers) and server-side applications (SharePoint) are where active exploitation is happening.
2. **Client-side posture is not the current bottleneck for this vendor stack.** This does not mean "no client risk" — it means *active weaponization* is server-weighted. Static CWE counts would have told you a different story.

## Step 4 — Inspect a single entry

```json
{
  "cveID": "CVE-2026-20131",
  "vendorProject": "Cisco",
  "product": "Secure Firewall Management Center (FMC)",
  "dateAdded": "2026-03-19",
  "sourceCwes": ["CWE-502"],
  "derivedMappingExpression": "#2 | #3",
  "primaryCluster": "#2",
  "clusterSet": ["#2", "#3"],
  "confidence": "Allowed",
  "derivationStatus": "ok",
  "contextResolvedBy": "product-heuristic",
  "contextHeuristicNotes": "FMC is a management server — server role."
}
```

**Reading this row, left to right:**

- CWE-502 (Deserialization of Untrusted Data) maps to `#2 | #3` in TLCTC because deserialization flaws are role-dependent.
- The product-role heuristic saw `Cisco :: Secure Firewall Management Center (FMC)` and fired the "FMC is a management server" rule → `primaryCluster = #2`.
- `clusterSet` still reports `["#2", "#3"]` — useful if you want to ask "which clusters does this CVE *touch*?", but the canonical answer is `#2`.

## Step 5 — Translate to action

| Cluster | What "active exploitation" means for your controls |
|---------|----------------------------------------------------|
| `#2` | Patch internet-facing services. Validate network segmentation of management planes. Check telemetry for exploitation attempts against the specific CVEs. |
| `#1` | Review the privilege/feature being abused — is your configuration defended in depth, or does a single misuse cascade? |
| `#3` | Attack surface is the endpoint client — patch browser/office suites, review attachment handling policy. |

The 6 "derivation-pending" entries need CVE-level analysis before they slot into this table. Start with their `shortDescription` field and the vendor advisory linked in KEV's `notes`.

## Step 6 — Don't skip the confidence column

```python
low_conf = [e for e in q1_2026 if e.get("confidence") == "Allowed-with-Review"]
```

`Allowed-with-Review` means the source CWE's TLCTC mapping was flagged as context-dependent. If you're making a prioritisation call on a specific `Allowed-with-Review` row (e.g., Cisco SD-WAN CVE-2022-20775), re-read the source CWE's `mappingRationale` in [`mappings/mitre-cwe/tlctc-cwe.json`](../../mitre-cwe/tlctc-cwe.json) and confirm the chosen cluster matches the actual exploitation pattern described in the CVE advisory.

## Summary

The KEV mapping is a **signal**, not a dashboard. Use it to:

- See which TLCTC clusters are under active weaponization *right now*.
- Compare against your own control posture (which clusters are you strongest/weakest on?).
- Weight vulnerability management effort by what attackers are *actually using*, not just what's patchable.

It is **not** a replacement for CVE-level triage. Every row links back to a source CVE + CWE; click through before acting on a specific vulnerability.
