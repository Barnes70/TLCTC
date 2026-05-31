from cli.reporters import cluster_summary


def render(classified) -> str:
    summary = cluster_summary(classified)
    lines = ["## TLCTC cluster exposure (SARIF)", "", "| Cluster | Findings |", "|---|---|"]
    for cluster, n in summary.items():
        lines.append(f"| {cluster} | {n} |")
    lines.append("")
    for r in classified:
        if r.status == "classified":
            lines.append(f"- **{r.primary_cluster}** `{r.finding.uri}` — "
                         f"{r.finding.message} ({r.provenance.get('identifier')})")
    low = [r for r in classified if r.status == "low_confidence"]
    if low:
        lines += ["", "### Low-confidence (Discouraged verdict)"]
        for r in low:
            lines.append(f"- {r.primary_cluster} `{r.finding.uri}` — "
                         f"{r.provenance.get('identifier')}")
    return "\n".join(lines) + "\n"
