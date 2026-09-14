#!/usr/bin/env python3
"""Shared helpers for stewardship doc gates (no invent-product surface).

Fail-closed pins (live path after #46; second-pass after #65; third-pass after #104):
- SECRET_PATTERNS: ghp_/gho_/ghu_/ghs_/ghr_, github_pat_, PRIVATE KEY,
  sk-/rk-, api_key/secret/password/token, aws_secret_access_key, xox*,
  npm_, AIza
- SECRET_URL_HINTS: token=/access_token=/api_key=/apikey=/client_secret=
  plus ghp_/gho_/github_pat_ prefixes (URL-ish query + token prefixes)
- FORBIDDEN_BADGE_HINTS: invent-product / social chrome (coverage, codecov,
  coveralls, downloads, discord, twitter, x.com, stars, forks, followers,
  npm/, pypi/, producthunt, buymeacoffee, opencollective)
- DANGEROUS_LINK_SCHEMES: javascript:/data:/vbscript:/file:
- strip_fenced_code via FENCED_BLOCK_RE (``` or ~~~); has_dangerous_scheme;
  scan_secrets; markdown_files; load_workflow_text; fail
- Second-pass: ROOT parents[1] / FENCED_BLOCK_RE DOTALL / helper doc pins /
  scan_secrets needles / relative_to / strip().lower() / startswith /
  errors.append / password|passwd|token / OPENSSH+EC / Public docs /
  invent-product surface / social chrome / Link schemes / is_file+sorted /
  workflows path / return None
- Third-pass: future annotations / import re+Path / exact PRIVATE KEY+gh*
  +github_pat+sk|rk patterns / SECRET_PATTERNS tuple typing /
  FENCED_BLOCK_RE.sub / label or relative_to / pattern.search /
  lowered=text.lower / re.escape / https? URL-ish / ROOT.glob+found.update /
  set[Path] / workflows path join / for-loops over schemes+patterns+hints /
  Shared helpers doc / hint.endswith(=) / MEMORY dumps / str|None+list[Path] /
  FORBIDDEN_BADGE_HINTS head / SECRET_URL_HINTS ghp_+gho_+github_pat_ members
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Public docs must not ship secrets / private MEMORY dumps.
# Fail-closed after #46: live secret scan covers CI tokens + private keys.
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
DANGEROUS_LINK_SCHEMES = (
    "javascript:",
    "data:",
    "vbscript:",
    "file:",
)

# Fenced code: ``` or ~~~, optional language tag.
FENCED_BLOCK_RE = re.compile(r"(?:```|~~~).*?(?:```|~~~)", re.DOTALL)


def fail(msg: str, errors: list[str]) -> None:
    """Gate fail-closed helper: append msg to errors."""
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
    """Load .github/workflows/<name> text for CI pin checks."""
    path = ROOT / ".github" / "workflows" / name
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")
