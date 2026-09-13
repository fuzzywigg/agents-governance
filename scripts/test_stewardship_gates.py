#!/usr/bin/env python3
"""Self-tests for stewardship gates (positive live-tree + negative fixtures).

Runs in CI after the live-tree gates so regressions in checkers fail closed.
Does not invent product surface — only validates gate behavior.
TOKENMAXX coverage: badge / wiki / schema / relative / workflow / secrets /
lycheeignore shields / actionlint-style / markdown-link edges.
Deepened after #29: cancel-in-progress:true / agents exclude / md **/*.md /
lycheeignore http://* / Repo-Stewardship actionlint.
Deepened after #30: Python 3.12 pin / Home invent+secrets / existing-path fixtures.
Deepened after #31: lychee --verbose/--no-progress + stewardship actions/checkout
+ commerce/coveralls/x.com badge hints + wiki L0/secret/surface/governance.
Deepened after #32: link/markdown actions/checkout + lychee-action + MD013
+ twitter/codecov/downloads/github_pat + wiki discord/js + schema edit_policy.
Deepened after #33: lycheeverse/lychee-action / markdownlint-cli2-action /
MD013 line_length / pip install PyYAML / deepen edges.
Deepened after #34: DavidAnson/markdownlint-cli2-action / --github-token /
MD024 / download-actionlint.bash / deepen edges.
Deepened after #35: MD024 siblings_only / rhysd/actionlint / curl download /
lychee-action with: token: / deepen edges.
Deepened after #36: MD013 line_length 200 / MD024 siblings_only:true /
raw.githubusercontent.com + curl -fsSL / deepen edges.
Deepened after #37: markdownlint default:true / get_actionlint.outputs /
actionlint /v1.7.7/ path / lychee --max-concurrency 8 --timeout 20
--max-retries 3 / deepen edges.
Deepened after #38: MD033/MD041/MD060 false / markdownlint-cli2-action@v24 /
setup-python@v5 / id: get_actionlint / deepen edges.
Deepened after #39: actions/checkout@v7 / lychee-action@v2 / job timeouts
20/10/15 / weekly crons / ubuntu-latest / pip --quiet / shell: bash /
actionlint -color / CI workflow pin edges (not fixture-reject spam).
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
  push:
    paths:
      - "**/*.md"
      - ".lycheeignore"
  pull_request:
  schedule:
    - cron: "0 6 * * 1"
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: link-check-test
  cancel-in-progress: true
jobs:
  link-check:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v7
      - uses: lycheeverse/lychee-action@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          args: >-
            lychee --verbose --no-progress --max-concurrency 8 --timeout 20
            --max-retries 3 --exclude-loopback --exclude-path .github/agents
            --github-token GITHUB_TOKEN
          fail: true
"""
    lint = """name: Markdown Lint
on:
  pull_request:
  schedule:
    - cron: "30 6 * * 1"
  workflow_dispatch:
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
      - uses: actions/checkout@v7
      - uses: DavidAnson/markdownlint-cli2-action@v24
      - run: echo markdownlint "**/*.md" OWASP-AGENTIC.md .github/agents .markdownlint.json
"""
    stew = """name: Stewardship Checks
on:
  pull_request:
  schedule:
    - cron: "15 6 * * 1"
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: stewardship-test
  cancel-in-progress: true
jobs:
  stewardship:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install --quiet pyyaml
      - run: bash scripts/run_stewardship_checks.sh
      - run: python3 scripts/test_stewardship_gates.py
      - run: python3 scripts/test_wiki_outline.py
      - name: Download actionlint
        id: get_actionlint
        run: bash <(curl -fsSL https://raw.githubusercontent.com/rhysd/actionlint/v1.7.7/scripts/download-actionlint.bash) 1.7.7
        shell: bash
      - name: actionlint existing workflow paths
        run: ${{ steps.get_actionlint.outputs.executable }} -color .github/workflows/link-check.yml .github/workflows/markdown-lint.yml .github/workflows/stewardship-checks.yml
"""
    (wf / "link-check.yml").write_text(link, encoding="utf-8")
    (wf / "markdown-lint.yml").write_text(lint, encoding="utf-8")
    (wf / "stewardship-checks.yml").write_text(stew, encoding="utf-8")
    _write(
        tmp / ".lycheeignore",
        "# flaky badge CDN\nhttps://img\\.shields\\.io\n",
    )
    _write(
        tmp / ".markdownlint.json",
        '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
        '  "MD024": { "siblings_only": true },\n'
        '  "MD033": false,\n  "MD041": false,\n  "MD060": false\n}\n',
    )


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
        "Executable enforcement: stewardship-checks.yml badge gate (quiet stewardship).\n"
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
        "python3 scripts/test_wiki_outline.py\n"
        "CI: markdown-lint.yml, link-check.yml, stewardship-checks.yml\n",
    )
    _write(tmp / "README.md", readme)
    return scripts


def _seed_schema_tree(
    tmp: Path,
    *,
    agents: str | None = None,
    claude: str | None = None,
    badge: str | None = None,
    publish: str | None = None,
    backlog: str | None = None,
) -> Path:
    scripts = _seed_scripts(tmp, "check_stewardship_schema.py")
    _write(
        tmp / "AGENTS.md",
        agents
        or (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        ),
    )
    _write(
        tmp / "CLAUDE.md",
        claude
        or (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        ),
    )
    _write(
        tmp / "docs" / "badge-standard.md",
        badge
        or (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        ),
    )
    _write(
        tmp / "docs" / "wiki" / "PUBLISH.md",
        publish
        or (
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"#16\"\n```\n"
        ),
    )
    _write(
        tmp / "docs" / "issue-backlog.md",
        backlog
        or (
            "# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: x\nedit_policy: x\n```\n"
        ),
    )
    return scripts


def _seed_wiki_tree(tmp: Path, *, extra_pages: tuple[str, ...] = (), mutate=None) -> Path:
    scripts = _seed_scripts(tmp, "check_wiki_outline.py")
    wiki = tmp / "docs" / "wiki"
    pages = {
        "Home.md": (
            "# Home\n\n"
            "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
            "[AGENTS-ECOSYSTEM](https://github.com/fuzzywigg/agents-governance/"
            "blob/main/AGENTS-ECOSYSTEM.md)\n"
            "[Badge](../badge-standard.md)\n"
            "[Overview](Overview.md)\n"
            "[Autonomy-Levels](Autonomy-Levels.md)\n"
            "[Repo-Stewardship](Repo-Stewardship.md)\n"
            "[Agent-Routing](Agent-Routing.md)\n"
            "[Security-Boundaries](Security-Boundaries.md)\n\n"
            "## Out of scope\n\nSecrets and invent product frameworks.\n\n"
            "Maintained by smtp.eth.\n"
        ),
        "PUBLISH.md": (
            "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
            "purpose: x\ncloses: \"#16\"\n```\n\n"
            "In-repo source under docs/wiki; remote agents-governance.wiki.git.\n\n"
            "| `Home.md` | Home |\n| `Overview.md` | Overview |\n"
            "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
            "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
            "| `Agent-Routing.md` | Agent-Routing |\n"
            "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
            "Do **not** push `PUBLISH.md`.\n"
            "Link Check and Markdown Lint. No secrets. No MEMORY dumps.\n"
        ),
        "Repo-Stewardship.md": (
            "# Repo\n\n[← Home](Home.md)\n\n"
            "markdown-lint link-check stewardship-checks\n"
            "run_stewardship_checks.sh relative links badge\n"
            "test_stewardship_gates.py\n"
            "actionlint on existing workflow paths\n"
            "AGENTS-ECOSYSTEM approval boundary\n"
            "no invent product\n"
        ),
        "Autonomy-Levels.md": (
            "# A\n\n[Home](Home.md)\n\nL0 L1 L2 L3 autonomy .kill_switch\n"
        ),
        "Security-Boundaries.md": (
            "# S\n\n[Home](Home.md)\n\nkill switch secret credential SECURITY.md\n"
        ),
        "Agent-Routing.md": (
            "# R\n\n[Home](Home.md)\n\nsurface routing copilot geryon\n"
        ),
        "Overview.md": (
            "# O\n\n[Home](Home.md)\n\ngovernance public AGENTS-ECOSYSTEM scratchpad\n"
        ),
    }
    for name in extra_pages:
        pages[name] = f"# {name}\n\n[Home](Home.md)\n"
    if mutate:
        mutate(pages)
    for name, body in pages.items():
        _write(wiki / name, body)
    return scripts


def assert_fail_script(script_path: Path, cwd: Path, needle: str) -> None:
    proc = run(script_path, cwd)
    blob = proc.stdout + proc.stderr
    if proc.returncode == 0:
        raise AssertionError(f"{script_path.name} unexpectedly passed\n{blob}")
    if needle not in blob:
        raise AssertionError(f"{script_path.name} missing {needle!r}\n{blob}")


def assert_pass_script(script_path: Path, cwd: Path) -> None:
    proc = run(script_path, cwd)
    if proc.returncode != 0:
        raise AssertionError(
            f"{script_path.name} unexpectedly failed\n{proc.stdout}{proc.stderr}"
        )


# --- Badge fixtures ---------------------------------------------------------


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


def test_badge_rejects_http_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](http://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
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
            "must be https://",
        )


def test_badge_rejects_stewardship_product_badge() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = _good_readme() + (
            "\n[![Stewardship](https://img.shields.io/badge/stewardship-x-green)]"
            "(https://example.com)\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        # Stewardship marketed as a badge anywhere in README fails closed.
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not add a Stewardship",
        )


def test_badge_rejects_wrong_license_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(https://example.com/not-license)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "License badge link must point at LICENSE",
        )


def test_badge_rejects_missing_workflow_dispatch() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("workflow_dispatch:", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "workflow_dispatch",
        )


def test_badge_rejects_missing_fail_true() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("fail: true", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fail: true",
        )


def test_badge_rejects_missing_markdownlint_config() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(".markdownlint.json", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".markdownlint.json",
        )


def test_badge_rejects_missing_contributing_invent_warning() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(
            tmp_path / "CONTRIBUTING.md",
            "# Contributing\n\nRun `bash scripts/run_stewardship_checks.sh`.\n",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "invent-product",
        )


def test_badge_passes_good_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        assert_pass_script(scripts / "check_badge_standard.py", tmp_path)


# --- Relative link fixtures -------------------------------------------------


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
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_ignore_tilde_fences() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(
            tmp_path / "README.md",
            "# Title\n\n~~~\n[broken](./missing-tilde.md)\n~~~\n",
        )
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_javascript_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](javascript:alert(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_data_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](data:text/html,hi)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_http_insecure() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](http://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_relative_links_reject_protocol_relative() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](//evil.example/x)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "protocol-relative",
        )


def test_relative_links_reject_encoded_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        # %2e%2e == ..
        _write(tmp_path / "README.md", "# T\n\n[x](%2e%2e/%2e%2e/etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_relative_links_reject_cross_file_missing_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A\n\nSee [b](b.md#nope).\n")
        _write(tmp_path / "b.md", "# B\n\nBody.\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "missing heading",
        )


def test_relative_links_accept_valid_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Section One\n\nSee [x](#section-one).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_skip_owasp_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\nOk.\n")
        _write(tmp_path / "OWASP-AGENTIC.md", "# O\n\n[broken](./missing.md)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


# --- Wiki fixtures ----------------------------------------------------------


def test_wiki_rejects_unexpected_page() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_wiki_tree(tmp_path, extra_pages=("Extra.md",))
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Unexpected markdown",
        )


def test_wiki_rejects_missing_home_backlink() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = "# O\n\ngovernance public\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "must link back to Home.md",
        )


def test_wiki_rejects_invent_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[![coverage](https://img.shields.io/badge/coverage-99-green)]"
                "(https://codecov.io)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_missing_topic_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Autonomy-Levels.md"] = "# A\n\n[Home](Home.md)\n\nlevels only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_wiki_rejects_http_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[site](http://example.com)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_secret_pattern() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "token: ghp_" + ("a" * 36) + "\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "secret-like pattern",
        )


def test_wiki_rejects_missing_out_of_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Badge](../badge-standard.md)\n"
                "[Overview](Overview.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "Secrets and invent product frameworks mentioned without section.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Out of scope",
        )


# --- Schema fixtures --------------------------------------------------------


def test_schema_rejects_wrong_value() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/wrong/repo\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_inactive_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "status must be ACTIVE",
        )


def test_schema_rejects_missing_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "autonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_bad_autonomy_level() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 9\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level must be int in 0..3",
        )


def test_schema_rejects_bad_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier must be a positive int",
        )


def test_schema_rejects_bad_iso_date() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"13-04-2026\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ISO-8601",
        )


def test_schema_rejects_edit_policy_without_invent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"agents may edit freely\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "no-invent-product",
        )


def test_schema_rejects_wrong_surface() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: geryon\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "surface",
        )


def test_schema_rejects_bad_semver() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"v1\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "semver",
        )


def test_schema_rejects_closes_without_issue() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"soon\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "closes must reference an issue",
        )


def test_schema_rejects_empty_required_value() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: \"\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


# --- Common / workflow fixtures ---------------------------------------------


def test_common_secret_patterns() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    samples = (
        ("ghp_" + ("a" * 36), "ghp_"),
        ("-----BEGIN RSA PRIVATE KEY-----\nMIIE\n", "PRIVATE KEY"),
        ("aws_secret_access_key = '" + ("A" * 24) + "'", "aws_secret"),
        ("xoxb-" + ("1" * 12), "xoxb"),
        ('password = "hunter2xx"', "password"),
        ("npm_" + ("b" * 24), "npm_"),
        ("AIza" + ("c" * 24), "AIza"),
    )
    for sample, label in samples:
        if not any(p.search(sample) for p in SECRET_PATTERNS):
            raise AssertionError(f"{label} sample should match SECRET_PATTERNS: {sample!r}")


def test_common_dangerous_schemes() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    for target, want in (
        ("javascript:alert(1)", "javascript:"),
        ("DATA:text/html,x", "data:"),
        ("vbscript:msgbox", "vbscript:"),
        ("file:///etc/passwd", "file:"),
        ("https://example.com", None),
        ("./docs/x.md", None),
    ):
        got = has_dangerous_scheme(target)
        if got != want:
            raise AssertionError(f"has_dangerous_scheme({target!r})={got!r}, want {want!r}")


def test_workflow_hardening_requires_timeout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("timeout-minutes: 20", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_workflow_hardening_requires_schedule() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("schedule:", "sched_disabled:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "weekly schedule",
        )


def test_workflow_hardening_requires_concurrency() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("concurrency:", "group_disabled:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "concurrency",
        )


def test_workflow_hardening_requires_pyyaml_install() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("pyyaml", "notinstalled")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "PyYAML",
        )


def test_lycheeignore_requires_shields_exclude() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "# nothing about shields\nhttps://example.com/\n")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "img.shields.io",
        )


def test_lycheeignore_rejects_star_exclude() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "https://img\\.shields\\.io\nhttps://*\n")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not exclude all http",
        )


def test_missing_lycheeignore_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / ".lycheeignore").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Missing .lycheeignore",
        )


def test_missing_markdownlint_json_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / ".markdownlint.json").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Missing .markdownlint.json",
        )


def test_actionlint_rejects_pull_request_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8")
        # Keep pull_request: for hardening; add forbidden pull_request_target.
        text = text.replace(
            "pull_request:\n",
            "pull_request:\n  pull_request_target:\n",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read", "contents: write"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_unpinned_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "unpinned action",
        )


def test_actionlint_rejects_float_main_ref() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@main"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float on @main",
        )


def test_actionlint_requires_runs_on() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("runs-on:", "runner:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "runs-on",
        )


def test_stewardship_requires_actionlint_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("actionlint", "notlint")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actionlint",
        )


def test_link_check_requires_lycheeignore_reference() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(".lycheeignore", ".ignore-links")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".lycheeignore",
        )


def test_badge_rejects_missing_license_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / "LICENSE").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Missing LICENSE",
        )


def test_badge_rejects_forbidden_hint_in_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=codecov)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_wrong_link_check_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/other.yml/badge.svg)]"
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
            "link-check.yml/badge.svg",
        )


def test_badge_rejects_missing_readme_badge_doc_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = _good_readme().replace("docs/badge-standard.md", "docs/other.md")
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "docs/badge-standard.md",
        )


def test_badge_rejects_missing_agents_selftest_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(
            tmp_path / "AGENTS.md",
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n\n"
            "## 3. Testing Requirements\n\n"
            "bash scripts/run_stewardship_checks.sh\n"
            "CI: markdown-lint.yml, link-check.yml, stewardship-checks.yml\n",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "test_stewardship_gates.py",
        )


def test_workflow_rejects_missing_permissions_read() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("contents: read", "contents: none")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: read",
        )


def test_workflow_rejects_missing_exclude_loopback() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--exclude-loopback", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exclude loopback",
        )


def test_workflow_rejects_missing_max_retries() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--max-retries 3", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--max-retries",
        )


# --- Extra markdown-link / relative fixtures --------------------------------


def test_relative_links_reject_file_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](file:///etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_vbscript_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](vbscript:msgbox(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_empty_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x]()\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_accept_mailto() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[mail](mailto:ops@example.com)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_accept_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[ok](https://example.com/docs)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_skip_github_agents() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\nOk.\n")
        _write(
            tmp_path / ".github" / "agents" / "notes.md",
            "# Agents\n\n[broken](./missing.md)\n",
        )
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_broken_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n![alt](./missing.png)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_cross_file_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A\n\nSee [b](b.md#section-two).\n")
        _write(tmp_path / "b.md", "# B\n\n## Section Two\n\nBody.\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_github_slug_punctuation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(
            tmp_path / "README.md",
            "# Title\n\n## A & B\n\nSee [x](#a--b).\n",
        )
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


# --- Extra wiki / schema fixtures -------------------------------------------


def test_wiki_rejects_missing_page() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_wiki_tree(tmp_path)
        (tmp_path / "docs" / "wiki" / "Overview.md").unlink()
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Missing required wiki source page",
        )


def test_wiki_rejects_missing_readme_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[Badge](../badge-standard.md)\n"
                "[Overview](Overview.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "must link back to the repository README",
        )


def test_wiki_rejects_missing_ci_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "run_stewardship_checks.sh relative links badge\n"
                "no invent product\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "stewardship CI workflows",
        )


def test_wiki_rejects_dangerous_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](javascript:alert(1))\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_passes_good_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_wiki_tree(tmp_path)
        assert_pass_script(scripts / "check_wiki_outline.py", tmp_path)


def test_schema_rejects_missing_yaml_block() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents="# AGENTS\n\nNo metadata fence.\n",
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "no fenced",
        )


def test_schema_rejects_missing_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        (tmp_path / "CLAUDE.md").unlink()
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing file",
        )


def test_schema_passes_good_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(tmp_path)
        assert_pass_script(scripts / "check_stewardship_schema.py", tmp_path)


def test_common_secret_url_hints() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_URL_HINTS  # noqa: E402

    required = ("token=", "access_token=", "api_key=", "ghp_", "github_pat_")
    for hint in required:
        if hint not in SECRET_URL_HINTS:
            raise AssertionError(f"SECRET_URL_HINTS missing {hint!r}")


def test_common_forbidden_badge_hints() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    required = ("coverage", "codecov", "discord", "stars", "producthunt")
    for hint in required:
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_github_slug_helper() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    if github_slug("Section One") != "section-one":
        raise AssertionError("github_slug Section One")
    if github_slug("A & B") != "a--b":
        raise AssertionError(f"github_slug A & B -> {github_slug('A & B')!r}")


# --- TOKENMAXX deepen after #27: actionlint / link-check / wiki / schema -----


