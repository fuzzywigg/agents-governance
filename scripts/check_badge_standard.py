#!/usr/bin/env python3
"""Enforce docs/badge-standard.md against README.md (executable gate).

Fail-closed pins (live path after #48; second-pass after #61):
- REQUIRED_ORDER: Link Check → Markdown Lint → License (exactly MAX_BADGES = 3)
- EXPECTED_REPO: fuzzywigg/agents-governance
- REQUIRED_WORKFLOWS: link-check.yml / markdown-lint.yml / stewardship-checks.yml
- live badge row is Link Check → Markdown Lint → License
- Badge images https-only; link-check.yml/badge.svg + markdown-lint.yml/badge.svg
- License via img.shields.io/github/license/; contiguous row; no invent-product
- Quiet stewardship: no Stewardship product/status badge; no fourth badge
- Second-pass: path constants / exact REQUIRED_ORDER+EXPECTED_REPO assigns /
  actions/workflows/*.yml/badge.svg / fail needles / LICENSE link / FAILED+OK

Fail-closed actionlint-style pins (live path after #75; second-pass after #83/#86; third-pass after #94):
- top-level name: / jobs.*.runs-on / jobs.*.steps / timeout-minutes
- no pull_request_target / no permissions: write-all / no contents: write
- no id-token: write / actions must be @-pinned (not main|master|latest)
- docker:// uses skipped; unpinned uses rejected
- Second-pass: exact name/uses regexes / write-all+contents+id-token regexes /
  docker startswith / @ not in uses / rsplit / group(1).strip() /
  fail needles / least-privilege+OIDC+majors comments / REQUIRED_WORKFLOWS loop
- Third-pass after #94: concurrency:+cancel-in-progress: / permissions: present /
  reject actions|packages|pull-requests: write / finditer uses / docker continue /
  rsplit[-1] / third-pass docstring
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
    SECRET_URL_HINTS,
    fail,
    load_workflow_text,
    scan_secrets,
)

README = ROOT / "README.md"
LICENSE = ROOT / "LICENSE"
BADGE_STANDARD = ROOT / "docs" / "badge-standard.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
AGENTS = ROOT / "AGENTS.md"
LYCHEEIGNORE = ROOT / ".lycheeignore"
MARKDOWNLINT_CONFIG = ROOT / ".markdownlint.json"
WORKFLOWS = ROOT / ".github" / "workflows"
RELATIVE_LINK_GATE = ROOT / "scripts" / "check_relative_links.py"
WIKI_OUTLINE_GATE = ROOT / "scripts" / "check_wiki_outline.py"
SCHEMA_GATE = ROOT / "scripts" / "check_stewardship_schema.py"
COMMON_GATE = ROOT / "scripts" / "stewardship_common.py"
RUN_STEWARDSHIP = ROOT / "scripts" / "run_stewardship_checks.sh"
BADGE_GATE = Path(__file__).resolve()

REQUIRED_ORDER = ("Link Check", "Markdown Lint", "License")
MAX_BADGES = 3
EXPECTED_REPO = "fuzzywigg/agents-governance"
REQUIRED_WORKFLOWS = (
    "link-check.yml",
    "markdown-lint.yml",
    "stewardship-checks.yml",
)

BADGE_LINE_RE = re.compile(
    r"^\[!\[(?P<label>[^\]]+)\]\((?P<img>[^)]+)\)\]\((?P<link>[^)]+)\)\s*$"
)
REPO_FROM_GITHUB_RE = re.compile(
    r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/\s?#]+)",
    re.IGNORECASE,
)
REPO_FROM_SHIELDS_RE = re.compile(
    r"https://img\.shields\.io/github/(?:license|actions)/"
    r"(?P<owner>[^/]+)/(?P<repo>[^/\s?#]+)",
    re.IGNORECASE,
)


def extract_badge_row(text: str) -> tuple[list[re.Match[str]], list[str]]:
    """Return consecutive badge lines immediately after the first H1."""
    errors: list[str] = []
    lines = text.splitlines()
    h1_idx = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if h1_idx is None:
        fail("README.md missing H1 (# title)", errors)
        return [], errors

    badges: list[re.Match[str]] = []
    i = h1_idx + 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    while i < len(lines):
        match = BADGE_LINE_RE.match(lines[i])
        if not match:
            break
        badges.append(match)
        i += 1
        # Strict row: no blank lines between badges.
        if i < len(lines) and lines[i].strip() == "":
            j = i
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and BADGE_LINE_RE.match(lines[j]):
                fail(
                    "Badge row must be contiguous (no blank lines between badge lines)",
                    errors,
                )
            break
    if not badges:
        fail(
            "README.md must place the required badge row immediately under the H1 "
            "(after optional blank lines)",
            errors,
        )
    return badges, errors


def check_workflows_and_license(errors: list[str]) -> None:
    for name in REQUIRED_WORKFLOWS:
        path = WORKFLOWS / name
        if not path.is_file():
            fail(f"Missing workflow required by stewardship CI: {path.relative_to(ROOT)}", errors)
    if not LICENSE.is_file():
        fail("Missing LICENSE (required for License badge)", errors)
    if not BADGE_STANDARD.is_file():
        fail("Missing docs/badge-standard.md", errors)
    if not LYCHEEIGNORE.is_file():
        fail("Missing .lycheeignore (lychee link-check excludes)", errors)
    if not MARKDOWNLINT_CONFIG.is_file():
        fail("Missing .markdownlint.json (markdown-lint config)", errors)
    else:
        # Live markdown-lint config pins MD013 line length (docs stay scannable).
        md_cfg = MARKDOWNLINT_CONFIG.read_text(encoding="utf-8")
        if "MD013" not in md_cfg:
            fail(
                ".markdownlint.json must configure MD013 (line length) for docs lint",
                errors,
            )
        # Fail-closed: MD013 must set line_length (live path after #33).
        if "line_length" not in md_cfg:
            fail(
                ".markdownlint.json MD013 must set line_length for docs lint",
                errors,
            )
        # Fail-closed after #36: live MD013 line_length pin is 200 (docs stay scannable).
        if not re.search(r'"line_length"\s*:\s*200\b', md_cfg):
            fail(
                ".markdownlint.json MD013 must pin line_length: 200 for docs lint",
                errors,
            )
        # Fail-closed after #34: live config pins MD024 siblings_only (heading dupes).
        if "MD024" not in md_cfg:
            fail(
                ".markdownlint.json must configure MD024 (siblings_only) for docs lint",
                errors,
            )
        # Fail-closed after #35: MD024 must set siblings_only (symmetric with line_length).
        if "siblings_only" not in md_cfg:
            fail(
                ".markdownlint.json MD024 must set siblings_only for docs lint",
                errors,
            )
        # Fail-closed after #36: MD024 siblings_only must be true (not false / bare).
        if not re.search(r'"siblings_only"\s*:\s*true\b', md_cfg):
            fail(
                ".markdownlint.json MD024 must set siblings_only: true for docs lint",
                errors,
            )
        # Fail-closed after #37: live config enables markdownlint default rule set.
        if not re.search(r'"default"\s*:\s*true\b', md_cfg):
            fail(
                ".markdownlint.json must set default: true for docs lint",
                errors,
            )
        # Fail-closed after #38: live config disables MD033 (inline HTML allowed in docs).
        if not re.search(r'"MD033"\s*:\s*false\b', md_cfg):
            fail(
                ".markdownlint.json must set MD033: false for docs lint",
                errors,
            )
        # Fail-closed after #38: live config disables MD041 (first-line H1 not required).
        if not re.search(r'"MD041"\s*:\s*false\b', md_cfg):
            fail(
                ".markdownlint.json must set MD041: false for docs lint",
                errors,
            )
        # Fail-closed after #38: live config disables MD060 (table column style).
        if not re.search(r'"MD060"\s*:\s*false\b', md_cfg):
            fail(
                ".markdownlint.json must set MD060: false for docs lint",
                errors,
            )
        # Fail-closed after #100: exact live MD013 object (docs-lint slice).
        if '"MD013": { "line_length": 200 }' not in md_cfg:
            fail(
                '.markdownlint.json must pin "MD013": { "line_length": 200 }',
                errors,
            )
        # Fail-closed after #100: exact live MD024 object (docs-lint slice).
        if '"MD024": { "siblings_only": true }' not in md_cfg:
            fail(
                '.markdownlint.json must pin "MD024": { "siblings_only": true }',
                errors,
            )


def check_lycheeignore(errors: list[str]) -> None:
    r"""Keep flaky badge CDN out of lychee; license badge stays in stewardship.

    Live fail-closed pins after #100 (docs-lint slice; not CI workflow spam):
    escaped img\.shields\.io; modelcontextprotocol.io + linuxfoundation.org
    live excludes; stewardship/license-badge commentary; reject https://* /
    http://* / bare *; not wiki / relative pin spam.
    """
    if not LYCHEEIGNORE.is_file():
        return
    text = LYCHEEIGNORE.read_text(encoding="utf-8")
    # Accept literal or regex-escaped host form from #26.
    if "img.shields.io" not in text and r"img\.shields\.io" not in text:
        fail(
            ".lycheeignore must exclude flaky img.shields.io badge CDN "
            "(license badge presence remains stewardship-enforced)",
            errors,
        )
    # Fail-closed after #100: live tree pins the regex-escaped shields form.
    if r"img\.shields\.io" not in text:
        fail(
            r".lycheeignore must pin escaped img\.shields\.io exclude "
            "(live docs-lint path)",
            errors,
        )
    # Fail-closed after #100: live excludes for known lychee false-positives.
    if "modelcontextprotocol.io" not in text:
        fail(
            ".lycheeignore must exclude modelcontextprotocol.io "
            "(live lychee false-positive path)",
            errors,
        )
    if "linuxfoundation.org" not in text:
        fail(
            ".lycheeignore must exclude linuxfoundation.org "
            "(live lychee false-positive path)",
            errors,
        )
    # Fail-closed after #100: commentary must keep stewardship license-badge posture.
    lowered = text.lower()
    if "stewardship" not in lowered and "license badge" not in lowered:
        fail(
            ".lycheeignore must note stewardship/license-badge enforcement "
            "(CDN exclude is not a missing License badge)",
            errors,
        )
    # Fail-closed after #100: live commentary keeps known false-positive rationale.
    if "308" not in text:
        fail(
            ".lycheeignore must note modelcontextprotocol.io 308 redirect rationale",
            errors,
        )
    if "103" not in text:
        fail(
            ".lycheeignore must note linuxfoundation.org 103 early-hints rationale",
            errors,
        )
    # Do not quietly drop fail-closed posture by ignoring everything.
    if text.strip() == "*" or "https://*" in text or "http://*" in text:
        fail(
            ".lycheeignore must not exclude all http(s) targets "
            "(https://* / http://* / bare *)",
            errors,
        )

def check_actionlint_style(errors: list[str]) -> None:
    """Static actionlint-like checks on existing workflow paths only.

    Live fail-closed pins after #75 (not badge-row / relative-pin spam):
    top-level name: / jobs.*.runs-on / jobs.*.steps / timeout-minutes;
    reject pull_request_target / permissions: write-all / contents: write /
    id-token: write; @-pin actions (not main|master|latest); skip docker://;
    reject unpinned action uses.
    Second-pass after #83/#86: exact name/uses regexes /
    write-all+contents+id-token regexes / docker startswith /
    @ not in uses / rsplit / group(1).strip() / fail needles /
    least-privilege+OIDC+majors comments / REQUIRED_WORKFLOWS loop.
    Third-pass after #94: concurrency:+cancel-in-progress: / permissions: present /
    reject actions|packages|pull-requests: write / finditer uses /
    docker continue / rsplit[-1] / third-pass docstring.
    """
    for name in REQUIRED_WORKFLOWS:
        text = load_workflow_text(name)
        if text is None:
            continue
        if not re.search(r"(?m)^name:\s*\S", text):
            fail(f"{name}: actionlint-style requires top-level name:", errors)
        if "runs-on:" not in text:
            fail(f"{name}: actionlint-style requires jobs.*.runs-on", errors)
        if "steps:" not in text:
            fail(f"{name}: actionlint-style requires jobs.*.steps", errors)
        if "pull_request_target:" in text:
            fail(f"{name}: must not use pull_request_target (actionlint harden)", errors)
        if re.search(r"(?m)^\s*permissions:\s*write-all\s*$", text):
            fail(f"{name}: must not set permissions: write-all", errors)
        # Prefer least privilege: contents: read already required; reject write on contents.
        if re.search(r"(?m)^\s*contents:\s*write\s*$", text):
            fail(f"{name}: contents: write is forbidden on stewardship workflows", errors)
        # Fail-closed after #75: OIDC write not needed for docs CI paths.
        if re.search(r"(?m)^\s*id-token:\s*write\s*$", text):
            fail(f"{name}: id-token: write is forbidden on stewardship workflows", errors)
        # Third-pass after #94: reversible CI concurrency cancel pins.
        if "concurrency:" not in text:
            fail(f"{name}: actionlint-style requires concurrency:", errors)
        if "cancel-in-progress:" not in text:
            fail(f"{name}: actionlint-style requires cancel-in-progress:", errors)
        # Third-pass after #94: permissions block must be present (least privilege).
        if "permissions:" not in text:
            fail(f"{name}: actionlint-style requires permissions:", errors)
        # Third-pass after #94: reject extra write scopes on docs CI paths.
        if re.search(r"(?m)^\s*actions:\s*write\s*$", text):
            fail(f"{name}: actions: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*packages:\s*write\s*$", text):
            fail(f"{name}: packages: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*pull-requests:\s*write\s*$", text):
            fail(f"{name}: pull-requests: write is forbidden on stewardship workflows", errors)
        # Pin GitHub Actions majors (actionlint / supply-chain hygiene).
        for match in re.finditer(r"(?m)^\s*-\s*uses:\s*([^\s#]+)", text):
            uses = match.group(1).strip()
            if uses.startswith("docker://"):
                continue
            if "@" not in uses:
                fail(f"{name}: unpinned action uses: {uses}", errors)
                continue
            ref = uses.rsplit("@", 1)[-1]
            if ref in {"main", "master", "latest"}:
                fail(f"{name}: action must not float on @{ref}: {uses}", errors)
        # jobs must declare timeout (already checked globally; keep local needle).
        if "timeout-minutes:" not in text:
            fail(f"{name}: actionlint-style requires timeout-minutes on jobs", errors)


def check_workflow_hardening(errors: list[str]) -> None:
    """Harden existing lint/link/stewardship workflows (triggers, perms, concurrency)."""
    for name in REQUIRED_WORKFLOWS:
        text = load_workflow_text(name)
        if text is None:
            continue
        if "pull_request:" not in text:
            fail(f"{name} must run on pull_request", errors)
        if "workflow_dispatch:" not in text:
            fail(f"{name} must allow workflow_dispatch (manual re-run)", errors)
        if "permissions:" not in text or "contents: read" not in text:
            fail(f"{name} must set permissions.contents: read", errors)
        if "concurrency:" not in text:
            fail(f"{name} must declare a concurrency group", errors)
        if "cancel-in-progress:" not in text:
            fail(
                f"{name} concurrency must set cancel-in-progress "
                "(supersede stale runs on the same ref)",
                errors,
            )
        # Fail-closed: cancel-in-progress must be true (not false / empty).
        if not re.search(r"(?m)^\s*cancel-in-progress:\s*true\s*$", text):
            fail(
                f"{name} concurrency must set cancel-in-progress: true",
                errors,
            )
        if "timeout-minutes:" not in text:
            fail(f"{name} jobs must set timeout-minutes", errors)
        if "schedule:" not in text:
            fail(f"{name} must include a weekly schedule drift catch", errors)

    link = load_workflow_text("link-check.yml") or ""
    if "lychee" not in link.lower():
        fail("link-check.yml must invoke lychee", errors)
    # Live path after #32: lychee runs via lychee-action (not a bare CLI invent).
    if "lychee-action" not in link.lower():
        fail("link-check.yml must invoke lychee-action on the existing path", errors)
    # Fail-closed after #33: org-qualified lycheeverse/lychee-action (existing path).
    if "lycheeverse/lychee-action" not in link.lower():
        fail(
            "link-check.yml must invoke lycheeverse/lychee-action on the existing path",
            errors,
        )
    # Fail-closed after #34: live lychee args pass --github-token (auth path).
    if "--github-token" not in link:
        fail(
            "link-check.yml must pass lychee --github-token on the existing path",
            errors,
        )
    # Fail-closed after #35: lychee-action with: token: (secrets.GITHUB_TOKEN path).
    if not re.search(r"(?m)^\s*token:\s*\S", link):
        fail(
            "link-check.yml must pass lychee-action with: token: on the existing path",
            errors,
        )
    # Fail-closed: link-check must checkout before lychee (symmetric with stewardship).
    if "actions/checkout" not in link:
        fail(
            "link-check.yml must checkout the repository (actions/checkout)",
            errors,
        )
    # Fail-closed after #39: live link-check checkout pin is @v7.
    if not re.search(r"(?i)actions/checkout@v7\b", link):
        fail(
            "link-check.yml must pin actions/checkout@v7",
            errors,
        )
    # Fail-closed after #39: live lychee-action major pin is @v2.
    if not re.search(r"(?i)lycheeverse/lychee-action@v2\b", link):
        fail(
            "link-check.yml must pin lycheeverse/lychee-action@v2",
            errors,
        )
    # Fail-closed after #39: live link-check job timeout pin is 20.
    if not re.search(r"(?m)^\s*timeout-minutes:\s*20\s*$", link):
        fail(
            "link-check.yml must pin timeout-minutes: 20",
            errors,
        )
    # Fail-closed after #39: live weekly cron is 0 6 * * 1 (Monday 06:00 UTC).
    if 'cron: "0 6 * * 1"' not in link and "cron: '0 6 * * 1'" not in link:
        fail(
            'link-check.yml must pin weekly cron: "0 6 * * 1"',
            errors,
        )
    # Fail-closed after #39: live runner is ubuntu-latest.
    if "ubuntu-latest" not in link:
        fail(
            "link-check.yml must run on ubuntu-latest",
            errors,
        )
    if '"**/*.md"' not in link and "'**/*.md'" not in link and "**/*.md" not in link:
        fail(
            "link-check.yml must scan **/*.md markdown sources (paths or lychee args)",
            errors,
        )
    if "--exclude-path" not in link and "exclude-path" not in link:
        fail("link-check.yml must exclude .github/agents (or equivalent path)", errors)
    if ".github/agents" not in link:
        fail(
            "link-check.yml exclude-path must target .github/agents "
            "(agent prompt files stay out of lychee)",
            errors,
        )
    if "--max-concurrency" not in link:
        fail("link-check.yml must cap lychee --max-concurrency", errors)
    # Fail-closed after #37: live lychee concurrency pin is 8.
    if not re.search(r"--max-concurrency\s+8\b", link):
        fail(
            "link-check.yml must pin lychee --max-concurrency 8",
            errors,
        )
    if "--timeout" not in link:
        fail("link-check.yml must set lychee --timeout", errors)
    # Fail-closed after #37: live lychee timeout pin is 20.
    if not re.search(r"--timeout\s+20\b", link):
        fail(
            "link-check.yml must pin lychee --timeout 20",
            errors,
        )
    if "--max-retries" not in link:
        fail("link-check.yml must set lychee --max-retries", errors)
    # Fail-closed after #37: live lychee max-retries pin is 3.
    if not re.search(r"--max-retries\s+3\b", link):
        fail(
            "link-check.yml must pin lychee --max-retries 3",
            errors,
        )
    if "fail: true" not in link and "fail:true" not in link:
        fail("link-check.yml must set fail: true so broken links fail the job", errors)
    if "--exclude-loopback" not in link and "exclude-loopback" not in link:
        fail("link-check.yml must exclude loopback targets", errors)
    # Live link-check contract: quiet CI logs + verbose failure detail (after #31).
    if "--no-progress" not in link:
        fail("link-check.yml must set lychee --no-progress", errors)
    if "--verbose" not in link:
        fail("link-check.yml must set lychee --verbose", errors)
    # Private-repo / rate-limit auth for lychee (existing path from # link-check harden).
    if "GITHUB_TOKEN" not in link:
        fail(
            "link-check.yml must pass GITHUB_TOKEN for private-repo / GitHub auth",
            errors,
        )

    lint = load_workflow_text("markdown-lint.yml") or ""
    if "markdownlint" not in lint.lower():
        fail("markdown-lint.yml must invoke markdownlint", errors)
    # Fail-closed after #33: live path uses markdownlint-cli2-action (not a bare invent).
    if "markdownlint-cli2-action" not in lint.lower():
        fail(
            "markdown-lint.yml must invoke markdownlint-cli2-action on the existing path",
            errors,
        )
    # Fail-closed after #34: org-qualified DavidAnson/markdownlint-cli2-action.
    if "davidanson/markdownlint-cli2-action" not in lint.lower():
        fail(
            "markdown-lint.yml must invoke DavidAnson/markdownlint-cli2-action "
            "on the existing path",
            errors,
        )
    # Fail-closed after #38: live markdownlint-cli2-action pin is @v24.
    if not re.search(r"(?i)davidanson/markdownlint-cli2-action@v24\b", lint):
        fail(
            "markdown-lint.yml must pin DavidAnson/markdownlint-cli2-action@v24",
            errors,
        )
    # Fail-closed: markdown-lint must checkout before lint (symmetric with stewardship).
    if "actions/checkout" not in lint:
        fail(
            "markdown-lint.yml must checkout the repository (actions/checkout)",
            errors,
        )
    # Fail-closed after #39: live markdown-lint checkout pin is @v7.
    if not re.search(r"(?i)actions/checkout@v7\b", lint):
        fail(
            "markdown-lint.yml must pin actions/checkout@v7",
            errors,
        )
    # Fail-closed after #39: live markdown-lint job timeout pin is 10.
    if not re.search(r"(?m)^\s*timeout-minutes:\s*10\s*$", lint):
        fail(
            "markdown-lint.yml must pin timeout-minutes: 10",
            errors,
        )
    # Fail-closed after #39: live weekly cron is 30 6 * * 1 (Monday 06:30 UTC).
    if 'cron: "30 6 * * 1"' not in lint and "cron: '30 6 * * 1'" not in lint:
        fail(
            'markdown-lint.yml must pin weekly cron: "30 6 * * 1"',
            errors,
        )
    # Fail-closed after #39: live runner is ubuntu-latest.
    if "ubuntu-latest" not in lint:
        fail(
            "markdown-lint.yml must run on ubuntu-latest",
            errors,
        )
    if '"**/*.md"' not in lint and "'**/*.md'" not in lint and "**/*.md" not in lint:
        fail(
            "markdown-lint.yml must scan **/*.md markdown sources (globs or paths)",
            errors,
        )
    if "OWASP-AGENTIC.md" not in lint:
        fail("markdown-lint.yml must exclude OWASP-AGENTIC.md", errors)
    if ".markdownlint.json" not in lint:
        fail("markdown-lint.yml must use .markdownlint.json config", errors)
    if ".github/agents" not in lint:
        fail("markdown-lint.yml must exclude .github/agents/**", errors)

    stew = load_workflow_text("stewardship-checks.yml") or ""
    if "run_stewardship_checks.sh" not in stew:
        fail("stewardship-checks.yml must run scripts/run_stewardship_checks.sh", errors)
    if "test_stewardship_gates.py" not in stew:
        fail("stewardship-checks.yml must run scripts/test_stewardship_gates.py", errors)
    # Fail-closed: stewardship must checkout the tree before running gates (live path).
    if "actions/checkout" not in stew:
        fail(
            "stewardship-checks.yml must checkout the repository (actions/checkout)",
            errors,
        )
    # Fail-closed after #39: live stewardship checkout pin is @v7.
    if not re.search(r"(?i)actions/checkout@v7\b", stew):
        fail(
            "stewardship-checks.yml must pin actions/checkout@v7",
            errors,
        )
    # Fail-closed after #39: live stewardship job timeout pin is 15.
    if not re.search(r"(?m)^\s*timeout-minutes:\s*15\s*$", stew):
        fail(
            "stewardship-checks.yml must pin timeout-minutes: 15",
            errors,
        )
    # Fail-closed after #39: live weekly cron is 15 6 * * 1 (Monday 06:15 UTC).
    if 'cron: "15 6 * * 1"' not in stew and "cron: '15 6 * * 1'" not in stew:
        fail(
            'stewardship-checks.yml must pin weekly cron: "15 6 * * 1"',
            errors,
        )
    # Fail-closed after #39: live runner is ubuntu-latest.
    if "ubuntu-latest" not in stew:
        fail(
            "stewardship-checks.yml must run on ubuntu-latest",
            errors,
        )
    if "setup-python" not in stew.lower() and "actions/setup-python" not in stew:
        fail("stewardship-checks.yml must set up Python for gate scripts", errors)
    # Fail-closed after #38: live setup-python pin is @v5.
    if not re.search(r"(?i)actions/setup-python@v5\b", stew):
        fail(
            "stewardship-checks.yml must pin actions/setup-python@v5",
            errors,
        )
    # Fail-closed: pin the Python minor used by gate scripts (live path after #30).
    if "python-version" not in stew:
        fail(
            "stewardship-checks.yml must set python-version for gate scripts",
            errors,
        )
    if "3.12" not in stew:
        fail(
            "stewardship-checks.yml must pin Python 3.12 for gate scripts",
            errors,
        )
    if "pyyaml" not in stew.lower():
        fail("stewardship-checks.yml must install PyYAML for schema parsing", errors)
    # Fail-closed after #33: live path installs PyYAML via pip (existing install step).
    if "pip install" not in stew.lower() and "pip3 install" not in stew.lower():
        fail(
            "stewardship-checks.yml must pip install PyYAML for schema parsing",
            errors,
        )
    # Fail-closed after #39: live pip install uses --quiet (CI noise control).
    if "--quiet" not in stew.lower() and " -q " not in stew.lower():
        fail(
            "stewardship-checks.yml must pip install --quiet PyYAML",
            errors,
        )
    # Fail-closed after #34: actionlint comes from rhysd download script (existing path).
    if "download-actionlint.bash" not in stew.lower():
        fail(
            "stewardship-checks.yml must download actionlint via download-actionlint.bash",
            errors,
        )
    # Fail-closed after #35: org-qualified rhysd/actionlint download (existing path).
    if "rhysd/actionlint" not in stew.lower():
        fail(
            "stewardship-checks.yml must download actionlint from rhysd/actionlint",
            errors,
        )
    # Fail-closed after #35: live download uses curl (fsSL raw.githubusercontent path).
    if "curl" not in stew.lower():
        fail(
            "stewardship-checks.yml must curl the actionlint download script",
            errors,
        )
    # Fail-closed after #36: live curl uses -fsSL (fail/silent/show-error/location).
    if "fssl" not in stew.lower():
        fail(
            "stewardship-checks.yml must curl -fsSL the actionlint download script",
            errors,
        )
    # Fail-closed after #36: live download host is raw.githubusercontent.com.
    if "raw.githubusercontent.com" not in stew.lower():
        fail(
            "stewardship-checks.yml must download actionlint from raw.githubusercontent.com",
            errors,
        )
    # Fail-closed after #37: live download URL pins /v1.7.7/ path (not floating tip).
    if "/v1.7.7/" not in stew:
        fail(
            "stewardship-checks.yml must pin actionlint download path /v1.7.7/",
            errors,
        )
    # Fail-closed after #37: live run uses get_actionlint.outputs.executable.
    if "get_actionlint.outputs.executable" not in stew:
        fail(
            "stewardship-checks.yml must run actionlint via get_actionlint.outputs.executable",
            errors,
        )
    # Fail-closed after #38: live download step sets id: get_actionlint.
    if not re.search(r"(?m)^\s*(?:-\s*)?id:\s*get_actionlint\s*$", stew):
        fail(
            "stewardship-checks.yml must set id: get_actionlint on the download step",
            errors,
        )
    # Fail-closed after #39: live download step pins shell: bash.
    if not re.search(r"(?m)^\s*shell:\s*bash\s*$", stew):
        fail(
            "stewardship-checks.yml must set shell: bash on the actionlint download step",
            errors,
        )
    if "actionlint" not in stew.lower():
        fail(
            "stewardship-checks.yml must run actionlint on existing workflow paths",
            errors,
        )
    # Fail-closed after #39: live actionlint run passes -color (CI log readability).
    if not re.search(
        r"get_actionlint\.outputs\.executable[^\\n]*-color\b",
        stew,
    ):
        fail(
            "stewardship-checks.yml must run actionlint with -color",
            errors,
        )
    # Pin actionlint major.minor.patch in the download / run step (supply-chain).
    if "1.7.7" not in stew:
        fail(
            "stewardship-checks.yml must pin actionlint 1.7.7 on existing workflow paths",
            errors,
        )
    # Explicitly lint only the three existing workflow paths (no invent workflows).
    for wf_name in REQUIRED_WORKFLOWS:
        if wf_name not in stew:
            fail(
                "stewardship-checks.yml actionlint must target existing "
                f"workflow path {wf_name}",
                errors,
            )

    # Link-check path filter / lycheeignore stay wired after shields harden (#26).
    if ".lycheeignore" not in link:
        fail(
            "link-check.yml must reference .lycheeignore (paths filter or args) "
            "so shields CDN excludes stay wired",
            errors,
        )
    # Fail-closed after #72: CI workflow second-pass helper / constant / needle pins
    # (CI workflow slice only; not badge / wiki / relative / schema / common spam).
    if "name: Link Check" not in link:
        fail(
            'link-check.yml must keep workflow name: Link Check',
            errors,
        )
    if "name: Markdown Lint" not in lint:
        fail(
            'markdown-lint.yml must keep workflow name: Markdown Lint',
            errors,
        )
    if "name: Stewardship Checks" not in stew:
        fail(
            'stewardship-checks.yml must keep workflow name: Stewardship Checks',
            errors,
        )
    if 'branches: ["**"]' not in link and "branches: ['**']" not in link:
        fail(
            'link-check.yml must push on branches: ["**"]',
            errors,
        )
    if 'branches: ["**"]' not in lint and "branches: ['**']" not in lint:
        fail(
            'markdown-lint.yml must push on branches: ["**"]',
            errors,
        )
    if 'branches: ["**"]' not in stew and "branches: ['**']" not in stew:
        fail(
            'stewardship-checks.yml must push on branches: ["**"]',
            errors,
        )
    if "link-check-" not in link:
        fail(
            "link-check.yml concurrency group must be prefixed link-check-",
            errors,
        )
    if "markdown-lint-" not in lint:
        fail(
            "markdown-lint.yml concurrency group must be prefixed markdown-lint-",
            errors,
        )
    if "stewardship-checks-" not in stew:
        fail(
            "stewardship-checks.yml concurrency group must be prefixed "
            "stewardship-checks-",
            errors,
        )
    if "github.workflow" not in link or "github.ref" not in link:
        fail(
            "link-check.yml concurrency must include github.workflow and github.ref",
            errors,
        )
    if "github.workflow" not in lint or "github.ref" not in lint:
        fail(
            "markdown-lint.yml concurrency must include github.workflow and github.ref",
            errors,
        )
    if "github.workflow" not in stew or "github.ref" not in stew:
        fail(
            "stewardship-checks.yml concurrency must include github.workflow "
            "and github.ref",
            errors,
        )
    if not re.search(r"(?m)^\s*link-check:\s*$", link):
        fail(
            "link-check.yml must declare job id link-check:",
            errors,
        )
    if not re.search(r"(?m)^\s*lint:\s*$", lint):
        fail(
            "markdown-lint.yml must declare job id lint:",
            errors,
        )
    if not re.search(r"(?m)^\s*stewardship:\s*$", stew):
        fail(
            "stewardship-checks.yml must declare job id stewardship:",
            errors,
        )
    if ".github/workflows/link-check.yml" not in link:
        fail(
            "link-check.yml paths filter must include "
            ".github/workflows/link-check.yml",
            errors,
        )
    if ".github/workflows/markdown-lint.yml" not in lint:
        fail(
            "markdown-lint.yml paths filter must include "
            ".github/workflows/markdown-lint.yml",
            errors,
        )
    if "scripts/**" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include scripts/**",
            errors,
        )
    if "docs/**" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include docs/**",
            errors,
        )
    if '"README.md"' not in stew and "'README.md'" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include README.md",
            errors,
        )
    if "secrets.GITHUB_TOKEN" not in link:
        fail(
            "link-check.yml must reference secrets.GITHUB_TOKEN",
            errors,
        )
    if 'python-version: "3.12"' not in stew and "python-version: '3.12'" not in stew:
        fail(
            'stewardship-checks.yml must pin python-version: "3.12"',
            errors,
        )
    if "pip install --quiet pyyaml" not in stew.lower():
        fail(
            "stewardship-checks.yml must pip install --quiet pyyaml",
            errors,
        )
    if "bash scripts/run_stewardship_checks.sh" not in stew:
        fail(
            "stewardship-checks.yml must run bash scripts/run_stewardship_checks.sh",
            errors,
        )
    if "python3 scripts/test_stewardship_gates.py" not in stew:
        fail(
            "stewardship-checks.yml must run python3 scripts/test_stewardship_gates.py",
            errors,
        )
    if 'config: ".markdownlint.json"' not in lint and "config: '.markdownlint.json'" not in lint:
        fail(
            'markdown-lint.yml must set config: ".markdownlint.json"',
            errors,
        )
    if "!.github/agents/**" not in lint:
        fail(
            "markdown-lint.yml globs must exclude !.github/agents/**",
            errors,
        )
    if "!OWASP-AGENTIC.md" not in lint:
        fail(
            "markdown-lint.yml globs must exclude !OWASP-AGENTIC.md",
            errors,
        )
    # actionlint must list all three workflow paths in one run step.
    if (
        ".github/workflows/link-check.yml" not in stew
        or ".github/workflows/markdown-lint.yml" not in stew
        or ".github/workflows/stewardship-checks.yml" not in stew
    ):
        fail(
            "stewardship-checks.yml actionlint must list all three "
            ".github/workflows/*.yml paths",
            errors,
        )
    if "download-actionlint.bash) 1.7.7" not in stew and "download-actionlint.bash ) 1.7.7" not in stew:
        fail(
            "stewardship-checks.yml must pass actionlint version 1.7.7 to download script",
            errors,
        )


def check_badge_standard_doc(errors: list[str]) -> None:
    """Ensure docs/badge-standard.md still documents the same required order."""
    text = BADGE_STANDARD.read_text(encoding="utf-8")
    for label in REQUIRED_ORDER:
        if f"| {label} |" not in text and f"| {label}" not in text:
            if label not in text:
                fail(f"docs/badge-standard.md must document required badge '{label}'", errors)
    if "link-check.yml/badge.svg" not in text:
        fail("docs/badge-standard.md canonical snippet missing link-check badge.svg", errors)
    if "markdown-lint.yml/badge.svg" not in text:
        fail("docs/badge-standard.md canonical snippet missing markdown-lint badge.svg", errors)
    if "img.shields.io/github/license/" not in text:
        fail("docs/badge-standard.md canonical snippet missing shields license image", errors)
    lowered = text.lower()
    if "do not invent product badges" not in lowered and "invent product" not in lowered:
        fail("docs/badge-standard.md must retain no-invent-product edit policy wording", errors)
    if "three badges" not in lowered and "3 badges" not in lowered and "three badges max" not in lowered:
        # Accept "Three badges max" prose from Rules section.
        if "badges max" not in lowered:
            fail("docs/badge-standard.md must state three-badge max / keep-the-row-thin rule", errors)
    if "stewardship-checks" in text and "badge" in lowered:
        # Fail-closed: stewardship-checks mention must refuse a fourth badge explicitly.
        has_fourth = "fourth" in lowered
        has_refusal = (
            "intentionally" in lowered
            or "not** added" in lowered
            or "not added" in lowered
        )
        if not has_fourth or not has_refusal:
            fail(
                "docs/badge-standard.md mentioning stewardship-checks must refuse a fourth badge",
                errors,
            )


def check_readme_consistency(text: str, errors: list[str]) -> None:
    if "docs/badge-standard.md" not in text and "./docs/badge-standard.md" not in text:
        fail("README.md Documents section must link to docs/badge-standard.md", errors)
    if "run_stewardship_checks.sh" not in text and "scripts/run_stewardship_checks" not in text:
        fail(
            "README.md must document bash scripts/run_stewardship_checks.sh for local gates",
            errors,
        )
    # No quiet stewardship marketed as a fourth README badge.
    if re.search(r"\[!\[.*[Ss]tewardship", text):
        fail("README.md must not add a Stewardship product/status badge", errors)


def check_contributing_and_agents(errors: list[str]) -> None:
    if CONTRIBUTING.is_file():
        text = CONTRIBUTING.read_text(encoding="utf-8")
        if "run_stewardship_checks.sh" not in text:
            fail("CONTRIBUTING.md must document scripts/run_stewardship_checks.sh", errors)
        if "invent" not in text.lower():
            fail("CONTRIBUTING.md must warn against invent-product badges", errors)
        scan_secrets(CONTRIBUTING, errors)
    else:
        fail("Missing CONTRIBUTING.md", errors)

    if AGENTS.is_file():
        text = AGENTS.read_text(encoding="utf-8")
        for needle in (
            "run_stewardship_checks.sh",
            "test_stewardship_gates.py",
            "markdown-lint.yml",
            "link-check.yml",
            "stewardship-checks.yml",
            "relative",
        ):
            if needle not in text:
                fail(f"AGENTS.md §3 / testing must mention {needle}", errors)
        scan_secrets(AGENTS, errors)
    else:
        fail("Missing AGENTS.md", errors)


def check_badge_standard_gate_contract(errors: list[str]) -> None:
    """Fail-close live badge-standard gate wiring (after #61; deepen after #48)."""
    if not BADGE_GATE.is_file():
        fail("Missing scripts/check_badge_standard.py (badge-standard gate)", errors)
        return
    text = BADGE_GATE.read_text(encoding="utf-8")
    # Split pin literals so self-mutation of contiguous names cannot neutralize checks
    # or rewrite fail-message needles that self-tests assert on.
    order_pin = "REQUIRED_" + "ORDER"
    max_pin = "MAX_" + "BADGES"
    repo_const_pin = "EXPECTED_" + "REPO"
    workflows_pin = "REQUIRED_" + "WORKFLOWS"
    badge_re_pin = "BADGE_" + "LINE_RE"
    gh_re_pin = "REPO_FROM_" + "GITHUB_RE"
    shields_re_pin = "REPO_FROM_" + "SHIELDS_RE"
    if order_pin not in text:
        fail("check_badge_standard.py must declare " + order_pin, errors)
    if max_pin not in text:
        fail("check_badge_standard.py must declare " + max_pin, errors)
    if repo_const_pin not in text:
        fail("check_badge_standard.py must declare " + repo_const_pin, errors)
    if workflows_pin not in text:
        fail("check_badge_standard.py must declare " + workflows_pin, errors)
    if badge_re_pin not in text:
        fail("check_badge_standard.py must declare " + badge_re_pin, errors)
    if gh_re_pin not in text:
        fail("check_badge_standard.py must declare " + gh_re_pin, errors)
    if shields_re_pin not in text:
        fail("check_badge_standard.py must declare " + shields_re_pin, errors)
    # Live required badge labels (order is the public front-door contract).
    for label in (
        "Link " + "Check",
        "Markdown " + "Lint",
        "Lic" + "ense",
    ):
        if f'"{label}"' not in text and f"'{label}'" not in text:
            fail(
                "check_badge_standard.py " + order_pin + " must pin " + label,
                errors,
            )
    max_eq = max_pin + " = 3"
    # Require spaced form only (nospace MAX_BADGES=3 in prose is not the live pin).
    if max_eq not in text:
        fail(
            "check_badge_standard.py must pin " + max_eq + " (three badges max)",
            errors,
        )
    repo_slug = "fuzzywigg/" + "agents-governance"
    if repo_slug not in text:
        fail(
            "check_badge_standard.py " + repo_const_pin + " must pin " + repo_slug,
            errors,
        )
    for wf in (
        "link-check" + ".yml",
        "markdown-lint" + ".yml",
        "stewardship-checks" + ".yml",
    ):
        if wf not in text:
            fail(
                "check_badge_standard.py " + workflows_pin + " must pin " + wf,
                errors,
            )
    for fn in (
        "extract_badge_row",
        "check_badges",
        "check_badge_standard_doc",
        "check_readme_consistency",
        "check_contributing_and_agents",
        "check_lycheeignore",
        "check_actionlint_style",
        "check_workflow_hardening",
        "check_workflows_and_license",
    ):
        if f"def {fn}(" not in text:
            fail(
                "check_badge_standard.py must provide " + fn + "()",
                errors,
            )
    # Live badge image / link needles (split to resist self-mutation).
    link_svg = "link-check.yml/" + "badge.svg"
    md_svg = "markdown-lint.yml/" + "badge.svg"
    shields = "img.shields.io/github/" + "license/"
    if link_svg not in text:
        fail("check_badge_standard.py must pin " + link_svg, errors)
    if md_svg not in text:
        fail("check_badge_standard.py must pin " + md_svg, errors)
    if shields not in text:
        fail("check_badge_standard.py must pin " + shields, errors)
    contiguous_pin = "contigu" + "ous"
    if contiguous_pin not in text.lower():
        fail(
            "check_badge_standard.py must keep " + contiguous_pin + " badge-row pin",
            errors,
        )
    https_pin = "https:" + "//"
    if https_pin not in text:
        fail(
            "check_badge_standard.py must require " + https_pin + " badge images",
            errors,
        )
    invent_pin = "inv" + "ent"
    if invent_pin not in text.lower():
        fail(
            "check_badge_standard.py must retain " + invent_pin + "-product wording",
            errors,
        )
    fourth_pin = "four" + "th"
    if fourth_pin not in text.lower():
        fail(
            "check_badge_standard.py must retain " + fourth_pin + "-badge refusal pin",
            errors,
        )
    stew_reject = "Stewardship product/" + "status badge"
    if stew_reject.lower() not in text.lower():
        fail(
            "check_badge_standard.py must reject " + stew_reject,
            errors,
        )
    # Fail-closed after #48: module docstring must name live badge row order.
    live_row = "live badge row is " + "Link Check"
    if live_row.lower() not in text.lower():
        fail(
            "check_badge_standard.py must pin " + live_row
            + " → Markdown Lint → License",
            errors,
        )
    forbidden_pin = "FORBIDDEN_" + "BADGE_HINTS"
    secret_pin = "SECRET_" + "URL_HINTS"
    scan_pin = "scan_" + "secrets"
    if forbidden_pin not in text:
        fail("check_badge_standard.py must use " + forbidden_pin, errors)
    if secret_pin not in text:
        fail("check_badge_standard.py must use " + secret_pin, errors)
    if scan_pin not in text:
        fail("check_badge_standard.py must scan docs via " + scan_pin, errors)
    # Fail-closed after #61: second-pass helper / constant / needle pins
    # (badge-standard slice only; not wiki / relative / schema / common / CI spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    order_eq = (
        "REQUIRED_ORDER = ("
        '"Link Check", "Markdown Lint", "License")'
    )
    if order_eq not in text and order_eq.replace('"', "'") not in text:
        fail(
            "check_badge_standard.py must set REQUIRED_ORDER = "
            '("Link Check", "Markdown Lint", "License")',
            errors,
        )
    repo_eq = 'EXPECTED_REPO = "fuzzywigg/' + 'agents-governance"'
    if repo_eq not in text:
        fail(
            "check_badge_standard.py must set EXPECTED_REPO = "
            '"fuzzywigg/agents-governance"',
            errors,
        )
    for path_needle in (
        "README" + ".md",
        "LIC" + "ENSE",
        "badge-standard" + ".md",
        "CONTRIBUTING" + ".md",
        "AGENTS" + ".md",
        ".lychee" + "ignore",
        ".markdownlint" + ".json",
    ):
        quoted = f'"{path_needle}"'
        if quoted not in text and f"'{path_needle}'" not in text:
            if path_needle == "LICENSE" and (
                ' / "LICENSE"' in text or " / 'LICENSE'" in text
            ):
                continue
            fail(
                "check_badge_standard.py must pin path " + path_needle,
                errors,
            )
    contract_fn = "check_badge_standard_" + "gate_contract"
    if f"def {contract_fn}(" not in text:
        fail(
            "check_badge_standard.py must provide " + contract_fn + "()",
            errors,
        )
    if "def " + "main(" not in text:
        fail(
            "check_badge_standard.py must provide main()",
            errors,
        )
    full_link_svg = "actions/workflows/link-check.yml/" + "badge.svg"
    full_md_svg = "actions/workflows/markdown-lint.yml/" + "badge.svg"
    if full_link_svg not in text:
        fail(
            "check_badge_standard.py must pin " + full_link_svg,
            errors,
        )
    if full_md_svg not in text:
        fail(
            "check_badge_standard.py must pin " + full_md_svg,
            errors,
        )
    exactly_pin = "Badge row must have " + "exactly"
    if exactly_pin not in text:
        fail(
            "check_badge_standard.py must emit " + exactly_pin + " needle",
            errors,
        )
    order_needle = "Badge labels must be " + "in order"
    if order_needle not in text:
        fail(
            "check_badge_standard.py must emit " + order_needle + " needle",
            errors,
        )
    contig_needle = "Badge row must be " + "contiguous"
    if contig_needle not in text:
        fail(
            "check_badge_standard.py must emit " + contig_needle + " needle",
            errors,
        )
    h1_needle = "missing " + "H1"
    if h1_needle not in text:
        fail(
            "check_badge_standard.py must emit " + h1_needle + " needle",
            errors,
        )
    unexpected_needle = "Unexpected badge " + "label"
    if unexpected_needle not in text:
        fail(
            "check_badge_standard.py must emit " + unexpected_needle + " needle",
            errors,
        )
    forbidden_needle = "Forbidden invent-product / social badge " + "hint"
    if forbidden_needle not in text:
        fail(
            "check_badge_standard.py must emit " + forbidden_needle + " needle",
            errors,
        )
    secret_needle = "Secret-like token in badge " + "URL"
    if secret_needle not in text:
        fail(
            "check_badge_standard.py must emit " + secret_needle + " needle",
            errors,
        )
    failed_banner = "Badge standard check " + "FAILED"
    if failed_banner not in text:
        fail(
            "check_badge_standard.py must print " + failed_banner,
            errors,
        )
    ok_match = "OK: README badge row matches docs/" + "badge-standard.md"
    if ok_match not in text:
        fail(
            "check_badge_standard.py must keep " + ok_match + " success needle",
            errors,
        )
    endswith_lic = 'endswith("/' + 'LICENSE")'
    if endswith_lic not in text:
        fail(
            "check_badge_standard.py must accept License badge link endswith /LICENSE",
            errors,
        )
    dot_lic = '"./' + 'LICENSE"'
    if dot_lic not in text:
        fail(
            "check_badge_standard.py must accept relative ./LICENSE License badge link",
            errors,
        )
    load_wf = "load_workflow_" + "text"
    if load_wf not in text:
        fail(
            "check_badge_standard.py must use " + load_wf + " for workflow pins",
            errors,
        )
    invent_doc = "do not invent product " + "badges"
    if invent_doc not in text.lower():
        fail(
            "check_badge_standard.py must retain " + invent_doc + " doc wording pin",
            errors,
        )
    intent_pin = "intent" + "ionally"
    if intent_pin not in text.lower():
        fail(
            "check_badge_standard.py must retain " + intent_pin
            + " fourth-badge refusal wording",
            errors,
        )
    quiet_pin = "quiet " + "stewardship"
    if quiet_pin not in text.lower():
        fail(
            "check_badge_standard.py must retain " + quiet_pin + " wording",
            errors,
        )
    selftest_pin = "test_stewardship_" + "gates.py"
    if selftest_pin not in text:
        fail(
            "check_badge_standard.py AGENTS.md pins must require " + selftest_pin,
            errors,
        )
    relative_pin = '"' + "rel" + "ative" + '"'
    if relative_pin not in text:
        fail(
            "check_badge_standard.py AGENTS.md pins must require relative mention",
            errors,
        )
    https_start = 'img.startswith("https:' + '//")'
    if https_start not in text:
        fail(
            "check_badge_standard.py must require img.startswith(https://)",
            errors,
        )
    http_link_reject = 'link.startswith("http:' + '//")'
    if http_link_reject not in text:
        fail(
            "check_badge_standard.py must reject link.startswith(http://)",
            errors,
        )




