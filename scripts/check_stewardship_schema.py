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

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from stewardship_common import ROOT, fail, scan_secrets  # noqa: E402

# First fenced ```yaml block after the H1 is the document metadata schema.
FENCED_YAML_RE = re.compile(r"^```yaml\n(.*?)\n```", re.MULTILINE | re.DOTALL)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

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
    "docs/issue-backlog.md": {
        "status",
        "tier",
        "created",
        "owner",
        "edit_policy",
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

# Value constraints already implied by live docs (fail closed on drift).
EXPECTED_VALUES: dict[str, dict[str, object]] = {
    "AGENTS.md": {
        "parent_governance": "github.com/fuzzywigg/agents-governance",
        "autonomy_level": 1,
        "maintainer": "smtp.eth",
        "scope": "repository-specific",
    },
    "CLAUDE.md": {
        "repo": "agents-governance",
        "owner": "fuzzywigg (smtp.eth)",
        "surface": "copilot",
        "autonomy_level": 1,
        "parent_governance": "github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md",
    },
    "docs/badge-standard.md": {
        "status": "ACTIVE",
        "tier": 1,
        "owner": "copilot",
    },
    "docs/wiki/PUBLISH.md": {
        "status": "ACTIVE",
    },
    "docs/issue-backlog.md": {
        "status": "ACTIVE",
        "tier": 1,
    },
}

DATE_KEYS = ("created", "last_updated")


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
            fail(f"missing file: {rel}", errors)
            continue
        try:
            block = first_yaml_block(path)
            data = load_yaml(block)
        except Exception as exc:  # noqa: BLE001 — gate must report any parse failure
            fail(f"{rel}: {exc}", errors)
            continue
        missing = sorted(required_keys - set(data))
        if missing:
            fail(f"{rel}: missing metadata keys: {', '.join(missing)}", errors)

        status = data.get("status")
        if "status" in required_keys and status is not None and str(status).upper() != "ACTIVE":
            if rel.startswith("docs/"):
                fail(f"{rel}: status must be ACTIVE for active stewardship docs", errors)

        expected = EXPECTED_VALUES.get(rel, {})
        for key, want in expected.items():
            got = data.get(key)
            if got != want:
                fail(f"{rel}: metadata {key}={got!r} (expected {want!r})", errors)

        if "autonomy_level" in data:
            level = data["autonomy_level"]
            if not isinstance(level, int) or level not in (0, 1, 2, 3):
                fail(f"{rel}: autonomy_level must be int in 0..3 (got {level!r})", errors)

        if "tier" in data:
            tier = data["tier"]
            if not isinstance(tier, int) or tier < 1:
                fail(f"{rel}: tier must be a positive int (got {tier!r})", errors)

        for date_key in DATE_KEYS:
            if date_key not in data:
                continue
            raw = str(data[date_key])
            if not ISO_DATE_RE.match(raw):
                fail(f"{rel}: {date_key} must be ISO-8601 date-prefixed (got {raw!r})", errors)

        if "edit_policy" in data:
            policy = str(data["edit_policy"]).lower()
            if "invent" not in policy and rel == "docs/badge-standard.md":
                fail(f"{rel}: edit_policy must retain no-invent-product wording", errors)

        scan_secrets(path, errors)

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
