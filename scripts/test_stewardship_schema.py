#!/usr/bin/env python3
"""TOKENMAXX schema-gate self-tests (dedicated slice — not stewardship mega-fixtures).

Deepens check_stewardship_schema.py only: bool-vs-int, string scalars, nested
reject, empty YAML, semver/date/closes/edit_policy/expected-value edges, plus
parse_simple_yaml / load_yaml / is_plain_int helpers. No invent-product surface.
Wired into stewardship-checks.yml after the live-tree gates.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load_schema_module():
    path = SCRIPTS / "check_stewardship_schema.py"
    spec = importlib.util.spec_from_file_location("check_stewardship_schema", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SCHEMA = _load_schema_module()


def run(script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_scripts(tmp: Path) -> Path:
    scripts_dir = tmp / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    for name in ("stewardship_common.py", "check_stewardship_schema.py"):
        shutil.copy2(SCRIPTS / name, scripts_dir / name)
    return scripts_dir


def _default_agents() -> str:
    return (
        "# AGENTS\n\n```yaml\n"
        'version: "1.0.0"\n'
        'last_updated: "2026-04-13"\n'
        "maintainer: smtp.eth\n"
        "scope: repository-specific\n"
        "parent_governance: github.com/fuzzywigg/agents-governance\n"
        "autonomy_level: 1\n"
        "```\n"
    )


def _default_claude() -> str:
    return (
        "# CLAUDE\n\n```yaml\n"
        "repo: agents-governance\n"
        'owner: "fuzzywigg (smtp.eth)"\n'
        "surface: copilot\n"
        "autonomy_level: 1\n"
        'last_updated: "2026-04-13"\n'
        "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n"
        "```\n"
    )


def _default_badge() -> str:
    return (
        "# B\n\n```yaml\n"
        "status: ACTIVE\n"
        "tier: 1\n"
        'created: "2026-09-13"\n'
        "owner: copilot\n"
        "scope: x\n"
        'edit_policy: "do not invent product badges"\n'
        'closes: "#16"\n'
        "```\n"
    )


def _default_publish() -> str:
    return (
        "# P\n\n```yaml\n"
        "status: ACTIVE\n"
        'created: "2026-09-13"\n'
        "purpose: x\n"
        'closes: "#16"\n'
        "```\n"
    )


def _default_backlog() -> str:
    return (
        "# I\n\n```yaml\n"
        "status: ACTIVE\n"
        "tier: 1\n"
        'created: "2026-09-13"\n'
        "owner: x\n"
        "edit_policy: x\n"
        "```\n"
    )


def _seed_schema_tree(
    tmp: Path,
    *,
    agents: str | None = None,
    claude: str | None = None,
    badge: str | None = None,
    publish: str | None = None,
    backlog: str | None = None,
) -> Path:
    scripts = _seed_scripts(tmp)
    _write(tmp / "AGENTS.md", agents or _default_agents())
    _write(tmp / "CLAUDE.md", claude or _default_claude())
    _write(tmp / "docs" / "badge-standard.md", badge or _default_badge())
    _write(tmp / "docs" / "wiki" / "PUBLISH.md", publish or _default_publish())
    _write(tmp / "docs" / "issue-backlog.md", backlog or _default_backlog())
    return scripts


def assert_fail(script_path: Path, cwd: Path, needle: str) -> None:
    proc = run(script_path, cwd)
    blob = proc.stdout + proc.stderr
    if proc.returncode == 0:
        raise AssertionError(f"{script_path.name} unexpectedly passed\n{blob}")
    if needle not in blob:
        raise AssertionError(f"{script_path.name} missing {needle!r}\n{blob}")


def assert_pass(script_path: Path, cwd: Path) -> None:
    proc = run(script_path, cwd)
    if proc.returncode != 0:
        raise AssertionError(
            f"{script_path.name} unexpectedly failed\n{proc.stdout}{proc.stderr}"
        )


def assert_pass_live() -> None:
    proc = run(SCRIPTS / "check_stewardship_schema.py", ROOT)
    if proc.returncode != 0:
        raise AssertionError(f"live schema gate failed\n{proc.stdout}{proc.stderr}")


def _agents_with(**overrides: object) -> str:
    base: dict[str, object] = {
        "version": '"1.0.0"',
        "last_updated": '"2026-04-13"',
        "maintainer": "smtp.eth",
        "scope": "repository-specific",
        "parent_governance": "github.com/fuzzywigg/agents-governance",
        "autonomy_level": "1",
    }
    base.update(overrides)
    body = "\n".join(f"{k}: {v}" for k, v in base.items())
    return f"# AGENTS\n\n```yaml\n{body}\n```\n"


def _claude_with(**overrides: object) -> str:
    base: dict[str, object] = {
        "repo": "agents-governance",
        "owner": '"fuzzywigg (smtp.eth)"',
        "surface": "copilot",
        "autonomy_level": "1",
        "last_updated": '"2026-04-13"',
        "parent_governance": "github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md",
    }
    base.update(overrides)
    body = "\n".join(f"{k}: {v}" for k, v in base.items())
    return f"# CLAUDE\n\n```yaml\n{body}\n```\n"


def _badge_with(**overrides: object) -> str:
    base: dict[str, object] = {
        "status": "ACTIVE",
        "tier": "1",
        "created": '"2026-09-13"',
        "owner": "copilot",
        "scope": "x",
        "edit_policy": '"do not invent product badges"',
        "closes": '"#16"',
    }
    base.update(overrides)
    body = "\n".join(f"{k}: {v}" for k, v in base.items())
    return f"# B\n\n```yaml\n{body}\n```\n"


def _publish_with(**overrides: object) -> str:
    base: dict[str, object] = {
        "status": "ACTIVE",
        "created": '"2026-09-13"',
        "purpose": "x",
        "closes": '"#16"',
    }
    base.update(overrides)
    body = "\n".join(f"{k}: {v}" for k, v in base.items())
    return f"# P\n\n```yaml\n{body}\n```\n"


def _backlog_with(**overrides: object) -> str:
    base: dict[str, object] = {
        "status": "ACTIVE",
        "tier": "1",
        "created": '"2026-09-13"',
        "owner": "x",
        "edit_policy": "x",
    }
    base.update(overrides)
    body = "\n".join(f"{k}: {v}" for k, v in base.items())
    return f"# I\n\n```yaml\n{body}\n```\n"


# --- helper unit tests -------------------------------------------------------


def test_helper_is_plain_int_rejects_bool() -> None:
    assert SCHEMA.is_plain_int(1) is True
    assert SCHEMA.is_plain_int(0) is True
    assert SCHEMA.is_plain_int(True) is False
    assert SCHEMA.is_plain_int(False) is False
    assert SCHEMA.is_plain_int(1.0) is False
    assert SCHEMA.is_plain_int("1") is False
    assert SCHEMA.is_plain_int(None) is False


def test_helper_parse_simple_yaml_ints_and_bools() -> None:
    data = SCHEMA.parse_simple_yaml("tier: 1\nautonomy_level: 2\nflag: true\n")
    assert data["tier"] == 1
    assert data["autonomy_level"] == 2
    assert data["flag"] is True


def test_helper_parse_simple_yaml_null_tilde() -> None:
    data = SCHEMA.parse_simple_yaml("owner: null\nscope: ~\n")
    assert data["owner"] is None
    assert data["scope"] is None


def test_helper_parse_simple_yaml_quoted() -> None:
    data = SCHEMA.parse_simple_yaml("maintainer: \"smtp.eth\"\nscope: 'repository-specific'\n")
    assert data["maintainer"] == "smtp.eth"
    assert data["scope"] == "repository-specific"


def test_helper_parse_simple_yaml_rejects_nested_empty() -> None:
    try:
        SCHEMA.parse_simple_yaml("owner:\n")
    except ValueError as exc:
        assert "nested" in str(exc).lower() or "empty" in str(exc).lower()
    else:
        raise AssertionError("expected ValueError for empty nested value")


def test_helper_parse_simple_yaml_rejects_pipe() -> None:
    try:
        SCHEMA.parse_simple_yaml("purpose: |\n")
    except ValueError:
        return
    raise AssertionError("expected ValueError for pipe block")


def test_helper_parse_simple_yaml_rejects_gt() -> None:
    try:
        SCHEMA.parse_simple_yaml("purpose: >\n")
    except ValueError:
        return
    raise AssertionError("expected ValueError for gt block")


def test_helper_parse_simple_yaml_rejects_no_colon() -> None:
    try:
        SCHEMA.parse_simple_yaml("not-a-mapping-line\n")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_helper_parse_simple_yaml_rejects_empty_key() -> None:
    try:
        SCHEMA.parse_simple_yaml(": value\n")
    except ValueError:
        return
    raise AssertionError("expected ValueError for empty key")


def test_helper_parse_simple_yaml_skips_comments() -> None:
    data = SCHEMA.parse_simple_yaml("# comment\ntier: 1\n")
    assert data == {"tier": 1}


def test_helper_load_yaml_rejects_empty_block() -> None:
    try:
        SCHEMA.load_yaml("   \n\n")
    except ValueError as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("expected empty-block ValueError")


def test_helper_load_yaml_rejects_list() -> None:
    try:
        SCHEMA.load_yaml("- a\n- b\n")
    except ValueError as exc:
        assert "mapping" in str(exc).lower()
    else:
        raise AssertionError("expected mapping ValueError")


def test_helper_load_yaml_mapping_ok() -> None:
    data = SCHEMA.load_yaml("status: ACTIVE\ntier: 1\n")
    assert data["status"] == "ACTIVE"
    assert data["tier"] == 1


def test_helper_semver_rejects_v_prefix() -> None:
    assert SCHEMA.SEMVER_RE.match("1.0.0")
    assert not SCHEMA.SEMVER_RE.match("v1.0.0")
    assert not SCHEMA.SEMVER_RE.match("1.0")
    assert not SCHEMA.SEMVER_RE.match("1.0.0-rc1")


def test_helper_iso_date_prefix() -> None:
    assert SCHEMA.ISO_DATE_RE.match("2026-04-13")
    assert SCHEMA.ISO_DATE_RE.match("2026-04-13T12:00:00Z")
    assert not SCHEMA.ISO_DATE_RE.match("04-13-2026")
    assert not SCHEMA.ISO_DATE_RE.match("2026/04/13")


def test_helper_issue_ref() -> None:
    assert SCHEMA.ISSUE_REF_RE.search("#16")
    assert SCHEMA.ISSUE_REF_RE.search("closes #16")
    assert not SCHEMA.ISSUE_REF_RE.search("#")
    assert not SCHEMA.ISSUE_REF_RE.search("issue 16")


def test_helper_doc_schemas_cover_five() -> None:
    assert len(SCHEMA.DOC_SCHEMAS) == 5
    for name in (
        "AGENTS.md",
        "CLAUDE.md",
        "docs/badge-standard.md",
        "docs/wiki/PUBLISH.md",
        "docs/issue-backlog.md",
    ):
        assert name in SCHEMA.DOC_SCHEMAS


def test_helper_expected_values_agents_parent() -> None:
    assert (
        SCHEMA.EXPECTED_VALUES["AGENTS.md"]["parent_governance"]
        == "github.com/fuzzywigg/agents-governance"
    )


def test_helper_expected_values_claude_surface() -> None:
    assert SCHEMA.EXPECTED_VALUES["CLAUDE.md"]["surface"] == "copilot"


def test_helper_string_keys_include_status() -> None:
    assert "status" in SCHEMA.STRING_KEYS
    assert "edit_policy" in SCHEMA.STRING_KEYS
    assert "autonomy_level" not in SCHEMA.STRING_KEYS


def test_helper_int_keys() -> None:
    assert SCHEMA.INT_KEYS == frozenset({"autonomy_level", "tier"})


def test_live_schema_passes() -> None:
    assert_pass_live()


def test_fixture_good_passes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)


def test_schema_rejects_autonomy_bool_true() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: true\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_bool_false() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: false\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_yaml_yes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: yes\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_yaml_no() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: no\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_tier_bool_true() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: true\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_tier_yaml_yes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: yes\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_backlog_tier_bool() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: true\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_claude_autonomy_bool() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: true\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_float() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1.5\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_tier_float() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1.5\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_string_digit() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: "1"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_neg() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: -1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            '0..3',
        )

def test_schema_rejects_autonomy_four() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 4\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            '0..3',
        )

def test_schema_rejects_tier_zero() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'positive int',
        )

def test_schema_rejects_tier_neg() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: -2\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'positive int',
        )

def test_schema_rejects_nested_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner:\n  name: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'scalar',
        )

def test_schema_rejects_list_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope:\n  - x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'scalar',
        )

def test_schema_rejects_nested_agents_maintainer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer:\n  name: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'scalar',
        )

def test_schema_rejects_status_bool() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: true\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_status_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: 1\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_owner_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: 1\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_purpose_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: 1\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_surface_bool() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: true\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_version_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: 1\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_empty_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: ""\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_null_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: null\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_tilde_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: ~\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_whitespace_purpose() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: "   "\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_empty_edit_policy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: ""\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_null_closes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: x\ncloses: null\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_empty_yaml_block() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\n\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'empty',
        )

def test_schema_rejects_missing_agents_version() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_agents_last_updated() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_agents_maintainer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_agents_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_agents_parent_governance() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_agents_autonomy_level() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_claude_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_claude_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_claude_surface() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_claude_autonomy_level() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_claude_last_updated() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_claude_parent_governance() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_wrong_maintainer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: other\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: global\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_parent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: example.com/x\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_autonomy_expected() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 0\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_claude_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: other\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_claude_surface() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: cursor\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_claude_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "other"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_claude_parent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_badge_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: human\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_badge_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 2\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_badge_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ACTIVE',
        )

def test_schema_rejects_inactive_publish() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: INACTIVE\ncreated: "2026-09-13"\npurpose: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ACTIVE',
        )

def test_schema_rejects_inactive_backlog() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: archived\ntier: 1\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ACTIVE',
        )

def test_schema_rejects_backlog_wrong_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 2\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_semver_v_prefix() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "v1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'semver',
        )

def test_schema_rejects_semver_two_part() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'semver',
        )

def test_schema_rejects_semver_prerelease() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0-rc1"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'semver',
        )

def test_schema_rejects_bad_agents_date() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "04-13-2026"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ISO-8601',
        )

def test_schema_rejects_bad_claude_date() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026/04/13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ISO-8601',
        )

def test_schema_rejects_bad_badge_created() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "Sept 13, 2026"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ISO-8601',
        )

def test_schema_rejects_bad_publish_created() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "13-09-2026"\npurpose: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ISO-8601',
        )

def test_schema_rejects_closes_without_hash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'issue',
        )

def test_schema_rejects_closes_hash_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'issue',
        )

def test_schema_rejects_publish_closes_no_issue() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: x\ncloses: "soon"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'issue',
        )

def test_schema_rejects_edit_policy_no_invent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "agent editable"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'invent',
        )

def test_schema_rejects_missing_yaml_fence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\nno fence\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'yaml',
        )

def test_schema_rejects_unparseable_yaml() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\n: : :\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'AGENTS.md',
        )

def test_schema_rejects_secret_ghp() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: "ghp_abcdefghijklmnopqrstuvwxyz12"\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'secret',
        )

def test_schema_accepts_datetime_prefixed_date() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13T00:00:00Z"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)

def test_schema_accepts_closes_with_prose() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "Closes #16"\n```\n',
        )
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)

def test_schema_accepts_quoted_active_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: "ACTIVE"\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)

def test_schema_accepts_backlog_without_invent_word() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: x\nedit_policy: "Agent-editable"\n```\n',
        )
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)

def test_schema_rejects_wrong_maintainer_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: andrew\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_scope_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: ecosystem\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_claude_autonomy_two() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 2\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_badge_owner_empty_str() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: ""\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_publish_purpose_null() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: null\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_backlog_owner_null() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: null\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_agents_parent_empty() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: ""\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_claude_repo_empty() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: ""\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_tier_as_string() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: "1"\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_autonomy_as_string_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: "1"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_status_draft_lower() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: draft\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ACTIVE',
        )

def test_schema_rejects_publish_status_pending() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: PENDING\ncreated: "2026-09-13"\npurpose: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ACTIVE',
        )

def test_schema_rejects_backlog_status_todo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: TODO\ntier: 1\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ACTIVE',
        )

def test_schema_rejects_semver_four_part() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'semver',
        )

def test_schema_rejects_semver_empty() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: ""\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'non-empty',
        )

def test_schema_rejects_date_year_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ISO-8601',
        )

def test_schema_rejects_closes_issue_word() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "issue 16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'issue',
        )

def test_schema_rejects_edit_policy_product_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "no product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'invent',
        )

def test_schema_rejects_list_closes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: x\ncloses:\n  - "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'scalar',
        )

def test_schema_rejects_nested_edit_policy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy:\n  text: invent\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'scalar',
        )

def test_schema_rejects_missing_badge_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_badge_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_badge_created() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_badge_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_badge_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_badge_edit_policy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_badge_closes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_publish_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\ncreated: "2026-09-13"\npurpose: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_publish_created() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\npurpose: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_publish_purpose() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_publish_closes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_backlog_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\ntier: 1\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_backlog_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_backlog_created() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_backlog_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_missing_backlog_edit_policy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'missing metadata keys',
        )

def test_schema_rejects_secret_github_pat() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: ACTIVE\ncreated: "2026-09-13"\npurpose: "github_pat_ABCDEFGHIJKLMNOPQRSTUVWXYZ"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'secret',
        )

def test_schema_rejects_secret_npm() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: x\nedit_policy: "npm_abcdefghijklmnopqrstuvwxyz12"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'secret',
        )

def test_schema_rejects_backlog_tier_yes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: yes\ncreated: "2026-09-13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_claude_autonomy_yes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: yes\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_agents_autonomy_on() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: on\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_badge_tier_on() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: on\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_accepts_good_defaults() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)

def test_schema_accepts_closes_paren_issue() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "(#16)"\n```\n',
        )
        assert_pass(scripts / "check_stewardship_schema.py", tmp_path)

def test_schema_rejects_autonomy_bool_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: True\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_tier_false() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: false\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'plain int',
        )

def test_schema_rejects_status_false() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish='# P\n\n```yaml\nstatus: false\ncreated: "2026-09-13"\npurpose: x\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_maintainer_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: 1\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_repo_bool() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: true\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_scope_bool() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: false\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_closes_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: 16\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_created_int() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: 20260913\nowner: copilot\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'string',
        )

def test_schema_rejects_wrong_badge_owner_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: smtp.eth\nscope: x\nedit_policy: "do not invent product badges"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_wrong_claude_surface_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: "fuzzywigg (smtp.eth)"\nsurface: browser-claude\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'expected',
        )

def test_schema_rejects_semver_letters() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "a.b.c"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: repository-specific\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'semver',
        )

def test_schema_rejects_date_slash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog='# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026/09/13"\nowner: x\nedit_policy: x\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'ISO-8601',
        )

def test_schema_rejects_edit_policy_invent_absent_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge='# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: "2026-09-13"\nowner: copilot\nscope: x\nedit_policy: "keep thin badge row"\ncloses: "#16"\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'invent',
        )

def test_schema_rejects_secret_sk() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents='# AGENTS\n\n```yaml\nversion: "1.0.0"\nlast_updated: "2026-04-13"\nmaintainer: smtp.eth\nscope: "sk-abcdefghijklmnopqrstuvwxyz12"\nparent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'secret',
        )

def test_schema_rejects_secret_xoxb() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude='# CLAUDE\n\n```yaml\nrepo: "xoxb-1234567890-abcdefghij"\nowner: "fuzzywigg (smtp.eth)"\nsurface: copilot\nautonomy_level: 1\nlast_updated: "2026-04-13"\nparent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n',
        )
        assert_fail(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            'secret',
        )

def test_schema_rejects_missing_agents_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        (tmp_path / "AGENTS.md").unlink()
        assert_fail(scripts / "check_stewardship_schema.py", tmp_path, "missing file")


def test_schema_rejects_missing_badge_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        (tmp_path / "docs" / "badge-standard.md").unlink()
        assert_fail(scripts / "check_stewardship_schema.py", tmp_path, "missing file")


def test_schema_rejects_missing_publish_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        (tmp_path / "docs" / "wiki" / "PUBLISH.md").unlink()
        assert_fail(scripts / "check_stewardship_schema.py", tmp_path, "missing file")


def test_schema_rejects_missing_backlog_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        (tmp_path / "docs" / "issue-backlog.md").unlink()
        assert_fail(scripts / "check_stewardship_schema.py", tmp_path, "missing file")


def test_schema_rejects_missing_claude_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        (tmp_path / "CLAUDE.md").unlink()
        assert_fail(scripts / "check_stewardship_schema.py", tmp_path, "missing file")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in tests:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}", file=sys.stderr)
    if failed:
        print(f"Schema self-tests FAILED: {failed}/{len(tests)}", file=sys.stderr)
        return 1
    print(f"OK: stewardship schema self-tests passed ({len(tests)} cases + live tree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
