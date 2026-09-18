"""Deterministic STIX ids and the fixed constants of the TLCTC extension."""
from __future__ import annotations

import json
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
STIX_DIR = HERE.parent / "stix"
PINNED_DIR = HERE.parent / "pinned"

TLCTC_EXT_ID = "extension-definition--69b4eaba-45a8-4101-b935-3a7ae2cb3a1a"
AF_EXT_ID = "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4"
TLCTC_IDENTITY_ID = "identity--025fe838-800e-4b4f-a9c3-2fab5d1366f5"
SITE = "https://www.tlctc.net"


def stix_id(obj_type: str, name: str) -> str:
    """uuid5 over NAMESPACE_URL and https://www.tlctc.net/stix/<name>, so the same input gives the same id."""
    return f"{obj_type}--{uuid.uuid5(uuid.NAMESPACE_URL, f'{SITE}/stix/{name}')}"


def load_extension_objects() -> list[dict]:
    """The TLCTC identity and extension-definition, as published in stix/tlctc-attack-flow-extension.json."""
    with open(STIX_DIR / "tlctc-attack-flow-extension.json", encoding="utf-8") as fh:
        return json.load(fh)["objects"]


def load_attack_flow_extension_objects() -> list[dict]:
    """The Attack Flow extension-definition and its creator identity, as pinned from upstream."""
    with open(PINNED_DIR / "attack-flow-extension-2.0.0.json", encoding="utf-8") as fh:
        return json.load(fh)["objects"]


def af_extension_block() -> dict:
    return {AF_EXT_ID: {"extension_type": "new-sdo"}}
