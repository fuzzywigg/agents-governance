#!/usr/bin/env python3
"""Enforce docs/wiki/PUBLISH.md page set and acceptance checks (executable gate)."""

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
# Fail-closed after wiki-outline deepen: Home must keep ecosystem policy pointer.
ECOSYSTEM_LINK_HINTS = (
    "AGENTS-ECOSYSTEM.md",
    "agents-governance/blob/main/AGENTS-ECOSYSTEM.md",
)

# Public acceptance: stewardship CI called out on Repo-Stewardship.
STEWARDSHIP_CI_HINTS = (
    "markdown-lint",
    "link-check",
    "stewardship-checks",
)

# Topic anchors expected on key publishable pages (no invent-product content).
# Deepened after #41: L2/L3/kill_switch, SECURITY.md/credential, copilot/geryon,
# AGENTS-ECOSYSTEM/scratchpad, test_stewardship_gates.py — all already live.
PAGE_TOPIC_HINTS: dict[str, tuple[str, ...]] = {
    "Autonomy-Levels.md": ("L0", "L1", "L2", "L3", "autonomy", "kill_switch"),
    "Security-Boundaries.md": ("kill", "secret", "credential", "SECURITY.md"),
    "Agent-Routing.md": ("surface", "routing", "copilot", "geryon"),
    "Overview.md": ("governance", "public", "AGENTS-ECOSYSTEM", "scratchpad"),
    "Repo-Stewardship.md": (
        "run_stewardship_checks.sh",
        "badge",
        "test_stewardship_gates.py",
    ),
}

MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(\s*([^)\s]*)(?:\s+\"[^\"]*\")?\s*\)")
ATX_H1_RE = re.compile(r"(?m)^#\s+\S")
OUT_OF_SCOPE_HEADING_RE = re.compile(r"(?im)^##\s+Out of scope\s*$")


def has_atx_h1(text: str) -> bool:
    """True if page has a non-empty ATX H1 (# Title)."""
    return ATX_H1_RE.search(text) is not None


def page_is_empty(text: str) -> bool:
    """True if page has no non-whitespace content."""
    return not text.strip()


def has_out_of_scope_heading(text: str) -> bool:
    """True if Home retains an explicit ## Out of scope heading."""
    return OUT_OF_SCOPE_HEADING_RE.search(text) is not None


def iter_markdown_link_targets(text: str) -> list[str]:
    """Return markdown link/image targets (fences should be stripped by caller)."""
    return [m.group(2).strip().strip("<>") for m in MD_LINK_RE.finditer(text)]


def is_protocol_relative(target: str) -> bool:
    """True for //host protocol-relative links."""
    return target.startswith("//")


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


def _check_link_schemes(name: str, text: str, errors: list[str]) -> None:
    """Reject dangerous / insecure / protocol-relative markdown link targets."""
    # Ignore fenced examples (publish scripts, yaml snippets).
    body = strip_fenced_code(text)
    for target in iter_markdown_link_targets(body):
        dangerous = has_dangerous_scheme(target)
        if dangerous:
            fail(f"{name}: dangerous link scheme '{dangerous}'", errors)
        if target.lower().startswith("http://"):
            fail(f"{name}: insecure http:// link (use https://)", errors)
        if is_protocol_relative(target):
            fail(f"{name}: protocol-relative link not allowed", errors)


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
        if page_is_empty(publish_text):
            fail(f"{OPERATOR_ONLY} must not be empty", errors)
        if not has_atx_h1(publish_text):
            fail(f"{OPERATOR_ONLY} must start with an ATX H1 heading", errors)
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
        if "No secrets" not in publish_text and "secrets" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention secrets prohibition", errors)
        # Fail-closed after wiki-outline deepen: operator path must keep wiki remote + source.
        if ".wiki.git" not in publish_text.lower() and "wiki.git" not in publish_text.lower():
            fail("PUBLISH.md must mention the .wiki.git publish remote", errors)
        if "docs/wiki" not in publish_text:
            fail("PUBLISH.md must retain docs/wiki as the in-repo source path", errors)
        if "MEMORY" not in publish_text and "memory" not in publish_text.lower():
            fail("PUBLISH.md acceptance checks must mention MEMORY prohibition", errors)
        _check_link_schemes(OPERATOR_ONLY, publish_text, errors)
        _reject_invent_badge_chrome(OPERATOR_ONLY, publish_text, errors)

    home = WIKI / "Home.md"
    if home.is_file():
        home_text = home.read_text(encoding="utf-8")
        if page_is_empty(home_text):
            fail("Home.md must not be empty", errors)
        if not has_atx_h1(home_text):
            fail("Home.md must start with an ATX H1 heading", errors)
        if not any(hint in home_text for hint in README_LINK_HINTS):
            fail("Home.md must link back to the repository README", errors)
        if not any(hint in home_text for hint in BADGE_STANDARD_HINTS):
            fail("Home.md must link to the badge standard", errors)
        if not any(hint in home_text for hint in ECOSYSTEM_LINK_HINTS):
            fail("Home.md must link to AGENTS-ECOSYSTEM.md (ecosystem policy)", errors)
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
        if not has_out_of_scope_heading(home_text):
            fail("Home.md must retain an explicit ## Out of scope heading", errors)
        if "smtp.eth" not in home_text.lower():
            fail("Home.md must retain smtp.eth maintainer attribution", errors)

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
        if "AGENTS-ECOSYSTEM" not in ste_text:
            fail(
                "Repo-Stewardship.md must mention AGENTS-ECOSYSTEM approval boundary",
                errors,
            )

    for name in PUBLISHABLE_PAGES:
        path = WIKI / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if page_is_empty(text):
            fail(f"{name} must not be empty", errors)
            continue
        if not has_atx_h1(text):
            fail(f"{name} must start with an ATX H1 heading", errors)
        if name != "Home.md" and "](Home.md)" not in text:
            fail(f"{name} must link back to Home.md", errors)
        for topic in PAGE_TOPIC_HINTS.get(name, ()):
            if topic.lower() not in text.lower():
                fail(f"{name} must retain topic hint '{topic}'", errors)
        _reject_invent_badge_chrome(name, text, errors)
        _check_link_schemes(name, text, errors)
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