def test_actionlint_rejects_write_all() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "permissions:\n  contents: read",
            "permissions: write-all",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_master_ref() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@master"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float on @master",
        )


def test_actionlint_rejects_float_latest_ref() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@latest"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float on @latest",
        )


def test_actionlint_requires_name() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("name: Link Check\n", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "top-level name:",
        )


def test_actionlint_requires_steps() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("steps:", "phase:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "steps",
        )


def test_link_check_requires_github_token() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("GITHUB_TOKEN", "NO_TOKEN")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "GITHUB_TOKEN",
        )


def test_link_check_requires_lychee_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("lychee", "linktool")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "lychee",
        )


def test_link_check_requires_exclude_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--exclude-path .github/agents", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exclude .github/agents",
        )


def test_link_check_requires_max_concurrency() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--max-concurrency 8", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--max-concurrency",
        )


def test_link_check_requires_lychee_timeout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--timeout 20", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--timeout",
        )


def test_markdown_lint_requires_owasp_exclude() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("OWASP-AGENTIC.md", "OTHER.md")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "OWASP-AGENTIC.md",
        )


def test_markdown_lint_requires_agents_exclude() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(".github/agents", ".github/other")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".github/agents",
        )


def test_markdown_lint_requires_markdownlint_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("markdownlint", "mdl")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdownlint",
        )


def test_stewardship_requires_selftest_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "test_stewardship_gates.py", "test_other.py"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "test_stewardship_gates.py",
        )


def test_stewardship_requires_setup_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("setup-python", "setup-node")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Python",
        )


def test_stewardship_requires_run_script() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "run_stewardship_checks.sh", "run_other.sh"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "run_stewardship_checks.sh",
        )


def test_stewardship_requires_actionlint_version_pin() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("1.7.7", "9.9.9")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "1.7.7",
        )


def test_stewardship_requires_actionlint_all_workflows() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            ".github/workflows/markdown-lint.yml",
            ".github/workflows/other-lint.yml",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdown-lint.yml",
        )


def test_workflow_rejects_missing_pull_request() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("pull_request:", "push_request:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request",
        )


def test_badge_rejects_missing_h1() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = _good_readme().replace("# agents-governance", "agents-governance")
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "missing H1",
        )


def test_badge_rejects_two_badges_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_rejects_http_badge_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(http://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
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
            "must use https://",
        )


def test_badge_rejects_wrong_markdown_lint_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/wrong-lint.yml/badge.svg)]"
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
            "markdown-lint.yml/badge.svg",
        )


def test_badge_rejects_missing_readme_stewardship_script() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = _good_readme().replace("run_stewardship_checks.sh", "run_other.sh")
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "run_stewardship_checks.sh",
        )


def test_badge_rejects_missing_contributing_script() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(
            tmp_path / "CONTRIBUTING.md",
            "# Contributing\n\nDo not invent product badges.\n",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "run_stewardship_checks.sh",
        )


def test_badge_rejects_missing_workflow_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / ".github" / "workflows" / "markdown-lint.yml").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Missing workflow",
        )


def test_lycheeignore_accepts_regex_escaped_shields() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "https://img\\.shields\\.io\n")
        assert_pass_script(scripts / "check_badge_standard.py", tmp_path)


def test_lycheeignore_accepts_literal_shields() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "https://img.shields.io/\n")
        assert_pass_script(scripts / "check_badge_standard.py", tmp_path)


def test_relative_links_accept_tel() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[call](tel:+15551212)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_nul() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](./ok%00.md)\n")
        _write(tmp_path / "ok.md", "# Ok\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "NUL",
        )


def test_relative_links_reject_bare_hash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](#)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_accept_title_attr() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A\n")
        _write(tmp_path / "README.md", '# T\n\n[x](a.md "title here")\n')
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_accept_existing_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "pic.png", "x")
        _write(tmp_path / "README.md", "# T\n\n![alt](./pic.png)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_wiki_rejects_missing_publish() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_wiki_tree(tmp_path)
        (tmp_path / "docs" / "wiki" / "PUBLISH.md").unlink()
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Missing operator page",
        )


def test_wiki_rejects_missing_badge_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Overview](Overview.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "badge standard",
        )


def test_wiki_rejects_missing_home_page_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Badge](../badge-standard.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Overview.md",
        )


def test_wiki_rejects_missing_publish_do_not_push() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "purpose: x\ncloses: \"#16\"\n```\n\n"
                "| `Home.md` | Home |\n| `Overview.md` | Overview |\n"
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
                "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
                "| `Agent-Routing.md` | Agent-Routing |\n"
                "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
                "Link Check and Markdown Lint. No secrets.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "not pushed",
        )


def test_wiki_rejects_missing_relative_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "markdown-lint link-check stewardship-checks\n"
                "run_stewardship_checks.sh badge\n"
                "no invent product\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "relative-link",
        )


def test_wiki_rejects_missing_invent_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "markdown-lint link-check stewardship-checks\n"
                "run_stewardship_checks.sh relative links badge\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent",
        )


def test_schema_rejects_wrong_maintainer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: other\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "maintainer",
        )


def test_schema_rejects_wrong_claude_parent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/other/repo\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_wrong_badge_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: geryon\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "owner",
        )


def test_schema_rejects_secret_in_doc() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n\n"
                "token: ghp_" + ("a" * 36) + "\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "secret-like",
        )


def test_common_strip_fenced() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import strip_fenced_code  # noqa: E402

    text = "# T\n\n```md\n[x](./missing.md)\n```\n\nok\n"
    out = strip_fenced_code(text)
    if "[x](./missing.md)" in out:
        raise AssertionError("fenced link should be stripped")
    if "ok" not in out:
        raise AssertionError("non-fenced text should remain")


def test_common_dangerous_schemes_complete() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import DANGEROUS_LINK_SCHEMES  # noqa: E402

    required = ("javascript:", "data:", "vbscript:", "file:")
    for scheme in required:
        if scheme not in DANGEROUS_LINK_SCHEMES:
            raise AssertionError(f"DANGEROUS_LINK_SCHEMES missing {scheme!r}")


# --- TOKENMAXX deepen after #28: existing-path fixtures only ----------------


def test_workflow_requires_cancel_in_progress() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true", "cancel-in-progress-disabled: true"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress",
        )


def test_link_check_requires_markdown_glob() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("**/*.md", "**/*.txt")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "**/*.md",
        )


def test_actionlint_requires_timeout_minutes_local() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("timeout-minutes:", "timebox-minutes:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_actionlint_allows_docker_uses_without_pin() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "- uses: actions/checkout@v7",
            "- uses: docker://alpine:3.20\n      - uses: actions/checkout@v7",
        )
        path.write_text(text, encoding="utf-8")
        assert_pass_script(scripts / "check_badge_standard.py", tmp_path)


def test_badge_rejects_missing_badge_standard_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / "docs" / "badge-standard.md").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "docs/badge-standard.md",
        )


def test_badge_rejects_missing_contributing_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / "CONTRIBUTING.md").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "CONTRIBUTING.md",
        )


def test_badge_rejects_license_image_wrong_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/license-MIT-blue)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "img.shields.io/github/license/",
        )


def test_badge_rejects_license_image_missing_repo_slug() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/other/repo)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fuzzywigg/agents-governance",
        )


def test_badge_rejects_secret_in_readme_body() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = _good_readme() + "\napi_key: " + ("k" * 20) + "\n"
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "secret-like",
        )


def test_badge_rejects_agents_missing_link_check_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8").replace(
            "link-check.yml", "linkcheck.yml"
        )
        (tmp_path / "AGENTS.md").write_text(agents, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "link-check.yml",
        )


def test_badge_rejects_agents_missing_markdown_lint_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8").replace(
            "markdown-lint.yml", "md-lint.yml"
        )
        (tmp_path / "AGENTS.md").write_text(agents, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdown-lint.yml",
        )


def test_badge_rejects_agents_missing_stewardship_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8").replace(
            "stewardship-checks.yml", "stew-checks.yml"
        )
        (tmp_path / "AGENTS.md").write_text(agents, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "stewardship-checks.yml",
        )


def test_badge_rejects_agents_missing_run_script_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8").replace(
            "run_stewardship_checks.sh", "run_checks.sh"
        )
        (tmp_path / "AGENTS.md").write_text(agents, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "run_stewardship_checks.sh",
        )


def test_badge_doc_rejects_missing_invent_wording() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("do not invent product badges", "keep badges minimal")
        doc = doc.replace("invent product", "product chrome")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "invent",
        )


def test_badge_doc_rejects_missing_three_badge_max() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("Three badges max", "Keep badges thin")
        doc = doc.replace("three badges", "badges")
        doc = doc.replace("3 badges", "badges")
        doc = doc.replace("badges max", "badges thin")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "three-badge",
        )


def test_badge_doc_rejects_stewardship_without_fourth_refusal() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("fourth", "extra")
        doc = doc.replace("intentionally", "usually")
        doc = doc.replace("not** added", "deferred")
        doc = doc.replace("not added", "deferred")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fourth badge",
        )


def test_badge_accepts_absolute_license_blob_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(https://github.com/fuzzywigg/agents-governance/blob/main/LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_pass_script(scripts / "check_badge_standard.py", tmp_path)


def test_lycheeignore_rejects_https_star() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "https://*\n")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not exclude all http",
        )


def test_relative_links_accept_angle_bracket_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A\n\n[x](<https://example.com/path>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_accept_license_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "LICENSE", "MIT\n")
        _write(tmp_path / "a.md", "# A\n\n[License](LICENSE)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_github_slug_ampersand() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # GitHub: strip '&' then map spaces → '-' yielding double hyphen.
    if github_slug("A & B") != "a--b":
        raise AssertionError(f"unexpected slug: {github_slug('A & B')!r}")


def test_relative_links_accept_ampersand_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A & B\n\n[jump](#a--b)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_whitespace_only_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        # Spaces inside () are stripped → empty → fail closed.
        _write(tmp_path / "a.md", "# A\n\n[x](   )\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_wiki_rejects_missing_publish_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                pages["PUBLISH.md"]
                .replace("Link Check", "CI Check")
                .replace("link-check", "ci-check")
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Link Check",
        )


def test_wiki_rejects_missing_publish_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                pages["PUBLISH.md"]
                .replace("Markdown Lint", "Doc Lint")
                .replace("markdown", "docsfmt")
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Markdown",
        )


def test_wiki_rejects_missing_publish_secrets() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                pages["PUBLISH.md"]
                .replace("No secrets.", "No tokens.")
                .replace("secrets", "tokens")
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "secrets",
        )


def test_wiki_rejects_missing_overview_topic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = "# O\n\n[Home](Home.md)\n\nsummary only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "governance",
        )


def test_wiki_rejects_missing_security_topic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Security-Boundaries.md"] = "# S\n\n[Home](Home.md)\n\nboundaries\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "kill",
        )


def test_wiki_rejects_stars_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge stars chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "stars",
        )


def test_wiki_rejects_missing_wiki_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_wiki_outline.py")
        # No docs/wiki created → fail closed.
        proc = run(scripts / "check_wiki_outline.py", tmp_path)
        blob = proc.stdout + proc.stderr
        if proc.returncode == 0:
            raise AssertionError(f"wiki check unexpectedly passed\n{blob}")
        if "docs/wiki/" not in blob:
            raise AssertionError(f"missing docs/wiki/ failure\n{blob}")


def test_schema_rejects_wrong_agents_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: ecosystem-wide\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "scope",
        )


def test_schema_rejects_wrong_agents_parent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/other/governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_wrong_claude_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: other-repo\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "repo",
        )


def test_schema_rejects_inactive_publish_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: DRAFT\ncreated: \"2026-09-13\"\npurpose: x\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_backlog_wrong_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog=(
                "# I\n\n```yaml\nstatus: ACTIVE\ntier: 9\ncreated: \"2026-09-13\"\n"
                "owner: x\nedit_policy: x\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_schema_rejects_autonomy_as_string() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\n"
                "autonomy_level: \"1\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_bad_claude_date() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"13-04-2026\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ISO-8601",
        )


def test_schema_rejects_unparseable_yaml() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\n: bad\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "AGENTS.md",
        )


def test_common_secret_patterns_extended() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    samples = (
        "npm_" + ("n" * 24),
        "AIza" + ("A" * 35),
        "xoxb-1234567890-abcdefghij",
        'aws_secret_access_key: "' + ("A" * 24) + '"',
        "github_pat_" + ("p" * 22),
        "sk-" + ("s" * 24),
    )
    for sample in samples:
        if not any(p.search(sample) for p in SECRET_PATTERNS):
            raise AssertionError(f"SECRET_PATTERNS missed {sample[:20]!r}...")


def test_common_forbidden_badge_hints_extended() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    required = (
        "producthunt",
        "buymeacoffee",
        "opencollective",
        "coveralls",
        "pypi/",
        "npm/",
    )
    for hint in required:
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_has_dangerous_scheme_helper() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("javascript:alert(1)") != "javascript:":
        raise AssertionError("expected javascript: match")
    if has_dangerous_scheme("https://example.com") is not None:
        raise AssertionError("https should be clean")


def test_common_load_workflow_text_helper() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import load_workflow_text  # noqa: E402

    text = load_workflow_text("link-check.yml")
    if text is None or "lychee" not in text.lower():
        raise AssertionError("load_workflow_text failed for link-check.yml")
    if load_workflow_text("does-not-exist.yml") is not None:
        raise AssertionError("missing workflow should return None")


def test_common_fail_helper_appends() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import fail  # noqa: E402

    errors: list[str] = []
    fail("one", errors)
    fail("two", errors)
    if errors != ["one", "two"]:
        raise AssertionError(f"fail() append broken: {errors!r}")


def test_common_markdown_files_helper() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import markdown_files  # noqa: E402

    found = markdown_files("README.md", "docs/badge-standard.md")
    names = {p.name for p in found}
    if "README.md" not in names or "badge-standard.md" not in names:
        raise AssertionError(f"markdown_files missed expected paths: {names}")


def test_markdown_lint_requires_config_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            ".markdownlint.json", ".markdownlint.yaml"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".markdownlint.json",
        )


def test_stewardship_requires_actionlint_link_check_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            ".github/workflows/link-check.yml",
            ".github/workflows/links.yml",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "link-check.yml",
        )


def test_stewardship_requires_actionlint_stewardship_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            ".github/workflows/stewardship-checks.yml",
            ".github/workflows/stew.yml",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "stewardship-checks.yml",
        )


def test_workflow_rejects_missing_dispatch_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "workflow_dispatch:", "workflow_call:"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "workflow_dispatch",
        )


# --- TOKENMAXX deepen after #29: existing-path fixtures only ----------------


def test_workflow_requires_cancel_in_progress_true() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true", "cancel-in-progress: false"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_requires_cancel_in_progress_true_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true", "cancel-in-progress: false"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_link_check_requires_agents_exclude_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "--exclude-path .github/agents", "--exclude-path vendor/agents"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".github/agents",
        )


def test_markdown_lint_requires_markdown_glob() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("**/*.md", "**/*.txt")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "**/*.md",
        )


def test_lycheeignore_rejects_http_star() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "http://*\n")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not exclude all http",
        )


def test_stewardship_requires_actionlint_markdown_lint_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            ".github/workflows/markdown-lint.yml",
            ".github/workflows/md-lint.yml",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdown-lint.yml",
        )


def test_actionlint_rejects_unpinned_second_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "- uses: actions/setup-python@v5",
            "- uses: actions/setup-python",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "unpinned action",
        )


def test_actionlint_rejects_float_main_on_setup_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "- uses: actions/setup-python@v5",
            "- uses: actions/setup-python@main",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "@main",
        )


def test_workflow_rejects_missing_schedule_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("schedule:", "scheduled:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "schedule",
        )


def test_workflow_rejects_missing_concurrency_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("concurrency:", "serial:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "concurrency",
        )


def test_badge_rejects_link_check_relative_workflow_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(.github/workflows/link-check.yml)\n"
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
            "absolute https://",
        )


def test_badge_rejects_markdown_lint_relative_workflow_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(.github/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "absolute https://",
        )


def test_badge_accepts_dot_slash_license_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(./LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_pass_script(scripts / "check_badge_standard.py", tmp_path)


def test_badge_rejects_forbidden_coverage_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(https://example.com/coverage)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "coverage",
        )


def test_badge_rejects_secret_url_token_query() -> None:
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


def test_badge_doc_rejects_missing_link_check_label() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("Link Check", "Link Gate").replace("link-check", "linkgate")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Link Check",
        )


def test_badge_doc_rejects_missing_shields_license_snippet() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("img.shields.io/github/license/", "shields.io/license/")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "shields license image",
        )


def test_badge_rejects_four_badges() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
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
            "[![Extra](https://img.shields.io/badge/extra-x-red)]"
            "(https://example.com/extra)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_relative_links_accept_angle_bracket_relative() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "b.md", "# B\n")
        _write(tmp_path / "a.md", "# A\n\n[x](<b.md>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_github_slug_backticks() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    if github_slug("`Code` Title") != "code-title":
        raise AssertionError(f"unexpected slug: {github_slug('`Code` Title')!r}")


def test_relative_links_github_slug_markdown_link_heading() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    if github_slug("[Linked](https://example.com) Heading") != "linked-heading":
        raise AssertionError(
            f"unexpected slug: {github_slug('[Linked](https://example.com) Heading')!r}"
        )


def test_relative_links_accept_nested_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "x.md", "# X\n")
        _write(tmp_path / "a.md", "# A\n\n[x](docs/x.md)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_missing_nested() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A\n\n[x](docs/missing.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_image_with_title() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "img.png", "x")
        _write(tmp_path / "a.md", '# A\n\n![alt](img.png "title")\n')
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_percent_encoded_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        # %2e%2e is ".." — must fail closed as repo escape.
        _write(tmp_path / "a.md", "# A\n\n[x](%2e%2e/%2e%2e/etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_wiki_rejects_missing_actionlint_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                pages["Repo-Stewardship.md"]
                .replace("actionlint", "workflow-lint")
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "actionlint",
        )


def test_wiki_rejects_missing_autonomy_topic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Autonomy-Levels.md"] = "# A\n\n[Home](Home.md)\n\nlevels only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "L0",
        )


def test_wiki_rejects_missing_routing_topic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Agent-Routing.md"] = "# R\n\n[Home](Home.md)\n\nagents only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "surface",
        )


def test_wiki_rejects_missing_home_out_of_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                pages["Home.md"]
                .replace("## Out of scope", "## Limits")
                .replace("Out of scope", "Limits")
                .replace("out of scope", "limits")
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Out of scope",
        )


def test_wiki_rejects_forks_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge forks chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "forks",
        )


def test_wiki_rejects_codecov_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[![cov](https://codecov.io/gh/x/badge.svg)](https://codecov.io)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "codecov",
        )


def test_wiki_rejects_missing_home_to_routing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "[Agent-Routing](Agent-Routing.md)\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Agent-Routing.md",
        )


def test_wiki_rejects_secret_in_publish() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\napi_key: " + ("z" * 20) + "\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "secret-like",
        )


def test_wiki_rejects_missing_publish_page_table_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(
                "| `Security-Boundaries.md` | Security-Boundaries |\n", ""
            ).replace("Security-Boundaries", "SecBounds")

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Security-Boundaries",
        )


def test_schema_rejects_wrong_badge_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_wrong_badge_tier() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 2\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_schema_rejects_publish_closes_without_issue() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n"
                "closes: \"soon\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "closes",
        )