def check_docs_lint_gate_contract(errors: list[str]) -> None:
    """Fail-close live docs-lint wiring (after #100; not CI workflow spam)."""
    if not BADGE_GATE.is_file():
        fail("Missing scripts/check_badge_standard.py (docs-lint host)", errors)
        return
    text = BADGE_GATE.read_text(encoding="utf-8")
    # Split pin literals so self-mutation of contiguous names cannot neutralize checks.
    host_pin = "docs-lint " + "host"
    if host_pin not in text:
        fail(
            "check_docs_lint_gate_contract must keep " + host_pin + " pin",
            errors,
        )
    spam_pin = "not CI workflow " + "spam"
    if spam_pin not in text:
        fail(
            "check_docs_lint_gate_contract must keep " + spam_pin + " pin",
            errors,
        )
    wiki_spam = "not wiki / relative " + "pin spam"
    if wiki_spam not in text:
        fail(
            "check_docs_lint_gate_contract must keep " + wiki_spam + " pin",
            errors,
        )
    lychee_const = "LYCHEE" + "IGNORE"
    md_const = "MARKDOWNLINT_" + "CONFIG"
    if lychee_const not in text:
        fail(
            "check_badge_standard.py must declare " + lychee_const,
            errors,
        )
    if md_const not in text:
        fail(
            "check_badge_standard.py must declare " + md_const,
            errors,
        )
    lychee_path = '".lychee' + 'ignore"'
    md_path = '".markdownlint' + '.json"'
    if lychee_path not in text and "'.lycheeignore'" not in text:
        fail(
            "check_badge_standard.py must pin path .lycheeignore",
            errors,
        )
    if md_path not in text and "'.markdownlint.json'" not in text:
        fail(
            "check_badge_standard.py must pin path .markdownlint.json",
            errors,
        )
    fn_pin = "check_lychee" + "ignore"
    if f"def {fn_pin}(" not in text:
        fail(
            "check_badge_standard.py must provide " + fn_pin + "()",
            errors,
        )
    contract_fn = "check_docs_lint_" + "gate_contract"
    if f"def {contract_fn}(" not in text:
        fail(
            "check_badge_standard.py must provide " + contract_fn + "()",
            errors,
        )
    live_doc = "Live fail-closed pins after " + "#100"
    if live_doc not in text:
        fail(
            "check_lycheeignore must keep " + live_doc + " docstring pin",
            errors,
        )
    escaped_pin = r"img\.shields" + r"\.io"
    if escaped_pin not in text:
        fail(
            "check_lycheeignore must pin escaped " + escaped_pin,
            errors,
        )
    mcp_pin = "modelcontextprotocol" + ".io"
    if mcp_pin not in text:
        fail(
            "check_lycheeignore must pin " + mcp_pin + " exclude",
            errors,
        )
    lfs_pin = "linuxfoundation" + ".org"
    if lfs_pin not in text:
        fail(
            "check_lycheeignore must pin " + lfs_pin + " exclude",
            errors,
        )
    stew_note = "stewardship/license-badge " + "enforcement"
    if stew_note not in text:
        fail(
            "check_lycheeignore must keep " + stew_note + " needle",
            errors,
        )
    https_star = "https://" + "*"
    http_star = "http://" + "*"
    if https_star not in text:
        fail(
            "check_lycheeignore must reject " + https_star,
            errors,
        )
    if http_star not in text:
        fail(
            "check_lycheeignore must reject " + http_star,
            errors,
        )
    md013_obj = '"MD013": { "line_length": ' + "200 }"
    if md013_obj not in text:
        fail(
            "check_workflows_and_license must pin MD013 line_length 200 object",
            errors,
        )
    md024_obj = '"MD024": { "siblings_only": ' + "true }"
    if md024_obj not in text:
        fail(
            "check_workflows_and_license must pin MD024 siblings_only true object",
            errors,
        )
    for rule in ("MD033", "MD041", "MD060"):
        needle = f'"{rule}"' + r"\s*:\s*false"
        if needle not in text:
            fail(
                f"check_workflows_and_license must pin {rule}: false regex",
                errors,
            )
    default_true = r'"default"\s*:\s*true'
    if default_true not in text:
        fail(
            "check_workflows_and_license must pin default: true regex",
            errors,
        )
    line_len_re = r'"line_length"\s*:\s*200'
    if line_len_re not in text:
        fail(
            "check_workflows_and_license must pin line_length: 200 regex",
            errors,
        )
    siblings_re = r'"siblings_only"\s*:\s*true'
    if siblings_re not in text:
        fail(
            "check_workflows_and_license must pin siblings_only: true regex",
            errors,
        )
    call_lychee = fn_pin + "(errors)"
    if call_lychee not in text:
        fail(
            "main must call " + call_lychee,
            errors,
        )
    contract_call = contract_fn + "(errors)"
    if contract_call not in text:
        fail(
            "main must call " + contract_call,
            errors,
        )
    docs_slice = "docs-lint " + "slice"
    if docs_slice not in text:
        fail(
            "docs-lint contract must keep " + docs_slice + " wording",
            errors,
        )
    # Deepen after #100: live false-positive rationale + path assigns + workflows helper.
    redirect_308 = "308 " + "redirect"
    if redirect_308 not in text:
        fail(
            "check_lycheeignore must keep " + redirect_308 + " rationale pin",
            errors,
        )
    hints_103 = "103 " + "early"
    if hints_103 not in text:
        fail(
            "check_lycheeignore must keep " + hints_103 + " rationale pin",
            errors,
        )
    lychee_assign = "LYCHEEIGNORE = ROOT / " + '".lychee' + 'ignore"'
    md_assign = "MARKDOWNLINT_CONFIG = ROOT / " + '".markdownlint' + '.json"'
    if lychee_assign not in text:
        fail(
            "check_badge_standard.py must assign " + lychee_assign,
            errors,
        )
    if md_assign not in text:
        fail(
            "check_badge_standard.py must assign " + md_assign,
            errors,
        )
    workflows_fn = "def check_workflows_and_" + "license("
    if workflows_fn not in text:
        fail(
            "check_badge_standard.py must provide check_workflows_and_license()",
            errors,
        )
    missing_lychee = "Missing .lychee" + "ignore"
    missing_md = "Missing .markdownlint" + ".json"
    if missing_lychee not in text:
        fail(
            "check_workflows_and_license must keep " + missing_lychee + " needle",
            errors,
        )
    if missing_md not in text:
        fail(
            "check_workflows_and_license must keep " + missing_md + " needle",
            errors,
        )
    cdn_note = "CDN exclude is not a missing " + "License badge"
    if cdn_note not in text:
        fail(
            "check_lycheeignore must keep " + cdn_note + " needle",
            errors,
        )
    call_workflows = "check_workflows_and_license" + "(errors)"
    if call_workflows not in text:
        fail(
            "main must call " + call_workflows,
            errors,
        )


