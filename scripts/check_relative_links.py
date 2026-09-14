#!/usr/bin/env python3
"""Offline relative markdown link integrity (complements lychee external checks).

Fail-closed pins (live path after #55; deepen after #41; third-pass after #90):
- Skip via SKIP_FILES / SKIP_PARTS / SKIP_PREFIXES: OWASP-AGENTIC.md /
  .github/agents / .git / node_modules (align lint/lychee)
- MD_LINK_RE scans links + images; strip_fenced_code before scan; fully_unquote
  with _MAX_UNQUOTE_PASSES = 4 nested percent-decode (traversal fail-closed)
- should_skip / iter_markdown / headings_in / check_file / github_slug helpers
- Allow https:// / mailto: / tel:; reject empty targets, bare `#`, empty
  path# fragments, query strings, protocol-relative `//`, insecure http://,
  dangerous schemes, NUL, repo escapes; angle-bracket targets supported
- Third-pass: MD_LINK_RE+ATX_HEADING_RE exact / SKIP_* exact assigns /
  OK+FAILED banners / empty+http+protocol-relative+dangerous needles /
  utf-8 / as_posix / .md suffix / ValueError / sorted / UNICODE /
  space-to-dash slug / Percent-decode+Cap nested / empty () fail-closed /
  sys.exit / urllib.unquote / group(2) / startswith# / split# /
  files scanned / stewardship_common import / title attr / #{1,6} /
  slug punctuation strip / Offline+lychee docstring / path.parent
- Wiki-index after #176: broken internal stub links / empty markdown index /
  no markdown files found / duplicate slug headings_in set collapse via
  {github_slug(match.group(2))} (not wiki-badge #141 / fixtures #173 spam)
- Deepen after #189: wiki-index/badge leftover — broken relative link fail needle /
  empty markdown index fail-closed / Duplicate slug edge set collapse /
  NOT path-order #189 / NOT stewardship-schema sibling
  (lands closed #185/#172 leftover on tip; not schema #191; distinct from
  stewardship-badge lint #208 / path-filter/path-order #225 / Pass-2 leftover + md/link #220 /
  schema fourth-pass #216; lands closed #222/#215/#196 leftover after #225 tip)
- Wiki/mdlink leftover residual after #278 tip (markdown link residual harden;
  lands closed #281/#277 leftover; NOT lychee/blob-503 leftover #278 /
  NOT Pass-2 residual + templates #272 / NOT path-edges leftover #262 /
  NOT wiki/mdlink leftover #252 / NOT stewardship-schema leftover #258 /
  NOT path-filter/path-order leftover #244 / NOT md/link residual layouts #239):
  exact empty fragment in relative link / relative link must not include query string /
  relative link escapes repo / missing heading # /
  OK: relative markdown links resolve / raw.startswith("#")
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from stewardship_common import (  # noqa: E402
    ROOT,
    fail,
    has_dangerous_scheme,
    strip_fenced_code,
)

# Match CI markdown-lint / link-check exclusions where applicable.
SKIP_PARTS = {".git", "node_modules"}
SKIP_PREFIXES = (
    str(Path(".github") / "agents"),
)
# Align with markdown-lint exclusion for the long-form OWASP mapping.
SKIP_FILES = {
    "OWASP-AGENTIC.md",
}

# Captures markdown links and images: [text](target) / ![alt](target)
# Allow empty () so missing targets fail closed (markdown-link coverage).
MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(\s*([^)\s]*)(?:\s+\"[^\"]*\")?\s*\)")
# ATX headings for fragment checks (GitHub-ish slug approximation).
ATX_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

# Cap nested percent-decoding so %252e-style traversal cannot escape quietly.
_MAX_UNQUOTE_PASSES = 4


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if path.name in SKIP_FILES:
        return True
    if any(part in SKIP_PARTS for part in path.parts):
        return True
    return any(rel.startswith(prefix.replace("\\", "/")) for prefix in SKIP_PREFIXES)


def fully_unquote(raw: str) -> str:
    """Percent-decode until stable (capped) so nested %2e traversal fail-closes."""
    decoded = raw
    for _ in range(_MAX_UNQUOTE_PASSES):
        nxt = unquote(decoded)
        if nxt == decoded:
            break
        decoded = nxt
    return decoded


def github_slug(heading: str) -> str:
    """Approximate GitHub heading anchors for fragment checks.

    GitHub replaces each space with '-' (so "A & B" → "a--b" after '&' is
    stripped). Do not collapse whitespace runs before that mapping.
    """
    text = heading.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = text.strip().replace(" ", "-")
    return text


def headings_in(path: Path) -> set[str]:
    """Collect ATX heading slugs; duplicate headings collapse to one slug."""
    text = path.read_text(encoding="utf-8")
    # Duplicate slug edge: set collapse — two "## Section" → {"section"}.
    return {github_slug(match.group(2)) for match in ATX_HEADING_RE.finditer(text)}


def iter_markdown() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if p.is_file() and not should_skip(p))


def check_file(path: Path, errors: list[str]) -> None:
    # Ignore example targets inside fenced code (canonical snippets, publish scripts).
    text = strip_fenced_code(path.read_text(encoding="utf-8"))
    for match in MD_LINK_RE.finditer(text):
        raw = match.group(2).strip().strip("<>")
        if not raw or raw in {"#"}:
            fail(f"{path.relative_to(ROOT)}: empty relative link target", errors)
            continue

        dangerous = has_dangerous_scheme(raw)
        if dangerous:
            fail(
                f"{path.relative_to(ROOT)}: dangerous link scheme '{dangerous}' → {raw}",
                errors,
            )
            continue

        if raw.lower().startswith(("http://", "https://", "mailto:", "tel:")):
            if raw.lower().startswith("http://"):
                fail(
                    f"{path.relative_to(ROOT)}: insecure http:// link (use https://) → {raw}",
                    errors,
                )
            continue
        if raw.startswith("//"):
            fail(
                f"{path.relative_to(ROOT)}: protocol-relative link not allowed → {raw}",
                errors,
            )
            continue

        # Percent-encoded path traversal (e.g. %2e%2e/.. / %252e) must not escape.
        decoded = fully_unquote(raw)
        if "\0" in decoded:
            fail(f"{path.relative_to(ROOT)}: NUL in link target → {raw}", errors)
            continue

        # Ignore pure fragment self-links without a path (same-file anchors).
        if raw.startswith("#"):
            dest = path
            frag = raw[1:]
            if not frag.strip():
                fail(f"{path.relative_to(ROOT)}: empty relative link target", errors)
                continue
            slugs = headings_in(dest)
            normalized = frag.strip().lower()
            if normalized not in slugs and github_slug(frag) not in slugs:
                fail(
                    f"{path.relative_to(ROOT)}: missing heading #{frag} in "
                    f"{dest.relative_to(ROOT)}",
                    errors,
                )
            continue

        check_target = decoded if decoded != raw else raw
        has_hash = "#" in check_target
        target, frag = (
            (check_target.split("#", 1) + [""])[:2] if has_hash else (check_target, "")
        )
        # Fail-closed after #41: empty fragment on path# (e.g. README.md#) is not a
        # valid same-file / cross-file anchor — symmetric with bare `#`.
        if has_hash and not frag.strip():
            fail(
                f"{path.relative_to(ROOT)}: empty fragment in relative link → {raw}",
                errors,
            )
            continue
        # Relative paths must not carry query strings (offline resolve is path-only).
        if "?" in target:
            fail(
                f"{path.relative_to(ROOT)}: relative link must not include query string → {raw}",
                errors,
            )
            continue
        if not target:
            dest = path
        else:
            dest = (path.parent / target).resolve()
            try:
                dest.relative_to(ROOT.resolve())
            except ValueError:
                fail(
                    f"{path.relative_to(ROOT)}: relative link escapes repo: {raw}",
                    errors,
                )
                continue
            if not dest.exists():
                fail(
                    f"{path.relative_to(ROOT)}: broken relative link → {raw}",
                    errors,
                )
                continue

        if frag and dest.suffix.lower() == ".md" and dest.is_file():
            slugs = headings_in(dest)
            normalized = frag.strip().lower()
            if normalized not in slugs and github_slug(frag) not in slugs:
                fail(
                    f"{path.relative_to(ROOT)}: missing heading #{frag} in "
                    f"{dest.relative_to(ROOT)}",
                    errors,
                )


def main() -> int:
    errors: list[str] = []
    files = iter_markdown()
    if not files:
        print("FAIL: no markdown files found", file=sys.stderr)
        return 1

    for path in files:
        check_file(path, errors)

    if errors:
        print("Relative link check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: relative markdown links resolve ({len(files)} files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