def test_schema_rejects_empty_agents_maintainer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: \"\"\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_tier_as_string() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog=(
                "# I\n\n```yaml\nstatus: ACTIVE\ntier: \"1\"\ncreated: \"2026-09-13\"\n"
                "owner: x\nedit_policy: x\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_schema_rejects_autonomy_out_of_range() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\n"
                "autonomy_level: 9\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_non_mapping_yaml() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\n- version: \"1.0.0\"\n- autonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "mapping",
        )


def test_schema_rejects_bad_badge_created_date() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"09/13/2026\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ISO-8601",
        )


def test_common_secret_url_hints_complete() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_URL_HINTS  # noqa: E402

    required = (
        "token=",
        "access_token=",
        "api_key=",
        "apikey=",
        "client_secret=",
        "ghp_",
        "gho_",
        "github_pat_",
    )
    for hint in required:
        if hint not in SECRET_URL_HINTS:
            raise AssertionError(f"SECRET_URL_HINTS missing {hint!r}")


def test_common_forbidden_badge_hints_social() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    required = ("coverage", "codecov", "discord", "twitter", "forks", "followers")
    for hint in required:
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_secret_patterns_private_key() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "-----BEGIN RSA PRIVATE KEY-----\nMIIE\n"
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missed RSA private key block")


def test_common_strip_fenced_tilde() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import strip_fenced_code  # noqa: E402

    text = "before\n~~~md\n[bad](missing.md)\n~~~\nafter\n"
    stripped = strip_fenced_code(text)
    if "missing.md" in stripped:
        raise AssertionError("tilde fence not stripped")
    if "before" not in stripped or "after" not in stripped:
        raise AssertionError("strip_fenced_code removed surrounding prose")


def test_common_scan_secrets_ghp() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.md"
        path.write_text("token ghp_" + ("x" * 36) + "\n", encoding="utf-8")
        # scan_secrets uses ROOT-relative labels; call with label override.
        errors: list[str] = []
        # Monkey via label to avoid ROOT.relative_to issues outside repo.
        text = path.read_text(encoding="utf-8")
        from stewardship_common import SECRET_PATTERNS, fail  # noqa: E402

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail("doc.md matches forbidden secret-like pattern", errors)
        if not errors:
            raise AssertionError("expected ghp_ secret detection")


def test_markdown_lint_requires_agents_exclude_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            ".github/agents", ".github/prompts"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".github/agents",
        )


def test_link_check_requires_fail_true_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("fail: true", "fail: false")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fail: true",
        )


def test_stewardship_requires_pyyaml_install_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("pyyaml", "ruamel")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "PyYAML",
        )


def test_workflow_rejects_missing_permissions_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "permissions:\n  contents: read\n", ""
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: read",
        )


# --- TOKENMAXX deepen after #30: existing-path fixtures only ----------------


def test_stewardship_requires_python_version_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("python-version", "py-version")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "python-version",
        )


def test_stewardship_requires_python_312_pin() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("3.12", "3.11")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "3.12",
        )


def test_workflow_requires_cancel_in_progress_true_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true", "cancel-in-progress: false"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_actionlint_rejects_float_master_on_setup_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/setup-python@v5", "actions/setup-python@master"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "@master",
        )


def test_actionlint_rejects_float_latest_on_setup_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/setup-python@v5", "actions/setup-python@latest"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "@latest",
        )


def test_actionlint_rejects_contents_write_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read", "contents: write"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_workflow_rejects_missing_timeout_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("timeout-minutes: 15", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_workflow_rejects_missing_dispatch_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("workflow_dispatch:", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "workflow_dispatch",
        )


def test_lycheeignore_rejects_bare_star() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        _write(tmp_path / ".lycheeignore", "*\n")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not exclude all http",
        )


def test_link_check_requires_markdown_glob_not_txt() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("**/*.md", "**/*.txt")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "**/*.md",
        )


def test_badge_rejects_discord_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(https://discord.gg/example)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "discord",
        )


def test_badge_rejects_producthunt_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(https://www.producthunt.com/posts/x)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "producthunt",
        )


def test_badge_rejects_api_key_query() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?api_key=abc)]"
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


def test_badge_rejects_access_token_query() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?access_token=abc)]"
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


def test_badge_rejects_http_license_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](http://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must be https://",
        )


def test_badge_rejects_license_first_order() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(
            tmp_path,
            _good_readme(("License", "Link Check", "Markdown Lint")),
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Badge labels must be in order",
        )


def test_badge_doc_rejects_missing_markdown_lint_snippet() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("markdown-lint.yml/badge.svg", "md-lint.yml/badge.svg")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdown-lint",
        )


def test_badge_doc_rejects_missing_link_check_snippet() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        doc = (tmp_path / "docs" / "badge-standard.md").read_text(encoding="utf-8")
        doc = doc.replace("link-check.yml/badge.svg", "linkgate.yml/badge.svg")
        (tmp_path / "docs" / "badge-standard.md").write_text(doc, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "link-check",
        )


def test_badge_rejects_missing_workflow_link_check_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / ".github" / "workflows" / "link-check.yml").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Missing workflow",
        )


def test_relative_links_skip_node_modules() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\nOk.\n")
        _write(
            tmp_path / "node_modules" / "pkg" / "README.md",
            "# Pkg\n\n[broken](./missing.md)\n",
        )
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_javascript_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](JAVASCRIPT:alert(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_data_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](DATA:text/html,hi)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_nested_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](../../etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_relative_links_github_slug_numbers() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    if github_slug("Section 2.1") != "section-21":
        raise AssertionError(f"unexpected slug: {github_slug('Section 2.1')!r}")


def test_relative_links_accept_numbered_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(
            tmp_path / "README.md",
            "# Title\n\n## Section 2.1\n\nSee [x](#section-21).\n",
        )
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_accept_mailto_and_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(
            tmp_path / "README.md",
            "# T\n\n[mail](mailto:ops@example.com)\n[web](https://example.com)\n",
        )
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_file_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](FILE:///etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_invent_on_home() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "Secrets and invent product frameworks.",
                "Secrets and private frameworks.",
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_missing_secrets_on_home() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "Secrets and invent product frameworks.",
                "Invent product frameworks only.",
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "secrets",
        )


def test_wiki_rejects_missing_l1_on_autonomy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Autonomy-Levels.md"] = "# A\n\n[Home](Home.md)\n\nL0 autonomy only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "L1",
        )


def test_wiki_rejects_missing_kill_on_security() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Security-Boundaries.md"] = (
                "# S\n\n[Home](Home.md)\n\nsecret boundary only\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "kill",
        )


def test_wiki_rejects_downloads_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge downloads chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "downloads",
        )


def test_wiki_rejects_missing_home_to_security() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "[Security-Boundaries](Security-Boundaries.md)\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Security-Boundaries.md",
        )


def test_wiki_rejects_missing_publish_overview_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                pages["PUBLISH.md"]
                .replace("| `Overview.md` | Overview |\n", "")
                .replace("Overview", "Summ")
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Overview",
        )


def test_wiki_rejects_data_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](data:text/html,hi)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_badge_topic_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "markdown-lint link-check stewardship-checks\n"
                "run_stewardship_checks.sh relative links\n"
                "actionlint on existing workflow paths\n"
                "no invent product\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "badge",
        )


def test_schema_rejects_wrong_claude_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"other\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "owner",
        )


def test_schema_rejects_wrong_claude_autonomy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 2\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_inactive_backlog_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog=(
                "# I\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: x\nedit_policy: x\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_empty_badge_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: \"\"\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_missing_badge_closes_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_agents_autonomy_drift() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 0\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_publish_missing_purpose_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_float_autonomy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\n"
                "autonomy_level: 1.5\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_common_forbidden_badge_hints_commerce() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    required = ("producthunt", "buymeacoffee", "opencollective", "npm/", "pypi/")
    for hint in required:
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_secret_patterns_sk_token() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "sk-" + ("A" * 24)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missed sk- token")


def test_common_has_dangerous_scheme_casefold() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("JaVaScRiPt:alert(1)") != "javascript:":
        raise AssertionError("has_dangerous_scheme should casefold javascript:")


def test_common_scan_secrets_url_token_hint() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_URL_HINTS  # noqa: E402

    if "token=" not in SECRET_URL_HINTS:
        raise AssertionError("SECRET_URL_HINTS missing token=")
    sample = "https://example.com/x?token=abc"
    if "token=" not in sample:
        raise AssertionError("fixture sample broken")


def test_markdown_lint_requires_owasp_exclude_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "OWASP-AGENTIC.md", "OWASP-OTHER.md"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "OWASP-AGENTIC.md",
        )


def test_stewardship_requires_timeout_minutes_needle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("timeout-minutes", "timeout_mins")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_actionlint_rejects_write_all_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "permissions:\n  contents: read",
            "permissions: write-all",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_badge_rejects_stars_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=stars)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "stars",
        )


def test_relative_links_accept_parent_relative_existing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Root\n")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[up](../README.md)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_wiki_rejects_twitter_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge twitter chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "twitter",
        )


def test_schema_rejects_wrong_agents_version_semver_prerelease() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0-beta\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "semver",
        )


def test_common_dangerous_schemes_file() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("file:///tmp/x") != "file:":
        raise AssertionError("file: scheme should be dangerous")


# --- TOKENMAXX deepen after #31: existing-path fixtures only ----------------


def test_link_check_requires_no_progress() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--no-progress", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--no-progress",
        )


def test_link_check_requires_verbose() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--verbose", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--verbose",
        )


def test_stewardship_requires_actions_checkout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "local/repo-checkout@v4"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actions/checkout",
        )


def test_workflow_requires_cancel_in_progress_true_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true", "cancel-in-progress: false"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_actionlint_rejects_pull_request_target_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "pull_request:\n",
            "pull_request:\n  pull_request_target:\n",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_unpinned_setup_python() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/setup-python@v5", "actions/setup-python"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "unpinned action",
        )


def test_badge_rejects_coveralls_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=coveralls)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_buymeacoffee_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=buymeacoffee)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_opencollective_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=opencollective)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_npm_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/npm/v/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_pypi_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/pypi/v/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_followers_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=followers)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_x_com_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=x.com)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_apikey_query() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?apikey=abc)]"
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


def test_badge_rejects_client_secret_query() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?client_secret=abc)]"
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


def test_badge_rejects_gho_token_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?x=gho_abcdefghij)]"
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


def test_badge_rejects_license_wrong_shields_slug() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/other/repo)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "repo slug",
        )


def test_badge_rejects_missing_stewardship_workflow_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / ".github" / "workflows" / "stewardship-checks.yml").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Missing workflow",
        )


def test_badge_doc_rejects_missing_license_label() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8").replace("| License |", "| SPDX |")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "License",
        )


def test_relative_links_skip_git_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\nOk.\n")
        _write(tmp_path / ".git" / "notes.md", "# Git\n\n[broken](./missing.md)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_vbscript_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](VBSCRIPT:msgbox(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_encoded_nested_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](%2e%2e/%2e%2e/%2e%2e/etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_relative_links_accept_same_dir_existing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "a.md", "# A\n")
        _write(tmp_path / "README.md", "# T\n\n[x](a.md)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_github_slug_underscore() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # GitHub-ish: underscore emphasis markers are stripped (foo_bar → foobar).
    if github_slug("foo_bar") != "foobar":
        raise AssertionError(f"github_slug foo_bar -> {github_slug('foo_bar')!r}")


def test_relative_links_accept_underscore_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## foo_bar\n\nSee [x](#foobar).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_wiki_rejects_missing_l0_on_autonomy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Autonomy-Levels.md"] = "# A\n\n[Home](Home.md)\n\nL1 autonomy\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_wiki_rejects_missing_secret_on_security() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Security-Boundaries.md"] = "# S\n\n[Home](Home.md)\n\nkill switch only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_wiki_rejects_missing_surface_on_routing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Agent-Routing.md"] = "# R\n\n[Home](Home.md)\n\nrouting only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_wiki_rejects_missing_governance_on_overview() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = "# O\n\n[Home](Home.md)\n\npublic only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_wiki_rejects_missing_public_on_overview() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = "# O\n\n[Home](Home.md)\n\ngovernance only\n"

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_wiki_rejects_missing_home_to_autonomy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Badge](../badge-standard.md)\n"
                "[Overview](Overview.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Autonomy-Levels.md",
        )


def test_wiki_rejects_followers_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge followers chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_x_com_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge x.com chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_missing_publish_home_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "purpose: x\ncloses: \"#16\"\n```\n\n"
                "| `Overview.md` | Overview |\n"
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
                "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
                "| `Agent-Routing.md` | Agent-Routing |\n"
                "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
                "Do **not** push `PUBLISH.md`.\n"
                "Link Check and Markdown Lint. No secrets.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Home.md",
        )


def test_wiki_rejects_file_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](file:///etc/passwd)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_schema_rejects_missing_claude_surface_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "autonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_missing_backlog_owner_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog=(
                "# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "edit_policy: x\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_empty_publish_purpose() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: \"   \"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_empty_agents_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: \"\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_wrong_agents_autonomy_zero() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 0\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_missing_publish_closes_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_missing_claude_repo_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_badge_closes_without_hash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "closes must reference an issue",
        )


def test_common_forbidden_badge_hints_registry() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    required = (
        "coveralls",
        "buymeacoffee",
        "opencollective",
        "npm/",
        "pypi/",
        "followers",
        "x.com",
    )
    for hint in required:
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_secret_url_hints_apikey_client() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_URL_HINTS  # noqa: E402

    for hint in ("apikey=", "client_secret=", "gho_"):
        if hint not in SECRET_URL_HINTS:
            raise AssertionError(f"SECRET_URL_HINTS missing {hint!r}")


def test_common_secret_patterns_gho() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "gho_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("gho_ sample should match SECRET_PATTERNS")


def test_common_scan_secrets_url_apikey() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.md"
        path.write_text(
            "See https://example.com/x?apikey=supersecretvalue\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        scan_secrets(path, errors, label="fixture.md")
        if not errors:
            raise AssertionError("apikey= URL hint should fail scan_secrets")


def test_markdown_lint_requires_markdown_glob_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("**/*.md", "*.markdown")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "**/*.md",
        )


def test_link_check_requires_exclude_loopback_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--exclude-loopback", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exclude loopback",
        )


def test_stewardship_requires_python_312_pin_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("3.12", "3.11")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "3.12",
        )


def test_workflow_rejects_missing_schedule_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("schedule:", "sched_disabled:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "weekly schedule",
        )


def test_badge_rejects_forks_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=forks)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_accept_docs_nested_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\nSee [b](b.md#section-two).\n")
        _write(tmp_path / "docs" / "b.md", "# B\n\n## Section Two\n\nBody.\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_wiki_rejects_missing_run_script_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "markdown-lint link-check stewardship-checks\n"
                "relative links badge\n"
                "no invent product\n"
                "actionlint on existing workflow paths\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "run_stewardship_checks.sh",
        )


def test_schema_rejects_wrong_claude_surface_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: browser-claude\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "surface",
        )


def test_common_dangerous_schemes_vbscript() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("vbscript:msgbox") != "vbscript:":
        raise AssertionError("vbscript: scheme should be dangerous")


# --- TOKENMAXX deepen after #32: checkout / lychee-action / MD013 / edges -----


def test_link_check_requires_lychee_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("lychee-action", "lychee-cli")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "lychee-action",
        )


def test_link_check_requires_actions_checkout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("actions/checkout", "actions/noop")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actions/checkout",
        )


def test_markdown_lint_requires_actions_checkout() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("actions/checkout", "actions/noop")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actions/checkout",
        )


def test_markdownlint_json_requires_md013() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text('{\n  "default": true\n}\n', encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD013",
        )


def test_actionlint_rejects_pull_request_target_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "write-all\npermissions:\n  contents: read",
        )
        # Force a top-level permissions: write-all line.
        text = "permissions: write-all\n" + text
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_badge_rejects_twitter_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=twitter)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_codecov_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=codecov)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_downloads_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=downloads)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_github_pat_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?github_pat_ABC)]"
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


def test_badge_rejects_ghp_token_hint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?x=ghp_abcdefghijklmnopqrst)]"
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


def test_badge_rejects_markdown_lint_first_order() -> None:
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


def test_badge_doc_rejects_missing_three_badges_max_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        for needle in ("Three badges max", "three badges", "badges max"):
            text = text.replace(needle, "badge row")
            text = text.replace(needle.title(), "badge row")
            text = text.replace(needle.lower(), "badge row")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "three-badge",
        )


def test_badge_rejects_missing_agents_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        (tmp_path / "AGENTS.md").unlink()
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "AGENTS.md",
        )


def test_relative_links_reject_javascript_mixed_case() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](JavaScript:alert(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_data_mixed_case() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](DATA:text/plain,hi)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_accept_tel_with_title() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", '# T\n\n[call](tel:+15551212 "phone")\n')
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_github_slug_colon_punct() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Colon stripped: "Note: one" → "note-one"
    if github_slug("Note: one") != "note-one":
        raise AssertionError(f"github_slug Note: one -> {github_slug('Note: one')!r}")


def test_relative_links_accept_colon_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Note: one\n\nSee [x](#note-one).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_missing_image_nested() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n![x](images/missing.png)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_license_from_docs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "LICENSE", "MIT\n")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[L](../LICENSE)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_http_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](HTTP://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_missing_home_to_overview() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Badge](../badge-standard.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Overview.md",
        )


def test_wiki_rejects_discord_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge discord chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_buymeacoffee_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge buymeacoffee chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_javascript_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](javascript:alert(1))\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_autonomy_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "purpose: x\ncloses: \"#16\"\n```\n\n"
                "| `Home.md` | Home |\n"
                "| `Overview.md` | Overview |\n"
                "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
                "| `Agent-Routing.md` | Agent-Routing |\n"
                "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
                "Do **not** push `PUBLISH.md`.\n"
                "Link Check and Markdown Lint. No secrets.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Autonomy-Levels.md",
        )


def test_wiki_rejects_missing_publish_security_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "purpose: x\ncloses: \"#16\"\n```\n\n"
                "| `Home.md` | Home |\n"
                "| `Overview.md` | Overview |\n"
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
                "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
                "| `Agent-Routing.md` | Agent-Routing |\n\n"
                "Do **not** push `PUBLISH.md`.\n"
                "Link Check and Markdown Lint. No secrets.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Security-Boundaries.md",
        )


def test_wiki_rejects_missing_publish_routing_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "purpose: x\ncloses: \"#16\"\n```\n\n"
                "| `Home.md` | Home |\n"
                "| `Overview.md` | Overview |\n"
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
                "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
                "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
                "Do **not** push `PUBLISH.md`.\n"
                "Link Check and Markdown Lint. No secrets.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Agent-Routing.md",
        )


def test_wiki_rejects_opencollective_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge opencollective chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_missing_actionlint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "markdown-lint link-check stewardship-checks\n"
                "run_stewardship_checks.sh relative links badge\n"
                "no invent product\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "actionlint",
        )


def test_schema_rejects_empty_badge_edit_policy() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_empty_claude_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_missing_agents_version_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_missing_backlog_edit_policy_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            backlog=(
                "# I\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: x\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_tier_zero() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_schema_rejects_empty_publish_created() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            publish=(
                "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"\"\npurpose: x\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_wrong_badge_owner_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: geryon\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "owner",
        )


