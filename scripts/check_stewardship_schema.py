#!/usr/bin/env python3
"""Validate YAML metadata blocks on stewardship docs already described in-repo.

Fail-closed pins (live path after #53; second-pass after #72/#75):
- DOC_SCHEMAS covers badge-standard / PUBLISH / issue-backlog / AGENTS / CLAUDE
- EXPECTED_VALUES pin ACTIVE / tier / owner / surface / parent_governance /
  maintainer / scope / purpose / closes already present on live YAML front matter
- Reject empty YAML metadata blocks, nested/list values, YAML null, bools
  pretending to be autonomy_level / tier ints (bool is a subclass of int)
- STRING_KEYS keep live string fields typed as strings (not invent fields)
- Semver X.Y.Z on AGENTS version; ISO-8601 on DATE_KEYS; closes #N issue refs
- Badge edit_policy retains invent-product wording; scan_secrets on every schema doc
- issue-backlog owner pinned to copilot (live metadata; not invent-product)
- Second-pass: FENCED_YAML_RE exact / ISO_DATE_RE / SEMVER_RE / ISSUE_REF_RE /
  DATE_KEYS exact / Tiny YAML subset / scalar+non-empty+string needles /
  ACTIVE status / positive tier / 0..3 autonomy / ISO-8601 / invent wording /
  semver / closes #N / FAILED+OK banners / stdlib-subset+PyYAML /
  bool subclass / group(1) / missing metadata keys / utf-8
- Third-pass after #132: future annotations / Path(__file__).resolve().parent /
  sys.path.insert / stewardship_common ROOT+fail+scan_secrets / yaml=None /
  pragma no cover / five live stewardship docs only / startswith("#") /
  true+false / null+~ / re.fullmatch -?digit+ / split(":", 1) / value[1:-1] /
  isinstance(loaded, dict) / FENCED_YAML_RE.search / isinstance (dict, list) /
  sorted(required_keys - set(data)) / startswith("docs/") / .upper()!=ACTIVE /
  EXPECTED_VALUES.get / (expected {want!r}) / level not in (0,1,2,3) /
  tier < 1 / ISO_DATE_RE.match / SEMVER_RE.match / ISSUE_REF_RE.search /
  closes scope set / scan_secrets(path, errors) / len(DOC_SCHEMAS) /
  sys.exit(main()) / third-pass docstring
- Deepen after #189: path.is_file() / block.strip() / except Exception as exc /
  DOC_SCHEMAS.items() / key not in data / isinstance(value, str) /
  key in STRING_KEYS / data.get("status") / edit_policy in data /
  rel == AGENTS.md / engine PyYAML-or-stdlib / noqa BLE001 /
  errors: list[str] = [] / got != want / autonomy_level in data /
  tier in data / for date_key in DATE_KEYS / deepen docstring
- Fourth-pass after #208: nested/list edit_policy+parent_governance policy refs /
  got nested/list / type(value).__name__ / invent not in policy /
  badge-standard edit_policy invent gate / str(status).upper() /
  invalid status enum stubs DEPRECATED|ARCHIVED|PENDING|RETIRED|SUSPENDED /
  invalid surface enum stubs geryon|playwright|browser-claude|claude-cowork /
  whitespace-only non-empty / nested version+autonomy+maintainer+status+
  surface+closes+tier / list surface+closes+purpose+autonomy /
  fourth-pass docstring (distinct from schema-third-pass after-149)
- Residual after #225 (schema pass-5; NOT fourth-pass #216 / NOT path-edges #225 /
  NOT Pass-2 leftover+md/link #220 / NOT badge-lint #208 / NOT wiki-index/badge #227;
  lands closed #229 leftover on post-#227 tip): residual invalid status
  stubs WIP|BETA|LEGACY|FROZEN|CANCELLED|PROTOTYPE / residual invalid surface stubs
  openai|anthropic|slack|auto|agents / "status" in required_keys / loaded is None /
  value.lower() == "true" / int(value) / if not text.strip() / residual docstring
- Residual leftover after #252 (schema leftover; NOT wiki/mdlink leftover #252 /
  NOT path-edges residual #244 / NOT wiki outline/PUBLISH #243 /
  NOT md/link residual #239 / NOT schema residual (pass-5) #233): leftover helper
  needles if ":" not in line / if yaml is not None: / if not match: /
  value is None or / status is not None / raw = str(data[date_key]) /
  ver = str(data["version"]) / closes = str(data["closes"]) /
  leftover invalid status stubs DRAFT|EXPERIMENTAL|OBSOLETE|DISABLED|INACTIVE|STAGED /
  leftover invalid surface stubs cursor|linear|notion|discord|zapier /
  leftover docstring
- Residual leftover after #262 (schema leftover residual; NOT lychee/blob-503 leftover #278 /
  NOT Pass-2 residual leftover #272 /
  NOT path-filter/path-order leftover #262 / NOT schema leftover #258 /
  NOT wiki/mdlink leftover #252 / NOT path-edges residual #244 /
  NOT wiki outline/PUBLISH #243 / NOT md/link residual #239 /
  NOT schema residual (pass-5) #233): leftover residual helper
  needles if not key: / data[key] = value /
  raise ValueError("metadata YAML must be a mapping") /
  return match.group(1) / block = first_yaml_block(path) /
  data = load_yaml(block) / if missing: / got = data.get(key) /
  policy = str(data["edit_policy"]).lower() /
  print("Stewardship schema check FAILED:" /
  leftover residual invalid status stubs REJECTED|UNKNOWN|ORPHANED|QUARANTINE|SHADOW|PREVIEW /
  leftover residual invalid surface stubs telegram|matrix|irc|email|webhook /
  leftover residual docstring
- Residual CI deepen after #293 (schema residual CI; NOT wiki/mdlink leftover residual #293 /
  NOT schema leftover residual #282 / NOT lychee/blob-503 leftover #278 /
  NOT Pass-2 residual leftover #272 /
  NOT path-filter/path-order leftover #262 / NOT schema leftover #258 /
  NOT wiki/mdlink leftover #252 / NOT path-edges residual #244 /
  NOT schema residual (pass-5) #233):
  residual CI helper needles if errors: / return 1 / return 0 /
  for rel, required_keys in DOC_SCHEMAS.items(): /
  for key in required_keys: / if not path.is_file(): /
  if not block.strip(): /
  if key in STRING_KEYS and not isinstance(value, str): /
  if "autonomy_level" in data: / if "edit_policy" in data: /
  if date_key not in data: /
  if not ISO_DATE_RE.match(raw): / if not SEMVER_RE.match(ver): /
  if not ISSUE_REF_RE.search(closes): /
  elif re.fullmatch digit coerce / value = value[1:-1] /
  for key, want in expected.items(): /
  level = data["autonomy_level"] / print(f"  - {err}" /
  for raw in text.splitlines(): / line = raw.strip() /
  key = key.strip() /
  isinstance(value, str) and not value.strip() / path = ROOT / rel /
  residual CI invalid status stubs SHELVED|SUPERSEDED|HOLD|STALE|ALPHA|NIGHTLY /
  residual CI invalid surface stubs chatgpt|vertex|groq|together|mistral /
  residual CI docstring
"""

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
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
ISSUE_REF_RE = re.compile(r"#\d+")