def check_actionlint_style_gate_contract(errors: list[str]) -> None:
    """Fail-close live actionlint-style gate wiring (after #75; not relative-pin spam)."""
    if not BADGE_GATE.is_file():
        fail("Missing scripts/check_badge_standard.py (actionlint-style host)", errors)
        return
    text = BADGE_GATE.read_text(encoding="utf-8")
    # Split pin literals so self-mutation of contiguous names cannot neutralize checks.
    fn_pin = "check_actionlint_" + "style"
    if f"def {fn_pin}(" not in text:
        fail(
            "check_badge_standard.py must provide " + fn_pin + "()",
            errors,
        )
    doc_pin = "Static actionlint-like " + "checks"
    if doc_pin not in text:
        fail(
            "check_actionlint_style must keep " + doc_pin + " docstring pin",
            errors,
        )
    live_pin = "Live fail-closed pins after " + "#75"
    if live_pin not in text:
        fail(
            "check_actionlint_style must keep " + live_pin + " docstring pin",
            errors,
        )
    load_pin = "load_workflow_" + "text"
    if load_pin not in text:
        fail(
            "check_actionlint_style must use " + load_pin + " for workflow bodies",
            errors,
        )
    name_pin = "top-level " + "name:"
    if name_pin not in text:
        fail(
            "check_actionlint_style must require " + name_pin,
            errors,
        )
    runs_pin = "jobs.*." + "runs-on"
    if runs_pin not in text:
        fail(
            "check_actionlint_style must require " + runs_pin,
            errors,
        )
    steps_pin = "jobs.*." + "steps"
    if steps_pin not in text:
        fail(
            "check_actionlint_style must require " + steps_pin,
            errors,
        )
    timeout_pin = "timeout-" + "minutes:"
    if timeout_pin not in text:
        fail(
            "check_actionlint_style must require " + timeout_pin,
            errors,
        )
    prt_pin = "pull_request_" + "target"
    if prt_pin not in text:
        fail(
            "check_actionlint_style must reject " + prt_pin,
            errors,
        )
    harden_pin = "actionlint " + "harden"
    if harden_pin not in text:
        fail(
            "check_actionlint_style must keep " + harden_pin + " wording",
            errors,
        )
    write_all_pin = "write-" + "all"
    if write_all_pin not in text:
        fail(
            "check_actionlint_style must reject permissions: " + write_all_pin,
            errors,
        )
    contents_write_pin = "contents: " + "write"
    if contents_write_pin not in text:
        fail(
            "check_actionlint_style must reject " + contents_write_pin,
            errors,
        )
    id_token_pin = "id-token: " + "write"
    if id_token_pin not in text:
        fail(
            "check_actionlint_style must reject " + id_token_pin,
            errors,
        )
    docker_pin = "docker:" + "//"
    if docker_pin not in text:
        fail(
            "check_actionlint_style must skip " + docker_pin + " uses",
            errors,
        )
    unpinned_pin = "unpinned action " + "uses"
    if unpinned_pin not in text:
        fail(
            "check_actionlint_style must reject " + unpinned_pin,
            errors,
        )
    # Float-ref set must stay exactly main/master/latest.
    main_master = '"main"' + ', "master"'
    main_master_alt = "'main'" + ", 'master'"
    master_mid = ', "master", ' + '"latest"'
    master_mid_alt = ", 'master', " + "'latest'"
    master_latest = '"master"' + ', "latest"'
    master_latest_alt = "'master'" + ", 'latest'"
    if main_master not in text and main_master_alt not in text:
        fail(
            "check_actionlint_style must reject float @main",
            errors,
        )
    if master_mid not in text and master_mid_alt not in text:
        fail(
            "check_actionlint_style must reject float @master",
            errors,
        )
    if master_latest not in text and master_latest_alt not in text:
        fail(
            "check_actionlint_style must reject float @latest",
            errors,
        )
    float_set_pin = '{"main", ' + '"master", ' + '"latest"}'
    float_set_pin_alt = "{'main', " + "'master', " + "'latest'}"
    if float_set_pin not in text and float_set_pin_alt not in text:
        fail(
            "check_actionlint_style must pin float set "
            "{main, master, latest}",
            errors,
        )
    call_pin = fn_pin + "(errors)"
    if call_pin not in text:
        fail(
            "main must call " + call_pin,
            errors,
        )
    # Fail-closed after #83/#86: second-pass helper / constant / needle pins
    # (actionlint-style slice only; not schema / badge / wiki / relative /
    # common / CI workflow pin spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    name_re = 'r"(?m)^name:' + '\\s*\\S"'
    name_re_sq = "r'(?m)^name:" + "\\s*\\S'"
    if name_re not in text and name_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact top-level name: regex",
            errors,
        )
    uses_re = 'r"(?m)^\\s*-\\s*uses:\\s*(' + '[^\\s#]+)"'
    uses_re_sq = "r'(?m)^\\s*-\\s*uses:\\s*(" + "[^\\s#]+)'"
    if uses_re not in text and uses_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact uses: capture regex",
            errors,
        )
    write_all_re = 'r"(?m)^\\s*permissions:\\s*write-' + 'all\\s*$"'
    write_all_re_sq = "r'(?m)^\\s*permissions:\\s*write-" + "all\\s*$'"
    if write_all_re not in text and write_all_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact permissions: write-all regex",
            errors,
        )
    contents_write_re = 'r"(?m)^\\s*contents:\\s*' + 'write\\s*$"'
    contents_write_re_sq = "r'(?m)^\\s*contents:\\s*" + "write\\s*$'"
    if contents_write_re not in text and contents_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact contents: write regex",
            errors,
        )
    id_token_re = 'r"(?m)^\\s*id-token:\\s*' + 'write\\s*$"'
    id_token_re_sq = "r'(?m)^\\s*id-token:\\s*" + "write\\s*$'"
    if id_token_re not in text and id_token_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact id-token: write regex",
            errors,
        )
    docker_startswith = "startswith(" + '"docker://"' + ")"
    docker_startswith_sq = "startswith(" + "'docker://'" + ")"
    if docker_startswith not in text and docker_startswith_sq not in text:
        fail(
            "check_actionlint_style must skip uses via " + docker_startswith,
            errors,
        )
    at_not_in = '"@" not in ' + "uses"
    at_not_in_sq = "'@' not in " + "uses"
    if at_not_in not in text and at_not_in_sq not in text:
        fail(
            "check_actionlint_style must reject unpinned via " + at_not_in,
            errors,
        )
    rsplit_pin = 'rsplit("@", ' + "1)"
    rsplit_pin_sq = "rsplit('@', " + "1)"
    if rsplit_pin not in text and rsplit_pin_sq not in text:
        fail(
            "check_actionlint_style must split action refs via " + rsplit_pin,
            errors,
        )
    group_strip = "match.group(1)" + ".strip()"
    if group_strip not in text:
        fail(
            "check_actionlint_style must take uses via " + group_strip,
            errors,
        )
    runs_membership = '"runs-on:" not in ' + "text"
    runs_membership_sq = "'runs-on:' not in " + "text"
    if runs_membership not in text and runs_membership_sq not in text:
        fail(
            "check_actionlint_style must require runs-on: via membership check",
            errors,
        )
    steps_membership = '"steps:" not in ' + "text"
    steps_membership_sq = "'steps:' not in " + "text"
    if steps_membership not in text and steps_membership_sq not in text:
        fail(
            "check_actionlint_style must require steps: via membership check",
            errors,
        )
    prt_membership = '"pull_request_target:" in ' + "text"
    prt_membership_sq = "'pull_request_target:' in " + "text"
    if prt_membership not in text and prt_membership_sq not in text:
        fail(
            "check_actionlint_style must reject pull_request_target: via membership",
            errors,
        )
    timeout_membership = '"timeout-minutes:" not in ' + "text"
    timeout_membership_sq = "'timeout-minutes:' not in " + "text"
    if timeout_membership not in text and timeout_membership_sq not in text:
        fail(
            "check_actionlint_style must require timeout-minutes: via membership",
            errors,
        )
    none_continue = "if text is " + "None:"
    if none_continue not in text:
        fail(
            "check_actionlint_style must continue when load_workflow_text returns None",
            errors,
        )
    required_loop = "for name in REQUIRED_" + "WORKFLOWS:"
    if required_loop not in text:
        fail(
            "check_actionlint_style must iterate REQUIRED_WORKFLOWS",
            errors,
        )
    least_priv = "Prefer least " + "privilege"
    if least_priv not in text:
        fail(
            "check_actionlint_style must keep " + least_priv + " comment",
            errors,
        )
    oidc_pin = "OIDC write not needed for docs CI " + "paths"
    if oidc_pin not in text:
        fail(
            "check_actionlint_style must keep " + oidc_pin + " comment",
            errors,
        )
    majors_pin = "Pin GitHub Actions " + "majors"
    if majors_pin not in text:
        fail(
            "check_actionlint_style must keep " + majors_pin + " comment",
            errors,
        )
    timeout_comment = "jobs must declare " + "timeout"
    if timeout_comment not in text:
        fail(
            "check_actionlint_style must keep " + timeout_comment + " comment",
            errors,
        )
    fail_top_name = "actionlint-style requires top-level " + "name:"
    if fail_top_name not in text:
        fail(
            "check_actionlint_style must emit " + fail_top_name + " fail needle",
            errors,
        )
    fail_runs = "actionlint-style requires jobs.*.runs-" + "on"
    if fail_runs not in text:
        fail(
            "check_actionlint_style must emit " + fail_runs + " fail needle",
            errors,
        )
    fail_steps = "actionlint-style requires jobs.*." + "steps"
    if fail_steps not in text:
        fail(
            "check_actionlint_style must emit " + fail_steps + " fail needle",
            errors,
        )
    fail_prt = "must not use pull_request_target (actionlint " + "harden)"
    if fail_prt not in text:
        fail(
            "check_actionlint_style must emit " + fail_prt + " fail needle",
            errors,
        )
    fail_write_all = "must not set permissions: write-" + "all"
    if fail_write_all not in text:
        fail(
            "check_actionlint_style must emit " + fail_write_all + " fail needle",
            errors,
        )
    fail_contents = "contents: write is forbidden on stewardship " + "workflows"
    if fail_contents not in text:
        fail(
            "check_actionlint_style must emit " + fail_contents + " fail needle",
            errors,
        )
    fail_id_token = "id-token: write is forbidden on stewardship " + "workflows"
    if fail_id_token not in text:
        fail(
            "check_actionlint_style must emit " + fail_id_token + " fail needle",
            errors,
        )
    fail_unpinned = "unpinned action " + "uses:"
    if fail_unpinned not in text:
        fail(
            "check_actionlint_style must emit " + fail_unpinned + " fail needle",
            errors,
        )
    fail_float = "action must not float on " + "@"
    if fail_float not in text:
        fail(
            "check_actionlint_style must emit " + fail_float + " fail needle",
            errors,
        )
    fail_timeout = "actionlint-style requires timeout-minutes on " + "jobs"
    if fail_timeout not in text:
        fail(
            "check_actionlint_style must emit " + fail_timeout + " fail needle",
            errors,
        )
    second_pass_doc = "Second-pass after #83/#86: exact name/" + "uses"
    if second_pass_doc not in text:
        fail(
            "check_actionlint_style docstring must pin " + second_pass_doc,
            errors,
        )
    module_second = "second-pass after #83/" + "#86"
    if module_second not in text:
        fail(
            "check_badge_standard.py module docstring must pin actionlint "
            + module_second,
            errors,
        )
    contract_fn = "check_actionlint_style_gate_" + "contract"
    self_text = BADGE_GATE.read_text(encoding="utf-8")
    if f"def {contract_fn}(" not in self_text:
        fail(
            "check_badge_standard.py must provide " + contract_fn + "()",
            errors,
        )
    if contract_fn + "(" not in self_text.replace(f"def {contract_fn}(", "", 1):
        fail(
            "check_badge_standard.py main must call " + contract_fn + "()",
            errors,
        )

    # Fail-closed after #94: third-pass helper / constant / needle pins
    # (actionlint-style reversible CI slice only; not lychee/mdlint/workflow spam).
    third_pass_doc = "Third-pass after " + "#94"
    if third_pass_doc not in text:
        fail(
            "check_actionlint_style docstring must pin " + third_pass_doc,
            errors,
        )
    module_third = "third-pass after " + "#94"
    if module_third not in text:
        fail(
            "check_badge_standard.py module docstring must pin actionlint "
            + module_third,
            errors,
        )
    concurrency_membership = '"concurrency:" not in ' + "text"
    concurrency_membership_sq = "'concurrency:' not in " + "text"
    if concurrency_membership not in text and concurrency_membership_sq not in text:
        fail(
            "check_actionlint_style must require concurrency: via membership",
            errors,
        )
    cancel_membership = '"cancel-in-progress:" not in ' + "text"
    cancel_membership_sq = "'cancel-in-progress:' not in " + "text"
    if cancel_membership not in text and cancel_membership_sq not in text:
        fail(
            "check_actionlint_style must require cancel-in-progress: via membership",
            errors,
        )
    permissions_membership = '"permissions:" not in ' + "text"
    permissions_membership_sq = "'permissions:' not in " + "text"
    if permissions_membership not in text and permissions_membership_sq not in text:
        fail(
            "check_actionlint_style must require permissions: via membership",
            errors,
        )
    actions_write_re = 'r"(?m)^\\s*actions:\\s*' + 'write\\s*$"'
    actions_write_re_sq = "r'(?m)^\\s*actions:\\s*" + "write\\s*$'"
    if actions_write_re not in text and actions_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact actions: write regex",
            errors,
        )
    packages_write_re = 'r"(?m)^\\s*packages:\\s*' + 'write\\s*$"'
    packages_write_re_sq = "r'(?m)^\\s*packages:\\s*" + "write\\s*$'"
    if packages_write_re not in text and packages_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact packages: write regex",
            errors,
        )
    pr_write_re = 'r"(?m)^\\s*pull-requests:\\s*' + 'write\\s*$"'
    pr_write_re_sq = "r'(?m)^\\s*pull-requests:\\s*" + "write\\s*$'"
    if pr_write_re not in text and pr_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact pull-requests: write regex",
            errors,
        )
    finditer_pin = "re.finditer("
    if finditer_pin not in text:
        fail(
            "check_actionlint_style must scan uses via re.finditer",
            errors,
        )
    # Split construction keeps second-pass startswith/rsplit self-tests fail-closed.
    docker_continue = 'if uses.startswith("docker:' + '//"):'
    if docker_continue not in text:
        fail(
            "check_actionlint_style must continue after docker:// uses",
            errors,
        )
    rsplit_tail = 'rsplit("@", 1)' + "[-1]"
    if rsplit_tail not in text:
        fail(
            'check_actionlint_style must take ref via rsplit("@", 1)[-1]',
            errors,
        )
    fail_concurrency = "actionlint-style requires concurrency:"
    if fail_concurrency not in text:
        fail(
            "check_actionlint_style must emit " + fail_concurrency + " fail needle",
            errors,
        )
    fail_cancel = "actionlint-style requires cancel-in-progress:"
    if fail_cancel not in text:
        fail(
            "check_actionlint_style must emit " + fail_cancel + " fail needle",
            errors,
        )
    fail_permissions = "actionlint-style requires permissions:"
    if fail_permissions not in text:
        fail(
            "check_actionlint_style must emit " + fail_permissions + " fail needle",
            errors,
        )
    fail_actions = "actions: write is forbidden on stewardship " + "workflows"
    if fail_actions not in text:
        fail(
            "check_actionlint_style must emit " + fail_actions + " fail needle",
            errors,
        )
    fail_packages = "packages: write is forbidden on stewardship " + "workflows"
    if fail_packages not in text:
        fail(
            "check_actionlint_style must emit " + fail_packages + " fail needle",
            errors,
        )
    fail_prs = "pull-requests: write is forbidden on stewardship " + "workflows"
    if fail_prs not in text:
        fail(
            "check_actionlint_style must emit " + fail_prs + " fail needle",
            errors,
        )
    reversible_pin = "reversible CI " + "concurrency"
    if reversible_pin not in text:
        fail(
            "check_actionlint_style must keep " + reversible_pin + " wording",
            errors,
        )




