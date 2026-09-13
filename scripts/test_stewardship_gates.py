#!/usr/bin/env python3
"""Self-tests for stewardship gates (positive live-tree + negative fixtures).

Runs in CI after the live-tree gates so regressions in checkers fail closed.
Does not invent product surface — only validates gate behavior.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

GATE_SCRIPTS = (
    "check_badge_standard.py",
    "check_wiki_outline.py",
    "check_stewardship_schema.py",
    "check_relative_links.py",
)

SHARED_SCRIPTS = ("stewardship_common.py",)


def run(script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def assert_pass_live(script: str) -> None:
    proc = run(SCRIPTS / script, ROOT)
    if proc.returncode != 0:
        raise AssertionError(f"{script} failed on live tree\n{proc.stdout}{proc.stderr}")


def _seed_scripts(tmp: Path, *names: str) -> Path:
    scripts_dir = tmp / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    for name in (*SHARED_SCRIPTS, *names):
        shutil.copy2(SCRIPTS / name, scripts_dir / name)
    return scripts_dir


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _minimal_workflows(tmp: Path) -> None:
    wf = tmp / ".github" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)
    link = """name: Link Check
on:
  pull_request:
permissions:
  contents: read
concurrency:
  group: link-check-test
  cancel-in-progress: true
jobs:
  link-check:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo lychee --max-concurrency 8 --timeout 20 --max-retries 3 --exclude-path .github/agents
"""
    lint = """name: Markdown Lint
on:
  pull_request:
  schedule:
    - cron: "30 6 * * 1"
permissions:
  contents: read
concurrency:
  group: markdown-lint-test
  cancel-in-progress: true
jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo markdownlint OWASP-AGENTIC.md
"""
    stew = """name: Stewardship Checks
on:
  pull_request:
  schedule:
    - cron: "15 6 * * 1"
permissions:
  contents: read
concurrency:
  group: stewardship-test
  cancel-in-progress: true
jobs:
  stewardship:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: bash scripts/run_stewardship_checks.sh
      - run: python3 scripts/test_stewardship_gates.py
