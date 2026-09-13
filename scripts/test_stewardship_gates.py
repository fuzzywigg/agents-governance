#!/usr/bin/env python3
"""Self-tests for stewardship gates (positive live-tree + negative fixtures).

Runs in CI after the live-tree gates so regressions in checkers fail closed.
Does not invent product surface — only validates gate behavior.
TOKENMAXX coverage: badge / wiki / schema / relative / workflow / secrets.
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
      - run: echo lychee --max-concurrency 8 --timeout 20 --max-retries 3 --exclude-loopback --exclude-path .github/agents
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
      - uses: actions/setup-python@v5
      - run: pip install pyyaml
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
        # Relative (13)
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
        # Wiki (7)
        test_wiki_rejects_unexpected_page,
        test_wiki_rejects_missing_home_backlink,
        test_wiki_rejects_invent_chrome,
        test_wiki_rejects_missing_topic_hint,
        test_wiki_rejects_http_link,
        test_wiki_rejects_secret_pattern,
        test_wiki_rejects_missing_out_of_scope,
        # Schema (11)
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
        # Common / workflow (6)
        test_common_secret_patterns,
        test_common_dangerous_schemes,
        test_workflow_hardening_requires_timeout,
        test_workflow_hardening_requires_schedule,
        test_workflow_hardening_requires_concurrency,
        test_workflow_hardening_requires_pyyaml_install,
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
