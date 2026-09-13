#!/usr/bin/env python3
"""Enforce docs/badge-standard.md against README.md (executable gate)."""

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


def check_lycheeignore(errors: list[str]) -> None:
    """Keep flaky badge CDN out of lychee; license badge stays in stewardship."""
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
    # Do not quietly drop fail-closed posture by ignoring everything.
    if text.strip() == "*" or "https://*" in text or "http://*" in text:
        fail(
            ".lycheeignore must not exclude all http(s) targets "
            "(https://* / http://* / bare *)",
            errors,
        )


def check_actionlint_style(errors: list[str]) -> None:
    """Static actionlint-like checks on existing workflow paths only."""
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
    if "actionlint" not in stew.lower():
        fail(
            "stewardship-checks.yml must run actionlint on existing workflow paths",
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
        ):
            if needle not in text:
                fail(f"AGENTS.md §3 / testing must mention {needle}", errors)
        scan_secrets(AGENTS, errors)
    else:
        fail("Missing AGENTS.md", errors)


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
    if not README.is_file():
        print("FAIL: README.md missing", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    check_workflows_and_license(errors)
    check_lycheeignore(errors)
    check_workflow_hardening(errors)
    check_actionlint_style(errors)
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
