#!/usr/bin/env python3
"""Shared helpers for stewardship doc gates (no invent-product surface)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Public docs must not ship secrets / private MEMORY dumps.
SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(sk|rk)-[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)(?:password|passwd|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
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


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


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
            if re.search(rf"[?&]{re.escape(hint)}", lowered) or f"{hint}" in lowered and (
                "http://" in lowered or "https://" in lowered
            ):
                # Require the hint to appear inside a URL-looking substring.
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
