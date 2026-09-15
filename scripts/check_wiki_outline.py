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
- Deepen after #189: wiki-index/badge leftover — exact PUBLISHABLE_PAGES contiguous
  order / for page in PUBLISHABLE_PAGES TOC loop / skip Home.md /
  ]({page})+]({stem}) link forms / empty index (no publishable page links) comment /
  NOT path-order #189 / NOT stewardship-schema sibling / NOT path-filter #176 spam
  (lands closed #185/#172 leftover on tip; not schema #191; distinct from
  stewardship-badge lint #208 / path-filter/path-order #225 / Pass-2 leftover + md/link #220 /
  schema fourth-pass #216; lands closed #222/#215/#196 leftover after #225 tip)
- Wiki outline/PUBLISH leftover after #233: existing docs/wiki pages only —
  PUBLISH.md pages-table row order / Pages to publish heading /
  one-shot wiki.git clone / cp docs/wiki/{page} list (no operator PUBLISH.md) /
  git add six publishable files / git push origin / purpose+closes #16 YAML /
  Fallback .wiki.git / badge-standard blob rewrite / drop in-repo PUBLISH.md bullet /
  OPERATOR_ONLY not in PUBLISHABLE_PAGES
  (NOT wiki-index/badge leftover #227 / NOT stewardship-checks/schema residual #233 /
  NOT path-filter/path-order #225 / NOT Pass-2 leftover + md/link #220;
  existing pages only — do not invent extra wiki files)
- Lands closed #238 leftover after #239 tip (NOT md/link residual #239)
- Wiki/mdlink leftover after #243: PUBLISH YAML status+created+purpose block /
  ## One-shot publish (after wiki exists) / exact wiki.git clone dest /
  contiguous six-page cp list / cd /tmp/agents-governance.wiki /
  git commit #16 / git push origin master / ## Acceptance checks /
  ## Fallback / Repository not found / Home (landing) table cell /
  Home operator PUBLISH.md omit-when-copying
  (NOT wiki outline/PUBLISH leftover #243 saturated pins / NOT md/link residual layouts #239 /
  NOT path-filter/path-order leftover #244 / NOT stewardship-checks/schema #233 /
  NOT wiki-index/badge leftover #227; existing pages only — do not invent extra wiki files)
- Wiki/mdlink leftover residual after #282 tip (beyond #252 saturated after_243 pins;
  lands closed #281/#277 leftover on post-#282 tip; NOT stewardship-schema residual #282 /
  NOT lychee/blob-503 leftover #278 / NOT Pass-2 residual + templates #272 /
  NOT path-edges leftover #262 / NOT wiki/mdlink leftover #252 /
  NOT stewardship-schema leftover #258 / NOT path-filter/path-order leftover #244 /
  NOT wiki outline/PUBLISH leftover #243 / NOT md/link residual layouts #239 /
  NOT stewardship-checks/schema residual #233;
  existing pages only — do not invent extra wiki files):
  contiguous YAML status+created+purpose+closes block /
  | Source file | Wiki page | table header /
  ordered sibling table cells Overview..Security-Boundaries /
  Do **not** push `PUBLISH.md` to the wiki (operator instructions only). /
  # From a clean worktree of agents-governance /
  or main — match the wiki default branch /
  Link Check and Markdown Lint stay green on the PR that updates sources /
  [Home.md](./Home.md) fallback link /
  Settings Features Wikis init path /
  create any page once in the GitHub UI, then re-run the clone
- Wiki/mdlink leftover residual after #320 tip (beyond #293 saturated after_293 pins;
  lands #325/#318/#308/#307/#302 leftover; NOT stewardship-schema residual CI leftover residual #320 /
  NOT path-filter/path-order leftover #314 /
  NOT stewardship-schema residual CI leftover #309 /
  NOT stewardship-schema residual CI #299 /
  NOT stewardship-schema residual CI #297 /
  NOT wiki/mdlink leftover residual #293 / NOT stewardship-schema residual #282 /
  NOT lychee/blob-503 leftover #278 / NOT Pass-2 residual + templates #272 /
  NOT path-edges leftover #262 / NOT wiki/mdlink leftover #252 /
  NOT stewardship-schema leftover #258 / NOT path-filter/path-order leftover #244 /
  NOT wiki outline/PUBLISH leftover #243 / NOT md/link residual layouts #239;
  existing pages only — do not invent extra wiki files):
  # Publishing this wiki outline to GitHub Wiki /
  The Markdown under `docs/wiki/` is the **in-repo source** for the public wiki /
  GitHub Wiki is a separate git repo /
  |-------------|-----------| table separator /
  When copying `Home.md` / `Repo-Stewardship.md` to the wiki, rewrite relative /
  `../badge-standard.md` links to: /
  Wiki Home links back to the repository README acceptance /
  No secrets, private MEMORY, or private-template internals /
  In-repo `docs/wiki/` remains the editable source; wiki push is a copy /
  Until the `.wiki.git` remote exists, treat /
  as the public landing page linked from the README /
  If clone fails with "Repository not found", the wiki has never been initialized: /
  push `Home.md`) init path /
  full git push origin master   # or main line /
  Home ## Start here / | Page | What it covers | /
  ## Source of truth (repository) / Canonical public governance front door /
  This wiki is the **public narrative layer** /
  Repo-Stewardship ## Front-door duties / ## Docs quality CI
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

    # Wiki outline/PUBLISH leftover after #233: operator PUBLISH.md is not a
    # public wiki page (existing pages only — do not invent extra wiki files).
    if OPERATOR_ONLY in PUBLISHABLE_PAGES:
        fail(
            "PUBLISH.md is operator-only and must not be in PUBLISHABLE_PAGES",
            errors,
        )

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
        # Wiki outline/PUBLISH leftover after #233 (existing pages only).
        if "## Pages to publish" not in publish_text:
            fail("PUBLISH.md must keep ## Pages to publish heading", errors)
        last_row_at = -1
        for name in PUBLISHABLE_PAGES:
            row = f"| `{name}` |"
            found = publish_text.find(row)
            if found < 0:
                fail(
                    f"PUBLISH.md pages table must keep ordered row for {name}",
                    errors,
                )
                continue
            if found < last_row_at:
                fail(
                    "PUBLISH.md pages table must keep publishable page order",
                    errors,
                )
            last_row_at = found
        if "agents-governance.wiki.git" not in publish_text:
            fail(
                "PUBLISH.md one-shot must clone agents-governance.wiki.git",
                errors,
            )
        if "cp docs/wiki/PUBLISH.md" in publish_text:
            fail(
                "PUBLISH.md one-shot must not copy operator PUBLISH.md",
                errors,
            )
        for name in PUBLISHABLE_PAGES:
            if f"docs/wiki/{name}" not in publish_text:
                fail(
                    f"PUBLISH.md one-shot must copy existing page docs/wiki/{name}",
                    errors,
                )
        git_add_six = "git add Home.md Overview.md Autonomy-Levels.md Repo-Stewardship.md Agent-Routing.md Security-Boundaries.md"
        if git_add_six not in publish_text:
            fail(
                "PUBLISH.md one-shot must git add the six publishable pages",
                errors,
            )
        if "git push origin" not in publish_text:
            fail("PUBLISH.md one-shot must git push origin", errors)
        if "Reversible publish path for docs/wiki" not in publish_text:
            fail("PUBLISH.md YAML must keep Reversible publish path purpose", errors)
        if 'closes: "#16"' not in publish_text and "closes: '#16'" not in publish_text:
            fail("PUBLISH.md YAML must keep closes: \"#16\"", errors)
        if ".wiki.git" not in publish_text:
            fail("PUBLISH.md fallback must mention .wiki.git remote", errors)
        if (
            "https://github.com/fuzzywigg/agents-governance/blob/main/docs/badge-standard.md"
            not in publish_text
        ):
            fail(
                "PUBLISH.md must keep badge-standard blob rewrite URL",
                errors,
            )
        if "drop the in-repo `PUBLISH.md` bullet" not in publish_text:
            fail(
                "PUBLISH.md must say drop the in-repo PUBLISH.md bullet from Home",
                errors,
            )
        # Wiki/mdlink leftover after #243 (existing pages only; residual vs #243).
        yaml_purpose_block = (
            "status: ACTIVE\n"
            'created: "2026-09-13"\n'
            'purpose: "Reversible publish path for docs/wiki → GitHub Wiki"'
        )
        if yaml_purpose_block not in publish_text:
            fail(
                "PUBLISH.md YAML must keep contiguous status/created/purpose block",
                errors,
            )
        if "## One-shot publish (after wiki exists)" not in publish_text:
            fail(
                "PUBLISH.md must keep ## One-shot publish (after wiki exists) heading",
                errors,
            )
        exact_clone = (
            "git clone https://github.com/fuzzywigg/agents-governance.wiki.git "
            "/tmp/agents-governance.wiki"
        )
        if exact_clone not in publish_text:
            fail(
                "PUBLISH.md one-shot must clone to /tmp/agents-governance.wiki",
                errors,
            )
        cp_six = (
            "cp docs/wiki/Home.md \\\n"
            "   docs/wiki/Overview.md \\\n"
            "   docs/wiki/Autonomy-Levels.md \\\n"
            "   docs/wiki/Repo-Stewardship.md \\\n"
            "   docs/wiki/Agent-Routing.md \\\n"
            "   docs/wiki/Security-Boundaries.md \\\n"
            "   /tmp/agents-governance.wiki/"
        )
        if cp_six not in publish_text:
            fail(
                "PUBLISH.md one-shot must keep contiguous six-page cp list",
                errors,
            )
        if "cd /tmp/agents-governance.wiki" not in publish_text:
            fail(
                "PUBLISH.md one-shot must cd /tmp/agents-governance.wiki",
                errors,
            )
        git_commit_16 = (
            'git commit -m "docs: publish public wiki outline from docs/wiki (#16)"'
        )
        if git_commit_16 not in publish_text:
            fail(
                "PUBLISH.md one-shot must git commit wiki outline from docs/wiki (#16)",
                errors,
            )
        if "git push origin master" not in publish_text:
            fail(
                "PUBLISH.md one-shot must git push origin master",
                errors,
            )
        if "## Acceptance checks" not in publish_text:
            fail("PUBLISH.md must keep ## Acceptance checks heading", errors)
        if "## Fallback\n" not in publish_text and "## Fallback\r\n" not in publish_text:
            fail("PUBLISH.md must keep ## Fallback heading", errors)
        if "Repository not found" not in publish_text:
            fail(
                "PUBLISH.md fallback must mention Repository not found",
                errors,
            )
        if "| `Home.md` | Home (landing) |" not in publish_text:
            fail(
                "PUBLISH.md pages table must keep Home (landing) cell",
                errors,
            )

        # Wiki/mdlink leftover residual after #282 tip (beyond #252 saturated pins; lands #281/#277).
        yaml_closes_block = (
            "status: ACTIVE\n"
            'created: "2026-09-13"\n'
            'purpose: "Reversible publish path for docs/wiki → GitHub Wiki"\n'
            'closes: "#16"'
        )
        if yaml_closes_block not in publish_text:
            fail(
                "PUBLISH.md YAML must keep contiguous status/created/purpose/closes block",
                errors,
            )
        if "| Source file | Wiki page |" not in publish_text:
            fail(
                "PUBLISH.md pages table must keep | Source file | Wiki page | header",
                errors,
            )
        for sibling_row in (
            "| `Overview.md` | Overview |",
            "| `Autonomy-Levels.md` | Autonomy-Levels |",
            "| `Repo-Stewardship.md` | Repo-Stewardship |",
            "| `Agent-Routing.md` | Agent-Routing |",
            "| `Security-Boundaries.md` | Security-Boundaries |",
        ):
            if sibling_row not in publish_text:
                fail(
                    f"PUBLISH.md pages table must keep sibling cell {sibling_row}",
                    errors,
                )
        if (
            "Do **not** push `PUBLISH.md` to the wiki (operator instructions only)."
            not in publish_text
        ):
            fail(
                "PUBLISH.md must keep full operator push prose "
                "(to the wiki / operator instructions only)",
                errors,
            )
        if "# From a clean worktree of agents-governance" not in publish_text:
            fail(
                "PUBLISH.md one-shot must keep clean worktree commentary",
                errors,
            )
        if "or main — match the wiki default branch" not in publish_text:
            fail(
                "PUBLISH.md one-shot must keep or main — match the wiki default branch",
                errors,
            )
        if (
            "Link Check and Markdown Lint stay green on the PR that updates sources"
            not in publish_text
        ):
            fail(
                "PUBLISH.md acceptance must keep Link Check and Markdown Lint stay green",
                errors,
            )
        if "[Home.md](./Home.md)" not in publish_text:
            fail(
                "PUBLISH.md fallback must keep [Home.md](./Home.md) relative link",
                errors,
            )
        if "Settings → Features → Wikis" not in publish_text:
            fail(
                "PUBLISH.md must keep Settings → Features → Wikis init path",
                errors,
            )
        if (
            "create any page once in the GitHub UI, then re-run the clone"
            not in publish_text
        ):
            fail(
                "PUBLISH.md fallback must keep create any page once in the GitHub UI",
                errors,
            )

        # Wiki/mdlink leftover residual after #320 tip (beyond #293 saturated pins; lands #325/#318/#308/#307/#302; NOT schema residual CI leftover residual #320).
        if "# Publishing this wiki outline to GitHub Wiki" not in publish_text:
            fail(
                "PUBLISH.md must keep # Publishing this wiki outline to GitHub Wiki H1",
                errors,
            )
        if (
            "The Markdown under `docs/wiki/` is the **in-repo source** for the public wiki"
            not in publish_text
        ):
            fail(
                "PUBLISH.md must keep in-repo source for the public wiki wording",
                errors,
            )
        if "GitHub Wiki is a separate git repo" not in publish_text:
            fail(
                "PUBLISH.md must keep GitHub Wiki is a separate git repo wording",
                errors,
            )
        if "|-------------|-----------|" not in publish_text:
            fail(
                "PUBLISH.md pages table must keep |-------------|-----------| separator",
                errors,
            )
        if (
            "When copying `Home.md` / `Repo-Stewardship.md` to the wiki, rewrite relative"
            not in publish_text
        ):
            fail(
                "PUBLISH.md must keep When copying Home.md / Repo-Stewardship.md "
                "rewrite relative wording",
                errors,
            )
        if "`../badge-standard.md` links to:" not in publish_text:
            fail(
                "PUBLISH.md must keep `../badge-standard.md` links to: rewrite hint",
                errors,
            )
        if (
            "Wiki Home links back to the repository [README]("
            "https://github.com/fuzzywigg/agents-governance/blob/main/README.md)"
            not in publish_text
        ):
            fail(
                "PUBLISH.md acceptance must keep Wiki Home links back to the "
                "repository README checkbox",
                errors,
            )
        if (
            "No secrets, private MEMORY, or private-template internals in published pages"
            not in publish_text
        ):
            fail(
                "PUBLISH.md acceptance must keep No secrets, private MEMORY, "
                "or private-template internals wording",
                errors,
            )
        if (
            "In-repo `docs/wiki/` remains the editable source; wiki push is a copy"
            not in publish_text
        ):
            fail(
                "PUBLISH.md acceptance must keep editable source; wiki push is a copy",
                errors,
            )
        if "Until the `.wiki.git` remote exists, treat" not in publish_text:
            fail(
                "PUBLISH.md fallback must keep Until the `.wiki.git` remote exists, treat",
                errors,
            )
        if (
            "as the public landing page linked from the README"
            not in publish_text
        ):
            fail(
                "PUBLISH.md fallback must keep as the public landing page "
                "linked from the README",
                errors,
            )
        if (
            'If clone fails with "Repository not found", the wiki has never been initialized:'
            not in publish_text
        ):
            fail(
                "PUBLISH.md fallback must keep If clone fails with Repository not found "
                "initialized wording",
                errors,
            )
        if "push `Home.md`)" not in publish_text:
            fail(
                "PUBLISH.md must keep push `Home.md`) wiki init path wording",
                errors,
            )
        full_push_line = (
            "git push origin master   # or main — match the wiki default branch"
        )
        if full_push_line not in publish_text:
            fail(
                "PUBLISH.md one-shot must keep full git push origin master "
                "# or main line",
                errors,
            )

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
        # Wiki/mdlink leftover after #243: operator publish path stays in-repo.
        if "](PUBLISH.md)" not in home_text or (
            "omit when copying pages to GitHub Wiki" not in home_text
        ):
            fail(
                "Home.md must keep operator PUBLISH.md link "
                "(omit when copying pages to GitHub Wiki)",
                errors,
            )
        # Wiki/mdlink leftover residual after #320 tip (existing Home.md only; lands #325/#318/#308/#307/#302; NOT schema residual CI leftover residual #320).
        if "## Start here" not in home_text:
            fail("Home.md must keep ## Start here heading", errors)
        if "| Page | What it covers |" not in home_text:
            fail(
                "Home.md must keep | Page | What it covers | TOC header",
                errors,
            )
        if "## Source of truth (repository)" not in home_text:
            fail(
                "Home.md must keep ## Source of truth (repository) heading",
                errors,
            )
        if "Canonical public governance front door" not in home_text:
            fail(
                "Home.md must keep Canonical public governance front door wording",
                errors,
            )
        if "This wiki is the **public narrative layer**" not in home_text:
            fail(
                "Home.md must keep This wiki is the **public narrative layer** wording",
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
        # Wiki/mdlink leftover residual after #320 tip (existing Repo-Stewardship only; lands #325/#318/#308/#307/#302; NOT schema residual CI leftover residual #320).
        if "## Front-door duties" not in ste_text:
            fail(
                "Repo-Stewardship.md must keep ## Front-door duties heading",
                errors,
            )
        if "## Docs quality CI" not in ste_text:
            fail(
                "Repo-Stewardship.md must keep ## Docs quality CI heading",
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