def test_schema_rejects_autonomy_three_ok_range_but_agents_expected() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 3\n```\n"
            ),
        )
        # autonomy 3 is in 0..3 range but EXPECTED_VALUES wants 1
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_common_secret_patterns_npm() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "npm_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("npm_ sample should match SECRET_PATTERNS")


def test_common_secret_patterns_aiza() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "AIza" + ("A" * 35)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("AIza sample should match SECRET_PATTERNS")


def test_common_secret_patterns_slack_xoxb() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "xoxb-" + ("a" * 12)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("xoxb- sample should match SECRET_PATTERNS")


def test_common_secret_url_hints_github_pat() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_URL_HINTS  # noqa: E402

    if "github_pat_" not in SECRET_URL_HINTS:
        raise AssertionError("SECRET_URL_HINTS missing github_pat_")


def test_common_forbidden_badge_hints_twitter_codecov() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("twitter", "codecov", "downloads", "discord"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_scan_secrets_github_pat() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.md"
        path.write_text(
            "token github_pat_" + ("x" * 22) + "\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        scan_secrets(path, errors, label="fixture.md")
        if not errors:
            raise AssertionError("github_pat_ should fail scan_secrets")


def test_common_dangerous_schemes_javascript() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("javascript:alert(1)") != "javascript:":
        raise AssertionError("javascript: scheme should be dangerous")


def test_stewardship_requires_actions_checkout_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("actions/checkout", "actions/noop")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actions/checkout",
        )


def test_link_check_requires_verbose_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--verbose", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--verbose",
        )


def test_link_check_requires_no_progress_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--no-progress", "")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--no-progress",
        )


def test_markdown_lint_requires_config_needle_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(".markdownlint.json", ".mdlrc")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            ".markdownlint.json",
        )


def test_lycheeignore_rejects_https_star_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".lycheeignore"
        path.write_text("https://*\n", encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "https://*",
        )


def test_workflow_rejects_missing_pull_request_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("pull_request:", "pull_req:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request",
        )


def test_badge_rejects_producthunt_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=producthunt)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_accept_nested_image_existing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        img = tmp_path / "docs" / "images" / "ok.png"
        img.parent.mkdir(parents=True, exist_ok=True)
        img.write_bytes(b"\x89PNG\r\n\x1a\n")
        _write(tmp_path / "docs" / "a.md", "# A\n\n![x](images/ok.png)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_wiki_rejects_data_scheme_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](data:text/plain,hi)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_schema_rejects_missing_claude_last_updated_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_common_has_dangerous_scheme_data() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("data:text/html,<b>") != "data:":
        raise AssertionError("data: scheme should be dangerous")



# --- TOKENMAXX deepen after #33: lycheeverse / cli2-action / line_length / edges ---


def test_link_check_requires_lycheeverse_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "lycheeverse/lychee-action", "other/lychee-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "lycheeverse/lychee-action",
        )


def test_markdown_lint_requires_cli2_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "markdownlint-cli2-action", "markdownlint-cli-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdownlint-cli2-action",
        )


def test_markdownlint_json_requires_md013_line_length() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text('{\n  "default": true,\n  "MD013": true\n}\n', encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "line_length",
        )


def test_stewardship_requires_pip_install_pyyaml() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("pip install", "npm install")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pip install",
        )


def test_actionlint_rejects_pull_request_target_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = "permissions: write-all\n" + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_latest_on_checkout_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@latest"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_rejects_missing_concurrency_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("concurrency:", "concurrency_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "concurrency",
        )


def test_workflow_rejects_missing_timeout_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("timeout-minutes:", "timeout_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_badge_rejects_coverage_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=coverage)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_stars_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=stars)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_token_query_still() -> None:
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


def test_badge_rejects_license_http_link() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(http://github.com/fuzzywigg/agents-governance/blob/main/LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must use https://",
        )


def test_badge_rejects_four_badges_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
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
            "[![Extra](https://img.shields.io/badge/extra-x-red)]"
            "(https://example.com)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_doc_rejects_missing_fourth_refusal_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("fourth", "extra").replace("intentionally", "maybe")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fourth badge",
        )


def test_relative_links_accept_https_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](HTTPS://example.com)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_accept_mailto_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](MAILTO:a@example.com)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_file_mixed_case() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](File:///etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_github_slug_tilde() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Tilde stripped: "Note~ one" → "note-one"
    if github_slug("Note~ one") != "note-one":
        raise AssertionError(f"github_slug Note~ one -> {github_slug('Note~ one')!r}")


def test_relative_links_accept_tilde_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Note~ one\n\nSee [x](#note-one).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_missing_parent_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](../missing.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_angle_bracket_mailto() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](<mailto:a@example.com>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_protocol_relative_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](//example.com/x)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "protocol-relative",
        )


def test_wiki_rejects_missing_home_to_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Badge](../badge-standard.md)\n"
                "[Overview](Overview.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n"
                "[Security-Boundaries](Security-Boundaries.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Repo-Stewardship.md",
        )


def test_wiki_rejects_coveralls_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge coveralls chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_producthunt_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge producthunt chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_npm_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge npm/ chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_pypi_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge pypi/ chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_http_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](HTTP://example.com)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_vbscript_scheme() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](vbscript:msgbox(1))\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_stewardship_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = (
                "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
                "purpose: x\ncloses: \"#16\"\n```\n\n"
                "| `Home.md` | Home |\n"
                "| `Overview.md` | Overview |\n"
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
                "| `Agent-Routing.md` | Agent-Routing |\n"
                "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
                "Do **not** push `PUBLISH.md`.\n"
                "Link Check and Markdown Lint. No secrets.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Repo-Stewardship.md",
        )


def test_wiki_rejects_missing_relative_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = (
                "# Repo\n\n[← Home](Home.md)\n\n"
                "markdown-lint link-check stewardship-checks\n"
                "run_stewardship_checks.sh badge\n"
                "no invent product\n"
                "actionlint on existing workflow paths\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "relative-link",
        )


def test_schema_rejects_empty_badge_closes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_empty_agents_version() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_missing_agents_autonomy_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: smtp.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_missing_claude_parent_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_empty_claude_last_updated() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            claude=(
                "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
                "surface: copilot\nautonomy_level: 1\nlast_updated: \"\"\n"
                "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_wrong_badge_scope_empty_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: \"   \"\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "must be non-empty",
        )


def test_schema_rejects_tier_negative() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: -1\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_schema_rejects_wrong_agents_maintainer_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            agents=(
                "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
                "maintainer: other.eth\nscope: repository-specific\n"
                "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "maintainer",
        )


def test_common_secret_patterns_ghs() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghs_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("ghs_ sample should match SECRET_PATTERNS")


def test_common_secret_patterns_ghu() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghu_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("ghu_ sample should match SECRET_PATTERNS")


def test_common_secret_patterns_rk_token() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "rk-" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("rk- sample should match SECRET_PATTERNS")


def test_common_secret_patterns_aws_secret() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = 'aws_secret_access_key = "' + ("A" * 24) + '"'
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("aws_secret_access_key sample should match SECRET_PATTERNS")


def test_common_secret_patterns_openssh_key() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "-----BEGIN OPENSSH PRIVATE KEY-----\n"
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("OPENSSH PRIVATE KEY sample should match SECRET_PATTERNS")


def test_common_forbidden_badge_hints_coveralls_producthunt() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("coveralls", "producthunt", "npm/", "pypi/"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_scan_secrets_npm() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.md"
        path.write_text("token npm_" + ("a" * 36) + "\n", encoding="utf-8")
        errors: list[str] = []
        scan_secrets(path, errors, label="fixture.md")
        if not errors:
            raise AssertionError("npm_ should fail scan_secrets")


def test_common_has_dangerous_scheme_file_still() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("FILE:///tmp/x") != "file:":
        raise AssertionError("FILE: scheme should be dangerous (casefold)")


def test_link_check_requires_lychee_action_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("lychee-action", "lychee-cli")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "lychee-action",
        )


def test_markdownlint_json_requires_md013_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text('{\n  "default": true\n}\n', encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD013",
        )


def test_markdown_lint_requires_actions_checkout_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("actions/checkout", "actions/noop")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actions/checkout",
        )


def test_link_check_requires_actions_checkout_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("actions/checkout", "actions/noop")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "actions/checkout",
        )


def test_stewardship_requires_pyyaml_install_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("pyyaml", "requests")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "PyYAML",
        )


def test_badge_rejects_discord_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=discord)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_reject_http_uppercase_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](HTTP://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_javascript_scheme_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](javascript:alert(1))\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_schema_rejects_tier_zero_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_schema_tree(
            tmp_path,
            badge=(
                "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
                "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
                "closes: \"#16\"\n```\n"
            ),
        )
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_common_dangerous_schemes_vbscript_still() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("VBSCRIPT:msgbox") != "vbscript:":
        raise AssertionError("VBSCRIPT: scheme should be dangerous")



# --- TOKENMAXX deepen after #34: DavidAnson / --github-token / MD024 / edges ---


def test_markdown_lint_requires_davidanson_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "DavidAnson/markdownlint-cli2-action",
            "OtherOrg/markdownlint-cli2-action",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "DavidAnson/markdownlint-cli2-action",
        )


def test_link_check_requires_github_token_flag() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--github-token", "--other-token")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--github-token",
        )


def test_markdownlint_json_requires_md024() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 }\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD024",
        )


def test_stewardship_requires_download_actionlint_bash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "download-actionlint.bash",
            "fetch-actionlint.sh",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "download-actionlint.bash",
        )


def test_actionlint_rejects_pull_request_target_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = "permissions: write-all\n" + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_main_on_checkout_markdown() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@main"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_rejects_missing_schedule_on_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("schedule:", "schedule_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "schedule",
        )


def test_workflow_rejects_missing_workflow_dispatch_on_link_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "workflow_dispatch:", "workflow_dispatch_off:"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "workflow_dispatch",
        )


def test_badge_rejects_followers_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=followers)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_forks_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=forks)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_npm_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/npm/v/fake)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_pypi_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/pypi/v/fake)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_apikey_query_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?api_key=abc)]"
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


def test_badge_rejects_link_check_http_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](http://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
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
            "must be https://",
        )


def test_badge_rejects_blank_line_between_still() -> None:
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


def test_badge_doc_rejects_missing_three_max_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("Three badges max", "Many badges ok").replace(
            "badges max", "badges plenty"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "three-badge",
        )


def test_relative_links_accept_tel_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](TEL:+15551212)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_javascript_mixed_case_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](JavaScript:alert(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_data_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](DATA:text/plain,hi)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_github_slug_asterisk() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Asterisk stripped: "Note* one" → "note-one"
    if github_slug("Note* one") != "note-one":
        raise AssertionError(f"github_slug Note* one -> {github_slug('Note* one')!r}")


def test_relative_links_accept_asterisk_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Note* one\n\nSee [x](#note-one).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_broken_nested_docs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "sub" / "a.md", "# A\n\n[x](../gone.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_angle_bracket_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](<https://example.com>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_empty_parens_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x]()\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_reject_percent_traversal_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](%2e%2e/%2e%2e/etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_wiki_rejects_missing_home_to_security() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = (
                "# Home\n\n"
                "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
                "[Badge](../badge-standard.md)\n"
                "[Overview](Overview.md)\n"
                "[Autonomy-Levels](Autonomy-Levels.md)\n"
                "[Repo-Stewardship](Repo-Stewardship.md)\n"
                "[Agent-Routing](Agent-Routing.md)\n\n"
                "## Out of scope\n\nSecrets and invent product frameworks.\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Security-Boundaries.md",
        )


def test_wiki_rejects_buymeacoffee_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge buymeacoffee chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_opencollective_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge opencollective chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_codecov_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge codecov chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_downloads_badge_chrome() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge downloads chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_file_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](FILE:///etc/passwd)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_overview_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(
                "| `Overview.md` |", "| Overview missing |"
            ).replace("`Overview.md`", "Overview")

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Overview.md",
        )


def test_wiki_rejects_missing_actionlint_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "actionlint", "workflow-lint"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "actionlint",
        )


def test_wiki_rejects_missing_invent_on_stewardship_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "invent", "productize"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent",
        )


def test_schema_rejects_empty_badge_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: \"\"\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_empty_agents_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: \"\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_missing_agents_version_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_missing_claude_surface_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "autonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_empty_publish_purpose() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: \"\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_wrong_badge_status_draft() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_autonomy_four_oob() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 4\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "0..3",
        )


def test_schema_rejects_wrong_claude_repo_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: other-repo\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "expected",
        )


def test_schema_rejects_closes_without_hash_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"issue sixteen\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "closes must reference",
        )


def test_common_secret_patterns_ghr() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghr_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("ghr_ sample should match SECRET_PATTERNS")


def test_common_secret_patterns_gho() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "gho_" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("gho_ sample should match SECRET_PATTERNS")


def test_common_secret_patterns_sk_token() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "sk-" + ("a" * 36)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("sk- sample should match SECRET_PATTERNS")


def test_common_secret_patterns_ec_key() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "-----BEGIN EC PRIVATE KEY-----\n"
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("EC PRIVATE KEY sample should match SECRET_PATTERNS")


def test_common_forbidden_badge_hints_followers_forks() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("followers", "forks", "discord", "stars"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint!r}")


def test_common_scan_secrets_aiza() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.md"
        path.write_text("key AIza" + ("a" * 35) + "\n", encoding="utf-8")
        errors: list[str] = []
        scan_secrets(path, errors, label="fixture.md")
        if not errors:
            raise AssertionError("AIza should fail scan_secrets")


def test_common_has_dangerous_scheme_javascript_still() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("JAVASCRIPT:alert(1)") != "javascript:":
        raise AssertionError("JAVASCRIPT: scheme should be dangerous (casefold)")


def test_markdown_lint_requires_cli2_action_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "markdownlint-cli2-action", "markdownlint-cli-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdownlint-cli2-action",
        )


def test_link_check_requires_lycheeverse_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "lycheeverse/lychee-action", "other/lychee-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "lycheeverse/lychee-action",
        )


def test_markdownlint_json_requires_line_length_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": true,\n  "MD024": true\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "line_length",
        )


def test_stewardship_requires_pip_install_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("pip install", "npm install")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pip install",
        )


def test_badge_rejects_twitter_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance?"
            "label=twitter)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_reject_http_mixed_case_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](Http://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_data_scheme_still_after_34() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](data:text/plain,hi)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_schema_rejects_tier_zero_still_after_34() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "positive int",
        )


def test_common_dangerous_schemes_data_still() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import DANGEROUS_LINK_SCHEMES  # noqa: E402

    if "data:" not in DANGEROUS_LINK_SCHEMES:
        raise AssertionError("DANGEROUS_LINK_SCHEMES missing data:")



def test_markdownlint_json_requires_siblings_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": true\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "siblings_only",
        )


def test_stewardship_requires_rhysd_actionlint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "rhysd/actionlint",
            "other/actionlint",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "rhysd/actionlint",
        )


def test_stewardship_requires_curl_download() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("curl", "wget")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "curl",
        )


def test_link_check_requires_action_token() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("token:", "auth_token:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "token:",
        )


def test_actionlint_rejects_pull_request_target_on_link_check_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_stewardship_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_link_check_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = "permissions: write-all\n" + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_latest_on_checkout_stewardship() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@latest"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_markdown_lint() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_rejects_missing_concurrency_on_link_check_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("concurrency:", "concurrency_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "concurrency",
        )


def test_workflow_rejects_missing_timeout_on_markdown_lint_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "timeout-minutes:", "timeout_minutes_off:"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_badge_rejects_buymeacoffee_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/buymeacoffee-x-yellow)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_opencollective_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/opencollective-x-blue)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_coveralls_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/coveralls/github/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_xcom_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/x.com-follow-black)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_client_secret_query_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?client_secret=abc)]"
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


def test_badge_rejects_markdown_lint_http_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](http://github.com/fuzzywigg/agents-governance/"
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
            "must be https://",
        )


def test_badge_rejects_four_badges_still_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
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
            "[![Stars](https://img.shields.io/github/stars/fuzzywigg/agents-governance)]"
            "(https://github.com/fuzzywigg/agents-governance)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_doc_rejects_missing_fourth_refusal_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("fourth", "extra").replace("intentionally", "maybe")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fourth badge",
        )


def test_relative_links_accept_mailto_mixed_case() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](Mailto:a@b.co)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_vbscript_mixed_case_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](VbScript:msgbox(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_file_uppercase_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](FILE:///etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_github_slug_underscore() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Underscore emphasis marker stripped: "Foo_bar" → "foobar"
    if github_slug("Foo_bar") != "foobar":
        raise AssertionError(f"github_slug Foo_bar -> {github_slug('Foo_bar')!r}")


def test_relative_links_accept_underscore_heading_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Foo_bar\n\nSee [x](#foobar).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_broken_docs_sibling() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](missing-sibling.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_angle_bracket_tel() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](<tel:+15551212>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_bare_hash_only_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](#)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_reject_encoded_escape_nested_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(
            tmp_path / "docs" / "sub" / "a.md",
            "# A\n\n[x](%2e%2e/%2e%2e/%2e%2e/etc/passwd)\n",
        )
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "escapes repo",
        )


def test_wiki_rejects_missing_home_to_overview_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "[Overview](Overview.md)\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Overview.md",
        )


def test_wiki_rejects_discord_badge_chrome_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "discord badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_twitter_badge_chrome_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "twitter badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_stars_badge_chrome_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "stars badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_forks_badge_chrome_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "forks badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_javascript_uppercase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](JAVASCRIPT:alert(1))\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_autonomy_row() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n", ""
            ).replace("`Autonomy-Levels.md`", "")

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Autonomy-Levels.md",
        )


def test_wiki_rejects_missing_ci_link_check_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "link-check", "link_check_off"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "link-check",
        )


def test_wiki_rejects_missing_badge_topic_on_stewardship_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "badge", "row"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "topic hint",
        )


def test_schema_rejects_empty_badge_scope() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: \"\"\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_empty_claude_owner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_missing_agents_maintainer_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "scope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_missing_claude_repo_key() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "missing metadata keys",
        )


def test_schema_rejects_empty_publish_closes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_wrong_publish_status_draft() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: DRAFT\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_autonomy_negative() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: -1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "0..3",
        )


def test_schema_rejects_wrong_agents_scope_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: ecosystem-wide\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "repository-specific",
        )


def test_schema_rejects_semver_prerelease_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0-rc1\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "semver",
        )


def test_common_secret_patterns_github_pat() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    blob = "token github_pat_" + ("A" * 22)
    if not any(p.search(blob) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing github_pat_")


def test_common_secret_patterns_xoxb() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    blob = "xoxb-" + ("a" * 12)
    if not any(p.search(blob) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing xoxb-")


def test_common_secret_patterns_rsa_key() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    blob = "-----BEGIN RSA PRIVATE KEY-----\nMII\n"
    if not any(p.search(blob) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing RSA PRIVATE KEY")


def test_common_forbidden_badge_hints_buymeacoffee_opencollective() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("buymeacoffee", "opencollective"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint}")


def test_common_scan_secrets_xoxb() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS, fail  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        path = tmp_path / "doc.md"
        path.write_text("# T\n\nxoxb-" + ("a" * 12) + "\n", encoding="utf-8")
        text = path.read_text(encoding="utf-8")
        errors: list[str] = []
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(
                    f"doc.md matches forbidden secret-like pattern: {pattern.pattern}",
                    errors,
                )
        if not errors:
            raise AssertionError("expected xoxb secret match")


def test_common_has_dangerous_scheme_vbscript_still() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("vbscript:msgbox(1)") != "vbscript:":
        raise AssertionError("has_dangerous_scheme vbscript failed")


def test_markdown_lint_requires_davidanson_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "DavidAnson/markdownlint-cli2-action",
            "Acme/markdownlint-cli2-action",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "DavidAnson/markdownlint-cli2-action",
        )


def test_link_check_requires_github_token_flag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--github-token", "--other-token")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--github-token",
        )


def test_markdownlint_json_requires_md024_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 }\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD024",
        )


def test_stewardship_requires_download_actionlint_bash_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "download-actionlint.bash",
            "fetch-actionlint.sh",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "download-actionlint.bash",
        )


