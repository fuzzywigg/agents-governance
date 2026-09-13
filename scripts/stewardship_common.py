#!/usr/bin/env python3
"""Shared helpers for stewardship doc gates (no invent-product surface).

Fail-closed pins (live path after #46 / badge-standard gate after #48):
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
- verify_badge_standard_source_contract: REQUIRED_ORDER / MAX_BADGES=3 /
  EXPECTED_REPO / BADGE_LINE_RE / contiguous / shields license / invent refuse
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


def verify_badge_standard_source_contract(errors: list[str]) -> None:
    """Fail-close live badge-standard gate source pins (after #48).

    Lives in stewardship_common so seeded mutations of check_badge_standard.py
    cannot rewrite the contract needles themselves.
    """
    path = ROOT / "scripts" / "check_badge_standard.py"
    if not path.is_file():
        fail("Missing scripts/check_badge_standard.py (badge-standard gate)", errors)
        return
    text = path.read_text(encoding="utf-8")
    if "REQUIRED_ORDER" not in text:
        fail("check_badge_standard.py must declare REQUIRED_ORDER", errors)
    if 'REQUIRED_ORDER = ("Link Check", "Markdown Lint", "License")' not in text:
        fail(
            "check_badge_standard.py REQUIRED_ORDER must pin "
            "Link Check → Markdown Lint → License",
            errors,
        )
    if "MAX_BADGES = 3" not in text:
        fail("check_badge_standard.py must pin MAX_BADGES = 3", errors)
    if 'EXPECTED_REPO = "fuzzywigg/agents-governance"' not in text:
        fail(
            "check_badge_standard.py must pin EXPECTED_REPO "
            "fuzzywigg/agents-governance",
            errors,
        )
    if "BADGE_LINE_RE" not in text:
        fail("check_badge_standard.py must declare BADGE_LINE_RE", errors)
    if "REPO_FROM_GITHUB_RE" not in text:
        fail("check_badge_standard.py must declare REPO_FROM_GITHUB_RE", errors)
    if "REPO_FROM_SHIELDS_RE" not in text:
        fail("check_badge_standard.py must declare REPO_FROM_SHIELDS_RE", errors)
    if "extract_badge_row" not in text:
        fail("check_badge_standard.py must provide extract_badge_row", errors)
    if "check_badges" not in text:
        fail("check_badge_standard.py must provide check_badges", errors)
    if "contiguous" not in text.lower():
        fail(
            "check_badge_standard.py must require contiguous badge row "
            "(no blank lines between badges)",
            errors,
        )
    if "link-check.yml/badge.svg" not in text:
        fail(
            "check_badge_standard.py must pin link-check.yml/badge.svg image",
            errors,
        )
    if "markdown-lint.yml/badge.svg" not in text:
        fail(
            "check_badge_standard.py must pin markdown-lint.yml/badge.svg image",
            errors,
        )
    if "img.shields.io/github/license/" not in text:
        fail(
            "check_badge_standard.py must pin img.shields.io/github/license/ "
            "License image",
            errors,
        )
    if "for hint in FORBIDDEN_BADGE_HINTS" not in text:
        fail(
            "check_badge_standard.py must reject invent-product chrome via "
            "FORBIDDEN_BADGE_HINTS",
            errors,
        )
    if "for hint in SECRET_URL_HINTS" not in text:
        fail(
            "check_badge_standard.py must reject secret URLs via SECRET_URL_HINTS",
            errors,
        )
    if "scan_secrets(README" not in text and "scan_secrets(BADGE_STANDARD" not in text:
        fail(
            "check_badge_standard.py must scan README/docs via scan_secrets",
            errors,
        )
    if "Stewardship" not in text:
        fail(
            "check_badge_standard.py must refuse a Stewardship product/status badge",
            errors,
        )
    if "fourth" not in text.lower():
        fail(
            "check_badge_standard.py docs pin must refuse a fourth badge",
            errors,
        )
    if "invent" not in text.lower():
        fail(
            "check_badge_standard.py must retain invent-product edit policy pins",
            errors,
        )
    if "absolute https://" not in text:
        fail(
            "check_badge_standard.py must require absolute https:// "
            "workflow badge links",
            errors,
        )
    if "/LICENSE" not in text:
        fail(
            "check_badge_standard.py must require License badge link → LICENSE",
            errors,
        )
