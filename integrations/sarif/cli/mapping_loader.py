"""Loads and indexes the canonical CWE→TLCTC and KEV→TLCTC mappings."""
import json
import re
from pathlib import Path

_CWE_RE = re.compile(r"(?:cwe[-_]?)?(\d+)", re.IGNORECASE)


def normalize_cwe(raw: str):
    """'cwe-89', 'CWE_89', '89' → 'CWE-89'. Returns None if not a CWE token."""
    if raw is None:
        return None
    m = _CWE_RE.fullmatch(str(raw).strip())
    return f"CWE-{int(m.group(1))}" if m else None


class MappingLoader:
    def __init__(self, cwe_path: Path, kev_path: Path):
        cwe_doc = json.loads(Path(cwe_path).read_text(encoding="utf-8"))
        kev_doc = json.loads(Path(kev_path).read_text(encoding="utf-8"))
        self._cwe = {e["cweId"].upper(): e for e in cwe_doc["mappings"]}
        kev_list = kev_doc.get("mappings") or kev_doc.get("entries", [])
        self._kev = {e["cveID"].upper(): e for e in kev_list}

    def cwe(self, token: str):
        norm = normalize_cwe(token)
        return self._cwe.get(norm.upper()) if norm else None

    def kev(self, cve_id: str):
        if not cve_id:
            return None
        return self._kev.get(str(cve_id).strip().upper())
