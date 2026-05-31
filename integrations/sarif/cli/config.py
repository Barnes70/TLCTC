"""Config loading: TOML or JSON file, env-var precedence, repo-relative defaults."""
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

# integrations/sarif/cli/config.py -> repo root is 3 parents up.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_CWE = _REPO_ROOT / "mappings" / "mitre-cwe" / "tlctc-cwe.json"
_DEFAULT_KEV = _REPO_ROOT / "mappings" / "cisa-kev" / "tlctc-kev.json"


@dataclass
class Config:
    cwe_mapping_path: Path = _DEFAULT_CWE
    kev_mapping_path: Path = _DEFAULT_KEV
    formats: list = field(default_factory=lambda: ["json"])
    source_globs: dict = field(default_factory=lambda: {"server": [], "client": []})
    fail_on_cluster: list = field(default_factory=list)


def _read_file(path: Path) -> dict:
    if path.suffix == ".toml":
        if tomllib is None:
            raise RuntimeError("TOML config requires Python 3.11+; use a .json config")
        return tomllib.loads(path.read_text(encoding="utf-8"))
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(path) -> Config:
    data = _read_file(Path(path)) if path else {}
    cfg = Config()
    if "cwe_mapping_path" in data:
        cfg.cwe_mapping_path = Path(data["cwe_mapping_path"])
    if "kev_mapping_path" in data:
        cfg.kev_mapping_path = Path(data["kev_mapping_path"])
    if "formats" in data:
        cfg.formats = list(data["formats"])
    if "source_globs" in data:
        cfg.source_globs = {
            "server": list(data["source_globs"].get("server", [])),
            "client": list(data["source_globs"].get("client", [])),
        }
    if "fail_on_cluster" in data:
        cfg.fail_on_cluster = list(data["fail_on_cluster"])
    env_formats = os.environ.get("TLCTC_SARIF_FORMATS")
    if env_formats:
        cfg.formats = [f.strip() for f in env_formats.split(",") if f.strip()]
    return cfg