def check_stewardship_common_contract(errors: list[str]) -> None:
    """Fail-close live stewardship_common wiring (after #65; deepen after #46)."""
    if not COMMON_GATE.is_file():
        fail("Missing scripts/stewardship_common.py (shared gate helpers)", errors)
        return
    text = COMMON_GATE.read_text(encoding="utf-8")
    if "SECRET_PATTERNS" not in text:
        fail("stewardship_common.py must declare SECRET_PATTERNS", errors)
    if "SECRET_URL_HINTS" not in text:
        fail("stewardship_common.py must declare SECRET_URL_HINTS", errors)
    if "FORBIDDEN_BADGE_HINTS" not in text:
        fail("stewardship_common.py must declare FORBIDDEN_BADGE_HINTS", errors)
    if "DANGEROUS_LINK_SCHEMES" not in text:
        fail("stewardship_common.py must declare DANGEROUS_LINK_SCHEMES", errors)
    if "FENCED_BLOCK_RE" not in text:
        fail("stewardship_common.py must declare FENCED_BLOCK_RE", errors)
    for fn in (
        "fail",
        "strip_fenced_code",
        "has_dangerous_scheme",
        "scan_secrets",
        "markdown_files",
        "load_workflow_text",
    ):
        if f"def {fn}(" not in text:
            fail(
                f"stewardship_common.py must provide {fn}()",
                errors,
            )
    # Fail-closed after #46: imported helpers keep distinctive doc pins.
    if "Gate fail-closed helper" not in text:
        fail(
            "stewardship_common.py fail() must keep Gate fail-closed helper pin",
            errors,
        )
    if "Load .github/workflows/" not in text:
        fail(
            "stewardship_common.py load_workflow_text must keep workflows load pin",
            errors,
        )
    # Live secret pattern needles (CI tokens / private keys / cloud keys).
    for needle in (
        "ghp_",
        "gho_",
        "ghu_",
        "ghs_",
        "ghr_",
        "github_pat_",
        "PRIVATE KEY",
        "sk-",
        "rk-",
        "api[_-]?key",
        "aws_secret_access_key",
        "xox",
        "npm_",
        "AIza",
    ):
        if needle not in text:
            fail(
                f"stewardship_common.py SECRET_PATTERNS must pin {needle}",
                errors,
            )
    # Live SECRET_URL_HINTS (query params + token prefixes).
    for hint in (
        "token=",
        "access_token=",
        "api_key=",
        "apikey=",
        "client_secret=",
    ):
        if f'"{hint}"' not in text and f"'{hint}'" not in text:
            fail(
                f"stewardship_common.py SECRET_URL_HINTS must pin {hint}",
                errors,
            )
    # Live invent-product / social badge chrome rejects.
    for hint in (
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
    ):
        if f'"{hint}"' not in text and f"'{hint}'" not in text:
            fail(
                f"stewardship_common.py FORBIDDEN_BADGE_HINTS must pin {hint}",
                errors,
            )
    # Live dangerous markdown link schemes.
    for scheme in ("javascript:", "data:", "vbscript:", "file:"):
        if f'"{scheme}"' not in text and f"'{scheme}'" not in text:
            fail(
                f"stewardship_common.py DANGEROUS_LINK_SCHEMES must pin {scheme}",
                errors,
            )
    if "```" not in text or "~~~" not in text:
        fail(
            "stewardship_common.py FENCED_BLOCK_RE must match ``` and ~~~ fences",
            errors,
        )
    # scan_secrets treats hints ending with '=' as URL-ish query params.
    if "endswith" not in text:
        fail(
            "stewardship_common.py scan_secrets must treat '=' hints as URL-ish",
            errors,
        )
    if "URL-ish secret hints" not in text:
        fail(
            "stewardship_common.py scan_secrets must keep URL-ish secret hints pin",
            errors,
        )
    if "invent" not in text.lower():
        fail(
            "stewardship_common.py must retain invent-product / no-invent wording",
            errors,
        )
    # Fail-closed after #46: module docstring must name live secret scan cover.
    if "live secret scan covers ci tokens" not in text.lower():
        fail(
            "stewardship_common.py must pin live secret scan covers CI tokens",
            errors,
        )
    # Fail-closed after #65: second-pass helper / constant / needle pins
    # (stewardship_common slice only; not badge / wiki / relative / schema / CI spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    root_pin = "Path(__file__).resolve().parents" + "[1]"
    if root_pin not in text:
        fail(
            "stewardship_common.py must set ROOT via Path(__file__).resolve().parents[1]",
            errors,
        )
    fence_dotall = "re.DOT" + "ALL"
    if fence_dotall not in text:
        fail(
            "stewardship_common.py FENCED_BLOCK_RE must use re.DOTALL",
            errors,
        )
    fence_pat = r"(?:```|~~~).*?(?:```|~~~)"
    if fence_pat not in text:
        fail(
            "stewardship_common.py FENCED_BLOCK_RE must match ```|~~~ fence pattern",
            errors,
        )
    strip_doc = "Remove fenced code blocks so example links do not fail " + "integrity gates."
    if strip_doc not in text:
        fail(
            "stewardship_common.py strip_fenced_code must keep integrity gates doc pin",
            errors,
        )
    danger_doc = "Return the matched dangerous scheme prefix, or " + "None."
    if danger_doc not in text:
        fail(
            "stewardship_common.py has_dangerous_scheme must keep scheme prefix doc pin",
            errors,
        )
    scan_doc = "Append errors if path content matches forbidden secret-like " + "patterns."
    if scan_doc not in text:
        fail(
            "stewardship_common.py scan_secrets must keep secret-like patterns doc pin",
            errors,
        )
    md_doc = "Collect markdown paths under ROOT for the given relative " + "globs."
    if md_doc not in text:
        fail(
            "stewardship_common.py markdown_files must keep relative globs doc pin",
            errors,
        )
    pattern_needle = "matches forbidden secret-like " + "pattern"
    if pattern_needle not in text:
        fail(
            "stewardship_common.py scan_secrets must emit " + pattern_needle + " needle",
            errors,
        )
    url_hint_needle = "secret-like URL " + "hint"
    if url_hint_needle not in text:
        fail(
            "stewardship_common.py scan_secrets must emit " + url_hint_needle + " needle",
            errors,
        )
    token_hint_needle = "secret-like token " + "hint"
    if token_hint_needle not in text:
        fail(
            "stewardship_common.py scan_secrets must emit " + token_hint_needle + " needle",
            errors,
        )
    if "relative_to" not in text:
        fail(
            "stewardship_common.py scan_secrets must use relative_to for labels",
            errors,
        )
    strip_lower = "strip()" + ".lower()"
    if strip_lower not in text and "strip().lower()" not in text:
        fail(
            "stewardship_common.py has_dangerous_scheme must strip().lower() targets",
            errors,
        )
    if "startswith" not in text:
        fail(
            "stewardship_common.py has_dangerous_scheme must startswith scheme prefixes",
            errors,
        )
    append_pin = "errors.append" + "(msg)"
    if append_pin not in text:
        fail(
            "stewardship_common.py fail() must errors.append(msg)",
            errors,
        )
    passwd_pin = "password|passwd|" + "token"
    if passwd_pin not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin password|passwd|token",
            errors,
        )
    if "OPENSSH" not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin OPENSSH private keys",
            errors,
        )
    # Live pattern uses: (?:RSA |OPENSSH |EC )?
    openssh_ec = "OPENSSH |" + "EC"
    if openssh_ec not in text and "OPENSSH|EC" not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin OPENSSH|EC private keys",
            errors,
        )
    public_docs = "Public docs must not ship " + "secrets"
    if public_docs not in text:
        fail(
            "stewardship_common.py must keep Public docs must not ship secrets pin",
            errors,
        )
    invent_surface = "no invent-product " + "surface"
    if invent_surface not in text:
        fail(
            "stewardship_common.py must keep no invent-product surface pin",
            errors,
        )
    social_chrome = "Invent-product / social " + "chrome"
    if social_chrome not in text:
        fail(
            "stewardship_common.py must keep Invent-product / social chrome pin",
            errors,
        )
    link_schemes = "Link schemes that must never " + "appear"
    if link_schemes not in text:
        fail(
            "stewardship_common.py must keep Link schemes that must never appear pin",
            errors,
        )
    if "is_file()" not in text:
        fail(
            "stewardship_common.py markdown_files must filter with is_file()",
            errors,
        )
    if "sorted(" not in text:
        fail(
            "stewardship_common.py markdown_files must sorted() results",
            errors,
        )
    workflows_pin = '"workflows"'
    if workflows_pin not in text and "'workflows'" not in text:
        fail(
            "stewardship_common.py load_workflow_text must pin workflows path segment",
            errors,
        )
    if "return None" not in text:
        fail(
            "stewardship_common.py load_workflow_text must return None when missing",
            errors,
        )
    schemes_eq = (
        'DANGEROUS_LINK_SCHEMES = (\n'
        '    "javascript:",\n'
        '    "data:",\n'
        '    "vbscript:",\n'
        '    "file:",\n'
        ")"
    )
    schemes_eq_sq = schemes_eq.replace('"', "'")
    if schemes_eq not in text and schemes_eq_sq not in text:
        fail(
            "stewardship_common.py must set DANGEROUS_LINK_SCHEMES = "
            '(javascript:/data:/vbscript:/file:)',
            errors,
        )
    url_hints_head = 'SECRET_URL_HINTS = (\n    "token=",'
    url_hints_head_sq = "SECRET_URL_HINTS = (\n    'token=',"
    if url_hints_head not in text and url_hints_head_sq not in text:
        fail(
            'stewardship_common.py must set SECRET_URL_HINTS starting with "token="',
            errors,
        )
    contract_fn = "check_stewardship_common_" + "contract"
    # Self-pin: this contract helper name must remain reachable from main.
    self_text = BADGE_GATE.read_text(encoding="utf-8")
    if f"def {contract_fn}(" not in self_text:
        fail(
            "check_badge_standard.py must provide " + contract_fn + "()",
            errors,
        )
    if contract_fn + "(" not in self_text.replace(f"def {contract_fn}(", "", 1):
        fail(
            "check_badge_standard.py main must call " + contract_fn + "()",
            errors,
        )