"""
    (wf / "link-check.yml").write_text(link, encoding="utf-8")
    (wf / "markdown-lint.yml").write_text(lint, encoding="utf-8")
    (wf / "stewardship-checks.yml").write_text(stew, encoding="utf-8")


def _badge_standard_doc() -> str:
    return (
        "# Badge\n\n"
        "```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
        "owner: copilot\nscope: test\nedit_policy: \"do not invent product badges\"\n"
        "closes: \"#16\"\n```\n\n"
        "| Link Check | x | y |\n| Markdown Lint | x | y |\n| License | x | y |\n\n"
        "link-check.yml/badge.svg\nmarkdown-lint.yml/badge.svg\n"
        "img.shields.io/github/license/\ndo not invent product badges\n"
        "Three badges max. A fourth Stewardship Checks badge is intentionally not added.\n"
    )


def _good_readme(order: tuple[str, str, str] | None = None) -> str:
    labels = order or ("Link Check", "Markdown Lint", "License")
    lines = ["# agents-governance", ""]
    for label in labels:
        if label == "Link Check":
            lines.append(
                "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
                "actions/workflows/link-check.yml/badge.svg)]"
                "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)"
            )
        elif label == "Markdown Lint":
            lines.append(
                "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
                "actions/workflows/markdown-lint.yml/badge.svg)]"
                "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)"
            )
        elif label == "License":
            lines.append(
                "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
                "(LICENSE)"
            )
        else:
            lines.append(
                f"[![{label}](https://img.shields.io/badge/{label}-x-red)]"
                f"(https://example.com/{label})"
            )
    lines.extend(
        [
            "",
            "See [docs/badge-standard.md](docs/badge-standard.md).",
            "Run `bash scripts/run_stewardship_checks.sh`.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _seed_badge_tree(tmp: Path, readme: str) -> Path:
    scripts = _seed_scripts(tmp, "check_badge_standard.py")
    _minimal_workflows(tmp)
    _write(tmp / "LICENSE", "MIT\n")
    _write(tmp / "docs" / "badge-standard.md", _badge_standard_doc())
    _write(
        tmp / "CONTRIBUTING.md",
        "# Contributing\n\nRun `bash scripts/run_stewardship_checks.sh`.\n"
        "Do not invent product badges.\n",
    )
    _write(
        tmp / "AGENTS.md",
        "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
        "maintainer: smtp.eth\nscope: repository-specific\n"
        "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n\n"
        "## 3. Testing Requirements\n\n"
        "bash scripts/run_stewardship_checks.sh\n"
        "python3 scripts/test_stewardship_gates.py\n"
        "CI: markdown-lint.yml, link-check.yml, stewardship-checks.yml\n",
    )
    _write(tmp / "README.md", readme)
    return scripts


def assert_fail_script(script_path: Path, cwd: Path, needle: str) -> None:
    proc = run(script_path, cwd)
    blob = proc.stdout + proc.stderr
    if proc.returncode == 0:
        raise AssertionError(f"{script_path.name} unexpectedly passed\n{blob}")
    if needle not in blob:
        raise AssertionError(f"{script_path.name} missing {needle!r}\n{blob}")


def test_badge_rejects_wrong_order() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(
            tmp_path,
            _good_readme(("Markdown Lint", "Link Check", "License")),
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Badge labels must be in order",
        )


def test_badge_rejects_invent_product() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = _good_readme() + (
            "[![coverage](https://codecov.io/gh/fuzzywigg/agents-governance/branch/main/graph/badge.svg)]"
            "(https://codecov.io)\n"
        )
        # Put invent badge in the row by appending before body — rebuild row.
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n"
            "[![coverage](https://codecov.io/gh/fuzzywigg/agents-governance/branch/main/graph/badge.svg)]"
            "(https://codecov.io)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_rejects_wrong_repo_slug() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/other/repo/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/other/repo/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Badge URL repo slug must be",
        )


def test_badge_rejects_noncontiguous_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contiguous",
        )


def test_badge_rejects_secret_url() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?token=abc)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Secret-like token",
        )


def test_relative_links_reject_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\nSee [missing](./nope.md).\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_reject_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\nSee [out](../../etc/passwd).\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_relative_links_reject_missing_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\nSee [x](#does-not-exist).\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "missing heading",
        )


def test_relative_links_ignore_fenced_examples() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(
            tmp_path / "README.md",
            "# Title\n\n```markdown\n[broken](./missing-in-fence.md)\n```\n",
        )
        proc = run(scripts / "check_relative_links.py", tmp_path)
        if proc.returncode != 0:
            raise AssertionError(
                f"fenced example should be ignored\n{proc.stdout}{proc.stderr}"
            )


def test_wiki_rejects_unexpected_page() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_wiki_outline.py")
        wiki = tmp_path / "docs" / "wiki"
        for name in (
            "Home.md",
            "Overview.md",
            "Autonomy-Levels.md",
            "Repo-Stewardship.md",
            "Agent-Routing.md",
            "Security-Boundaries.md",
            "PUBLISH.md",
            "Extra.md",
        ):
            body = f"# {name}\n\n[Home](Home.md)\n"
            if name == "Home.md":
                body = (
                    "# Home\n\n"
                    "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                    "[Badge](../badge-standard.md)\n"
                    "[Overview](Overview.md)\n"
                    "[Autonomy-Levels](Autonomy-Levels.md)\n"
                    "[Repo-Stewardship](Repo-Stewardship.md)\n"
                    "[Agent-Routing](Agent-Routing.md)\n"
                    "[Security-Boundaries](Security-Boundaries.md)\n\n"
                    "## Out of scope\n\nSecrets and invent product frameworks.\n"
                )
            elif name == "PUBLISH.md":
                body = (
                    "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                    "purpose: x\ncloses: \"#16\"\n```\n\n"
                    "| `Home.md` | Home |\n| `Overview.md` | Overview |\n"
                    "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
                    "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
                    "| `Agent-Routing.md` | Agent-Routing |\n"
                    "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
                    "Do **not** push `PUBLISH.md`.\n"
                    "Link Check and Markdown Lint. No secrets.\n"
                )
            elif name == "Repo-Stewardship.md":
                body = (
                    "# Repo\n\n[← Home](Home.md)\n\n"
                    "markdown-lint link-check stewardship-checks\n"
                    "run_stewardship_checks.sh relative links badge\n"
                    "no invent product\n"
                )
            elif name == "Autonomy-Levels.md":
                body = "# A\n\n[Home](Home.md)\n\nL0 L1 autonomy\n"
            elif name == "Security-Boundaries.md":
                body = "# S\n\n[Home](Home.md)\n\nkill switch secret\n"
            elif name == "Agent-Routing.md":
                body = "# R\n\n[Home](Home.md)\n\nsurface routing\n"
            elif name == "Overview.md":
                body = "# O\n\n[Home](Home.md)\n\ngovernance public\n"
            _write(wiki / name, body)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Unexpected markdown",
        )


def test_schema_rejects_wrong_value() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_stewardship_schema.py")
        _write(
            tmp_path / "AGENTS.md",
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/wrong/repo\nautonomy_level: 1\n```\n",
        )
        _write(
            tmp_path / "CLAUDE.md",
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n",
        )
        _write(
            tmp_path / "docs" / "badge-standard.md",
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n",
        )
        _write(
            tmp_path / "docs" / "wiki" / "PUBLISH.md",
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"#16\"\n```\n",
        )
        _write(
            tmp_path / "docs" / "issue-backlog.md",
            "# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: x\nedit_policy: x\n```\n",
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_inactive_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_stewardship_schema.py")
        _write(
            tmp_path / "AGENTS.md",
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n",
        )
        _write(
            tmp_path / "CLAUDE.md",
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n",
        )
        _write(
            tmp_path / "docs" / "badge-standard.md",
            "# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n",
        )
        _write(
            tmp_path / "docs" / "wiki" / "PUBLISH.md",
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"#16\"\n```\n",
        )
        _write(
            tmp_path / "docs" / "issue-backlog.md",
            "# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: x\nedit_policy: x\n```\n",
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "status must be ACTIVE",
        )


def test_common_secret_patterns() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: WPS433

    sample = "token: ghp_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("ghp_ token should match SECRET_PATTERNS")
    pem = "-----BEGIN RSA PRIVATE KEY-----\nMIIE\n"
    if not any(p.search(pem) for p in SECRET_PATTERNS):
        raise AssertionError("PEM private key should match SECRET_PATTERNS")


def test_workflow_hardening_requires_timeout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        # Break link-check timeout
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("timeout-minutes: 10", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def main() -> int:
    tests = [
        test_badge_rejects_wrong_order,
        test_badge_rejects_invent_product,
        test_badge_rejects_wrong_repo_slug,
        test_badge_rejects_noncontiguous_row,
        test_badge_rejects_secret_url,
        test_relative_links_reject_missing,
        test_relative_links_reject_escape,
        test_relative_links_reject_missing_fragment,
        test_relative_links_ignore_fenced_examples,
        test_wiki_rejects_unexpected_page,
        test_schema_rejects_wrong_value,
        test_schema_rejects_inactive_status,
        test_common_secret_patterns,
        test_workflow_hardening_requires_timeout,
    ]
    try:
        for script in GATE_SCRIPTS:
            assert_pass_live(script)
        for test in tests:
            test()
    except AssertionError as exc:
        print(f"Stewardship self-test FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"OK: stewardship gate self-tests passed ({len(tests)} cases + live tree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
