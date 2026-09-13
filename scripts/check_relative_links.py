#!/usr/bin/env python3
"""Offline relative markdown link integrity (complements lychee external checks)."""

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

# External schemes allowed after dangerous/http checks (fail-closed empty payload).
SAFE_EXTERNAL_SCHEMES = ("https://", "mailto:", "tel:")


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if path.name in SKIP_FILES:
        return True
    if any(part in SKIP_PARTS for part in path.parts):
        return True
    return any(rel.startswith(prefix.replace("\\", "/")) for prefix in SKIP_PREFIXES)


def has_control_chars(text: str) -> bool:
    """True if text contains ASCII control characters (incl. NUL / CR / LF / TAB)."""
    return any(ord(ch) < 32 for ch in text)


def empty_scheme_payload(raw: str) -> str | None:
    """Return scheme name if mailto:/tel: has an empty payload; else None."""
    lowered = raw.strip().lower()
    for scheme in ("mailto:", "tel:"):
        if lowered.startswith(scheme):
            payload = raw.strip()[len(scheme) :].strip()
            if not payload:
                return scheme.rstrip(":")
            return None
    return None


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
    text = path.read_text(encoding="utf-8")
    return {github_slug(match.group(2)) for match in ATX_HEADING_RE.finditer(text)}


def fragment_resolves(frag: str, slugs: set[str]) -> bool:
    """True if fragment matches a heading slug (normalized or github_slug)."""
    if not frag or not frag.strip():
        return False
    normalized = frag.strip().lower()
    return normalized in slugs or github_slug(frag) in slugs


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
            empty = empty_scheme_payload(raw)
            if empty:
                fail(
                    f"{path.relative_to(ROOT)}: empty {empty}: link payload → {raw}",
                    errors,
                )
            continue
        if raw.startswith("//"):
            fail(
                f"{path.relative_to(ROOT)}: protocol-relative link not allowed → {raw}",
                errors,
            )
            continue

        # Percent-encoded path traversal (e.g. %2e%2e/..) must not escape the repo.
        decoded = unquote(raw)
        if "\0" in decoded or has_control_chars(decoded):
            fail(
                f"{path.relative_to(ROOT)}: control char / NUL in link target → {raw}",
                errors,
            )
            continue
        # Windows-style backslash paths must not sneak past POSIX resolve checks.
        if "\\" in decoded:
            fail(
                f"{path.relative_to(ROOT)}: backslash path separator not allowed → {raw}",
                errors,
            )
            continue

        # Ignore pure fragment self-links without a path (same-file anchors).
        # Use decoded so percent-encoded whitespace fragments fail closed.
        if raw.startswith("#"):
            dest = path
            frag = decoded[1:] if decoded.startswith("#") else raw[1:]
            if not frag.strip():
                fail(
                    f"{path.relative_to(ROOT)}: empty / whitespace-only fragment → {raw}",
                    errors,
                )
                continue
            slugs = headings_in(dest)
            if not fragment_resolves(frag, slugs):
                fail(
                    f"{path.relative_to(ROOT)}: missing heading #{frag} in "
                    f"{dest.relative_to(ROOT)}",
                    errors,
                )
            continue

        check_target = decoded if decoded != raw else raw
        target, frag = (
            (check_target.split("#", 1) + [""])[:2] if "#" in check_target else (check_target, "")
        )
        if frag and not frag.strip():
            fail(
                f"{path.relative_to(ROOT)}: empty / whitespace-only fragment → {raw}",
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
            if not fragment_resolves(frag, slugs):
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