def check_stewardship_schema_gate_contract(errors: list[str]) -> None:
    """Fail-close live stewardship-schema gate wiring (after #72/#75; deepen after #53)."""
    if not SCHEMA_GATE.is_file():
        fail("Missing scripts/check_stewardship_schema.py (schema gate)", errors)
        return
    text = SCHEMA_GATE.read_text(encoding="utf-8")
    if "DOC_SCHEMAS" not in text:
        fail("check_stewardship_schema.py must declare DOC_SCHEMAS", errors)
    if "EXPECTED_VALUES" not in text:
        fail("check_stewardship_schema.py must declare EXPECTED_VALUES", errors)
    # Live stewardship docs covered by schema gate (no invent-product paths).
    for rel in (
        "docs/badge-standard.md",
        "docs/wiki/PUBLISH.md",
        "docs/issue-backlog.md",
        "AGENTS.md",
        "CLAUDE.md",
    ):
        if rel not in text:
            fail(
                f"check_stewardship_schema.py DOC_SCHEMAS must cover {rel}",
                errors,
            )
    for key in (
        "status",
        "tier",
        "created",
        "owner",
        "scope",
        "edit_policy",
        "closes",
        "version",
        "last_updated",
        "maintainer",
        "parent_governance",
        "autonomy_level",
        "repo",
        "surface",
        "purpose",
    ):
        if f'"{key}"' not in text and f"'{key}'" not in text:
            fail(
                f"check_stewardship_schema.py must pin metadata key {key}",
                errors,
            )
    if "SEMVER_RE" not in text:
        fail("check_stewardship_schema.py must declare SEMVER_RE", errors)
    if "ISO_DATE_RE" not in text:
        fail("check_stewardship_schema.py must declare ISO_DATE_RE", errors)
    if "ISSUE_REF_RE" not in text:
        fail("check_stewardship_schema.py must declare ISSUE_REF_RE", errors)
    if "FENCED_YAML_RE" not in text:
        fail("check_stewardship_schema.py must declare FENCED_YAML_RE", errors)
    if "```yaml" not in text:
        fail(
            "check_stewardship_schema.py must require fenced ```yaml metadata",
            errors,
        )
    if "DATE_KEYS" not in text:
        fail("check_stewardship_schema.py must declare DATE_KEYS", errors)
    if "STRING_KEYS" not in text:
        fail("check_stewardship_schema.py must declare STRING_KEYS", errors)
    if "reject_non_scalar" not in text:
        fail(
            "check_stewardship_schema.py must reject nested/list metadata via reject_non_scalar",
            errors,
        )
    if "empty yaml metadata block" not in text:
        fail(
            "check_stewardship_schema.py must reject empty yaml metadata blocks",
            errors,
        )
    if "isinstance(level, bool)" not in text and "isinstance(tier, bool)" not in text:
        fail(
            "check_stewardship_schema.py must reject bool pretending to be "
            "autonomy_level / tier ints",
            errors,
        )
    if "parse_simple_yaml" not in text:
        fail(
            "check_stewardship_schema.py must provide parse_simple_yaml fallback",
            errors,
        )
    if "load_yaml" not in text:
        fail("check_stewardship_schema.py must provide load_yaml", errors)
    if "first_yaml_block" not in text:
        fail("check_stewardship_schema.py must provide first_yaml_block", errors)
    if "safe_load" not in text:
        fail(
            "check_stewardship_schema.py must use yaml.safe_load when PyYAML present",
            errors,
        )
    if "must be a mapping" not in text:
        fail(
            "check_stewardship_schema.py load_yaml must keep "
            "'must be a mapping' reject",
            errors,
        )
    if "scan_secrets" not in text:
        fail(
            "check_stewardship_schema.py must scan schema docs via scan_secrets",
            errors,
        )
    if "invent" not in text.lower():
        fail(
            "check_stewardship_schema.py must retain invent-product edit_policy pin",
            errors,
        )
    if "smtp.eth" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin smtp.eth maintainer",
            errors,
        )
    if "repository-specific" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin repository-specific",
            errors,
        )
    if "copilot" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin copilot surface/owner",
            errors,
        )
    if "ACTIVE" not in text:
        fail(
            "check_stewardship_schema.py must require ACTIVE status on docs/",
            errors,
        )
    if "0..3" not in text:
        fail(
            "check_stewardship_schema.py must constrain autonomy_level to 0..3",
            errors,
        )
    # Fail-closed after #45: live issue-backlog owner is copilot.
    if "live backlog owner is copilot" not in text.lower():
        fail(
            "check_stewardship_schema.py must pin issue-backlog owner copilot",
            errors,
        )
    # Fail-closed after #53: live badge scope / PUBLISH purpose / closes #16 pins.
    if "public governance front-door repos" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin "
            "public governance front-door repos",
            errors,
        )
    if "Reversible publish path for docs/wiki" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin "
            "Reversible publish path for docs/wiki",
            errors,
        )
    if '"#16"' not in text and "'#16'" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin closes #16",
            errors,
        )
    if "AGENTS-ECOSYSTEM.md" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin AGENTS-ECOSYSTEM.md",
            errors,
        )
    if "github.com/fuzzywigg/agents-governance" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin "
            "github.com/fuzzywigg/agents-governance",
            errors,
        )
    if "fuzzywigg (smtp.eth)" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin fuzzywigg (smtp.eth)",
            errors,
        )
    if 'repo": "agents-governance"' not in text and "repo': 'agents-governance'" not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES must pin "
            'repo": "agents-governance"',
            errors,
        )
    # Fail-closed after #72/#75: second-pass helper / constant / needle pins
    # (schema slice only; not badge / wiki / relative / common / CI workflow /
    # actionlint pin spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    fence_exact = (
        'FENCED_YAML_RE = re.compile(r"^```yaml\\n(.*?)\\n```", '
        "re.MULTILINE | re.DOTALL)"
    )
    if fence_exact not in text:
        fail(
            "check_stewardship_schema.py must set FENCED_YAML_RE exact "
            "```yaml MULTILINE|DOTALL pattern",
            errors,
        )
    iso_exact = 'ISO_DATE_RE = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")'
    if iso_exact not in text:
        fail(
            "check_stewardship_schema.py must set ISO_DATE_RE exact "
            "YYYY-MM-DD prefix pattern",
            errors,
        )
    semver_exact = 'SEMVER_RE = re.compile(r"^\\d+\\.\\d+\\.\\d+$")'
    if semver_exact not in text:
        fail(
            "check_stewardship_schema.py must set SEMVER_RE exact X.Y.Z pattern",
            errors,
        )
    issue_exact = 'ISSUE_REF_RE = re.compile(r"#\\d+")'
    if issue_exact not in text:
        fail(
            "check_stewardship_schema.py must set ISSUE_REF_RE exact #N pattern",
            errors,
        )
    date_keys_exact = 'DATE_KEYS = ("created", "last_updated")'
    date_keys_sq = "DATE_KEYS = ('created', 'last_updated')"
    if date_keys_exact not in text and date_keys_sq not in text:
        fail(
            'check_stewardship_schema.py must set DATE_KEYS = ("created", "last_updated")',
            errors,
        )
    tiny_yaml = "Tiny YAML subset " + "parser"
    if tiny_yaml not in text:
        fail(
            "check_stewardship_schema.py parse_simple_yaml must keep Tiny YAML subset pin",
            errors,
        )
    scalar_doc = "stewardship metadata values must be " + "scalars"
    if scalar_doc not in text:
        fail(
            "check_stewardship_schema.py reject_non_scalar must keep scalars doc pin",
            errors,
        )
    no_fence = "no fenced ```yaml metadata block " + "found"
    if no_fence not in text:
        fail(
            "check_stewardship_schema.py first_yaml_block must keep no fenced ```yaml pin",
            errors,
        )
    unsupported = "unsupported YAML " + "line"
    if unsupported not in text:
        fail(
            "check_stewardship_schema.py parse_simple_yaml must keep unsupported YAML line pin",
            errors,
        )
    empty_key = "empty key in YAML " + "line"
    if empty_key not in text:
        fail(
            "check_stewardship_schema.py parse_simple_yaml must keep empty key pin",
            errors,
        )
    scalar_needle = "must be a " + "scalar"
    if scalar_needle not in text:
        fail(
            "check_stewardship_schema.py must emit must be a scalar needle",
            errors,
        )
    nonempty_needle = "must be " + "non-empty"
    if nonempty_needle not in text:
        fail(
            "check_stewardship_schema.py must emit must be non-empty needle",
            errors,
        )
    string_needle = "must be a " + "string"
    if string_needle not in text:
        fail(
            "check_stewardship_schema.py must emit must be a string needle",
            errors,
        )
    active_needle = "status must be ACTIVE for active stewardship " + "docs"
    if active_needle not in text:
        fail(
            "check_stewardship_schema.py must emit ACTIVE stewardship docs needle",
            errors,
        )
    tier_needle = "tier must be a positive " + "int"
    if tier_needle not in text:
        fail(
            "check_stewardship_schema.py must emit tier must be a positive int needle",
            errors,
        )
    autonomy_needle = "autonomy_level must be int in " + "0..3"
    if autonomy_needle not in text:
        fail(
            "check_stewardship_schema.py must emit autonomy_level must be int in 0..3 needle",
            errors,
        )
    iso_needle = "must be ISO-8601 date-" + "prefixed"
    if iso_needle not in text:
        fail(
            "check_stewardship_schema.py must emit ISO-8601 date-prefixed needle",
            errors,
        )
    invent_needle = "must retain no-invent-product " + "wording"
    if invent_needle not in text:
        fail(
            "check_stewardship_schema.py must emit no-invent-product wording needle",
            errors,
        )
    semver_needle = "version must be semver " + "X.Y.Z"
    if semver_needle not in text:
        fail(
            "check_stewardship_schema.py must emit version must be semver X.Y.Z needle",
            errors,
        )
    closes_needle = "closes must reference an issue like " + "#N ("
    if closes_needle not in text:
        fail(
            "check_stewardship_schema.py must emit closes must reference an issue like #N ( needle",
            errors,
        )
    failed_banner = "Stewardship schema check " + "FAILED"
    if failed_banner not in text:
        fail(
            "check_stewardship_schema.py must keep Stewardship schema check FAILED banner",
            errors,
        )
    ok_banner = "OK: stewardship metadata schemas " + "valid"
    if ok_banner not in text:
        fail(
            "check_stewardship_schema.py must keep OK: stewardship metadata schemas valid banner",
            errors,
        )
    if "stdlib-subset" not in text:
        fail(
            "check_stewardship_schema.py must retain stdlib-subset engine label",
            errors,
        )
    if "PyYAML" not in text:
        fail(
            "check_stewardship_schema.py must retain PyYAML engine label",
            errors,
        )
    bool_subclass = "bool is a subclass of " + "int"
    if bool_subclass not in text:
        fail(
            "check_stewardship_schema.py must keep bool is a subclass of int pin",
            errors,
        )
    if "match.group(1)" not in text:
        fail(
            "check_stewardship_schema.py first_yaml_block must return match.group(1)",
            errors,
        )
    missing_keys = "missing metadata " + "keys"
    if missing_keys not in text:
        fail(
            "check_stewardship_schema.py must emit missing metadata keys needle",
            errors,
        )
    if 'encoding="utf-8"' not in text and "encoding='utf-8'" not in text:
        fail(
            'check_stewardship_schema.py must read metadata with encoding="utf-8"',
            errors,
        )
    string_keys_head = 'STRING_KEYS = frozenset(\n    {\n        "status",'
    string_keys_head_sq = "STRING_KEYS = frozenset(\n    {\n        'status',"
    if string_keys_head not in text and string_keys_head_sq not in text:
        fail(
            'check_stewardship_schema.py must set STRING_KEYS frozenset starting with "status"',
            errors,
        )
    for sk in (
        '"edit_policy"',
        '"closes"',
        '"purpose"',
        '"version"',
        '"maintainer"',
        '"parent_governance"',
        '"repo"',
        '"surface"',
        '"last_updated"',
    ):
        if sk not in text and sk.replace('"', "'") not in text:
            fail(
                f"check_stewardship_schema.py STRING_KEYS must pin {sk}",
                errors,
            )
    second_pass_doc = "Second-pass: FENCED_YAML_RE " + "exact"
    if second_pass_doc not in text:
        fail(
            "check_stewardship_schema.py docstring must pin Second-pass: FENCED_YAML_RE exact",
            errors,
        )
    contract_fn = "check_stewardship_schema_gate_" + "contract"
    self_text = BADGE_GATE.read_text(encoding="utf-8")
    if f"def {contract_fn}(" not in self_text:
        fail(
            "check_badge_standard.py must provide " + contract_fn + "()",
            errors,
        )
    if contract_fn + "(" not in self_text.replace(f"def {contract_fn}(", "", 1):
        fail(
            "check_badge_standard.py main must call " + contract_fn + "()",
            errors,
        )


