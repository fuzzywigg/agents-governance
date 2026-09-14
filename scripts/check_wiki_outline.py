#!/usr/bin/env python3
"""Enforce docs/wiki/PUBLISH.md page set and acceptance checks (executable gate).

Fail-closed pins (live path after #59; deepen after #43; third-pass after #90):
- WIKI under docs/wiki; PUBLISHABLE_PAGES (6) + OPERATOR_ONLY PUBLISH.md
- PAGE_TOPIC_HINTS: L0–L3/autonomy, kill/secret/credential, surface/routing/
  copilot, governance/public, run_stewardship_checks.sh/badge
- README_LINK_HINTS / BADGE_STANDARD_HINTS / STEWARDSHIP_CI_HINTS
- _reject_invent_badge_chrome (stars/forks/followers social special-case)
- strip_fenced_code before link scan; angle-bracket strip; image+link RE
- Reject http:// / protocol-relative // / dangerous schemes; scan_secrets
- Home invent+secrets Out of scope + kill-switch; non-Home ](Home.md) backlink
- PUBLISH.md pages table must include | `Home.md` | (and siblings)
- Third-pass: WIKI exact / removesuffix / glob *.md / sorted(unexpected) /
  Link Check+Markdown Lint+No secrets / invent+secrets+kill Home needles /
  Repo-Stewardship relative+invent+actionlint+run_script needles /
  startswith //+http / group(2) / utf-8 / sys.exit / stewardship_common /
  downloads+discord+twitter+x.com / shields.io / [![ / badge in lowered /
  README+badge hint paths / pages+operator OK / update PUBLISH.md intentional /
  PAGE_TOPIC_HINTS keys / PAGE_TOPIC_HINTS.get / strip_fenced_code(text) /
  has_dangerous_scheme(target) / scan_secrets calls
- After #132 wiki-badge posture: status badges cover Link Check+Markdown Lint /
  product badge refusal / reject stewardship-checks.yml/badge.svg invent /
  reject embedded markdown badge images / PUBLISH Link Check+Markdown Lint exactly
- Wiki-index after #176: Home TOC empty-index reject / publishable page index stubs /
  Home.md must link to publishable page needle
  (not wiki-badge #141 / fixtures #173 / path-filter #176 spam)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from stewardship_common import (  # noqa: E402
    FORBIDDEN_BADGE_HINTS,
    ROOT,
    fail,
    has_dangerous_scheme,
    scan_secrets,
    strip_fenced_code,
)

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

# Topic anchors expected on key publishable pages (no invent-product content).
# Fail-closed after #43: pin live L2/L3 / credential / copilot wording already
# present on Autonomy-Levels / Security-Boundaries / Agent-Routing.
PAGE_TOPIC_HINTS: dict[str, tuple[str, ...]] = {
    "Autonomy-Levels.md": ("L0", "L1", "L2", "L3", "autonomy"),
    "Security-Boundaries.md": ("kill", "secret", "credential"),
    "Agent-Routing.md": ("surface", "routing", "copilot"),
    "Overview.md": ("governance", "public"),
    "Repo-Stewardship.md": ("run_stewardship_checks.sh", "badge"),
}


def _reject_invent_badge_chrome(name: str, text: str, errors: list[str]) -> None:
    lowered = text.lower()
    for hint in FORBIDDEN_BADGE_HINTS:
        # Only flag shield/badge-ish usage, not prose words like "stars" in narrative.
        if hint in ("stars", "forks", "followers", "downloads", "discord", "twitter", "x.com"):
            if f"badge" in lowered and hint in lowered:
                fail(f"{name}: invent-product / social badge chrome hint '{hint}'", errors)
            continue
        if hint in lowered and ("shields.io" in lowered or "badge" in lowered or "[![" in text):
            fail(f"{name}: invent-product / social badge chrome hint '{hint}'", errors)


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
            # Table row should name the source file in backticks.
            if f"| `{name}` |" not in publish_text and f"| `{name}`|" not in publish_text:
                if f"`{name}`" not in publish_text:
                    fail(f"PUBLISH.md pages table must include `{name}`", errors)
        if "Do **not** push `PUBLISH.md`" not in publish_text and "Do not push `PUBLISH.md`" not in publish_text:
            fail("PUBLISH.md must state that PUBLISH.md is not pushed to the wiki", errors)
        if "Link Check" not in publish_text and "link-check" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention Link Check", errors)
        if "Markdown Lint" not in publish_text and "markdown" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention Markdown Lint", errors)
        # Fail-closed after #132: exact badge-name phrases (wiki-badge posture).
        if "Link Check" not in publish_text:
            fail(
                "PUBLISH.md acceptance checks must mention Link Check exactly",
                errors,
            )
        if "Markdown Lint" not in publish_text:
            fail(
                "PUBLISH.md acceptance checks must mention Markdown Lint exactly",
                errors,
            )
        if "No secrets" not in publish_text and "secrets" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention secrets prohibition", errors)

    home = WIKI / "Home.md"
    if home.is_file():
        home_text = home.read_text(encoding="utf-8")
        if not any(hint in home_text for hint in README_LINK_HINTS):
            fail("Home.md must link back to the repository README", errors)
        if not any(hint in home_text for hint in BADGE_STANDARD_HINTS):
            fail("Home.md must link to the badge standard", errors)
        # Wiki-index: Home is the TOC — empty index (no publishable page links) fails.
        for page in PUBLISHABLE_PAGES:
            if page == "Home.md":
                continue
            stem = page.removesuffix(".md")
            if f"]({page})" not in home_text and f"]({stem})" not in home_text:
                fail(f"Home.md must link to publishable page {page}", errors)
        # Fail-closed: Out of scope must call out invent-product AND secrets
        # (not either/or) so quiet stewardship stays explicit on the wiki Home.
        if "invent" not in home_text.lower():
            fail(
                "Home.md must retain invent-product out-of-scope wording",
                errors,
            )
        if "secret" not in home_text.lower():
            fail(
                "Home.md must retain secrets out-of-scope wording",
                errors,
            )
        if "out of scope" not in home_text.lower():
            fail("Home.md must retain an Out of scope section", errors)
        # Fail-closed after #43: Home security row already names kill.
        if "kill" not in home_text.lower():
            fail(
                "Home.md must retain kill-switch security callout",
                errors,
            )
        # Fail-closed after #132: Home is narrative — no badge-row embeds.
        if "[![" in home_text:
            fail(
                "Home.md must not embed markdown badge images",
                errors,
            )

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
        if "run_stewardship_checks.sh" not in ste_text:
            fail("Repo-Stewardship.md must document bash scripts/run_stewardship_checks.sh", errors)
        if "relative" not in ste_text.lower() and "check_relative_links" not in ste_text:
            fail("Repo-Stewardship.md must mention relative-link gate coverage", errors)
        if "invent" not in ste_text.lower():
            fail("Repo-Stewardship.md must retain no-invent-product stewardship wording", errors)
        # Existing CI path: stewardship runs actionlint on the three workflows.
        if "actionlint" not in ste_text.lower():
            fail(
                "Repo-Stewardship.md must mention actionlint on existing workflow paths",
                errors,
            )
        # Fail-closed after #132: wiki-badge posture (Link Check + Markdown Lint only).
        if "Link Check" not in ste_text or "Markdown Lint" not in ste_text:
            fail(
                "Repo-Stewardship.md must name Link Check and Markdown Lint status badges",
                errors,
            )
        if "status badges cover" not in ste_text.lower():
            fail(
                "Repo-Stewardship.md must keep status badges cover wording",
                errors,
            )
        if "product badge" not in ste_text.lower():
            fail(
                "Repo-Stewardship.md must refuse stewardship as a product badge",
                errors,
            )

    for name in PUBLISHABLE_PAGES:
        path = WIKI / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if name != "Home.md" and "](Home.md)" not in text:
            fail(f"{name} must link back to Home.md", errors)
        for topic in PAGE_TOPIC_HINTS.get(name, ()):
            if topic.lower() not in text.lower():
                fail(f"{name} must retain topic hint '{topic}'", errors)
        _reject_invent_badge_chrome(name, text, errors)
        # Fail-closed after #132: no fourth-badge invent / no badge-row embeds on wiki.
        if "stewardship-checks.yml/badge.svg" in text:
            fail(
                f"{name}: must not invent stewardship-checks.yml/badge.svg "
                "(no fourth badge)",
                errors,
            )
        if "[![" in text and "badge.svg" in text.lower():
            fail(
                f"{name}: must not embed markdown badge images "
                "(wiki is narrative, not badge row)",
                errors,
            )
        # Public wiki: no insecure http://, protocol-relative, or dangerous
        # schemes outside fences (strip fences so publish/bash examples pass).
        scan_text = strip_fenced_code(text)
        for match in re.finditer(
            r"!?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)",
            scan_text,
        ):
            target = match.group(2).strip().strip("<>")
            dangerous = has_dangerous_scheme(target)
            if dangerous:
                fail(f"{name}: dangerous link scheme '{dangerous}'", errors)
            if target.startswith("//"):
                fail(
                    f"{name}: protocol-relative link '{target}' (use https://)",
                    errors,
                )
            if target.lower().startswith("http://"):
                fail(f"{name}: insecure http:// link (use https://)", errors)
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
