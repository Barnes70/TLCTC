"""TLCTCClassify -- preProcessingScript for the TLCTC Threat incident type.

Reads incident_tlctcattcktechniques (list of ATT&CK technique IDs) and applies
the attck-tlctc-lookup list to derive:

  - incident_tlctccluster          (primary strategic cluster, e.g. '#9')
  - incident_tlctcoperationalid    (e.g. 'TLCTC-09.00')
  - incident_tlctcvelocityclass    (derived from incident_tlctcdeltat if present)
  - incident_tlctcfecexecuted      (true if any technique sequence ends in #7)

Enforces classification rules:

  - Axiom VI (Single-Cluster Rule): multi-step techniques (e.g. T1566.001 ->
    ['#9','#7']) record the FIRST cluster as primary and write the full
    sequence into incident.labels for downstream playbook chaining.
  - R-EXEC: if any technique sequence ends in #7, fec_executed is set true.
  - R-CRED: T1078, T1550, T1021.* always classify as #4 (the lookup encodes
    this -- credential APPLICATION is always #4 regardless of acquisition).

Layer 3 emission is performed at close by TLCTCEmitLayer3.
"""
import json
import re

import demistomock as demisto
from CommonServerPython import return_results


STRATEGIC_TO_OPERATIONAL = {
    "#1": "TLCTC-01.00", "#2": "TLCTC-02.00", "#3": "TLCTC-03.00",
    "#4": "TLCTC-04.00", "#5": "TLCTC-05.00", "#6": "TLCTC-06.00",
    "#7": "TLCTC-07.00", "#8": "TLCTC-08.00", "#9": "TLCTC-09.00",
    "#10": "TLCTC-10.00",
}

DELTA_T_RE = re.compile(
    r"^(instant|\?|~?(\d+)(ms|s|m|h|d|w|mo|y)|[<>]=?(\d+)(ms|s|m|h|d|w|mo|y))$"
)


def delta_t_to_seconds(dt):
    """Map a Δt string to a coarse seconds value for VC bucketing."""
    if not dt or dt in ("?", "instant"):
        return 0 if dt == "instant" else None
    m = re.match(r"^[<>]?=?~?(\d+)(ms|s|m|h|d|w|mo|y)$", dt)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2)
    mult = {
        "ms": 0.001, "s": 1, "m": 60, "h": 3600,
        "d": 86400, "w": 604800, "mo": 2592000, "y": 31536000,
    }[unit]
    return n * mult


def velocity_class(seconds):
    if seconds is None:
        return None
    if seconds < 60:
        return "VC-4"
    if seconds < 3600:
        return "VC-3"
    if seconds < 86400:
        return "VC-2"
    return "VC-1"


def main():
    incident = demisto.incident()
    cf = incident.get("CustomFields", {}) or {}

    techniques = cf.get("tlctcattcktechniques") or []
    if isinstance(techniques, str):
        techniques = [t.strip() for t in techniques.split(",") if t.strip()]

    raw = demisto.executeCommand("getList", {"listName": "attck-tlctc-lookup"})
    lookup_str = raw[0].get("Contents") if raw and isinstance(raw, list) else None
    try:
        lookup = json.loads(lookup_str) if lookup_str else {}
    except Exception:
        lookup = {}

    sequence = []
    fec_executed = False

    for tid in techniques:
        entry = lookup.get(tid) or lookup.get(tid.split(".")[0])
        if not entry:
            continue
        for cluster in entry.get("sequence", []):
            if sequence and sequence[-1] == cluster:
                continue
            sequence.append(cluster)
            if cluster == "#7":
                fec_executed = True

    if not sequence:
        return_results({
            "warning": "No TLCTC mapping derived. Manual classification required."
        })
        return

    primary = sequence[0]
    ops_id = STRATEGIC_TO_OPERATIONAL.get(primary, "")

    dt = cf.get("tlctcdeltat")
    vc = velocity_class(delta_t_to_seconds(dt)) if dt else None

    updates = {
        "tlctccluster": primary,
        "tlctcoperationalid": ops_id,
        "tlctcfecexecuted": fec_executed,
    }
    if vc:
        updates["tlctcvelocityclass"] = vc

    demisto.executeCommand("setIncident", {"customFields": json.dumps(updates)})

    demisto.executeCommand("setIncident", {
        "labels": json.dumps([{"type": "TLCTCSequence", "value": ",".join(sequence)}])
    })

    return_results({
        "primary_cluster": primary,
        "operational_id": ops_id,
        "full_sequence": sequence,
        "fec_executed": fec_executed,
        "velocity_class": vc,
    })


if __name__ in ("__main__", "__builtin__", "builtins"):
    main()