def check_wiki_outline_gate_contract(errors: list[str]) -> None:
    """Fail-close live wiki-outline gate wiring (after #90; deepen after #59/#43)."""
    if not WIKI_OUTLINE_GATE.is_file():
        fail("Missing scripts/check_wiki_outline.py (wiki-outline gate)", errors)
        return
    text = WIKI_OUTLINE_GATE.read_text(encoding="utf-8")
    # Publishable page set must stay aligned with docs/wiki/PUBLISH.md.
    for page in (
        "Home.md",
        "Overview.md",
        "Autonomy-Levels.md",
        "Repo-Stewardship.md",
        "Agent-Routing.md",
        "Security-Boundaries.md",
    ):
        if page not in text:
            fail(
                f"check_wiki_outline.py must list publishable page {page}",
                errors,
            )
    if "PUBLISH.md" not in text:
        fail(
            "check_wiki_outline.py must treat PUBLISH.md as operator-only",
            errors,
        )
    if "PUBLISHABLE_PAGES" not in text:
        fail(
            "check_wiki_outline.py must declare PUBLISHABLE_PAGES",
            errors,
        )
    if "PAGE_TOPIC_HINTS" not in text:
        fail(
            "check_wiki_outline.py must declare PAGE_TOPIC_HINTS",
            errors,
        )
    # Fail-closed after #43: live Autonomy-Levels covers L0–L3.
    for level in ("L0", "L1", "L2", "L3"):
        if f'"{level}"' not in text and f"'{level}'" not in text:
            fail(
                f"check_wiki_outline.py PAGE_TOPIC_HINTS must pin {level}",
                errors,
            )
    if '"credential"' not in text and "'credential'" not in text:
        fail(
            "check_wiki_outline.py PAGE_TOPIC_HINTS must pin credential "
            "on Security-Boundaries",
            errors,
        )
    if '"copilot"' not in text and "'copilot'" not in text:
        fail(
            "check_wiki_outline.py PAGE_TOPIC_HINTS must pin copilot "
            "on Agent-Routing",
            errors,
        )
    if "strip_fenced_code" not in text:
        fail(
            "check_wiki_outline.py must strip fenced code before link scan",
            errors,
        )
    if "has_dangerous_scheme" not in text:
        fail(
            "check_wiki_outline.py must reject dangerous link schemes",
            errors,
        )
    if "protocol-relative" not in text.lower():
        fail(
            "check_wiki_outline.py must reject protocol-relative // links",
            errors,
        )
    if '"//"' not in text and "'//'" not in text:
        fail(
            "check_wiki_outline.py must match protocol-relative // prefix",
            errors,
        )
    if "http://" not in text:
        fail(
            "check_wiki_outline.py must reject insecure http:// links",
            errors,
        )
    if "FORBIDDEN_BADGE_HINTS" not in text:
        fail(
            "check_wiki_outline.py must reject invent-product badge chrome "
            "via FORBIDDEN_BADGE_HINTS",
            errors,
        )
    if "STEWARDSHIP_CI_HINTS" not in text:
        fail(
            "check_wiki_outline.py must pin STEWARDSHIP_CI_HINTS",
            errors,
        )
    for needle in ("markdown-lint", "link-check", "stewardship-checks"):
        if needle not in text:
            fail(
                f"check_wiki_outline.py STEWARDSHIP_CI_HINTS must include {needle}",
                errors,
            )
    if "actionlint" not in text.lower():
        fail(
            "check_wiki_outline.py must require actionlint on Repo-Stewardship",
            errors,
        )
    if "invent" not in text.lower():
        fail(
            "check_wiki_outline.py must retain invent-product Home/stewardship pins",
            errors,
        )
    if "kill-switch" not in text.lower():
        fail(
            "check_wiki_outline.py must require Home kill-switch callout",
            errors,
        )
    if "scan_secrets" not in text:
        fail(
            "check_wiki_outline.py must scan wiki pages via scan_secrets",
            errors,
        )
    if "README_LINK_HINTS" not in text:
        fail(
            "check_wiki_outline.py must require Home README_LINK_HINTS",
            errors,
        )
    if "BADGE_STANDARD_HINTS" not in text:
        fail(
            "check_wiki_outline.py must require Home BADGE_STANDARD_HINTS",
            errors,
        )
    if "out of scope" not in text.lower():
        fail(
            "check_wiki_outline.py must require Home Out of scope section",
            errors,
        )
    # Fail-closed after #59: second-pass helper / constant / needle pins
    # (wiki-outline slice only; not relative / schema / badge / common / CI spam).
    if "OPERATOR_ONLY" not in text:
        fail(
            "check_wiki_outline.py must declare OPERATOR_ONLY",
            errors,
        )
    if 'OPERATOR_ONLY = "PUBLISH.md"' not in text and "OPERATOR_ONLY = 'PUBLISH.md'" not in text:
        fail(
            "check_wiki_outline.py must set OPERATOR_ONLY = \"PUBLISH.md\"",
            errors,
        )
    if '"docs"' not in text and "'docs'" not in text:
        fail(
            "check_wiki_outline.py WIKI must live under docs/",
            errors,
        )
    if '"wiki"' not in text and "'wiki'" not in text:
        fail(
            "check_wiki_outline.py WIKI must live under docs/wiki",
            errors,
        )
    if "_reject_invent_badge_chrome" not in text:
        fail(
            "check_wiki_outline.py must expose _reject_invent_badge_chrome helper",
            errors,
        )
    # Topic hint needles beyond L0–L3 / credential / copilot (first-pass).
    for topic in (
        "autonomy",
        "governance",
        "public",
        "kill",
        "secret",
        "surface",
        "routing",
        "run_stewardship_checks.sh",
        "badge",
    ):
        if f'"{topic}"' not in text and f"'{topic}'" not in text:
            fail(
                f"check_wiki_outline.py PAGE_TOPIC_HINTS must pin {topic}",
                errors,
            )
    if "](Home.md)" not in text:
        fail(
            "check_wiki_outline.py must require non-Home ](Home.md) backlinks",
            errors,
        )
    if "Unexpected markdown" not in text:
        fail(
            "check_wiki_outline.py must reject Unexpected markdown under docs/wiki/",
            errors,
        )
    if "Missing required wiki" not in text:
        fail(
            "check_wiki_outline.py must fail Missing required wiki source page",
            errors,
        )
    if "Wiki outline check FAILED" not in text:
        fail(
            "check_wiki_outline.py must print Wiki outline check FAILED",
            errors,
        )
    if "docs/wiki matches PUBLISH.md" not in text:
        fail(
            "check_wiki_outline.py must OK when docs/wiki matches PUBLISH.md",
            errors,
        )
    if 'strip("<>")' not in text and "strip('<>')" not in text:
        fail(
            "check_wiki_outline.py must strip angle brackets from targets",
            errors,
        )
    if r"!?\[" not in text and "!?[" not in text:
        fail(
            "check_wiki_outline.py link scan must match image links",
            errors,
        )
    if "Do **not** push" not in text and "Do not push" not in text:
        fail(
            "check_wiki_outline.py must require Do not push PUBLISH.md wording",
            errors,
        )
    readme_blob = (
        "https://github.com/fuzzywigg/agents-governance/blob/main/README.md"
    )
    if readme_blob not in text:
        fail(
            "check_wiki_outline.py README_LINK_HINTS must pin README blob URL",
            errors,
        )
    if "../badge-standard.md" not in text:
        fail(
            "check_wiki_outline.py BADGE_STANDARD_HINTS must pin ../badge-standard.md",
            errors,
        )
    for social in ("stars", "forks", "followers"):
        if f'"{social}"' not in text and f"'{social}'" not in text:
            fail(
                f"check_wiki_outline.py invent-chrome special-case must pin {social}",
                errors,
            )
    if "invent-product / social badge chrome" not in text:
        fail(
            "check_wiki_outline.py must emit invent-product / social badge chrome needle",
            errors,
        )
    if "| `Home.md` |" not in text and "|`Home.md`|" not in text:
        fail(
            "check_wiki_outline.py must require PUBLISH.md table row for Home.md",
            errors,
        )


    # Fail-closed after #90: third-pass helper / constant / needle pins
    # (wiki-outline slice only; not relative / schema / badge / common / CI
    # workflow / actionlint / markdownlint+lycheeignore pin spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    wiki_exact = 'WIKI = ROOT / "docs" / ' + '"wiki"'
    wiki_exact_sq = "WIKI = ROOT / 'docs' / " + "'wiki'"
    if wiki_exact not in text and wiki_exact_sq not in text:
        fail(
            "check_wiki_outline.py must set WIKI = ROOT / \"docs\" / \"wiki\"",
            errors,
        )
    removesuffix_pin = 'removesuffix(".md")'
    removesuffix_sq = "removesuffix('.md')"
    if removesuffix_pin not in text and removesuffix_sq not in text:
        fail(
            "check_wiki_outline.py must stem pages via removesuffix(\".md\")",
            errors,
        )
    glob_md = 'glob("*.md")'
    glob_md_sq = "glob('*.md')"
    if glob_md not in text and glob_md_sq not in text:
        fail(
            "check_wiki_outline.py must enumerate via glob(\"*.md\")",
            errors,
        )
    sorted_unexpected = "sorted(" + "unexpected)"
    if sorted_unexpected not in text:
        fail(
            "check_wiki_outline.py must sorted(unexpected) in Unexpected markdown fail",
            errors,
        )
    link_check_needle = '"Link Check"'
    link_check_sq = "'Link Check'"
    if link_check_needle not in text and link_check_sq not in text:
        fail(
            "check_wiki_outline.py must require PUBLISH.md Link Check acceptance",
            errors,
        )
    md_lint_needle = '"Markdown Lint"'
    md_lint_sq = "'Markdown Lint'"
    if md_lint_needle not in text and md_lint_sq not in text:
        fail(
            "check_wiki_outline.py must require PUBLISH.md Markdown Lint acceptance",
            errors,
        )
    no_secrets_needle = '"No secrets"'
    no_secrets_sq = "'No secrets'"
    if no_secrets_needle not in text and no_secrets_sq not in text:
        fail(
            "check_wiki_outline.py must require PUBLISH.md No secrets acceptance",
            errors,
        )
    invent_home = "invent-product out-of-scope " + "wording"
    if invent_home not in text:
        fail(
            "check_wiki_outline.py must emit invent-product out-of-scope wording needle",
            errors,
        )
    secrets_home = "secrets out-of-scope " + "wording"
    if secrets_home not in text:
        fail(
            "check_wiki_outline.py must emit secrets out-of-scope wording needle",
            errors,
        )
    kill_home = "kill-switch security " + "callout"
    if kill_home not in text:
        fail(
            "check_wiki_outline.py must emit kill-switch security callout needle",
            errors,
        )
    out_of_scope = "Out of scope " + "section"
    if out_of_scope not in text:
        fail(
            "check_wiki_outline.py must emit Out of scope section needle",
            errors,
        )
    relative_steward = "relative-link gate " + "coverage"
    if relative_steward not in text:
        fail(
            "check_wiki_outline.py must emit relative-link gate coverage needle",
            errors,
        )
    invent_steward = "no-invent-product stewardship " + "wording"
    if invent_steward not in text:
        fail(
            "check_wiki_outline.py must emit no-invent-product stewardship wording needle",
            errors,
        )
    actionlint_steward = "actionlint on existing workflow " + "paths"
    if actionlint_steward not in text:
        fail(
            "check_wiki_outline.py must emit actionlint on existing workflow paths needle",
            errors,
        )
    run_script_steward = "bash scripts/run_stewardship_" + "checks.sh"
    if run_script_steward not in text:
        fail(
            "check_wiki_outline.py must emit bash scripts/run_stewardship_checks.sh needle",
            errors,
        )
    startswith_slash = 'startswith("//")'
    startswith_slash_sq = "startswith('//')"
    if startswith_slash not in text and startswith_slash_sq not in text:
        fail(
            "check_wiki_outline.py must reject protocol-relative via startswith(\"//\")",
            errors,
        )
    startswith_http = 'startswith("http://")'
    startswith_http_sq = "startswith('http://')"
    if startswith_http not in text and startswith_http_sq not in text:
        fail(
            "check_wiki_outline.py must reject http via startswith(\"http://\")",
            errors,
        )
    if "match.group(2)" not in text:
        fail(
            "check_wiki_outline.py must read link targets via match.group(2)",
            errors,
        )
    if 'encoding="utf-8"' not in text and "encoding='utf-8'" not in text:
        fail(
            "check_wiki_outline.py must read wiki pages as utf-8",
            errors,
        )
    if "sys.exit(main())" not in text:
        fail(
            "check_wiki_outline.py must invoke sys.exit(main())",
            errors,
        )
    if "from stewardship_common import" not in text:
        fail(
            "check_wiki_outline.py must import from stewardship_common",
            errors,
        )
    for social in ("downloads", "discord", "twitter", "x.com"):
        if f'"{social}"' not in text and f"'{social}'" not in text:
            fail(
                f"check_wiki_outline.py invent-chrome special-case must pin {social}",
                errors,
            )
    if "shields.io" not in text:
        fail(
            "check_wiki_outline.py invent-chrome must match shields.io",
            errors,
        )
    if "[![" not in text:
        fail(
            "check_wiki_outline.py invent-chrome must match markdown badge [![",
            errors,
        )
    badge_lowered = '"badge" in ' + "lowered"
    badge_lowered_sq = "'badge' in " + "lowered"
    if badge_lowered not in text and badge_lowered_sq not in text:
        fail(
            "check_wiki_outline.py invent-chrome must gate social via badge in lowered",
            errors,
        )
    if '"../../README.md"' not in text and "'../../README.md'" not in text:
        fail(
            "check_wiki_outline.py README_LINK_HINTS must pin ../../README.md",
            errors,
        )
    if '"../README.md"' not in text and "'../README.md'" not in text:
        fail(
            "check_wiki_outline.py README_LINK_HINTS must pin ../README.md",
            errors,
        )
    if '"docs/badge-standard.md"' not in text and "'docs/badge-standard.md'" not in text:
        fail(
            "check_wiki_outline.py BADGE_STANDARD_HINTS must pin docs/badge-standard.md",
            errors,
        )
    badge_blob = (
        "https://github.com/fuzzywigg/agents-governance/blob/main/docs/badge-standard.md"
    )
    if badge_blob not in text:
        fail(
            "check_wiki_outline.py BADGE_STANDARD_HINTS must pin badge-standard blob URL",
            errors,
        )
    pages_operator_ok = "pages + operator " + "PUBLISH.md"
    if pages_operator_ok not in text:
        fail(
            "check_wiki_outline.py OK banner must report pages + operator PUBLISH.md",
            errors,
        )
    intentional_pin = "update PUBLISH.md page list if " + "intentional"
    if intentional_pin not in text:
        fail(
            "check_wiki_outline.py Unexpected markdown fail must keep intentional pin",
            errors,
        )
    for page_key in (
        "Autonomy-Levels.md",
        "Security-Boundaries.md",
        "Agent-Routing.md",
        "Overview.md",
        "Repo-Stewardship.md",
    ):
        if f'"{page_key}"' not in text and f"'{page_key}'" not in text:
            fail(
                f"check_wiki_outline.py PAGE_TOPIC_HINTS must key {page_key}",
                errors,
            )
    topic_get = "PAGE_TOPIC_HINTS.get(" + "name, ())"
    if topic_get not in text:
        fail(
            "check_wiki_outline.py must look up topics via PAGE_TOPIC_HINTS.get(name, ())",
            errors,
        )
    strip_call = "strip_fenced_code(" + "text)"
    if strip_call not in text:
        fail(
            "check_wiki_outline.py must call strip_fenced_code(text) before link scan",
            errors,
        )
    dangerous_call = "has_dangerous_scheme(" + "target)"
    if dangerous_call not in text:
        fail(
            "check_wiki_outline.py must call has_dangerous_scheme(target)",
            errors,
        )
    scan_path = "scan_secrets(path, " + "errors)"
    if scan_path not in text:
        fail(
            "check_wiki_outline.py must call scan_secrets(path, errors)",
            errors,
        )
    scan_publish = "scan_secrets(publish, " + "errors)"
    if scan_publish not in text:
        fail(
            "check_wiki_outline.py must call scan_secrets(publish, errors)",
            errors,
        )
    third_pass_doc = "Third-pass: WIKI exact / " + "removesuffix"
    if third_pass_doc not in text:
        fail(
            "check_wiki_outline.py docstring must keep Third-pass WIKI exact / removesuffix pin",
            errors,
        )
    if "def main" not in text:
        fail(
            "check_wiki_outline.py must expose def main",
            errors,
        )
    if "text.lower()" not in text:
        fail(
            "check_wiki_outline.py must use text.lower() for case-insensitive pins",
            errors,
        )
    present_set = "present - set(PUBLISHABLE_" + "PAGES)"
    if present_set not in text:
        fail(
            "check_wiki_outline.py must compute unexpected via present - set(PUBLISHABLE_PAGES)",
            errors,
        )
    operator_set = "{OPERATOR_" + "ONLY}"
    if operator_set not in text:
        fail(
            "check_wiki_outline.py unexpected set must subtract {OPERATOR_ONLY}",
            errors,
        )
    if "WIKI.is_dir()" not in text:
        fail(
            "check_wiki_outline.py must require WIKI.is_dir()",
            errors,
        )
    if "publish.is_file()" not in text:
        fail(
            "check_wiki_outline.py must gate PUBLISH checks via publish.is_file()",
            errors,
        )
    home_is_file = "home.is_" + "file()"
    if home_is_file not in text:
        fail(
            "check_wiki_outline.py must gate Home checks via home.is_file()",
            errors,
        )
    stewardship_is_file = "stewardship.is_" + "file()"
    if stewardship_is_file not in text:
        fail(
            "check_wiki_outline.py must gate Repo-Stewardship via stewardship.is_file()",
            errors,
        )
    len_pages = "len(PUBLISHABLE_" + "PAGES)"
    if len_pages not in text:
        fail(
            "check_wiki_outline.py OK banner must report len(PUBLISHABLE_PAGES)",
            errors,
        )
    missing_operator = "Missing operator page " + "{OPERATOR_ONLY}"
    # f-string form in source
    missing_operator_f = 'Missing operator page {OPERATOR_ONLY}'
    missing_operator_f2 = "Missing operator page {OPERATOR_ONLY}"
    if missing_operator_f not in text and missing_operator_f2 not in text:
        fail(
            "check_wiki_outline.py must emit Missing operator page OPERATOR_ONLY needle",
            errors,
        )
    contract_third = "third-pass after " + "#90"
    # also pin contract-side docstring via badge module reading itself? pin wiki module.
    if "third-pass after #90" not in text and contract_third not in text:
        fail(
            "check_wiki_outline.py docstring must keep third-pass after #90 pin",
            errors,
        )



