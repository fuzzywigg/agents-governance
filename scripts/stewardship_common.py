#!/usr/bin/env python3
"""Shared helpers for stewardship doc gates (no invent-product surface).

Fail-closed pins (live path after #46):
- SECRET_PATTERNS cover private keys / ghp|gho|ghu|ghs|ghr / github_pat_ /
  sk|rk- / api_key / aws_secret_access_key / xox[baprs]- / npm_ / AIza
- SECRET_URL_HINTS pin token= / access_token= / api_key= / apikey= /
  client_secret= / ghp_ / gho_ / github_pat_ (query hints only when endswith =)
- FORBIDDEN_BADGE_HINTS pin invent-product / social / registry chrome
  (coverage / codecov / discord / stars / npm/ / producthunt / …)
- DANGEROUS_LINK_SCHEMES pin javascript: / data: / vbscript: / file:
- FENCED_BLOCK_RE strips ``` and ~~~ fences before integrity scans
- Helpers: strip_fenced_code / has_dangerous_scheme / scan_secrets /
  markdown_files / load_workflow_text / fail (shared across gates)
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Public docs must not ship secrets / private MEMORY dumps.
# Fail-closed after #46: live secret patterns only (no invent-product surface).
SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(sk|rk)-[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)(?:password|passwd|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{20,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
)

# Fail-closed after #46: query-param hints end with "="; token prefixes do not.
SECRET_URL_HINTS = (
    "token=",
    "access_token=",
    "api_key=",
    "apikey=",
    "client_secret=",
    "ghp_",
    "gho_",
    "github_pat_",
)

# Invent-product / social chrome that must never appear as README badges.
# Fail-closed after #46: live forbidden badge chrome set (no fourth-badge spam).
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
    "producthunt",
    "buymeacoffee",
    "opencollective",
)

# Link schemes that must never appear as markdown targets in public docs.
# Fail-closed after #46: four live dangerous schemes only.
DANGEROUS_LINK_SCHEMES = (
    "javascript:",
    "data:",
    "vbscript:",
    "file:",
)

# Fenced code: ``` or ~~~, optional language tag.
# Fail-closed after #46: both fence styles stripped before link/secret scans.
FENCED_BLOCK_RE = re.compile(r"(?:```|~~~).*?(?:```|~~~)", re.DOTALL)


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks so example links do not fail integrity gates."""
    return FENCED_BLOCK_RE.sub("", text)


def has_dangerous_scheme(target: str) -> str | None:
    """Return the matched dangerous scheme prefix, or None."""
    lowered = target.strip().lower()
    for scheme in DANGEROUS_LINK_SCHEMES:
        if lowered.startswith(scheme):
            return scheme
    return None


def scan_secrets(path: Path, errors: list[str], *, label: str | None = None) -> None:
    """Append errors if path content matches forbidden secret-like patterns."""
    name = label or str(path.relative_to(ROOT))
    text = path.read_text(encoding="utf-8")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            fail(f"{name} matches forbidden secret-like pattern: {pattern.pattern}", errors)
    lowered = text.lower()
    for hint in SECRET_URL_HINTS:
        # Only flag URL-ish secret hints (query params / token prefixes), not prose.
        if hint.endswith("="):
            if re.search(rf"https?://[^\s)]*{re.escape(hint)}", lowered):
                fail(f"{name} contains secret-like URL hint '{hint}'", errors)
        elif hint in text:
            fail(f"{name} contains secret-like token hint '{hint}'", errors)


def markdown_files(*globs: str) -> list[Path]:
    """Collect markdown paths under ROOT for the given relative globs."""
    found: set[Path] = set()
    for pattern in globs:
        found.update(ROOT.glob(pattern))
    return sorted(p for p in found if p.is_file())


def load_workflow_text(name: str) -> str | None:
    path = ROOT / ".github" / "workflows" / name
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")