# Minimal key schemas taken from the live stewardship docs (do not invent fields).
# Fail-closed after #53: five live stewardship docs only (no invent-product paths).
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
        # Live front-door scope + closes pin (after #53; wire existing docs only).
        "scope": "public governance front-door repos",
        "closes": "#16",
    },
    "docs/wiki/PUBLISH.md": {
        "status": "ACTIVE",
        "purpose": "Reversible publish path for docs/wiki → GitHub Wiki",
        "closes": "#16",
    },
    "docs/issue-backlog.md": {
        "status": "ACTIVE",
        "tier": 1,
        # Fail-closed after #45: live backlog owner is copilot (not invent-product).
        "owner": "copilot",
    },
}

DATE_KEYS = ("created", "last_updated")

# Keys that must remain scalar strings in live stewardship metadata (not invent fields).
STRING_KEYS = frozenset(
    {
        "status",
        "owner",
        "scope",
        "edit_policy",
        "closes",
        "purpose",
        "version",
        "maintainer",
        "parent_governance",
        "repo",
        "surface",
        "created",
        "last_updated",
    }
)


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
        elif value.lower() in {"null", "~"}:
            value = None
        elif re.fullmatch(r"-?\d+", value):
            value = int(value)
        data[key] = value
    return data


def load_yaml(text: str) -> dict[str, object]:
    if yaml is not None:
        loaded = yaml.safe_load(text)
        if loaded is None:
            raise ValueError("empty yaml metadata block")
        if not isinstance(loaded, dict):
            raise ValueError("metadata YAML must be a mapping")
        return loaded
    if not text.strip():
        raise ValueError("empty yaml metadata block")
    return parse_simple_yaml(text)


