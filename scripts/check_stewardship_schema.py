#!/usr/bin/env python3
"""Validate YAML metadata blocks on stewardship docs already described in-repo."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs pyyaml; local may use stdlib fallback
    yaml = None

ROOT = Path(__file__).resolve().parents[1]

# First fenced ```yaml block after the H1 is the document metadata schema.
FENCED_YAML_RE = re.compile(r"^```yaml\n(.*?)\n```", re.MULTILINE | re.DOTALL)

# Minimal key schemas taken from the live stewardship docs (do not invent fields).
DOC_SCHEMAS: dict[str, set[str]] = {
    "docs/badge-standard.md": {
        "status",
        "tier",
        "created",
        "owner",
        "scope",
        "edit_policy",
        "closes",
    },
    "docs/wiki/PUBLISH.md": {
        "status",
        "created",
        "purpose",
        "closes",
    },
    "AGENTS.md": {
        "version",
        "last_updated",
        "maintainer",
        "scope",
        "parent_governance",
        "autonomy_level",
    },
    "CLAUDE.md": {
        "repo",
        "owner",
        "surface",
        "autonomy_level",
        "last_updated",
        "parent_governance",
    },
}


def parse_simple_yaml(text: str) -> dict[str, object]:
    """Tiny YAML subset parser (key: value / key: \"value\") when PyYAML is absent."""
    data: dict[str, object] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported YAML line: {raw!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"empty key in YAML line: {raw!r}")
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        elif value.lower() in {"true", "false"}:
            value = value.lower() == "true"
        elif re.fullmatch(r"-?\d+", value):
            value = int(value)
        data[key] = value
    return data


def load_yaml(text: str) -> dict[str, object]:
    if yaml is not None:
        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("metadata YAML must be a mapping")
        return loaded
    return parse_simple_yaml(text)


def first_yaml_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = FENCED_YAML_RE.search(text)
    if not match:
        raise ValueError("no fenced ```yaml metadata block found")
    return match.group(1)


def main() -> int:
    errors: list[str] = []
    for rel, required_keys in DOC_SCHEMAS.items():
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing file: {rel}")
            continue
        try:
            block = first_yaml_block(path)
            data = load_yaml(block)
        except Exception as exc:  # noqa: BLE001 — gate must report any parse failure
            errors.append(f"{rel}: {exc}")
            continue
        missing = sorted(required_keys - set(data))
        if missing:
            errors.append(f"{rel}: missing metadata keys: {', '.join(missing)}")
        status = data.get("status")
        if "status" in required_keys and status is not None and str(status).upper() != "ACTIVE":
            # badge-standard / PUBLISH declare ACTIVE; fail closed if drifted
            if rel.startswith("docs/"):
                errors.append(f"{rel}: status must be ACTIVE for active stewardship docs")

    if errors:
        print("Stewardship schema check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    engine = "PyYAML" if yaml is not None else "stdlib-subset"
    print(f"OK: stewardship metadata schemas valid ({engine}, {len(DOC_SCHEMAS)} docs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