def check_relative_link_gate_contract(errors: list[str]) -> None:
    """Fail-close live relative-link gate wiring (after #90; deepen after #55/#41)."""
    if not RELATIVE_LINK_GATE.is_file():
        fail("Missing scripts/check_relative_links.py (relative-link gate)", errors)
        return
    text = RELATIVE_LINK_GATE.read_text(encoding="utf-8")
    # Skip set must stay aligned with markdown-lint / lychee exclusions.
    if "OWASP-AGENTIC.md" not in text:
        fail(
            "check_relative_links.py must skip OWASP-AGENTIC.md (align markdown-lint)",
            errors,
        )
    if ".github" not in text or "agents" not in text:
        fail(
            "check_relative_links.py must skip .github/agents (align link-check)",
            errors,
        )
    if "node_modules" not in text:
        fail(
            "check_relative_links.py must skip node_modules in SKIP_PARTS",
            errors,
        )
    # Quoted ".git" only — bare .git also matches .github paths.
    if '".git"' not in text and "'.git'" not in text:
        fail(
            "check_relative_links.py must skip .git in SKIP_PARTS",
            errors,
        )
    if "strip_fenced_code" not in text:
        fail(
            "check_relative_links.py must strip fenced code before link scan",
            errors,
        )
    if "unquote" not in text and "fully_unquote" not in text:
        fail(
            "check_relative_links.py must percent-decode link targets (unquote)",
            errors,
        )
    if "fully_unquote" not in text:
        fail(
            "check_relative_links.py must fully_unquote nested percent-encoding",
            errors,
        )
    if '"//"' not in text and "'//'" not in text:
        fail(
            "check_relative_links.py must reject protocol-relative // links",
            errors,
        )
    if "github_slug" not in text:
        fail(
            "check_relative_links.py must resolve heading fragments via github_slug",
            errors,
        )
    if "ATX_HEADING_RE" not in text:
        fail(
            "check_relative_links.py must scan ATX headings for fragment checks",
            errors,
        )
    if "has_dangerous_scheme" not in text:
        fail(
            "check_relative_links.py must reject dangerous link schemes",
            errors,
        )
    if "empty fragment" not in text.lower():
        fail(
            "check_relative_links.py must reject empty path# fragments",
            errors,
        )
    if "query string" not in text.lower():
        fail(
            "check_relative_links.py must reject query strings on relative links",
            errors,
        )
    if "http://" not in text:
        fail(
            "check_relative_links.py must reject insecure http:// links",
            errors,
        )
    # Fail-closed after #55: second-pass helper / constant / allowlist pins
    # (relative-link slice only; not schema-scalar / badge / wiki / CI spam).
    if "MD_LINK_RE" not in text:
        fail(
            "check_relative_links.py must declare MD_LINK_RE for link/image scan",
            errors,
        )
    if "SKIP_PARTS" not in text:
        fail(
            "check_relative_links.py must declare SKIP_PARTS",
            errors,
        )
    if "SKIP_PREFIXES" not in text:
        fail(
            "check_relative_links.py must declare SKIP_PREFIXES",
            errors,
        )
    if "SKIP_FILES" not in text:
        fail(
            "check_relative_links.py must declare SKIP_FILES",
            errors,
        )
    if "_MAX_UNQUOTE_PASSES" not in text:
        fail(
            "check_relative_links.py must cap nested decode via _MAX_UNQUOTE_PASSES",
            errors,
        )
    if "_MAX_UNQUOTE_PASSES = 4" not in text and "_MAX_UNQUOTE_PASSES=4" not in text:
        fail(
            "check_relative_links.py must set _MAX_UNQUOTE_PASSES = 4",
            errors,
        )
    if "should_skip" not in text:
        fail(
            "check_relative_links.py must expose should_skip helper",
            errors,
        )
    if "iter_markdown" not in text:
        fail(
            "check_relative_links.py must expose iter_markdown helper",
            errors,
        )
    if "headings_in" not in text:
        fail(
            "check_relative_links.py must expose headings_in helper",
            errors,
        )
    if "def check_file" not in text:
        fail(
            "check_relative_links.py must expose check_file helper",
            errors,
        )
    if "mailto:" not in text:
        fail(
            "check_relative_links.py must allow mailto: targets",
            errors,
        )
    if "tel:" not in text:
        fail(
            "check_relative_links.py must allow tel: targets",
            errors,
        )
    # Require the human-readable NUL fail needle (not only the "\0" literal).
    if "NUL" not in text:
        fail(
            "check_relative_links.py must reject NUL in link targets",
            errors,
        )
    if r'"\0"' not in text and r"'\0'" not in text:
        fail(
            "check_relative_links.py must scan for NUL byte via \\0 literal",
            errors,
        )
    if 'strip("<>")' not in text and "strip('<>')" not in text:
        fail(
            "check_relative_links.py must strip angle brackets from targets",
            errors,
        )
    if r"!?\[" not in text and "!?[" not in text:
        fail(
            "check_relative_links.py MD_LINK_RE must match image links",
            errors,
        )
    if "escapes repo" not in text:
        fail(
            "check_relative_links.py must reject relative links that escape repo",
            errors,
        )
    if "broken relative link" not in text:
        fail(
            "check_relative_links.py must reject broken relative link targets",
            errors,
        )
    if "missing heading" not in text:
        fail(
            "check_relative_links.py must reject missing heading fragments",
            errors,
        )
    if "rglob" not in text:
        fail(
            "check_relative_links.py must rglob markdown files under ROOT",
            errors,
        )
    if "no markdown files found" not in text:
        fail(
            "check_relative_links.py must fail closed when no markdown files found",
            errors,
        )
    # Fail-closed after #83: third-pass helper / constant / needle pins
    # (relative-link slice only; not schema / badge / wiki / common / CI
    # workflow / actionlint pin spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    md_link_exact = (
        "MD_LINK_RE = re.compile(r\"!?\\[([^\\]]*)\\]\\(\\s*([^)\\s]*)"
        "(?:\\s+\\\"[^\\\"]*\\\")?\\s*\\)\")"
    )
    if md_link_exact not in text:
        fail(
            "check_relative_links.py must set MD_LINK_RE exact link/image pattern",
            errors,
        )
    atx_exact = (
        'ATX_HEADING_RE = re.compile(r"^(#{1,6})\\s+(.+?)\\s*$", re.MULTILINE)'
    )
    if atx_exact not in text:
        fail(
            "check_relative_links.py must set ATX_HEADING_RE exact #{1,6} MULTILINE",
            errors,
        )
    skip_parts_exact = 'SKIP_PARTS = {".git", "node_modules"}'
    skip_parts_sq = "SKIP_PARTS = {'.git', 'node_modules'}"
    skip_parts_alt = 'SKIP_PARTS = {"node_modules", ".git"}'
    if (
        skip_parts_exact not in text
        and skip_parts_sq not in text
        and skip_parts_alt not in text
    ):
        fail(
            'check_relative_links.py must set SKIP_PARTS = {".git", "node_modules"}',
            errors,
        )
    skip_files_exact = 'SKIP_FILES = {\n    "OWASP-AGENTIC.md",\n}'
    skip_files_one = 'SKIP_FILES = {"OWASP-AGENTIC.md"}'
    if skip_files_exact not in text and skip_files_one not in text:
        fail(
            'check_relative_links.py must set SKIP_FILES = {"OWASP-AGENTIC.md"}',
            errors,
        )
    skip_prefix_pin = 'Path(".github") / "agents"'
    skip_prefix_sq = "Path('.github') / 'agents'"
    if skip_prefix_pin not in text and skip_prefix_sq not in text:
        fail(
            'check_relative_links.py SKIP_PREFIXES must pin Path(".github") / "agents"',
            errors,
        )
    ok_banner = "OK: relative markdown links " + "resolve"
    if ok_banner not in text:
        fail(
            "check_relative_links.py must keep OK: relative markdown links resolve banner",
            errors,
        )
    failed_banner = "Relative link check " + "FAILED"
    if failed_banner not in text:
        fail(
            "check_relative_links.py must keep Relative link check FAILED banner",
            errors,
        )
    empty_needle = "empty relative link " + "target"
    if empty_needle not in text:
        fail(
            "check_relative_links.py must emit empty relative link target needle",
            errors,
        )
    http_needle = "insecure http:// link " + "(use https://)"
    if http_needle not in text:
        fail(
            "check_relative_links.py must emit insecure http:// link (use https://) needle",
            errors,
        )
    proto_needle = "protocol-relative link not " + "allowed"
    if proto_needle not in text:
        fail(
            "check_relative_links.py must emit protocol-relative link not allowed needle",
            errors,
        )
    dangerous_needle = "dangerous link " + "scheme"
    if dangerous_needle not in text:
        fail(
            "check_relative_links.py must emit dangerous link scheme needle",
            errors,
        )
    if 'encoding="utf-8"' not in text and "encoding='utf-8'" not in text:
        fail(
            "check_relative_links.py must read markdown as utf-8",
            errors,
        )
    if "as_posix()" not in text:
        fail(
            "check_relative_links.py should_skip must use as_posix()",
            errors,
        )
    md_suffix = 'dest.suffix.lower() == ".md"'
    md_suffix_sq = "dest.suffix.lower() == '.md'"
    if md_suffix not in text and md_suffix_sq not in text:
        fail(
            'check_relative_links.py must gate fragment checks on .md suffix',
            errors,
        )
    if "ValueError" not in text:
        fail(
            "check_relative_links.py must catch ValueError for repo escapes",
            errors,
        )
    if "sorted(" not in text:
        fail(
            "check_relative_links.py iter_markdown must sorted() results",
            errors,
        )
    if "re.UNICODE" not in text:
        fail(
            "check_relative_links.py github_slug must use re.UNICODE",
            errors,
        )
    space_dash = '.replace(" ", "-")'
    space_dash_sq = ".replace(' ', '-')"
    if space_dash not in text and space_dash_sq not in text:
        fail(
            'check_relative_links.py github_slug must replace spaces with "-"',
            errors,
        )
    percent_stable = "Percent-decode until " + "stable"
    if percent_stable not in text:
        fail(
            "check_relative_links.py fully_unquote must keep Percent-decode until stable pin",
            errors,
        )
    cap_nested = "Cap nested percent-" + "decoding"
    if cap_nested not in text and "%252e" not in text:
        fail(
            "check_relative_links.py must keep Cap nested percent-decoding / %252e pin",
            errors,
        )
    empty_parens = "Allow empty () so missing targets fail " + "closed"
    if empty_parens not in text and "missing targets fail closed" not in text:
        fail(
            "check_relative_links.py MD_LINK_RE must keep empty () fail-closed pin",
            errors,
        )
    if "sys.exit(main())" not in text:
        fail(
            "check_relative_links.py must invoke sys.exit(main())",
            errors,
        )
    if "from urllib.parse import unquote" not in text:
        fail(
            "check_relative_links.py must import unquote from urllib.parse",
            errors,
        )
    if "match.group(2)" not in text:
        fail(
            "check_relative_links.py must read link targets via match.group(2)",
            errors,
        )
    if 'startswith("#")' not in text and "startswith('#')" not in text:
        fail(
            "check_relative_links.py must handle same-file anchors via startswith('#')",
            errors,
        )
    if 'split("#", 1)' not in text and "split('#', 1)" not in text:
        fail(
            "check_relative_links.py must split fragments via split('#', 1)",
            errors,
        )
    if "files scanned" not in text:
        fail(
            "check_relative_links.py OK banner must report files scanned",
            errors,
        )
    if "from stewardship_common import" not in text:
        fail(
            "check_relative_links.py must import from stewardship_common",
            errors,
        )
    if r'\"[^\"]*\"' not in text and '"[^"]*"' not in text:
        fail(
            "check_relative_links.py MD_LINK_RE must allow title attributes",
            errors,
        )
    if "#{1,6}" not in text:
        fail(
            "check_relative_links.py ATX_HEADING_RE must pin #{1,6}",
            errors,
        )
    if r"[`*_~]" not in text and "[`*_~]" not in text:
        fail(
            "check_relative_links.py github_slug must strip punctuation [`*_~]",
            errors,
        )
    offline_doc = "Offline relative markdown link " + "integrity"
    if offline_doc not in text:
        fail(
            "check_relative_links.py module doc must keep Offline relative markdown link integrity",
            errors,
        )
    if "complements lychee" not in text:
        fail(
            "check_relative_links.py module doc must keep complements lychee pin",
            errors,
        )
    if "path.parent / target" not in text:
        fail(
            "check_relative_links.py must resolve via path.parent / target",
            errors,
        )
    if "fully_unquote(raw)" not in text:
        fail(
            "check_relative_links.py check_file must call fully_unquote(raw)",
            errors,
        )
    if "has_dangerous_scheme(raw)" not in text:
        fail(
            "check_relative_links.py check_file must call has_dangerous_scheme(raw)",
            errors,
        )
    third_pass_doc = "Third-pass: MD_LINK_RE+ATX_HEADING_RE " + "exact"
    if third_pass_doc not in text:
        fail(
            "check_relative_links.py docstring must keep Third-pass MD_LINK_RE+ATX exact pin",
            errors,
        )
    if "def main" not in text:
        fail(
            "check_relative_links.py must expose def main",
            errors,
        )
    if "relative_to(ROOT.resolve())" not in text and "relative_to(ROOT" not in text:
        fail(
            "check_relative_links.py must use relative_to(ROOT) for escape checks",
            errors,
        )


    if not RUN_STEWARDSHIP.is_file():
        fail("Missing scripts/run_stewardship_checks.sh", errors)
    else:
        run_text = RUN_STEWARDSHIP.read_text(encoding="utf-8")
        for gate in (
            "check_badge_standard.py",
            "check_wiki_outline.py",
            "check_stewardship_schema.py",
            "check_relative_links.py",
        ):
            if gate not in run_text:
                fail(
                    f"run_stewardship_checks.sh must invoke scripts/{gate}",
                    errors,
                )
        # Fail-closed: relative gate runs after schema (live order).
        badge_i = run_text.find("check_badge_standard.py")
        wiki_i = run_text.find("check_wiki_outline.py")
        schema_i = run_text.find("check_stewardship_schema.py")
        rel_i = run_text.find("check_relative_links.py")
        if min(badge_i, wiki_i, schema_i, rel_i) < 0 or not (
            badge_i < wiki_i < schema_i < rel_i
        ):
            fail(
                "run_stewardship_checks.sh must run gates in order: "
                "badge → wiki → schema → relative",
                errors,
            )


