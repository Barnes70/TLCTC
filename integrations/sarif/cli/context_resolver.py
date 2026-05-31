"""R-ROLE: resolve a '#2 | #3' alternation from the finding's file path.

server-role glob match → #2 (Exploiting Server); client-role → #3
(Exploiting Client). Returns (cluster_or_None, human_reason).
"""
from fnmatch import fnmatch


def _matches(uri, patterns):
    return any(fnmatch(uri, p) for p in patterns)


def resolve_role(uri: str, source_globs: dict):
    server = source_globs.get("server", [])
    client = source_globs.get("client", [])
    s, c = _matches(uri, server), _matches(uri, client)
    if s and not c:
        return "#2", f"server-role: '{uri}' matched a server glob (R-ROLE → #2)"
    if c and not s:
        return "#3", f"client-role: '{uri}' matched a client glob (R-ROLE → #3)"
    return None, f"unresolved: '{uri}' matched no (or both) role globs"