def test_badge_rejects_producthunt_hint_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/producthunt-x-red)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_reject_http_scheme_still_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](http://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_http_scheme_still_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](http://example.com)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "insecure http://",
        )


def test_schema_rejects_tier_zero_still_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "positive int",
        )


def test_common_dangerous_schemes_javascript_still() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import DANGEROUS_LINK_SCHEMES  # noqa: E402

    if "javascript:" not in DANGEROUS_LINK_SCHEMES:
        raise AssertionError("DANGEROUS_LINK_SCHEMES missing javascript:")


def test_lycheeignore_rejects_https_star_still_after_35() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".lycheeignore"
        path.write_text("https://*\n", encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not exclude all http",
        )


def test_markdownlint_json_requires_line_length_200() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 120 },\n'
            '  "MD024": { "siblings_only": true }\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "line_length: 200",
        )


def test_markdownlint_json_requires_siblings_only_true() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": false }\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "siblings_only: true",
        )


def test_stewardship_requires_raw_githubusercontent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "raw.githubusercontent.com",
            "cdn.example.com",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "raw.githubusercontent.com",
        )


def test_stewardship_requires_curl_fssl() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("-fsSL", "-fSL")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fsSL",
        )


def test_actionlint_rejects_pull_request_target_on_markdown_lint_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_link_check_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_stewardship_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = "permissions: write-all\n" + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_main_on_checkout_link_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@main"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_stewardship_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_rejects_missing_schedule_on_link_check_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("schedule:", "schedule_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "schedule",
        )


def test_workflow_rejects_missing_dispatch_on_stewardship_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "workflow_dispatch:", "workflow_dispatch_off:"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "workflow_dispatch",
        )


def test_badge_rejects_coverage_hint_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/coverage-99-green)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_stars_hint_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/stars/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_discord_hint_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/discord/123456)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_npm_hint_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/npm/v/fake)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_token_query_after_36() -> None:
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


def test_badge_rejects_link_check_http_image_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](http://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
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
            "must be https://",
        )


def test_badge_rejects_four_badges_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
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
            "[![Extra](https://img.shields.io/badge/extra-x-red)](https://example.com)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_doc_rejects_missing_three_max_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("Three badges max.", "Keep badges thin.")
        text = text.replace("three badges", "badges")
        text = text.replace("3 badges", "badges")
        text = text.replace("badges max", "badges")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "three-badge",
        )


def test_relative_links_accept_https_mixed_case_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](HtTpS://example.com)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_javascript_titlecase_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](Javascript:alert(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_data_titlecase_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](Data:text/plain,hi)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_github_slug_hash_punct_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Hash punctuation stripped: "Foo # Bar" → "foo--bar"
    got = github_slug("Foo # Bar")
    if got != "foo--bar":
        raise AssertionError(f"github_slug Foo # Bar -> {got!r}")


def test_relative_links_accept_hash_heading_fragment_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Foo # Bar\n\nSee [x](#foo--bar).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_broken_parent_docs_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](../missing.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_angle_bracket_mailto_mixed_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](<MailTo:a@b.co>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_empty_parens_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x]()\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_reject_protocol_relative_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](//evil.example/x)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "protocol-relative",
        )


def test_wiki_rejects_missing_home_to_routing_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "[Agent-Routing](Agent-Routing.md)\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Agent-Routing.md",
        )


def test_wiki_rejects_coveralls_badge_chrome_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "coveralls badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_producthunt_badge_chrome_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "producthunt badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_npm_badge_chrome_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge npm/ chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_pypi_badge_chrome_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge pypi/ chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_data_uppercase_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](DATA:text/plain,hi)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_security_row_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(
                "| `Security-Boundaries.md` | Security-Boundaries |\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Security-Boundaries.md",
        )


def test_wiki_rejects_missing_actionlint_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "actionlint on existing workflow paths\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "actionlint",
        )


def test_wiki_rejects_missing_relative_hint_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "relative links", "offline links"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "relative",
        )


def test_schema_rejects_empty_badge_edit_policy_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"\"\ncloses: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_empty_agents_maintainer_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: \"\"\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_missing_agents_parent_key_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "autonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_missing_claude_autonomy_key_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_empty_publish_created_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"\"\npurpose: x\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_wrong_badge_status_draft_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_autonomy_two_vs_expected_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 2\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_wrong_claude_parent_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/other/repo\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_closes_without_hash_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"issue 16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "closes",
        )


def test_common_secret_patterns_ghs_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghs_" + ("A" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing ghs_")


def test_common_secret_patterns_ghu_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghu_" + ("B" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing ghu_")


def test_common_secret_patterns_rk_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "rk-" + ("C" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing rk-")


def test_common_secret_patterns_aws_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "aws_secret_access_key = '" + ("D" * 20) + "'"
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing aws_secret_access_key")


def test_common_forbidden_badge_hints_coverage_stars_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("coverage", "stars"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint}")


def test_common_scan_secrets_ghs_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        target = tmp_path / "doc.md"
        target.write_text("# x\n\nghs_" + ("E" * 20) + "\n", encoding="utf-8")
        errors: list[str] = []
        # ROOT-relative label: scan_secrets uses path.relative_to(ROOT) by default;
        # pass label to avoid ROOT mismatch in temp trees.
        scan_secrets(target, errors, label="doc.md")
        if not errors:
            raise AssertionError("scan_secrets should flag ghs_")


def test_common_has_dangerous_scheme_file_still_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("FILE:///etc/passwd") != "file:":
        raise AssertionError("has_dangerous_scheme FILE: casefold failed")


def test_markdown_lint_requires_cli2_action_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "markdownlint-cli2-action", "markdownlint-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdownlint-cli2-action",
        )


def test_link_check_requires_lycheeverse_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "lycheeverse/lychee-action", "other/lychee-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "lycheeverse/lychee-action",
        )


def test_markdownlint_json_requires_siblings_only_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": true\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "siblings_only",
        )


def test_stewardship_requires_rhysd_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "rhysd/actionlint",
            "other/actionlint",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "rhysd/actionlint",
        )


def test_badge_rejects_twitter_hint_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/twitter/follow/x)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_reject_http_scheme_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](http://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_http_scheme_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](http://example.com)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "insecure http://",
        )


def test_schema_rejects_tier_zero_still_after_36() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "tier",
        )


def test_common_dangerous_schemes_data_still_after_36() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import DANGEROUS_LINK_SCHEMES  # noqa: E402

    if "data:" not in DANGEROUS_LINK_SCHEMES:
        raise AssertionError("DANGEROUS_LINK_SCHEMES missing data:")



def test_markdownlint_json_requires_default_true() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": false,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": true }\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "default: true",
        )


def test_stewardship_requires_get_actionlint_outputs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "get_actionlint.outputs.executable",
            "actionlint",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "get_actionlint.outputs.executable",
        )


def test_stewardship_requires_actionlint_v177_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("/v1.7.7/", "/main/")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "/v1.7.7/",
        )


def test_link_check_requires_max_concurrency_8() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "--max-concurrency 8", "--max-concurrency 32"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--max-concurrency 8",
        )


def test_link_check_requires_timeout_20() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--timeout 20", "--timeout 60")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--timeout 20",
        )


def test_link_check_requires_max_retries_3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "--max-retries 3", "--max-retries 10"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--max-retries 3",
        )


def test_actionlint_rejects_pull_request_target_on_stewardship_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_markdown_lint_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_link_check_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = "permissions: write-all\n" + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_latest_on_checkout_stewardship_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@latest"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_link_check_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_rejects_missing_concurrency_on_markdown_lint_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace("concurrency:", "concurrency_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "concurrency",
        )


def test_workflow_rejects_missing_timeout_on_stewardship_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "timeout-minutes:", "timeout_minutes_off:"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "timeout-minutes",
        )


def test_badge_rejects_codecov_hint_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/codecov/c/github/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_downloads_hint_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/downloads/fuzzywigg/agents-governance/total)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_followers_hint_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/followers/fuzzywigg)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_pypi_hint_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/pypi/v/fake)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_apikey_query_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg?apikey=abc)]"
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


def test_badge_rejects_markdown_lint_http_image_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](http://github.com/fuzzywigg/agents-governance/"
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
            "must be https://",
        )


def test_badge_rejects_four_badges_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
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
            "[![Extra](https://img.shields.io/badge/extra-x-red)](https://example.com)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_doc_rejects_missing_fourth_refusal_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("fourth", "extra")
        text = text.replace("intentionally", "quietly")
        text = text.replace("not added", "deferred")
        text = text.replace("not** added", "deferred")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "fourth badge",
        )


def test_relative_links_accept_https_uppercase_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](HTTPS://example.com)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_vbscript_titlecase_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](VbScript:msgbox(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_file_titlecase_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](File:///etc/passwd)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_github_slug_ampersand_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Ampersand stripped: "Foo & Bar" → "foo--bar"
    got = github_slug("Foo & Bar")
    if got != "foo--bar":
        raise AssertionError(f"github_slug Foo & Bar -> {got!r}")


def test_relative_links_accept_ampersand_heading_fragment_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Foo & Bar\n\nSee [x](#foo--bar).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_broken_sibling_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](missing.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_angle_bracket_tel_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](<tel:+15551212>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_bare_hash_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](#)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_reject_nested_dotdot_escape_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](%2e%2e/missing.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_wiki_rejects_missing_home_to_overview_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "[Overview](Overview.md)\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Overview.md",
        )


def test_wiki_rejects_discord_badge_chrome_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "discord badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_twitter_badge_chrome_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "twitter badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_stars_badge_chrome_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "stars badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_forks_badge_chrome_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "forks badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_javascript_uppercase_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](JAVASCRIPT:alert(1))\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_autonomy_row_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(
                "| `Autonomy-Levels.md` | Autonomy-Levels |\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Autonomy-Levels.md",
        )


def test_wiki_rejects_missing_ci_hint_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "markdown-lint", "md-quality"
            ).replace(
                "link-check", "url-scan"
            ).replace(
                "stewardship-checks", "quiet-gates"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "markdown-lint",
        )


def test_wiki_rejects_missing_badge_topic_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "badge", "status-chip"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "badge",
        )


def test_schema_rejects_empty_badge_scope_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: \"\"\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_empty_agents_scope_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: \"\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_missing_agents_maintainer_key_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "scope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "maintainer",
        )


def test_schema_rejects_missing_claude_repo_key_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "repo",
        )


def test_schema_rejects_empty_publish_closes_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_wrong_publish_status_draft_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: DRAFT\ncreated: \"2026-09-13\"\npurpose: x\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_autonomy_negative_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: -1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_wrong_agents_scope_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: ecosystem-wide\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "repository-specific",
        )


def test_schema_rejects_semver_prerelease_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0-rc1\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "semver",
        )


def test_common_secret_patterns_github_pat_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "github_pat_" + ("A" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing github_pat_")


def test_common_secret_patterns_xoxb_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "xoxb-" + ("B" * 12)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing xoxb-")


def test_common_secret_patterns_rsa_key_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "-----BEGIN RSA PRIVATE KEY-----\nAAAA\n"
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing RSA PRIVATE KEY")


def test_common_forbidden_badge_hints_buymeacoffee_opencollective_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("buymeacoffee", "opencollective"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint}")


def test_common_scan_secrets_xoxb_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        target = tmp_path / "doc.md"
        target.write_text("# x\n\nxoxb-" + ("C" * 12) + "\n", encoding="utf-8")
        errors: list[str] = []
        scan_secrets(target, errors, label="doc.md")
        if not errors:
            raise AssertionError("scan_secrets should flag xoxb-")


def test_common_has_dangerous_scheme_vbscript_still_after_37() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("VBSCRIPT:msgbox(1)") != "vbscript:":
        raise AssertionError("has_dangerous_scheme VBSCRIPT: casefold failed")


def test_markdown_lint_requires_davidanson_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "DavidAnson/markdownlint-cli2-action", "Other/markdownlint-cli2-action"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "DavidAnson/markdownlint-cli2-action",
        )


def test_link_check_requires_github_token_flag_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("--github-token", "--token")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--github-token",
        )


def test_markdownlint_json_requires_line_length_200_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 80 },\n'
            '  "MD024": { "siblings_only": true }\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "line_length: 200",
        )


def test_stewardship_requires_raw_githubusercontent_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "raw.githubusercontent.com",
            "cdn.example.com",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "raw.githubusercontent.com",
        )


def test_badge_rejects_coveralls_hint_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/coveralls/github/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_reject_http_scheme_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](http://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_wiki_rejects_http_scheme_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](http://example.com)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "insecure http://",
        )


def test_schema_rejects_tier_zero_still_after_37() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "positive int",
        )


def test_markdownlint_json_requires_md033_false() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": true },\n'
            '  "MD033": true,\n  "MD041": false,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD033: false",
        )


def test_markdownlint_json_requires_md041_false() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": true },\n'
            '  "MD033": false,\n  "MD041": true,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD041: false",
        )


def test_markdownlint_json_requires_md060_false() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": true },\n'
            '  "MD033": false,\n  "MD041": false,\n  "MD060": true\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "MD060: false",
        )


def test_markdown_lint_requires_cli2_action_v24() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "DavidAnson/markdownlint-cli2-action@v24",
            "DavidAnson/markdownlint-cli2-action@v20",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "markdownlint-cli2-action@v24",
        )


def test_stewardship_requires_setup_python_v5() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/setup-python@v5",
            "actions/setup-python@v4",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "setup-python@v5",
        )


def test_stewardship_requires_get_actionlint_id() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "id: get_actionlint",
            "id: download_actionlint",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "id: get_actionlint",
        )

def test_actionlint_rejects_pull_request_target_on_markdown_lint_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            "pull_request:",
            "pull_request_target:",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "pull_request_target",
        )


def test_actionlint_rejects_contents_write_on_link_check_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "contents: read",
            "contents: write",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "contents: write",
        )


def test_actionlint_rejects_write_all_on_stewardship_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = "permissions: write-all\n" + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "write-all",
        )


def test_actionlint_rejects_float_main_on_checkout_link_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "actions/checkout@v7", "actions/checkout@main"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "must not float",
        )


def test_workflow_requires_cancel_in_progress_true_not_false_on_stewardship_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "cancel-in-progress: true",
            "cancel-in-progress: false",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "cancel-in-progress: true",
        )


def test_workflow_rejects_missing_schedule_on_link_check_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace("schedule:", "schedule_off:")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "schedule",
        )


def test_workflow_rejects_missing_dispatch_on_stewardship_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "workflow_dispatch:", "workflow_dispatch_off:"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "workflow_dispatch",
        )


def test_badge_rejects_coverage_hint_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/badge/coverage-99-green)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_stars_hint_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/github/stars/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_discord_hint_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/discord/123456)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_npm_hint_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://img.shields.io/npm/v/fake)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_badge_rejects_token_query_after_38() -> None:
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


def test_badge_rejects_link_check_http_image_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](http://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
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
            "must be https://",
        )


def test_badge_rejects_four_badges_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
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
            "[![Extra](https://img.shields.io/badge/extra-x-red)](https://example.com)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "exactly 3 badges",
        )


def test_badge_doc_rejects_missing_three_max_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / "docs" / "badge-standard.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("Three badges max.", "Keep badges thin.")
        text = text.replace("three badges", "badges")
        text = text.replace("3 badges", "badges")
        text = text.replace("badges max", "badges")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "three-badge",
        )


def test_relative_links_accept_https_mixed_case_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](HtTpS://example.com)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_javascript_titlecase_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](Javascript:alert(1))\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_reject_data_titlecase_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](Data:text/plain,hi)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_relative_links_github_slug_hash_punct_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from check_relative_links import github_slug  # noqa: E402

    # Hash punctuation stripped: "Foo # Bar" → "foo--bar"
    got = github_slug("Foo # Bar")
    if got != "foo--bar":
        raise AssertionError(f"github_slug Foo # Bar -> {got!r}")


def test_relative_links_accept_hash_heading_fragment_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# Title\n\n## Foo # Bar\n\nSee [x](#foo--bar).\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_broken_parent_docs_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "docs" / "a.md", "# A\n\n[x](../missing.md)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "broken relative link",
        )


def test_relative_links_accept_angle_bracket_mailto_mixed_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](<MailTo:a@b.co>)\n")
        assert_pass_script(scripts / "check_relative_links.py", tmp_path)


def test_relative_links_reject_empty_parens_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x]()\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "empty relative link",
        )


def test_relative_links_reject_protocol_relative_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](//evil.example/x)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "protocol-relative",
        )


def test_wiki_rejects_missing_home_to_routing_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Home.md"] = pages["Home.md"].replace(
                "[Agent-Routing](Agent-Routing.md)\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Agent-Routing.md",
        )


def test_wiki_rejects_coveralls_badge_chrome_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "coveralls badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_producthunt_badge_chrome_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "producthunt badge chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_npm_badge_chrome_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge npm/ chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_pypi_badge_chrome_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "badge pypi/ chrome\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "invent-product",
        )


def test_wiki_rejects_data_uppercase_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Overview.md"] = (
                "# O\n\n[Home](Home.md)\n\ngovernance public\n"
                "[x](DATA:text/plain,hi)\n"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "dangerous link scheme",
        )


def test_wiki_rejects_missing_publish_security_row_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(
                "| `Security-Boundaries.md` | Security-Boundaries |\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "Security-Boundaries.md",
        )


def test_wiki_rejects_missing_actionlint_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "actionlint on existing workflow paths\n", ""
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "actionlint",
        )


def test_wiki_rejects_missing_relative_hint_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def mutate(pages: dict[str, str]) -> None:
            pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace(
                "relative links", "offline links"
            )

        scripts = _seed_wiki_tree(tmp_path, mutate=mutate)
        assert_fail_script(
            scripts / "check_wiki_outline.py",
            tmp_path,
            "relative",
        )


def test_schema_rejects_empty_badge_edit_policy_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"\"\ncloses: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_empty_agents_maintainer_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: \"\"\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_missing_agents_parent_key_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "autonomy_level: 1\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_missing_claude_autonomy_key_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_empty_publish_created_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        publish = (
            "# P\n\n```yaml\nstatus: ACTIVE\ncreated: \"\"\npurpose: x\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, publish=publish)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "non-empty",
        )


def test_schema_rejects_wrong_badge_status_draft_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: DRAFT\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "ACTIVE",
        )


def test_schema_rejects_autonomy_two_vs_expected_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = (
            "# AGENTS\n\n```yaml\nversion: \"1.0.0\"\nlast_updated: \"2026-04-13\"\n"
            "maintainer: smtp.eth\nscope: repository-specific\n"
            "parent_governance: github.com/fuzzywigg/agents-governance\nautonomy_level: 2\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, agents=agents)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "autonomy_level",
        )


def test_schema_rejects_wrong_claude_parent_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        claude = (
            "# CLAUDE\n\n```yaml\nrepo: agents-governance\nowner: \"fuzzywigg (smtp.eth)\"\n"
            "surface: copilot\nautonomy_level: 1\nlast_updated: \"2026-04-13\"\n"
            "parent_governance: github.com/other/repo\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, claude=claude)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "parent_governance",
        )


def test_schema_rejects_closes_without_hash_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"issue 16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "closes",
        )


def test_common_secret_patterns_ghs_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghs_" + ("A" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing ghs_")