def check_badges(badges: list[re.Match[str]], errors: list[str]) -> None:
    if len(badges) != MAX_BADGES:
        fail(
            f"Badge row must have exactly {MAX_BADGES} badges "
            f"(Link Check, Markdown Lint, License); found {len(badges)}",
            errors,
        )

    labels = [m.group("label") for m in badges]
    if labels != list(REQUIRED_ORDER):
        fail(
            f"Badge labels must be in order {list(REQUIRED_ORDER)}; found {labels}",
            errors,
        )

    for match in badges:
        label = match.group("label")
        img = match.group("img")
        link = match.group("link")
        blob = f"{label}|{img}|{link}".lower()

        if not img.startswith("https://"):
            fail(f"Badge image for {label} must be https://", errors)
        if link.startswith("http://"):
            fail(f"Badge link for {label} must use https:// when absolute", errors)

        for hint in FORBIDDEN_BADGE_HINTS:
            if hint in blob:
                fail(f"Forbidden invent-product / social badge hint '{hint}' in {label}", errors)
        for hint in SECRET_URL_HINTS:
            if hint in blob:
                fail(f"Secret-like token in badge URL for {label}", errors)

        for url in (img, link):
            repo_match = REPO_FROM_GITHUB_RE.search(url) or REPO_FROM_SHIELDS_RE.search(url)
            if repo_match:
                found = f"{repo_match.group('owner')}/{repo_match.group('repo')}"
                if found.lower() != EXPECTED_REPO.lower():
                    fail(
                        f"Badge URL repo slug must be {EXPECTED_REPO}; found {found} in {label}",
                        errors,
                    )

        if label == "Link Check":
            if "actions/workflows/link-check.yml/badge.svg" not in img:
                fail("Link Check image must use link-check.yml/badge.svg", errors)
            if "actions/workflows/link-check.yml" not in link:
                fail("Link Check link must target link-check.yml workflow", errors)
            if not link.startswith("https://"):
                fail("Link Check badge link must be an absolute https:// workflow URL", errors)
        elif label == "Markdown Lint":
            if "actions/workflows/markdown-lint.yml/badge.svg" not in img:
                fail("Markdown Lint image must use markdown-lint.yml/badge.svg", errors)
            if "actions/workflows/markdown-lint.yml" not in link:
                fail("Markdown Lint link must target markdown-lint.yml workflow", errors)
            if not link.startswith("https://"):
                fail("Markdown Lint badge link must be an absolute https:// workflow URL", errors)
        elif label == "License":
            shields_ok = "img.shields.io/github/license/" in img
            if not shields_ok:
                fail("License image must use img.shields.io/github/license/<owner>/<repo>", errors)
            if EXPECTED_REPO not in img:
                fail(
                    f"License shields image must include repo slug {EXPECTED_REPO}",
                    errors,
                )
            license_link_ok = link.endswith("/LICENSE") or link in {"LICENSE", "./LICENSE"}
            if not license_link_ok:
                fail("License badge link must point at LICENSE (relative or blob URL)", errors)
        else:
            fail(f"Unexpected badge label {label!r} (only {list(REQUIRED_ORDER)} allowed)", errors)


def main() -> int:
    errors: list[str] = []
    # Fail-closed after #48: self-contract first so helper renames fail closed
    # (report pin drift) instead of NameError mid-run.
    check_badge_standard_gate_contract(errors)
    # Fail-closed after #75: actionlint-style contract early (same self-host file)
    # so style-helper renames / needle drift fail closed before NameError.
    check_actionlint_style_gate_contract(errors)
    # Fail-closed after #100: docs-lint contract early (lycheeignore + markdownlint).
    check_docs_lint_gate_contract(errors)
    if errors:
        print("Badge standard check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if not README.is_file():
        print("FAIL: README.md missing", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    check_workflows_and_license(errors)
    check_lycheeignore(errors)
    check_workflow_hardening(errors)
    check_actionlint_style(errors)
    check_relative_link_gate_contract(errors)
    check_wiki_outline_gate_contract(errors)
    check_stewardship_schema_gate_contract(errors)
    check_stewardship_common_contract(errors)
    if BADGE_STANDARD.is_file():
        check_badge_standard_doc(errors)
        scan_secrets(BADGE_STANDARD, errors)
    check_readme_consistency(text, errors)
    check_contributing_and_agents(errors)
    scan_secrets(README, errors)
    badges, row_errors = extract_badge_row(text)
    errors.extend(row_errors)
    if badges:
        check_badges(badges, errors)

    if errors:
        print("Badge standard check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: README badge row matches docs/badge-standard.md ({', '.join(REQUIRED_ORDER)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
