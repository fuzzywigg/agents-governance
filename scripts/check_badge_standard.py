#!/usr/bin/env python3
"""Enforce docs/badge-standard.md against README.md (executable gate)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
LICENSE = ROOT / "LICENSE"
WORKFLOWS = ROOT / ".github" / "workflows"

REQUIRED_ORDER = ("Link Check", "Markdown Lint", "License")
MAX_BADGES = 3

# Status-only badges. Coverage / social / downloads are invent-product noise.
FORBIDDEN_BADGE_HINTS = (
    "coverage",
    "codecov",
    "coveralls",
    "downloads",
    "discord",
    "twitter",
    "x.com",
    "stars",
    "forks",
    "followers",
    "npm/",
    "pypi/",
)

SECRET_URL_HINTS = (
    "token=",
    "access_token=",
    "api_key=",
    "apikey=",
    "ghp_",
    "gho_",
    "github_pat_",
)

BADGE_LINE_RE = re.compile(
    r"^\[!\[(?P<label>[^\]]+)\]\((?P<img>[^)]+)\)\]\((?P<link>[^)]+)\)\s*$"
)


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def extract_badge_row(text: str) -> tuple[list[re.Match[str]], list[str]]:
    """Return consecutive badge lines immediately after the first H1."""
    errors: list[str] = []
    lines = text.splitlines()
    h1_idx = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if h1_idx is None:
        fail("README.md missing H1 (# title)", errors)
        return [], errors

    badges: list[re.Match[str]] = []
    i = h1_idx + 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    while i < len(lines):
        match = BADGE_LINE_RE.match(lines[i])
        if not match:
            break
        badges.append(match)
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            # allow blank lines between badge lines? standard says a row —
            # tolerate single blanks but stop at non-badge content
            if i + 1 < len(lines) and BADGE_LINE_RE.match(lines[i + 1]):
                i += 1
                continue
            break
    if not badges:
        fail(
            "README.md must place the required badge row immediately under the H1 "
            "(after optional blank lines)",
            errors,
        )
    return badges, errors


def check_workflows_and_license(errors: list[str]) -> None:
    for name in ("link-check.yml", "markdown-lint.yml"):
        path = WORKFLOWS / name
        if not path.is_file():
            fail(f"Missing workflow required by badge standard: {path.relative_to(ROOT)}", errors)
    if not LICENSE.is_file():
        fail("Missing LICENSE (required for License badge)", errors)


def check_badges(badges: list[re.Match[str]], errors: list[str]) -> None:
    if len(badges) > MAX_BADGES:
        fail(
            f"Badge row has {len(badges)} badges; standard allows at most {MAX_BADGES} "
            "unless smtp.eth adds an explicit fourth",
            errors,
        )

    labels = [m.group("label") for m in badges]
    if labels[: len(REQUIRED_ORDER)] != list(REQUIRED_ORDER):
        fail(
            f"Badge labels must be in order {list(REQUIRED_ORDER)}; found {labels}",
            errors,
        )

    for match in badges:
        label = match.group("label")
        img = match.group("img")
        link = match.group("link")
        blob = f"{label}|{img}|{link}".lower()

        for hint in FORBIDDEN_BADGE_HINTS:
            if hint in blob:
                fail(f"Forbidden invent-product / social badge hint '{hint}' in {label}", errors)
        for hint in SECRET_URL_HINTS:
            if hint in blob:
                fail(f"Secret-like token in badge URL for {label}", errors)

        if label == "Link Check":
            if "actions/workflows/link-check.yml/badge.svg" not in img:
                fail("Link Check image must use link-check.yml/badge.svg", errors)
            if "actions/workflows/link-check.yml" not in link:
                fail("Link Check link must target link-check.yml workflow", errors)
        elif label == "Markdown Lint":
            if "actions/workflows/markdown-lint.yml/badge.svg" not in img:
                fail("Markdown Lint image must use markdown-lint.yml/badge.svg", errors)
            if "actions/workflows/markdown-lint.yml" not in link:
                fail("Markdown Lint link must target markdown-lint.yml workflow", errors)
        elif label == "License":
            shields_ok = "img.shields.io/github/license/" in img
            if not shields_ok:
                fail("License image must use img.shields.io/github/license/<owner>/<repo>", errors)
            license_link_ok = link.endswith("/LICENSE") or link in {"LICENSE", "./LICENSE"}
            if not license_link_ok:
                fail("License badge link must point at LICENSE (relative or blob URL)", errors)


def main() -> int:
    errors: list[str] = []
    if not README.is_file():
        print("FAIL: README.md missing", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    check_workflows_and_license(errors)
    badges, row_errors = extract_badge_row(text)
    errors.extend(row_errors)
    if badges:
        check_badges(badges, errors)

    if errors:
        print("Badge standard check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: README badge row matches docs/badge-standard.md ({', '.join(REQUIRED_ORDER)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