def test_common_secret_patterns_ghu_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "ghu_" + ("B" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing ghu_")


def test_common_secret_patterns_rk_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "rk-" + ("C" * 20)
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing rk-")


def test_common_secret_patterns_aws_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import SECRET_PATTERNS  # noqa: E402

    sample = "aws_secret_access_key = '" + ("D" * 20) + "'"
    if not any(p.search(sample) for p in SECRET_PATTERNS):
        raise AssertionError("SECRET_PATTERNS missing aws_secret_access_key")


def test_common_forbidden_badge_hints_coverage_stars_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import FORBIDDEN_BADGE_HINTS  # noqa: E402

    for hint in ("coverage", "stars"):
        if hint not in FORBIDDEN_BADGE_HINTS:
            raise AssertionError(f"FORBIDDEN_BADGE_HINTS missing {hint}")


def test_common_scan_secrets_ghs_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import scan_secrets  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        target = tmp_path / "doc.md"
        target.write_text("# x\n\nghs_" + ("E" * 20) + "\n", encoding="utf-8")
        errors: list[str] = []
        # ROOT-relative label: scan_secrets uses path.relative_to(ROOT) by default;
        # pass label to avoid ROOT mismatch in temp trees.
        scan_secrets(target, errors, label="doc.md")
        if not errors:
            raise AssertionError("scan_secrets should flag ghs_")


def test_common_has_dangerous_scheme_file_still_after_38() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from stewardship_common import has_dangerous_scheme  # noqa: E402

    if has_dangerous_scheme("FILE:///etc/passwd") != "file:":
        raise AssertionError("has_dangerous_scheme FILE: casefold failed")



def test_markdownlint_json_requires_default_true_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": false,\n  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": true },\n'
            '  "MD033": false,\n  "MD041": false,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "default: true",
        )


def test_link_check_requires_max_concurrency_8_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            "--max-concurrency 8", "--max-concurrency 16"
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "--max-concurrency 8",
        )


def test_stewardship_requires_actionlint_v177_path_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace("/v1.7.7/", "/v1.7.6/")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "/v1.7.7/",
        )


def test_stewardship_requires_get_actionlint_outputs_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            "get_actionlint.outputs.executable",
            "actionlint",
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "get_actionlint.outputs.executable",
        )


def test_badge_rejects_codecov_hint_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        readme = (
            "# agents-governance\n\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![License](https://codecov.io/gh/fuzzywigg/agents-governance/branch/main/graph/badge.svg)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n"
        )
        scripts = _seed_badge_tree(tmp_path, readme)
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            "Forbidden invent-product",
        )


def test_relative_links_reject_http_scheme_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path, "check_relative_links.py")
        _write(tmp_path / "README.md", "# T\n\n[x](http://example.com)\n")
        assert_fail_script(
            scripts / "check_relative_links.py",
            tmp_path,
            "insecure http://",
        )


def test_schema_rejects_tier_zero_still_after_38() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        badge = (
            "# B\n\n```yaml\nstatus: ACTIVE\ntier: 0\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: x\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n"
        )
        scripts = _seed_schema_tree(tmp_path, badge=badge)
        assert_fail_script(
            scripts / "check_stewardship_schema.py",
            tmp_path,
            "positive int",
        )


# --- TOKENMAXX deepen after #39: CI workflow supply-chain / job contract pins ---

def test_link_check_requires_checkout_v7() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout@v4',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'checkout@v7',
        )

def test_markdown_lint_requires_checkout_v7() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout@v4',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'checkout@v7',
        )

def test_stewardship_requires_checkout_v7() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout@v4',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'checkout@v7',
        )

def test_link_check_requires_lychee_action_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'lycheeverse/lychee-action@v2',
            'lycheeverse/lychee-action@v1',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'lychee-action@v2',
        )

def test_link_check_requires_timeout_minutes_20() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'timeout-minutes: 20',
            'timeout-minutes: 10',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'timeout-minutes: 20',
        )

def test_markdown_lint_requires_timeout_minutes_10() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'timeout-minutes: 10',
            'timeout-minutes: 20',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'timeout-minutes: 10',
        )

def test_stewardship_requires_timeout_minutes_15() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'timeout-minutes: 15',
            'timeout-minutes: 10',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'timeout-minutes: 15',
        )

def test_link_check_requires_cron_0_6() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'cron: "0 6 * * 1"',
            'cron: "0 7 * * 1"',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'cron: "0 6 * * 1"',
        )

def test_markdown_lint_requires_cron_30_6() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'cron: "30 6 * * 1"',
            'cron: "30 7 * * 1"',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'cron: "30 6 * * 1"',
        )

def test_stewardship_requires_cron_15_6() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'cron: "15 6 * * 1"',
            'cron: "15 7 * * 1"',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'cron: "15 6 * * 1"',
        )

def test_link_check_requires_ubuntu_latest() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'ubuntu-latest',
            'ubuntu-22.04',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'ubuntu-latest',
        )

def test_markdown_lint_requires_ubuntu_latest() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'ubuntu-latest',
            'ubuntu-22.04',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'ubuntu-latest',
        )

def test_stewardship_requires_ubuntu_latest() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'ubuntu-latest',
            'ubuntu-22.04',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'ubuntu-latest',
        )

def test_stewardship_requires_pip_quiet() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'pip install --quiet pyyaml',
            'pip install pyyaml',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '--quiet',
        )

def test_stewardship_requires_shell_bash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'shell: bash',
            'shell: sh',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'shell: bash',
        )

def test_stewardship_requires_actionlint_color() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'get_actionlint.outputs.executable }} -color ',
            'get_actionlint.outputs.executable }} ',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '-color',
        )

def test_actionlint_rejects_pull_request_target_on_link_check_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'pull_request:',
            'pull_request_target:',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'pull_request_target',
        )

def test_actionlint_rejects_contents_write_on_markdown_lint_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'contents: read',
            'contents: write',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'contents: write',
        )

def test_actionlint_rejects_float_main_on_checkout_stewardship_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout@main',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'must not float',
        )

def test_actionlint_rejects_float_latest_on_checkout_markdown_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout@latest',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'must not float',
        )

def test_actionlint_rejects_float_master_on_checkout_link_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout@master',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'must not float',
        )

def test_actionlint_rejects_unpinned_checkout_on_link_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/checkout@v7',
            'actions/checkout',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'unpinned action',
        )

def test_actionlint_rejects_unpinned_lychee_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'lycheeverse/lychee-action@v2',
            'lycheeverse/lychee-action',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'unpinned action',
        )

def test_workflow_requires_cancel_in_progress_true_not_false_on_markdown_lint_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'cancel-in-progress: true',
            'cancel-in-progress: false',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'cancel-in-progress: true',
        )

def test_workflow_rejects_missing_schedule_on_markdown_lint_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'schedule:',
            'sched_off:',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'weekly schedule',
        )

def test_workflow_rejects_missing_dispatch_on_link_check_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'workflow_dispatch:',
            '',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'workflow_dispatch',
        )

def test_workflow_rejects_missing_concurrency_on_stewardship_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'concurrency:',
            'group_off:',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'concurrency',
        )

def test_workflow_rejects_missing_permissions_read_on_markdown_lint_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'contents: read',
            'contents: none',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'contents: read',
        )

def test_actionlint_rejects_contents_write_on_stewardship_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'contents: read',
            'contents: write',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'contents: write',
        )

def test_actionlint_rejects_pull_request_target_on_stewardship_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'pull_request:',
            'pull_request_target:',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'pull_request_target',
        )

def test_workflow_requires_cancel_in_progress_true_not_false_on_link_check_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'cancel-in-progress: true',
            'cancel-in-progress: false',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'cancel-in-progress: true',
        )

def test_workflow_rejects_missing_timeout_on_link_check_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'timeout-minutes: 20',
            '',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'timeout-minutes',
        )

def test_actionlint_rejects_write_all_on_link_check_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = 'permissions: write-all\n' + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'write-all',
        )

def test_actionlint_rejects_write_all_on_stewardship_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = 'permissions: write-all\n' + path.read_text(encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'write-all',
        )

def test_link_check_requires_fail_true_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'fail: true',
            'fail: false',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'fail: true',
        )

def test_link_check_requires_exclude_loopback_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            '--exclude-loopback',
            '--exclude-mail',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'loopback',
        )

def test_link_check_requires_github_token_flag_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            '--github-token',
            '--git-token',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '--github-token',
        )

def test_link_check_requires_action_token_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            'token:',
            'auth_token:',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'token:',
        )

def test_link_check_requires_max_concurrency_8_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            '--max-concurrency 8',
            '--max-concurrency 4',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '--max-concurrency 8',
        )

def test_link_check_requires_timeout_20_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            '--timeout 20',
            '--timeout 30',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '--timeout 20',
        )

def test_link_check_requires_max_retries_3_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "link-check.yml"
        text = path.read_text(encoding="utf-8").replace(
            '--max-retries 3',
            '--max-retries 5',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '--max-retries 3',
        )

def test_markdown_lint_requires_cli2_action_v24_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'DavidAnson/markdownlint-cli2-action@v24',
            'DavidAnson/markdownlint-cli2-action@v20',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'markdownlint-cli2-action@v24',
        )

def test_markdown_lint_requires_davidanson_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'DavidAnson/markdownlint-cli2-action@v24',
            'other/markdownlint-cli2-action@v24',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'DavidAnson/markdownlint-cli2-action',
        )

def test_markdown_lint_requires_config_needle_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            '.markdownlint.json',
            '.markdownlint.yml',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '.markdownlint.json',
        )

def test_markdown_lint_requires_owasp_exclude_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            'OWASP-AGENTIC.md',
            'OTHER-AGENTIC.md',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'OWASP-AGENTIC.md',
        )

def test_markdown_lint_requires_agents_exclude_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "markdown-lint.yml"
        text = path.read_text(encoding="utf-8").replace(
            '.github/agents',
            '.github/prompts',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '.github/agents',
        )

def test_markdownlint_json_requires_md033_false_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n  "MD024": { "siblings_only": true },\n  "MD033": true,\n  "MD041": false,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'MD033: false',
        )

def test_markdownlint_json_requires_md041_false_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n  "MD024": { "siblings_only": true },\n  "MD033": false,\n  "MD041": true,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'MD041: false',
        )

def test_markdownlint_json_requires_md060_false_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 200 },\n  "MD024": { "siblings_only": true },\n  "MD033": false,\n  "MD041": false,\n  "MD060": true\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'MD060: false',
        )

def test_markdownlint_json_requires_line_length_200_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": true,\n  "MD013": { "line_length": 120 },\n  "MD024": { "siblings_only": true },\n  "MD033": false,\n  "MD041": false,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'line_length: 200',
        )

def test_markdownlint_json_requires_default_true_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".markdownlint.json"
        path.write_text(
            '{\n  "default": false,\n  "MD013": { "line_length": 200 },\n  "MD024": { "siblings_only": true },\n  "MD033": false,\n  "MD041": false,\n  "MD060": false\n}\n',
            encoding="utf-8",
        )
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'default: true',
        )

def test_stewardship_requires_setup_python_v5_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'actions/setup-python@v5',
            'actions/setup-python@v4',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'setup-python@v5',
        )

def test_stewardship_requires_get_actionlint_id_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'id: get_actionlint',
            'id: download_actionlint',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'id: get_actionlint',
        )

def test_stewardship_requires_actionlint_v177_path_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            '/v1.7.7/',
            '/v1.7.6/',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '/v1.7.7/',
        )

def test_stewardship_requires_get_actionlint_outputs_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'get_actionlint.outputs.executable',
            'steps.actionlint.outputs.path',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'get_actionlint.outputs.executable',
        )

def test_stewardship_requires_python_312_pin_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            '"3.12"',
            '"3.11"',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            '3.12',
        )

def test_stewardship_requires_rhysd_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'rhysd/actionlint',
            'other/actionlint',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'rhysd/actionlint',
        )

def test_stewardship_requires_curl_fssl_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'curl -fsSL',
            'curl -sL',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'fsSL',
        )

def test_stewardship_requires_raw_githubusercontent_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".github" / "workflows" / "stewardship-checks.yml"
        text = path.read_text(encoding="utf-8").replace(
            'raw.githubusercontent.com',
            'cdn.example.com',
        )
        path.write_text(text, encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'raw.githubusercontent.com',
        )

def test_lycheeignore_rejects_https_star_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".lycheeignore"
        path.write_text('https://img\\.shields\\.io\nhttps://*\n', encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'https://*',
        )

def test_lycheeignore_rejects_http_star_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".lycheeignore"
        path.write_text('https://img\\.shields\\.io\nhttp://*\n', encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'http://*',
        )

def test_lycheeignore_requires_shields_exclude_still_after_39() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_badge_tree(tmp_path, _good_readme())
        path = tmp_path / ".lycheeignore"
        path.write_text('# no shields\n', encoding="utf-8")
        assert_fail_script(
            scripts / "check_badge_standard.py",
            tmp_path,
            'img.shields.io',
        )


