"""TLCTCEmitLayer3 -- closure script for the TLCTC Threat incident type.

Builds a Layer 3 attack-path JSON instance from incident fields and writes it
to incident_tlctcattackpath. Output validates against
json-schemas/layer-3/tlctc-attack-path.schema.json (TLCTC v2.1).

This is intentionally minimal -- analysts can hand-edit the resulting JSON in
the layout's 'Attack Path (Layer 3)' tab before close. The script never
overwrites a non-empty tlctcattackpath value (analyst-authored paths win).
"""
import json
import uuid
from datetime import datetime, timezone

import demistomock as demisto
from CommonServerPython import return_results


STRATEGIC_TO_OPERATIONAL = {
    "#1": "TLCTC-01.00", "#2": "TLCTC-02.00", "#3": "TLCTC-03.00",
    "#4": "TLCTC-04.00", "#5": "TLCTC-05.00", "#6": "TLCTC-06.00",
    "#7": "TLCTC-07.00", "#8": "TLCTC-08.00", "#9": "TLCTC-09.00",
    "#10": "TLCTC-10.00",
}
BRIDGE_CLUSTERS = {"#8", "#9", "#10"}


def main():
    incident = demisto.incident()
    cf = incident.get("CustomFields", {}) or {}

    existing = cf.get("tlctcattackpath")
    if existing and existing.strip() not in ("", "{}"):
        return_results({
            "info": "Layer 3 path already authored by analyst -- not overwriting."
        })
        return

    labels = incident.get("labels", []) or []
    seq_label = next(
        (l.get("value") for l in labels if l.get("type") == "TLCTCSequence"),
        None,
    )
    sequence = (
        seq_label.split(",")
        if seq_label
        else ([cf.get("tlctccluster")] if cf.get("tlctccluster") else [])
    )
    if not sequence:
        return_results({
            "warning": "No TLCTC sequence available; cannot emit Layer 3 path."
        })
        return

    raw_boundary = cf.get("tlctcboundary")
    boundary = None
    if raw_boundary:
        try:
            boundary = json.loads(raw_boundary)
        except Exception:
            boundary = None

    dre = cf.get("tlctcdre") or []
    if isinstance(dre, str):
        dre = [d.strip() for d in dre.split(",") if d.strip()]

    delta_t = cf.get("tlctcdeltat") or "?"
    fec_executed = bool(cf.get("tlctcfecexecuted"))

    path_sequence = []
    for idx, cluster in enumerate(sequence):
        step = {
            "step_id": f"s{idx + 1}",
            "cluster": cluster,
        }
        if idx < len(sequence) - 1:
            step["delta_t_to_next"] = delta_t
        if cluster in BRIDGE_CLUSTERS and boundary:
            step["topology_boundary"] = boundary
        if cluster == "#7" and fec_executed:
            step["fec_executed"] = True
        if idx == len(sequence) - 1 and dre:
            step["outcomes"] = dre
        path_sequence.append(step)

    payload = {
        "metadata": {
            "incident_id": str(incident.get("id") or uuid.uuid4()),
            "analyst_confidence": cf.get("tlctcanalystconfidence", "medium"),
            "tlctc_version": "2.1",
            "framework_ref": "tlctc-framework.v2.0.json",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "notes": (
                f"Auto-emitted by TLCTCEmitLayer3 from XSOAR incident "
                f"{incident.get('id')}."
            ),
        },
        "path_sequence": path_sequence,
    }

    demisto.executeCommand("setIncident", {
        "customFields": json.dumps({
            "tlctcattackpath": json.dumps(payload, indent=2)
        })
    })
    return_results({"emitted": True, "step_count": len(path_sequence)})


if __name__ in ("__main__", "__builtin__", "builtins"):
    main()
