#!/usr/bin/env python3
"""Enforce docs/wiki/PUBLISH.md page set and acceptance checks (executable gate)."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from stewardship_common import ROOT, fail, scan_secrets  # noqa: E402

WIKI = ROOT / "docs" / "wiki"

# Keep in sync with docs/wiki/PUBLISH.md "Pages to publish"
PUBLISHABLE_PAGES = (
    "Home.md",
    "Overview.md",
    "Autonomy-Levels.md",
    "Repo-Stewardship.md",
    "Agent-Routing.md",
    "Security-Boundaries.md",
)
OPERATOR_ONLY = "PUBLISH.md"

README_LINK_HINTS = (
    "https://github.com/fuzzywigg/agents-governance/blob/main/README.md",
    "../../README.md",
    "../README.md",  # would be wrong from wiki/, but catch if rewritten
)
BADGE_STANDARD_HINTS = (
    "../badge-standard.md",
    "docs/badge-standard.md",
    "https://github.com/fuzzywigg/agents-governance/blob/main/docs/badge-standard.md",
)

# Public acceptance: stewardship CI called out on Repo-Stewardship.
STEWARDSHIP_CI_HINTS = (
    "markdown-lint",
    "link-check",
    "stewardship-checks",
)


def main() -> int:
    errors: list[str] = []

    if not WIKI.is_dir():
        print("FAIL: docs/wiki/ missing", file=sys.stderr)
        return 1

    publish = WIKI / OPERATOR_ONLY
    if not publish.is_file():
        fail(f"Missing operator page {OPERATOR_ONLY}", errors)

    present = {p.name for p in WIKI.glob("*.md")}
    for name in PUBLISHABLE_PAGES:
        if name not in present:
            fail(f"Missing required wiki source page: docs/wiki/{name}", errors)

    unexpected = present - set(PUBLISHABLE_PAGES) - {OPERATOR_ONLY}
    if unexpected:
        fail(
            "Unexpected markdown under docs/wiki/ (update PUBLISH.md page list if intentional): "
            + ", ".join(sorted(unexpected)),
            errors,
        )

    if publish.is_file():
        publish_text = publish.read_text(encoding="utf-8")
        for name in PUBLISHABLE_PAGES:
            stem = name.removesuffix(".md")
            if f"`{name}`" not in publish_text and stem not in publish_text:
                fail(f"PUBLISH.md must list source file {name}", errors)
        if "Do **not** push `PUBLISH.md`" not in publish_text and "Do not push `PUBLISH.md`" not in publish_text:
            fail("PUBLISH.md must state that PUBLISH.md is not pushed to the wiki", errors)
        if "Link Check" not in publish_text and "link-check" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention Link Check", errors)
        if "Markdown Lint" not in publish_text and "markdown" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention Markdown Lint", errors)

    home = WIKI / "Home.md"
    if home.is_file():
        home_text = home.read_text(encoding="utf-8")
        if not any(hint in home_text for hint in README_LINK_HINTS):
            fail("Home.md must link back to the repository README", errors)
        if not any(hint in home_text for hint in BADGE_STANDARD_HINTS):
            fail("Home.md must link to the badge standard", errors)
        for page in PUBLISHABLE_PAGES:
            if page == "Home.md":
                continue
            stem = page.removesuffix(".md")
            if f"]({page})" not in home_text and f"]({stem})" not in home_text:
                fail(f"Home.md must link to publishable page {page}", errors)
        if "invent" not in home_text.lower() and "secrets" not in home_text.lower():
            fail("Home.md must retain out-of-scope wording for secrets / invent-product", errors)

    stewardship = WIKI / "Repo-Stewardship.md"
    if stewardship.is_file():
        ste_text = stewardship.read_text(encoding="utf-8")
        missing_ci = [h for h in STEWARDSHIP_CI_HINTS if h not in ste_text]
        if missing_ci:
            fail(
                "Repo-Stewardship.md must mention stewardship CI workflows: "
                + ", ".join(missing_ci),
                errors,
            )

    for name in PUBLISHABLE_PAGES:
        path = WIKI / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if name != "Home.md" and "](Home.md)" not in text:
            fail(f"{name} must link back to Home.md", errors)
        scan_secrets(path, errors)

    if publish.is_file():
        scan_secrets(publish, errors)

    if errors:
        print("Wiki outline check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        "OK: docs/wiki matches PUBLISH.md page set "
        f"({len(PUBLISHABLE_PAGES)} pages + operator PUBLISH.md)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