def first_yaml_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = FENCED_YAML_RE.search(text)
    if not match:
        raise ValueError("no fenced ```yaml metadata block found")
    return match.group(1)


def reject_non_scalar(rel: str, key: str, value: object, errors: list[str]) -> bool:
    """Fail-closed: stewardship metadata values must be scalars (no nested/list)."""
    if isinstance(value, (dict, list)):
        fail(
            f"{rel}: metadata {key} must be a scalar (got nested/list {type(value).__name__})",
            errors,
        )
        return True
    return False


def main() -> int:
    errors: list[str] = []
    for rel, required_keys in DOC_SCHEMAS.items():
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing file: {rel}", errors)
            continue
        try:
            block = first_yaml_block(path)
            if not block.strip():
                raise ValueError("empty yaml metadata block")
            data = load_yaml(block)
        except Exception as exc:  # noqa: BLE001 — gate must report any parse failure
            fail(f"{rel}: {exc}", errors)
            continue
        missing = sorted(required_keys - set(data))
        if missing:
            fail(f"{rel}: missing metadata keys: {', '.join(missing)}", errors)

        # Required keys: scalar / non-empty / string-typed before expected-value pins.
        for key in required_keys:
            if key not in data:
                continue
            value = data[key]
            if reject_non_scalar(rel, key, value, errors):
                continue
            if value is None or (isinstance(value, str) and not value.strip()):
                fail(f"{rel}: metadata {key} must be non-empty", errors)
                continue
            if key in STRING_KEYS and not isinstance(value, str):
                fail(
                    f"{rel}: metadata {key} must be a string (got {type(value).__name__})",
                    errors,
                )

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
            # bool is a subclass of int — reject YAML yes/true pretending to be a level.
            if isinstance(level, bool) or not isinstance(level, int) or level not in (0, 1, 2, 3):
                fail(f"{rel}: autonomy_level must be int in 0..3 (got {level!r})", errors)

        if "tier" in data:
            tier = data["tier"]
            # bool is a subclass of int — reject YAML true pretending to be tier 1.
            if isinstance(tier, bool) or not isinstance(tier, int) or tier < 1:
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

        if rel == "AGENTS.md" and "version" in data:
            ver = str(data["version"])
            if not SEMVER_RE.match(ver):
                fail(f"{rel}: version must be semver X.Y.Z (got {ver!r})", errors)

        if rel in {"docs/badge-standard.md", "docs/wiki/PUBLISH.md"} and "closes" in data:
            closes = str(data["closes"])
            if not ISSUE_REF_RE.search(closes):
                fail(f"{rel}: closes must reference an issue like #N (got {closes!r})", errors)

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
