#!/usr/bin/env python3
"""Self-tests for stewardship gates (positive live-tree + negative fixtures).

Runs in CI after the live-tree gates so regressions in checkers fail closed.
Does not invent product surface — only validates gate behavior.
TOKENMAXX coverage: badge / wiki / schema / relative / workflow / secrets /
lycheeignore shields / actionlint-style / markdown-link edges.
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
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - run: echo lychee --max-concurrency 8 --timeout 20 --max-retries 3 --exclude-loopback --exclude-path .github/agents --github-token GITHUB_TOKEN
    # lychee-action style
    # fail: true
"""
    # Keep fail: true as a top-level-ish needle the checker greps for:
    link = link.replace("# fail: true", "fail: true")
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
      - uses: actions/checkout@v4
      - run: echo markdownlint OWASP-AGENTIC.md .github/agents .markdownlint.json
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
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pyyaml
      - run: bash scripts/run_stewardship_checks.sh
      - run: python3 scripts/test_stewardship_gates.py
      - run: echo actionlint 1.7.7 .github/workflows/link-check.yml .github/workflows/markdown-lint.yml .github/workflows/stewardship-checks.yml
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
        '{\n  "default": true,\n  "MD013": { "line_length": 200 }\n}\n',
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
            "[Badge](../badge-standard.md)\n"
            "[Overview](Overview.md)\n"
            "[Autonomy-Levels](Autonomy-Levels.md)\n"
            "[Repo-Stewardship](Repo-Stewardship.md)\n"
            "[Agent-Routing](Agent-Routing.md)\n"
            "[Security-Boundaries](Security-Boundaries.md)\n\n"
            "## Out of scope\n\nSecrets and invent product frameworks.\n"
        ),
        "PUBLISH.md": (
            "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
            "purpose: x\ncloses: \"#16\"\n```\n\n"
            "| `Home.md` | Home |\n| `Overview.md` | Overview |\n"
            "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
            "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
            "| `Agent-Routing.md` | Agent-Routing |\n"
            "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
            "Do **not** push `PUBLISH.md`.\n"
            "Link Check and Markdown Lint. No secrets.\n"
        ),
        "Repo-Stewardship.md": (
            "# Repo\n\n[← Home](Home.md)\n\n"
            "markdown-lint link-check stewardship-checks\n"
            "run_stewardship_checks.sh relative links badge\n"
            "no invent product\n"
        ),
        "Autonomy-Levels.md": "# A\n\n[Home](Home.md)\n\nL0 L1 autonomy\n",
        "Security-Boundaries.md": "# S\n\n[Home](Home.md)\n\nkill switch secret\n",
        "Agent-Routing.md": "# R\n\n[Home](Home.md)\n\nsurface routing\n",
        "Overview.md": "# O\n\n[Home](Home.md)\n\ngovernance public\n",
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
        text = path.read_text(encoding="utf-8").replace("timeout-minutes: 10", "")
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
            "must not exclude all https",
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
            "actions/checkout@v4", "actions/checkout"
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
            "actions/checkout@v4", "actions/checkout@main"
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
            "actions/checkout@v4", "actions/checkout@master"
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
            "actions/checkout@v4", "actions/checkout@latest"
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
            "- uses: actions/checkout@v4",
            "- uses: docker://alpine:3.20\n      - uses: actions/checkout@v4",
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
            "must not exclude all https",
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
