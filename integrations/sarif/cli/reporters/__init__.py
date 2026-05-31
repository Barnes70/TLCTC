from collections import Counter


def cluster_summary(classified):
    c = Counter()
    for r in classified:
        if r.status == "classified" and r.primary_cluster:
            c[r.primary_cluster] += 1
    # Lowest-numbered cluster first for stable output.
    return dict(sorted(c.items(), key=lambda kv: int(kv[0][1:])))