def main() -> int:
    tests = [
        # Badge (13)
        test_badge_rejects_wrong_order,
        test_badge_rejects_invent_product,
        test_badge_rejects_wrong_repo_slug,
        test_badge_rejects_noncontiguous_row,
        test_badge_rejects_secret_url,
        test_badge_rejects_http_image,
        test_badge_rejects_stewardship_product_badge,
        test_badge_rejects_wrong_license_link,
        test_badge_rejects_missing_workflow_dispatch,
        test_badge_rejects_missing_fail_true,
        test_badge_rejects_missing_markdownlint_config,
        test_badge_rejects_missing_contributing_invent_warning,
        test_badge_passes_good_fixture,
        # Relative / markdown-link (13 + 9)
        test_relative_links_reject_missing,
        test_relative_links_reject_escape,
        test_relative_links_reject_missing_fragment,
        test_relative_links_ignore_fenced_examples,
        test_relative_links_ignore_tilde_fences,
        test_relative_links_reject_javascript_scheme,
        test_relative_links_reject_data_scheme,
        test_relative_links_reject_http_insecure,
        test_relative_links_reject_protocol_relative,
        test_relative_links_reject_encoded_escape,
        test_relative_links_reject_cross_file_missing_fragment,
        test_relative_links_accept_valid_fragment,
        test_relative_links_skip_owasp_file,
        test_relative_links_reject_file_scheme,
        test_relative_links_reject_vbscript_scheme,
        test_relative_links_reject_empty_target,
        test_relative_links_accept_mailto,
        test_relative_links_accept_https,
        test_relative_links_skip_github_agents,
        test_relative_links_reject_broken_image,
        test_relative_links_accept_cross_file_fragment,
        test_relative_links_github_slug_punctuation,
        # Wiki (7 + 5)
        test_wiki_rejects_unexpected_page,
        test_wiki_rejects_missing_home_backlink,
        test_wiki_rejects_invent_chrome,
        test_wiki_rejects_missing_topic_hint,
        test_wiki_rejects_http_link,
        test_wiki_rejects_secret_pattern,
        test_wiki_rejects_missing_out_of_scope,
        test_wiki_rejects_missing_page,
        test_wiki_rejects_missing_readme_link,
        test_wiki_rejects_missing_ci_hint,
        test_wiki_rejects_dangerous_scheme,
        test_wiki_passes_good_fixture,
        # Schema (11 + 3)
        test_schema_rejects_wrong_value,
        test_schema_rejects_inactive_status,
        test_schema_rejects_missing_key,
        test_schema_rejects_bad_autonomy_level,
        test_schema_rejects_bad_tier,
        test_schema_rejects_bad_iso_date,
        test_schema_rejects_edit_policy_without_invent,
        test_schema_rejects_wrong_surface,
        test_schema_rejects_bad_semver,
        test_schema_rejects_closes_without_issue,
        test_schema_rejects_empty_required_value,
        test_schema_rejects_missing_yaml_block,
        test_schema_rejects_missing_file,
        test_schema_passes_good_fixture,
        # Common / workflow / actionlint / lycheeignore (6 + 22)
        test_common_secret_patterns,
        test_common_dangerous_schemes,
        test_workflow_hardening_requires_timeout,
        test_workflow_hardening_requires_schedule,
        test_workflow_hardening_requires_concurrency,
        test_workflow_hardening_requires_pyyaml_install,
        test_lycheeignore_requires_shields_exclude,
        test_lycheeignore_rejects_star_exclude,
        test_missing_lycheeignore_fails,
        test_missing_markdownlint_json_fails,
        test_actionlint_rejects_pull_request_target,
        test_actionlint_rejects_contents_write,
        test_actionlint_rejects_unpinned_action,
        test_actionlint_rejects_float_main_ref,
        test_actionlint_requires_runs_on,
        test_stewardship_requires_actionlint_needle,
        test_link_check_requires_lycheeignore_reference,
        test_badge_rejects_missing_license_file,
        test_badge_rejects_forbidden_hint_in_row,
        test_badge_rejects_wrong_link_check_image,
        test_badge_rejects_missing_readme_badge_doc_link,
        test_badge_rejects_missing_agents_selftest_needle,
        test_workflow_rejects_missing_permissions_read,
        test_workflow_rejects_missing_exclude_loopback,
        test_workflow_rejects_missing_max_retries,
        test_common_secret_url_hints,
        test_common_forbidden_badge_hints,
        test_github_slug_helper,
        # TOKENMAXX deepen after #27 (+45)
        test_actionlint_rejects_write_all,
        test_actionlint_rejects_float_master_ref,
        test_actionlint_rejects_float_latest_ref,
        test_actionlint_requires_name,
        test_actionlint_requires_steps,
        test_link_check_requires_github_token,
        test_link_check_requires_lychee_needle,
        test_link_check_requires_exclude_path,
        test_link_check_requires_max_concurrency,
        test_link_check_requires_lychee_timeout,
        test_markdown_lint_requires_owasp_exclude,
        test_markdown_lint_requires_agents_exclude,
        test_markdown_lint_requires_markdownlint_needle,
        test_stewardship_requires_selftest_needle,
        test_stewardship_requires_setup_python,
        test_stewardship_requires_run_script,
        test_stewardship_requires_actionlint_version_pin,
        test_stewardship_requires_actionlint_all_workflows,
        test_workflow_rejects_missing_pull_request,
        test_badge_rejects_missing_h1,
        test_badge_rejects_two_badges_only,
        test_badge_rejects_http_badge_link,
        test_badge_rejects_wrong_markdown_lint_image,
        test_badge_rejects_missing_readme_stewardship_script,
        test_badge_rejects_missing_contributing_script,
        test_badge_rejects_missing_workflow_file,
        test_lycheeignore_accepts_regex_escaped_shields,
        test_lycheeignore_accepts_literal_shields,
        test_relative_links_accept_tel,
        test_relative_links_reject_nul,
        test_relative_links_reject_bare_hash,
        test_relative_links_accept_title_attr,
        test_relative_links_accept_existing_image,
        test_wiki_rejects_missing_publish,
        test_wiki_rejects_missing_badge_link,
        test_wiki_rejects_missing_home_page_link,
        test_wiki_rejects_missing_publish_do_not_push,
        test_wiki_rejects_missing_relative_hint,
        test_wiki_rejects_missing_invent_on_stewardship,
        test_schema_rejects_wrong_maintainer,
        test_schema_rejects_wrong_claude_parent,
        test_schema_rejects_wrong_badge_owner,
        test_schema_rejects_secret_in_doc,
        test_common_strip_fenced,
        test_common_dangerous_schemes_complete,
        # TOKENMAXX deepen after #28 (+48)
        test_workflow_requires_cancel_in_progress,
        test_link_check_requires_markdown_glob,
        test_actionlint_requires_timeout_minutes_local,
        test_actionlint_allows_docker_uses_without_pin,
        test_badge_rejects_missing_badge_standard_file,
        test_badge_rejects_missing_contributing_file,
        test_badge_rejects_license_image_wrong_path,
        test_badge_rejects_license_image_missing_repo_slug,
        test_badge_rejects_secret_in_readme_body,
        test_badge_rejects_agents_missing_link_check_needle,
        test_badge_rejects_agents_missing_markdown_lint_needle,
        test_badge_rejects_agents_missing_stewardship_needle,
        test_badge_rejects_agents_missing_run_script_needle,
        test_badge_doc_rejects_missing_invent_wording,
        test_badge_doc_rejects_missing_three_badge_max,
        test_badge_doc_rejects_stewardship_without_fourth_refusal,
        test_badge_accepts_absolute_license_blob_link,
        test_lycheeignore_rejects_https_star,
        test_relative_links_accept_angle_bracket_https,
        test_relative_links_accept_license_target,
        test_relative_links_github_slug_ampersand,
        test_relative_links_accept_ampersand_heading_fragment,
        test_relative_links_reject_whitespace_only_target,
        test_wiki_rejects_missing_publish_link_check,
        test_wiki_rejects_missing_publish_markdown_lint,
        test_wiki_rejects_missing_publish_secrets,
        test_wiki_rejects_missing_overview_topic,
        test_wiki_rejects_missing_security_topic,
        test_wiki_rejects_stars_badge_chrome,
        test_wiki_rejects_missing_wiki_dir,
        test_schema_rejects_wrong_agents_scope,
        test_schema_rejects_wrong_agents_parent,
        test_schema_rejects_wrong_claude_repo,
        test_schema_rejects_inactive_publish_status,
        test_schema_rejects_backlog_wrong_tier,
        test_schema_rejects_autonomy_as_string,
        test_schema_rejects_bad_claude_date,
        test_schema_rejects_unparseable_yaml,
        test_common_secret_patterns_extended,
        test_common_forbidden_badge_hints_extended,
        test_common_has_dangerous_scheme_helper,
        test_common_load_workflow_text_helper,
        test_common_fail_helper_appends,
        test_common_markdown_files_helper,
        test_markdown_lint_requires_config_needle,
        test_stewardship_requires_actionlint_link_check_path,
        test_stewardship_requires_actionlint_stewardship_path,
        test_workflow_rejects_missing_dispatch_on_stewardship,
        # TOKENMAXX deepen after #29 (+51)
        test_workflow_requires_cancel_in_progress_true,
        test_workflow_requires_cancel_in_progress_true_on_stewardship,
        test_link_check_requires_agents_exclude_path,
        test_markdown_lint_requires_markdown_glob,
        test_lycheeignore_rejects_http_star,
        test_stewardship_requires_actionlint_markdown_lint_path,
        test_actionlint_rejects_unpinned_second_action,
        test_actionlint_rejects_float_main_on_setup_python,
        test_workflow_rejects_missing_schedule_on_link_check,
        test_workflow_rejects_missing_concurrency_on_markdown_lint,
        test_badge_rejects_link_check_relative_workflow_link,
        test_badge_rejects_markdown_lint_relative_workflow_link,
        test_badge_accepts_dot_slash_license_link,
        test_badge_rejects_forbidden_coverage_hint,
        test_badge_rejects_secret_url_token_query,
        test_badge_doc_rejects_missing_link_check_label,
        test_badge_doc_rejects_missing_shields_license_snippet,
        test_badge_rejects_four_badges,
        test_relative_links_accept_angle_bracket_relative,
        test_relative_links_github_slug_backticks,
        test_relative_links_github_slug_markdown_link_heading,
        test_relative_links_accept_nested_path,
        test_relative_links_reject_missing_nested,
        test_relative_links_accept_image_with_title,
        test_relative_links_reject_percent_encoded_escape,
        test_wiki_rejects_missing_actionlint_on_stewardship,
        test_wiki_rejects_missing_autonomy_topic,
        test_wiki_rejects_missing_routing_topic,
        test_wiki_rejects_missing_home_out_of_scope,
        test_wiki_rejects_forks_badge_chrome,
        test_wiki_rejects_codecov_badge_chrome,
        test_wiki_rejects_missing_home_to_routing,
        test_wiki_rejects_secret_in_publish,
        test_wiki_rejects_missing_publish_page_table_row,
        test_schema_rejects_wrong_badge_status,
        test_schema_rejects_wrong_badge_tier,
        test_schema_rejects_publish_closes_without_issue,
        test_schema_rejects_empty_agents_maintainer,
        test_schema_rejects_tier_as_string,
        test_schema_rejects_autonomy_out_of_range,
        test_schema_rejects_non_mapping_yaml,
        test_schema_rejects_bad_badge_created_date,
        test_common_secret_url_hints_complete,
        test_common_forbidden_badge_hints_social,
        test_common_secret_patterns_private_key,
        test_common_strip_fenced_tilde,
        test_common_scan_secrets_ghp,
        test_markdown_lint_requires_agents_exclude_path,
        test_link_check_requires_fail_true_still,
        test_stewardship_requires_pyyaml_install_needle,
        test_workflow_rejects_missing_permissions_on_link_check,
        # TOKENMAXX deepen after #30 (+56)
        test_stewardship_requires_python_version_needle,
        test_stewardship_requires_python_312_pin,
        test_workflow_requires_cancel_in_progress_true_on_link_check,
        test_actionlint_rejects_float_master_on_setup_python,
        test_actionlint_rejects_float_latest_on_setup_python,
        test_actionlint_rejects_contents_write_on_stewardship,
        test_workflow_rejects_missing_timeout_on_stewardship,
        test_workflow_rejects_missing_dispatch_on_markdown_lint,
        test_lycheeignore_rejects_bare_star,
        test_link_check_requires_markdown_glob_not_txt,
        test_badge_rejects_discord_hint,
        test_badge_rejects_producthunt_hint,
        test_badge_rejects_api_key_query,
        test_badge_rejects_access_token_query,
        test_badge_rejects_http_license_image,
        test_badge_rejects_license_first_order,
        test_badge_doc_rejects_missing_markdown_lint_snippet,
        test_badge_doc_rejects_missing_link_check_snippet,
        test_badge_rejects_missing_workflow_link_check_file,
        test_relative_links_skip_node_modules,
        test_relative_links_reject_javascript_uppercase,
        test_relative_links_reject_data_uppercase,
        test_relative_links_reject_nested_escape,
        test_relative_links_github_slug_numbers,
        test_relative_links_accept_numbered_heading_fragment,
        test_relative_links_accept_mailto_and_https,
        test_relative_links_reject_file_uppercase,
        test_wiki_rejects_missing_invent_on_home,
        test_wiki_rejects_missing_secrets_on_home,
        test_wiki_rejects_missing_l1_on_autonomy,
        test_wiki_rejects_missing_kill_on_security,
        test_wiki_rejects_downloads_badge_chrome,
        test_wiki_rejects_missing_home_to_security,
        test_wiki_rejects_missing_publish_overview_row,
        test_wiki_rejects_data_scheme,
        test_wiki_rejects_missing_badge_topic_on_stewardship,
        test_schema_rejects_wrong_claude_owner,
        test_schema_rejects_wrong_claude_autonomy,
        test_schema_rejects_inactive_backlog_status,
        test_schema_rejects_empty_badge_scope,
        test_schema_rejects_missing_badge_closes_key,
        test_schema_rejects_agents_autonomy_drift,
        test_schema_rejects_publish_missing_purpose_key,
        test_schema_rejects_float_autonomy,
        test_common_forbidden_badge_hints_commerce,
        test_common_secret_patterns_sk_token,
        test_common_has_dangerous_scheme_casefold,
        test_common_scan_secrets_url_token_hint,
        test_markdown_lint_requires_owasp_exclude_still,
        test_stewardship_requires_timeout_minutes_needle,
        test_actionlint_rejects_write_all_on_markdown_lint,
        test_badge_rejects_stars_hint,
        test_relative_links_accept_parent_relative_existing,
        test_wiki_rejects_twitter_badge_chrome,
        test_schema_rejects_wrong_agents_version_semver_prerelease,
        test_common_dangerous_schemes_file,
        # TOKENMAXX deepen after #31 (+56)
        test_link_check_requires_no_progress,
        test_link_check_requires_verbose,
        test_stewardship_requires_actions_checkout,
        test_workflow_requires_cancel_in_progress_true_on_markdown_lint,
        test_actionlint_rejects_pull_request_target_on_stewardship,
        test_actionlint_rejects_unpinned_setup_python,
        test_badge_rejects_coveralls_hint,
        test_badge_rejects_buymeacoffee_hint,
        test_badge_rejects_opencollective_hint,
        test_badge_rejects_npm_hint,
        test_badge_rejects_pypi_hint,
        test_badge_rejects_followers_hint,
        test_badge_rejects_x_com_hint,
        test_badge_rejects_apikey_query,
        test_badge_rejects_client_secret_query,
        test_badge_rejects_gho_token_hint,
        test_badge_rejects_license_wrong_shields_slug,
        test_badge_rejects_missing_stewardship_workflow_file,
        test_badge_doc_rejects_missing_license_label,
        test_relative_links_skip_git_dir,
        test_relative_links_reject_vbscript_uppercase,
        test_relative_links_reject_encoded_nested_escape,
        test_relative_links_accept_same_dir_existing,
        test_relative_links_github_slug_underscore,
        test_relative_links_accept_underscore_heading_fragment,
        test_wiki_rejects_missing_l0_on_autonomy,
        test_wiki_rejects_missing_secret_on_security,
        test_wiki_rejects_missing_surface_on_routing,
        test_wiki_rejects_missing_governance_on_overview,
        test_wiki_rejects_missing_public_on_overview,
        test_wiki_rejects_missing_home_to_autonomy,
        test_wiki_rejects_followers_badge_chrome,
        test_wiki_rejects_x_com_badge_chrome,
        test_wiki_rejects_missing_publish_home_row,
        test_wiki_rejects_file_scheme,
        test_schema_rejects_missing_claude_surface_key,
        test_schema_rejects_missing_backlog_owner_key,
        test_schema_rejects_empty_publish_purpose,
        test_schema_rejects_empty_agents_scope,
        test_schema_rejects_wrong_agents_autonomy_zero,
        test_schema_rejects_missing_publish_closes_key,
        test_schema_rejects_missing_claude_repo_key,
        test_schema_rejects_badge_closes_without_hash,
        test_common_forbidden_badge_hints_registry,
        test_common_secret_url_hints_apikey_client,
        test_common_secret_patterns_gho,
        test_common_scan_secrets_url_apikey,
        test_markdown_lint_requires_markdown_glob_still,
        test_link_check_requires_exclude_loopback_still,
        test_stewardship_requires_python_312_pin_still,
        test_workflow_rejects_missing_schedule_on_stewardship,
        test_badge_rejects_forks_hint,
        test_relative_links_accept_docs_nested_fragment,
        test_wiki_rejects_missing_run_script_on_stewardship,
        test_schema_rejects_wrong_claude_surface_still,
        test_common_dangerous_schemes_vbscript,
        # TOKENMAXX deepen after #32 (+56)
        test_link_check_requires_lychee_action,
        test_link_check_requires_actions_checkout,
        test_markdown_lint_requires_actions_checkout,
        test_markdownlint_json_requires_md013,
        test_actionlint_rejects_pull_request_target_on_link_check,
        test_actionlint_rejects_contents_write_on_markdown_lint,
        test_actionlint_rejects_write_all_on_stewardship,
        test_workflow_requires_cancel_in_progress_true_not_false_on_link,
        test_badge_rejects_twitter_hint,
        test_badge_rejects_codecov_hint,
        test_badge_rejects_downloads_hint,
        test_badge_rejects_github_pat_hint,
        test_badge_rejects_ghp_token_hint,
        test_badge_rejects_markdown_lint_first_order,
        test_badge_doc_rejects_missing_three_badges_max_still,
        test_badge_rejects_missing_agents_file,
        test_relative_links_reject_javascript_mixed_case,
        test_relative_links_reject_data_mixed_case,
        test_relative_links_accept_tel_with_title,
        test_relative_links_github_slug_colon_punct,
        test_relative_links_accept_colon_heading_fragment,
        test_relative_links_reject_missing_image_nested,
        test_relative_links_accept_license_from_docs,
        test_relative_links_reject_http_uppercase,
        test_wiki_rejects_missing_home_to_overview,
        test_wiki_rejects_discord_badge_chrome,
        test_wiki_rejects_buymeacoffee_badge_chrome,
        test_wiki_rejects_javascript_scheme,
        test_wiki_rejects_missing_publish_autonomy_row,
        test_wiki_rejects_missing_publish_security_row,
        test_wiki_rejects_missing_publish_routing_row,
        test_wiki_rejects_opencollective_badge_chrome,
        test_wiki_rejects_missing_actionlint_still,
        test_schema_rejects_empty_badge_edit_policy,
        test_schema_rejects_empty_claude_owner,
        test_schema_rejects_missing_agents_version_key,
        test_schema_rejects_missing_backlog_edit_policy_key,
        test_schema_rejects_tier_zero,
        test_schema_rejects_empty_publish_created,
        test_schema_rejects_wrong_badge_owner_still,
        test_schema_rejects_autonomy_three_ok_range_but_agents_expected,
        test_common_secret_patterns_npm,
        test_common_secret_patterns_aiza,
        test_common_secret_patterns_slack_xoxb,
        test_common_secret_url_hints_github_pat,
        test_common_forbidden_badge_hints_twitter_codecov,
        test_common_scan_secrets_github_pat,
        test_common_dangerous_schemes_javascript,
        test_stewardship_requires_actions_checkout_still,
        test_link_check_requires_verbose_still,
        test_link_check_requires_no_progress_still,
        test_markdown_lint_requires_config_needle_still,
        test_lycheeignore_rejects_https_star_still,
        test_workflow_rejects_missing_pull_request_on_markdown_lint,
        test_badge_rejects_producthunt_hint_still,
        test_relative_links_accept_nested_image_existing,
        test_wiki_rejects_data_scheme_still,
        test_schema_rejects_missing_claude_last_updated_key,
        test_common_has_dangerous_scheme_data,
        # TOKENMAXX deepen after #33 (+56)
        test_link_check_requires_lycheeverse_action,
        test_markdown_lint_requires_cli2_action,
        test_markdownlint_json_requires_md013_line_length,
        test_stewardship_requires_pip_install_pyyaml,
        test_actionlint_rejects_pull_request_target_on_markdown_lint,
        test_actionlint_rejects_contents_write_on_link_check,
        test_actionlint_rejects_write_all_on_link_check,
        test_actionlint_rejects_float_latest_on_checkout_link,
        test_workflow_requires_cancel_in_progress_true_not_false_on_stewardship,
        test_workflow_rejects_missing_concurrency_on_stewardship,
        test_workflow_rejects_missing_timeout_on_markdown_lint,
        test_badge_rejects_coverage_hint_still,
        test_badge_rejects_stars_hint_still,
        test_badge_rejects_token_query_still,
        test_badge_rejects_license_http_link,
        test_badge_rejects_four_badges_still,
        test_badge_doc_rejects_missing_fourth_refusal_still,
        test_relative_links_accept_https_uppercase,
        test_relative_links_accept_mailto_uppercase,
        test_relative_links_reject_file_mixed_case,
        test_relative_links_github_slug_tilde,
        test_relative_links_accept_tilde_heading_fragment,
        test_relative_links_reject_missing_parent_file,
        test_relative_links_accept_angle_bracket_mailto,
        test_relative_links_reject_protocol_relative_still,
        test_wiki_rejects_missing_home_to_stewardship,
        test_wiki_rejects_coveralls_badge_chrome,
        test_wiki_rejects_producthunt_badge_chrome,
        test_wiki_rejects_npm_badge_chrome,
        test_wiki_rejects_pypi_badge_chrome,
        test_wiki_rejects_http_uppercase,
        test_wiki_rejects_vbscript_scheme,
        test_wiki_rejects_missing_publish_stewardship_row,
        test_wiki_rejects_missing_relative_hint_still,
        test_schema_rejects_empty_badge_closes,
        test_schema_rejects_empty_agents_version,
        test_schema_rejects_missing_agents_autonomy_key,
        test_schema_rejects_missing_claude_parent_key,
        test_schema_rejects_empty_claude_last_updated,
        test_schema_rejects_wrong_badge_scope_empty_still,
        test_schema_rejects_tier_negative,
        test_schema_rejects_wrong_agents_maintainer_still,
        test_common_secret_patterns_ghs,
        test_common_secret_patterns_ghu,
        test_common_secret_patterns_rk_token,
        test_common_secret_patterns_aws_secret,
        test_common_secret_patterns_openssh_key,
        test_common_forbidden_badge_hints_coveralls_producthunt,
        test_common_scan_secrets_npm,
        test_common_has_dangerous_scheme_file_still,
        test_link_check_requires_lychee_action_still,
        test_markdownlint_json_requires_md013_still,
        test_markdown_lint_requires_actions_checkout_still,
        test_link_check_requires_actions_checkout_still,
        test_stewardship_requires_pyyaml_install_still,
        test_badge_rejects_discord_hint_still,
        test_relative_links_reject_http_uppercase_still,
        test_wiki_rejects_javascript_scheme_still,
        test_schema_rejects_tier_zero_still,
        test_common_dangerous_schemes_vbscript_still,
        # TOKENMAXX deepen after #34 (+62)
        test_markdown_lint_requires_davidanson_action,
        test_link_check_requires_github_token_flag,
        test_markdownlint_json_requires_md024,
        test_stewardship_requires_download_actionlint_bash,
        test_actionlint_rejects_pull_request_target_on_stewardship,
        test_actionlint_rejects_contents_write_on_markdown_lint,
        test_actionlint_rejects_write_all_on_markdown_lint,
        test_actionlint_rejects_float_main_on_checkout_markdown,
        test_workflow_requires_cancel_in_progress_true_not_false_on_link_check,
        test_workflow_rejects_missing_schedule_on_stewardship,
        test_workflow_rejects_missing_workflow_dispatch_on_link_check,
        test_badge_rejects_followers_hint_still,
        test_badge_rejects_forks_hint_still,
        test_badge_rejects_npm_hint_still,
        test_badge_rejects_pypi_hint_still,
        test_badge_rejects_apikey_query_still,
        test_badge_rejects_link_check_http_image,
        test_badge_rejects_blank_line_between_still,
        test_badge_doc_rejects_missing_three_max_still,
        test_relative_links_accept_tel_uppercase,
        test_relative_links_reject_javascript_mixed_case_still,
        test_relative_links_reject_data_uppercase,
        test_relative_links_github_slug_asterisk,
        test_relative_links_accept_asterisk_heading_fragment,
        test_relative_links_reject_broken_nested_docs,
        test_relative_links_accept_angle_bracket_https,
        test_relative_links_reject_empty_parens_still,
        test_relative_links_reject_percent_traversal_still,
        test_wiki_rejects_missing_home_to_security,
        test_wiki_rejects_buymeacoffee_badge_chrome,
        test_wiki_rejects_opencollective_badge_chrome,
        test_wiki_rejects_codecov_badge_chrome,
        test_wiki_rejects_downloads_badge_chrome,
        test_wiki_rejects_file_uppercase,
        test_wiki_rejects_missing_publish_overview_row,
        test_wiki_rejects_missing_actionlint_hint_still,
        test_wiki_rejects_missing_invent_on_stewardship_still,
        test_schema_rejects_empty_badge_owner,
        test_schema_rejects_empty_agents_scope,
        test_schema_rejects_missing_agents_version_key,
        test_schema_rejects_missing_claude_surface_key,
        test_schema_rejects_empty_publish_purpose,
        test_schema_rejects_wrong_badge_status_draft,
        test_schema_rejects_autonomy_four_oob,
        test_schema_rejects_wrong_claude_repo_still,
        test_schema_rejects_closes_without_hash_still,
        test_common_secret_patterns_ghr,
        test_common_secret_patterns_gho,
        test_common_secret_patterns_sk_token,
        test_common_secret_patterns_ec_key,
        test_common_forbidden_badge_hints_followers_forks,
        test_common_scan_secrets_aiza,
        test_common_has_dangerous_scheme_javascript_still,
        test_markdown_lint_requires_cli2_action_still,
        test_link_check_requires_lycheeverse_still,
        test_markdownlint_json_requires_line_length_still,
        test_stewardship_requires_pip_install_still,
        test_badge_rejects_twitter_hint_still,
        test_relative_links_reject_http_mixed_case_still,
        test_wiki_rejects_data_scheme_still_after_34,
        test_schema_rejects_tier_zero_still_after_34,
        test_common_dangerous_schemes_data_still,
        # TOKENMAXX deepen after #35 (+62)
        test_markdownlint_json_requires_siblings_only,
        test_stewardship_requires_rhysd_actionlint,
        test_stewardship_requires_curl_download,
        test_link_check_requires_action_token,
        test_actionlint_rejects_pull_request_target_on_link_check_after_35,
        test_actionlint_rejects_contents_write_on_stewardship_after_35,
        test_actionlint_rejects_write_all_on_link_check_after_35,
        test_actionlint_rejects_float_latest_on_checkout_stewardship,
        test_workflow_requires_cancel_in_progress_true_not_false_on_markdown_lint,
        test_workflow_rejects_missing_concurrency_on_link_check_after_35,
        test_workflow_rejects_missing_timeout_on_markdown_lint_after_35,
        test_badge_rejects_buymeacoffee_hint_still,
        test_badge_rejects_opencollective_hint_still,
        test_badge_rejects_coveralls_hint_still,
        test_badge_rejects_xcom_hint_still,
        test_badge_rejects_client_secret_query_still,
        test_badge_rejects_markdown_lint_http_image,
        test_badge_rejects_four_badges_still_after_35,
        test_badge_doc_rejects_missing_fourth_refusal_still,
        test_relative_links_accept_mailto_mixed_case,
        test_relative_links_reject_vbscript_mixed_case_still,
        test_relative_links_reject_file_uppercase_after_35,
        test_relative_links_github_slug_underscore,
        test_relative_links_accept_underscore_heading_fragment,
        test_relative_links_reject_broken_docs_sibling,
        test_relative_links_accept_angle_bracket_tel,
        test_relative_links_reject_bare_hash_only_still,
        test_relative_links_reject_encoded_escape_nested_still,
        test_wiki_rejects_missing_home_to_overview_after_35,
        test_wiki_rejects_discord_badge_chrome_after_35,
        test_wiki_rejects_twitter_badge_chrome_after_35,
        test_wiki_rejects_stars_badge_chrome_after_35,
        test_wiki_rejects_forks_badge_chrome_after_35,
        test_wiki_rejects_javascript_uppercase,
        test_wiki_rejects_missing_publish_autonomy_row,
        test_wiki_rejects_missing_ci_link_check_still,
        test_wiki_rejects_missing_badge_topic_on_stewardship_still,
        test_schema_rejects_empty_badge_scope,
        test_schema_rejects_empty_claude_owner,
        test_schema_rejects_missing_agents_maintainer_key,
        test_schema_rejects_missing_claude_repo_key,
        test_schema_rejects_empty_publish_closes,
        test_schema_rejects_wrong_publish_status_draft,
        test_schema_rejects_autonomy_negative,
        test_schema_rejects_wrong_agents_scope_still,
        test_schema_rejects_semver_prerelease_still,
        test_common_secret_patterns_github_pat,
        test_common_secret_patterns_xoxb,
        test_common_secret_patterns_rsa_key,
        test_common_forbidden_badge_hints_buymeacoffee_opencollective,
        test_common_scan_secrets_xoxb,
        test_common_has_dangerous_scheme_vbscript_still,
        test_markdown_lint_requires_davidanson_still,
        test_link_check_requires_github_token_flag_still,
        test_markdownlint_json_requires_md024_still,
        test_stewardship_requires_download_actionlint_bash_still,
        test_badge_rejects_producthunt_hint_still,
        test_relative_links_reject_http_scheme_still_after_35,
        test_wiki_rejects_http_scheme_still_after_35,
        test_schema_rejects_tier_zero_still_after_35,
        test_common_dangerous_schemes_javascript_still,
        test_lycheeignore_rejects_https_star_still_after_35,
        # TOKENMAXX deepen after #36 (+62)
        test_markdownlint_json_requires_line_length_200,
        test_markdownlint_json_requires_siblings_only_true,
        test_stewardship_requires_raw_githubusercontent,
        test_stewardship_requires_curl_fssl,
        test_actionlint_rejects_pull_request_target_on_markdown_lint_after_36,
        test_actionlint_rejects_contents_write_on_link_check_after_36,
        test_actionlint_rejects_write_all_on_stewardship_after_36,
        test_actionlint_rejects_float_main_on_checkout_link_after_36,
        test_workflow_requires_cancel_in_progress_true_not_false_on_stewardship_after_36,
        test_workflow_rejects_missing_schedule_on_link_check_after_36,
        test_workflow_rejects_missing_dispatch_on_stewardship_after_36,
        test_badge_rejects_coverage_hint_after_36,
        test_badge_rejects_stars_hint_after_36,
        test_badge_rejects_discord_hint_after_36,
        test_badge_rejects_npm_hint_after_36,
        test_badge_rejects_token_query_after_36,
        test_badge_rejects_link_check_http_image_after_36,
        test_badge_rejects_four_badges_still_after_36,
        test_badge_doc_rejects_missing_three_max_after_36,
        test_relative_links_accept_https_mixed_case_after_36,
        test_relative_links_reject_javascript_titlecase_after_36,
        test_relative_links_reject_data_titlecase_after_36,
        test_relative_links_github_slug_hash_punct_after_36,
        test_relative_links_accept_hash_heading_fragment_after_36,
        test_relative_links_reject_broken_parent_docs_after_36,
        test_relative_links_accept_angle_bracket_mailto_mixed_after_36,
        test_relative_links_reject_empty_parens_after_36,
        test_relative_links_reject_protocol_relative_after_36,
        test_wiki_rejects_missing_home_to_routing_after_36,
        test_wiki_rejects_coveralls_badge_chrome_after_36,
        test_wiki_rejects_producthunt_badge_chrome_after_36,
        test_wiki_rejects_npm_badge_chrome_after_36,
        test_wiki_rejects_pypi_badge_chrome_after_36,
        test_wiki_rejects_data_uppercase_after_36,
        test_wiki_rejects_missing_publish_security_row_after_36,
        test_wiki_rejects_missing_actionlint_still_after_36,
        test_wiki_rejects_missing_relative_hint_still_after_36,
        test_schema_rejects_empty_badge_edit_policy_after_36,
        test_schema_rejects_empty_agents_maintainer_after_36,
        test_schema_rejects_missing_agents_parent_key_after_36,
        test_schema_rejects_missing_claude_autonomy_key_after_36,
        test_schema_rejects_empty_publish_created_after_36,
        test_schema_rejects_wrong_badge_status_draft_after_36,
        test_schema_rejects_autonomy_two_vs_expected_after_36,
        test_schema_rejects_wrong_claude_parent_still_after_36,
        test_schema_rejects_closes_without_hash_still_after_36,
        test_common_secret_patterns_ghs_after_36,
        test_common_secret_patterns_ghu_after_36,
        test_common_secret_patterns_rk_after_36,
        test_common_secret_patterns_aws_after_36,
        test_common_forbidden_badge_hints_coverage_stars_after_36,
        test_common_scan_secrets_ghs_after_36,
        test_common_has_dangerous_scheme_file_still_after_36,
        test_markdown_lint_requires_cli2_action_still_after_36,
        test_link_check_requires_lycheeverse_still_after_36,
        test_markdownlint_json_requires_siblings_only_still_after_36,
        test_stewardship_requires_rhysd_still_after_36,
        test_badge_rejects_twitter_hint_still_after_36,
        test_relative_links_reject_http_scheme_still_after_36,
        test_wiki_rejects_http_scheme_still_after_36,
        test_schema_rejects_tier_zero_still_after_36,
        test_common_dangerous_schemes_data_still_after_36,
        # TOKENMAXX deepen after #37 (+62)
        test_markdownlint_json_requires_default_true,
        test_stewardship_requires_get_actionlint_outputs,
        test_stewardship_requires_actionlint_v177_path,
        test_link_check_requires_max_concurrency_8,
        test_link_check_requires_timeout_20,
        test_link_check_requires_max_retries_3,
        test_actionlint_rejects_pull_request_target_on_stewardship_after_37,
        test_actionlint_rejects_contents_write_on_markdown_lint_after_37,
        test_actionlint_rejects_write_all_on_link_check_after_37,
        test_actionlint_rejects_float_latest_on_checkout_stewardship_after_37,
        test_workflow_requires_cancel_in_progress_true_not_false_on_link_check_after_37,
        test_workflow_rejects_missing_concurrency_on_markdown_lint_after_37,
        test_workflow_rejects_missing_timeout_on_stewardship_after_37,
        test_badge_rejects_codecov_hint_after_37,
        test_badge_rejects_downloads_hint_after_37,
        test_badge_rejects_followers_hint_after_37,
        test_badge_rejects_pypi_hint_after_37,
        test_badge_rejects_apikey_query_after_37,
        test_badge_rejects_markdown_lint_http_image_after_37,
        test_badge_rejects_four_badges_still_after_37,
        test_badge_doc_rejects_missing_fourth_refusal_after_37,
        test_relative_links_accept_https_uppercase_after_37,
        test_relative_links_reject_vbscript_titlecase_after_37,
        test_relative_links_reject_file_titlecase_after_37,
        test_relative_links_github_slug_ampersand_after_37,
        test_relative_links_accept_ampersand_heading_fragment_after_37,
        test_relative_links_reject_broken_sibling_after_37,
        test_relative_links_accept_angle_bracket_tel_after_37,
        test_relative_links_reject_bare_hash_after_37,
        test_relative_links_reject_nested_dotdot_escape_after_37,
        test_wiki_rejects_missing_home_to_overview_after_37,
        test_wiki_rejects_discord_badge_chrome_after_37,
        test_wiki_rejects_twitter_badge_chrome_after_37,
        test_wiki_rejects_stars_badge_chrome_after_37,
        test_wiki_rejects_forks_badge_chrome_after_37,
        test_wiki_rejects_javascript_uppercase_after_37,
        test_wiki_rejects_missing_publish_autonomy_row_after_37,
        test_wiki_rejects_missing_ci_hint_still_after_37,
        test_wiki_rejects_missing_badge_topic_still_after_37,
        test_schema_rejects_empty_badge_scope_after_37,
        test_schema_rejects_empty_agents_scope_after_37,
        test_schema_rejects_missing_agents_maintainer_key_after_37,
        test_schema_rejects_missing_claude_repo_key_after_37,
        test_schema_rejects_empty_publish_closes_after_37,
        test_schema_rejects_wrong_publish_status_draft_after_37,
        test_schema_rejects_autonomy_negative_after_37,
        test_schema_rejects_wrong_agents_scope_still_after_37,
        test_schema_rejects_semver_prerelease_still_after_37,
        test_common_secret_patterns_github_pat_after_37,
        test_common_secret_patterns_xoxb_after_37,
        test_common_secret_patterns_rsa_key_after_37,
        test_common_forbidden_badge_hints_buymeacoffee_opencollective_after_37,
        test_common_scan_secrets_xoxb_after_37,
        test_common_has_dangerous_scheme_vbscript_still_after_37,
        test_markdown_lint_requires_davidanson_still_after_37,
        test_link_check_requires_github_token_flag_still_after_37,
        test_markdownlint_json_requires_line_length_200_still_after_37,
        test_stewardship_requires_raw_githubusercontent_still_after_37,
        test_badge_rejects_coveralls_hint_still_after_37,
        test_relative_links_reject_http_scheme_still_after_37,
        test_wiki_rejects_http_scheme_still_after_37,
        test_schema_rejects_tier_zero_still_after_37,
        # TOKENMAXX deepen after #38 (+62)
        test_markdownlint_json_requires_md033_false,
        test_markdownlint_json_requires_md041_false,
        test_markdownlint_json_requires_md060_false,
        test_markdown_lint_requires_cli2_action_v24,
        test_stewardship_requires_setup_python_v5,
        test_stewardship_requires_get_actionlint_id,
        test_actionlint_rejects_pull_request_target_on_markdown_lint_after_38,
        test_actionlint_rejects_contents_write_on_link_check_after_38,
        test_actionlint_rejects_write_all_on_stewardship_after_38,
        test_actionlint_rejects_float_main_on_checkout_link_after_38,
        test_workflow_requires_cancel_in_progress_true_not_false_on_stewardship_after_38,
        test_workflow_rejects_missing_schedule_on_link_check_after_38,
        test_workflow_rejects_missing_dispatch_on_stewardship_after_38,
        test_badge_rejects_coverage_hint_after_38,
        test_badge_rejects_stars_hint_after_38,
        test_badge_rejects_discord_hint_after_38,
        test_badge_rejects_npm_hint_after_38,
        test_badge_rejects_token_query_after_38,
        test_badge_rejects_link_check_http_image_after_38,
        test_badge_rejects_four_badges_still_after_38,
        test_badge_doc_rejects_missing_three_max_after_38,
        test_relative_links_accept_https_mixed_case_after_38,
        test_relative_links_reject_javascript_titlecase_after_38,
        test_relative_links_reject_data_titlecase_after_38,
        test_relative_links_github_slug_hash_punct_after_38,
        test_relative_links_accept_hash_heading_fragment_after_38,
        test_relative_links_reject_broken_parent_docs_after_38,
        test_relative_links_accept_angle_bracket_mailto_mixed_after_38,
        test_relative_links_reject_empty_parens_after_38,
        test_relative_links_reject_protocol_relative_after_38,
        test_wiki_rejects_missing_home_to_routing_after_38,
        test_wiki_rejects_coveralls_badge_chrome_after_38,
        test_wiki_rejects_producthunt_badge_chrome_after_38,
        test_wiki_rejects_npm_badge_chrome_after_38,
        test_wiki_rejects_pypi_badge_chrome_after_38,
        test_wiki_rejects_data_uppercase_after_38,
        test_wiki_rejects_missing_publish_security_row_after_38,
        test_wiki_rejects_missing_actionlint_still_after_38,
        test_wiki_rejects_missing_relative_hint_still_after_38,
        test_schema_rejects_empty_badge_edit_policy_after_38,
        test_schema_rejects_empty_agents_maintainer_after_38,
        test_schema_rejects_missing_agents_parent_key_after_38,
        test_schema_rejects_missing_claude_autonomy_key_after_38,
        test_schema_rejects_empty_publish_created_after_38,
        test_schema_rejects_wrong_badge_status_draft_after_38,
        test_schema_rejects_autonomy_two_vs_expected_after_38,
        test_schema_rejects_wrong_claude_parent_still_after_38,
        test_schema_rejects_closes_without_hash_still_after_38,
        test_common_secret_patterns_ghs_after_38,
        test_common_secret_patterns_ghu_after_38,
        test_common_secret_patterns_rk_after_38,
        test_common_secret_patterns_aws_after_38,
        test_common_forbidden_badge_hints_coverage_stars_after_38,
        test_common_scan_secrets_ghs_after_38,
        test_common_has_dangerous_scheme_file_still_after_38,
        test_markdownlint_json_requires_default_true_still_after_38,
        test_link_check_requires_max_concurrency_8_still_after_38,
        test_stewardship_requires_actionlint_v177_path_still_after_38,
        test_stewardship_requires_get_actionlint_outputs_still_after_38,
        test_badge_rejects_codecov_hint_still_after_38,
        test_relative_links_reject_http_scheme_still_after_38,
        test_schema_rejects_tier_zero_still_after_38,

        # TOKENMAXX deepen after #39 (+62)
        test_link_check_requires_checkout_v7,
        test_markdown_lint_requires_checkout_v7,
        test_stewardship_requires_checkout_v7,
        test_link_check_requires_lychee_action_v2,
        test_link_check_requires_timeout_minutes_20,
        test_markdown_lint_requires_timeout_minutes_10,
        test_stewardship_requires_timeout_minutes_15,
        test_link_check_requires_cron_0_6,
        test_markdown_lint_requires_cron_30_6,
        test_stewardship_requires_cron_15_6,
        test_link_check_requires_ubuntu_latest,
        test_markdown_lint_requires_ubuntu_latest,
        test_stewardship_requires_ubuntu_latest,
        test_stewardship_requires_pip_quiet,
        test_stewardship_requires_shell_bash,
        test_stewardship_requires_actionlint_color,
        test_actionlint_rejects_pull_request_target_on_link_check_after_39,
        test_actionlint_rejects_contents_write_on_markdown_lint_after_39,
        test_actionlint_rejects_float_main_on_checkout_stewardship_after_39,
        test_actionlint_rejects_float_latest_on_checkout_markdown_after_39,
        test_actionlint_rejects_float_master_on_checkout_link_after_39,
        test_actionlint_rejects_unpinned_checkout_on_link_after_39,
        test_actionlint_rejects_unpinned_lychee_after_39,
        test_workflow_requires_cancel_in_progress_true_not_false_on_markdown_lint_after_39,
        test_workflow_rejects_missing_schedule_on_markdown_lint_after_39,
        test_workflow_rejects_missing_dispatch_on_link_check_after_39,
        test_workflow_rejects_missing_concurrency_on_stewardship_after_39,
        test_workflow_rejects_missing_permissions_read_on_markdown_lint_after_39,
        test_actionlint_rejects_contents_write_on_stewardship_after_39,
        test_actionlint_rejects_pull_request_target_on_stewardship_after_39,
        test_workflow_requires_cancel_in_progress_true_not_false_on_link_check_after_39,
        test_workflow_rejects_missing_timeout_on_link_check_after_39,
        test_actionlint_rejects_write_all_on_link_check_after_39,
        test_actionlint_rejects_write_all_on_stewardship_after_39,
        test_link_check_requires_fail_true_after_39,
        test_link_check_requires_exclude_loopback_after_39,
        test_link_check_requires_github_token_flag_after_39,
        test_link_check_requires_action_token_after_39,
        test_link_check_requires_max_concurrency_8_after_39,
        test_link_check_requires_timeout_20_after_39,
        test_link_check_requires_max_retries_3_after_39,
        test_markdown_lint_requires_cli2_action_v24_after_39,
        test_markdown_lint_requires_davidanson_after_39,
        test_markdown_lint_requires_config_needle_after_39,
        test_markdown_lint_requires_owasp_exclude_after_39,
        test_markdown_lint_requires_agents_exclude_after_39,
        test_markdownlint_json_requires_md033_false_still_after_39,
        test_markdownlint_json_requires_md041_false_still_after_39,
        test_markdownlint_json_requires_md060_false_still_after_39,
        test_markdownlint_json_requires_line_length_200_still_after_39,
        test_markdownlint_json_requires_default_true_still_after_39,
        test_stewardship_requires_setup_python_v5_still_after_39,
        test_stewardship_requires_get_actionlint_id_still_after_39,
        test_stewardship_requires_actionlint_v177_path_still_after_39,
        test_stewardship_requires_get_actionlint_outputs_still_after_39,
        test_stewardship_requires_python_312_pin_still_after_39,
        test_stewardship_requires_rhysd_still_after_39,
        test_stewardship_requires_curl_fssl_still_after_39,
        test_stewardship_requires_raw_githubusercontent_still_after_39,
        test_lycheeignore_rejects_https_star_still_after_39,
        test_lycheeignore_rejects_http_star_still_after_39,
        test_lycheeignore_requires_shields_exclude_still_after_39,

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
