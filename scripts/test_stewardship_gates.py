#!/usr/bin/env python3
"""Lightweight negative/positive self-tests for stewardship gates.

Runs in CI after the live-tree gates so regressions in checkers fail closed.
Does not invent product surface — only validates gate behavior.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def assert_fail(script: str, cwd: Path, needle: str) -> None:
    proc = run(script, cwd)
    if proc.returncode == 0:
        raise AssertionError(f"{script} unexpectedly passed in {cwd}\n{proc.stdout}{proc.stderr}")
    blob = proc.stdout + proc.stderr
    if needle not in blob:
        raise AssertionError(
            f"{script} failed but missing expected message {needle!r}\n{blob}"
        )


def assert_pass_live(script: str) -> None:
    proc = run(script, ROOT)
    if proc.returncode != 0:
        raise AssertionError(f"{script} failed on live tree\n{proc.stdout}{proc.stderr}")


def test_badge_rejects_wrong_order() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # Minimal fake tree
        (tmp_path / "docs").mkdir()
        (tmp_path / ".github" / "workflows").mkdir(parents=True)
        for name in ("link-check.yml", "markdown-lint.yml", "stewardship-checks.yml"):
            (tmp_path / ".github" / "workflows" / name).write_text("name: x\n", encoding="utf-8")
        (tmp_path / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (tmp_path / "docs" / "badge-standard.md").write_text(
            "# Badge\n\n```yaml\nstatus: ACTIVE\ntier: 1\ncreated: \"2026-09-13\"\n"
            "owner: copilot\nscope: test\nedit_policy: \"do not invent product badges\"\n"
            "closes: \"#16\"\n```\n\n"
            "| Link Check | x | y |\n| Markdown Lint | x | y |\n| License | x | y |\n\n"
            "link-check.yml/badge.svg\nmarkdown-lint.yml/badge.svg\n"
            "img.shields.io/github/license/\ndo not invent product badges\n",
            encoding="utf-8",
        )
        (tmp_path / "README.md").write_text(
            "# agents-governance\n\n"
            "[![Markdown Lint](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/markdown-lint.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/markdown-lint.yml)\n"
            "[![Link Check](https://github.com/fuzzywigg/agents-governance/"
            "actions/workflows/link-check.yml/badge.svg)]"
            "(https://github.com/fuzzywigg/agents-governance/actions/workflows/link-check.yml)\n"
            "[![License](https://img.shields.io/github/license/fuzzywigg/agents-governance)]"
            "(LICENSE)\n\n"
            "See [docs/badge-standard.md](docs/badge-standard.md).\n"
            "Run `bash scripts/run_stewardship_checks.sh`.\n",
            encoding="utf-8",
        )
        # Point checker ROOT via symlink layout: copy scripts and patch by running
        # from a mini-repo that includes scripts/ with ROOT detection.
        # Easier: invoke checker functions after temporarily monkeypatching — use
        # subprocess with SCRIPT that sets cwd incorrectly won't work because ROOT
        # is derived from script path. Instead, rewrite script copy:
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        for name in (
            "stewardship_common.py",
            "check_badge_standard.py",
        ):
            scripts_dir.joinpath(name).write_text(
                (SCRIPTS / name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / "check_badge_standard.py")],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            raise AssertionError(f"expected badge order failure\n{proc.stdout}{proc.stderr}")
        if "Badge labels must be in order" not in (proc.stdout + proc.stderr):
            raise AssertionError(f"missing order error\n{proc.stdout}{proc.stderr}")


def test_relative_links_reject_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        for name in ("stewardship_common.py", "check_relative_links.py"):
            scripts_dir.joinpath(name).write_text(
                (SCRIPTS / name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        (tmp_path / "README.md").write_text(
            "# T\n\nSee [missing](./nope.md).\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / "check_relative_links.py")],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            raise AssertionError("expected broken relative link failure")
        if "broken relative link" not in (proc.stdout + proc.stderr):
            raise AssertionError(f"missing broken-link message\n{proc.stdout}{proc.stderr}")


def main() -> int:
    try:
        assert_pass_live("check_badge_standard.py")
        assert_pass_live("check_wiki_outline.py")
        assert_pass_live("check_stewardship_schema.py")
        assert_pass_live("check_relative_links.py")
        test_badge_rejects_wrong_order()
        test_relative_links_reject_missing()
    except AssertionError as exc:
        print(f"Stewardship self-test FAILED: {exc}", file=sys.stderr)
        return 1
    print("OK: stewardship gate self-tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
