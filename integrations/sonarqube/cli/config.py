"""Configuration loader for the TLCTC SonarQube sidecar.

Supports two config file formats:
  - `.toml` via stdlib `tomllib` (Python 3.11+). The documented default.
  - `.json` via stdlib `json` (works on all supported Pythons).

When no config file is supplied, a built-in default RoleConfig is used so the
CLI remains operable in `validate` and `classify` flows without a TOML file.
Credentials are NEVER read from this file — use SONAR_URL / SONAR_TOKEN env
vars or the CLI flags.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

try:  # pragma: no cover - import-time check
    import tomllib as _tomllib
except ImportError:  # pragma: no cover - Python 3.10 and earlier
    _tomllib = None

from .context_resolver import ROLE_SERVER, RoleConfig

DEFAULT_SERVER_GLOBS: tuple[str, ...] = (
    "**/src/main/java/**",
    "**/src/main/kotlin/**",
    "**/src/main/scala/**",
    "**/server/**",
    "**/api/**",
    "**/backend/**",
    "**/handlers/**",
    "**/routes/**",
    "**/controllers/**",
    "**/services/**",
    "**/*.controller.*",
    "**/*Controller.java",
    "**/*Repository.java",
    "**/*Service.java",
    "**/*.go",
    "**/*.py",
    "**/*.rb",
    "**/*.php",
)

DEFAULT_CLIENT_GLOBS: tuple[str, ...] = (
    "**/src/main/webapp/**",
    "**/static/**",
    "**/public/**",
    "**/web/**",
    "**/frontend/**",
    "**/client/**",
    "**/ui/**",
    "**/*.html",
    "**/*.htm",
    "**/*.jsx",
    "**/*.tsx",
    "**/*.vue",
    "**/*.svelte",
)


@dataclass(frozen=True)
class Config:
    mapping_file: Path
    role_config: RoleConfig
    fail_on_clusters: tuple[int, ...]
    source: str  # "toml", "json", or "default"


def default(repo_root: Path | None = None) -> Config:
    """Built-in defaults used when no config file is supplied."""
    mapping = (repo_root / "mappings/mitre-cwe/tlctc-cwe.json").resolve() if repo_root else Path("../../mappings/mitre-cwe/tlctc-cwe.json")
    return Config(
        mapping_file=mapping,
        role_config=RoleConfig(
            server_globs=DEFAULT_SERVER_GLOBS,
            client_globs=DEFAULT_CLIENT_GLOBS,
            default_role=ROLE_SERVER,
        ),
        fail_on_clusters=(),
        source="default",
    )


def load(path: str | Path, repo_root: Path | None = None) -> Config:
    """Load a TOML or JSON config file."""
    p = Path(path).resolve()
    suffix = p.suffix.lower()
    if suffix == ".toml":
        return _load_toml(p, repo_root)
    if suffix == ".json":
        return _load_json(p, repo_root)
    raise ValueError(f"unsupported config extension: {suffix} (expected .toml or .json)")


def _load_toml(p: Path, repo_root: Path | None) -> Config:
    if _tomllib is None:
        raise RuntimeError(
            f"reading {p} requires Python 3.11+ (stdlib tomllib). "
            "Convert your config to JSON or upgrade Python."
        )
    raw = _tomllib.loads(p.read_text(encoding="utf-8"))
    return _from_raw(raw, p, repo_root, source="toml")


def _load_json(p: Path, repo_root: Path | None) -> Config:
    raw = json.loads(p.read_text(encoding="utf-8"))
    return _from_raw(raw, p, repo_root, source="json")


def _from_raw(raw: dict, p: Path, repo_root: Path | None, source: str) -> Config:
    section = raw.get("tlctc-sonar", {}) or {}
    mapping_rel = section.get("mapping_file") or _default_mapping_rel(repo_root, p)
    mp = Path(mapping_rel)
    mapping_path = (p.parent / mp).resolve() if not mp.is_absolute() else mp

    default_role = section.get("default_role", ROLE_SERVER)

    role_section = raw.get("role", {}) or {}
    server_globs = tuple(((role_section.get("server", {}) or {}).get("globs", []) or []))
    client_globs = tuple(((role_section.get("client", {}) or {}).get("globs", []) or []))

    fail_on = raw.get("fail_on", {}) or {}
    fail_on_clusters = tuple(int(c) for c in (fail_on.get("clusters", []) or []))

    return Config(
        mapping_file=mapping_path,
        role_config=RoleConfig(
            server_globs=server_globs or DEFAULT_SERVER_GLOBS,
            client_globs=client_globs or DEFAULT_CLIENT_GLOBS,
            default_role=default_role,
        ),
        fail_on_clusters=fail_on_clusters,
        source=source,
    )


def _default_mapping_rel(repo_root: Path | None, config_path: Path) -> str:
    if repo_root is not None:
        candidate = (repo_root / "mappings/mitre-cwe/tlctc-cwe.json").resolve()
        return str(candidate)
    return "../../mappings/mitre-cwe/tlctc-cwe.json"


def env_token() -> str | None:
    return os.environ.get("SONAR_TOKEN")


def env_url() -> str | None:
    return os.environ.get("SONAR_URL")
