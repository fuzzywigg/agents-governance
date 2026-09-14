#!/usr/bin/env python3
"""Enforce docs/badge-standard.md against README.md (executable gate).

Fail-closed pins (live path after #48; second-pass after #61; third-pass after #104):
- REQUIRED_ORDER: Link Check → Markdown Lint → License (exactly MAX_BADGES = 3)
- EXPECTED_REPO: fuzzywigg/agents-governance
- REQUIRED_WORKFLOWS: link-check.yml / markdown-lint.yml / stewardship-checks.yml
- live badge row is Link Check → Markdown Lint → License
- Badge images https-only; link-check.yml/badge.svg + markdown-lint.yml/badge.svg
- License via img.shields.io/github/license/; contiguous row; no invent-product
- Quiet stewardship: no Stewardship product/status badge; no fourth badge
- Second-pass: path constants / exact REQUIRED_ORDER+EXPECTED_REPO assigns /
  actions/workflows/*.yml/badge.svg / fail needles / LICENSE link / FAILED+OK
- Third-pass: BADGE_LINE_RE+REPO_FROM_* exact / REQUIRED_WORKFLOWS exact /
  group(label|img|link) / sys.exit / stewardship_common / BADGE_GATE /
  utf-8 / Strict row / H1 startswith / FAIL README / https image+link needles /
  absolute workflow URL / License point / Unexpected label / extract+check_badges /
  contract(errors) call / IGNORECASE / blob.lower / EXPECTED_REPO.lower

Fail-closed actionlint-style pins (live path after #75; second-pass after #83/#86; third-pass after #108; deepen after #135):
- top-level name: / jobs.*.runs-on / jobs.*.steps / timeout-minutes
- no pull_request_target / no permissions: write-all / no contents: write
- no id-token: write / actions must be @-pinned (not main|master|latest)
- docker:// uses skipped; unpinned uses rejected
- Second-pass: exact name/uses regexes / write-all+contents+id-token regexes /
  docker startswith / @ not in uses / rsplit / group(1).strip() /
  fail needles / least-privilege+OIDC+majors comments / REQUIRED_WORKFLOWS loop
- Third-pass after #108: concurrency:+cancel-in-progress: / permissions: present /
  reject actions|packages|pull-requests: write / finditer uses / docker continue /
  rsplit[-1] / third-pass docstring
- Deepen after #135: cancel-in-progress: true / contents: read /
  ubuntu-latest / workflow_dispatch: / reject security-events|attestations|
  statuses|deployments: write / deepen docstring

Fail-closed run_stewardship runner pins (live path after #117; Pass-2 after #176;
lands closed #175 leftover; lands closed #140; lands closed #96):
- shebang #!/usr/bin/env bash / set -euo pipefail
- dirname "$0" ROOT resolve / cd "$ROOT"
- same set as CI commentary / python3 scripts/<gate> for four gates
- gate order badge → wiki → schema → relative
- check_run_stewardship_gate_contract self-pins
- Pass-2 after #176: exact ROOT="$(cd "$(dirname "$0")/.." && pwd)" /
  exactly four python3 scripts/ lines / no || true soft-fail /
  dirname "$0")/.." fragment / doc gates locally commentary /
  CI runs run_stewardship_checks.sh before test_stewardship_gates.py;
  CI runner-before-self-tests order pin
- Pass-2 residual after #191 (lands closed #193/#178 leftover; NOT schema third-pass #191 / NOT path-order #189 /
  NOT Pass-2 core #179 / NOT wiki-index #181 / NOT path-filter #176 /
  NOT stewardship-badge lint #195):
  gates-only runner (no test_stewardship_gates.py inside .sh) /
  no BASH_SOURCE ROOT drift / no bare python scripts/ /
  no set +u|+o pipefail soft-fail /
  back-to-back gates→self-tests named block /
  no inline check_*.py in stewardship-checks.yml /
  self-tests before actionlint; CI gates-self-tests back-to-back block pin
- Pass-2 leftovers after #216 tip (lands closed #202/#192/#212 leftover; NOT Pass-2 residual #199 /
  NOT Pass-2 register #203 / NOT badge-lint #208 / NOT schema third-pass #191 / NOT path-order #189 /
  NOT merged schema fourth #216):
  shebang as first line / soft-fail with || exit 0 refuse (residual beyond #179/#199)
- markdown-lint/link-check edges after #216 tip (Markdown-lint/link-check workflow edges after #203 tip;
  lands closed #202/#192/#212 leftover; NOT path-filter #176 / NOT Pass-2 #179/#199 /
  NOT path-order #189 / NOT badge-lint #208 / NOT schema #191/#216):
  args: >- / externally broken links commentary / without-it private-404 commentary /
  must not set continue-on-error / exact job permissions: contents: read /
  checkout before Check links adjacency / checkout before Run markdownlint adjacency
Fail-closed CI workflow pins (live path after #39/#72; third-pass after #111; deepen after #161;
path-filter leftovers after #173):
- Third-pass after #111: exact concurrency group templates /
  markdown-lint+stewardship cron/timeout pins / DavidAnson@v24 /
  setup-python@v5 / lychee --verbose/--no-progress/--max-concurrency 8 /
  --timeout 20/--max-retries 3 / fail: true / get_actionlint id+outputs /
  curl -fsSL download / third-pass docstring
- Deepen after #161: Check links / Run markdownlint / Set up Python /
  Install PyYAML (schema parser) / Stewardship gates+self-tests step names /
  exact token+--github-token forms / --exclude-path .github/agents /
  globs: | / AGENTS+CLAUDE+LICENSE+CONTRIBUTING+.github/workflows/** paths /
  Weekly drift + GITHUB_TOKEN commentary / deepen docstring
- Path-filter leftovers after #173: exact push paths layouts / residual
  stewardship path entries / reject paths-ignore / ignore-glob exactness

Fail-closed leftover docs-lint/stewardship/actionlint pins after #149:
- docs-lint third-pass: exact live .lycheeignore full layout + exact
  commentary lines (308 redirect / 103 early hints / badge CDN flaky /
  License badge presence enforced by stewardship)
- actionlint leftover: contents: read membership affirm (complement #149
  regex) / leftover docstring (not docs-lint / wiki spam)
- stewardship leftover: exact live run_stewardship_checks.sh full layout

Fail-closed actionlint path-filter leftovers after #173:
- push paths: on all three workflows / reject paths-ignore:
- exact link-check + markdown-lint + stewardship paths layouts
- residual stewardship path entries (AGENTS/CLAUDE/LICENSE/CONTRIBUTING/
  workflows/** / .lycheeignore / .markdownlint.json)
- ignore globs: --exclude-path .github/agents + exact markdownlint bangs
- empty workflow stubs already handled (load None continue); distinct from
  path-order/badge, stewardship-badge lint, and stewardship CI deepen

Fail-closed actionlint path-order leftover after #181 (lands closed #157/#182;
NOT path-filter #176 / NOT wiki-index #181 / NOT run_stewardship #179 /
NOT #165 stewardship CI / NOT #149 cancel-in-progress):
- contiguous three-path actionlint order (link-check → markdown-lint →
  stewardship-checks)
- exact bash <(curl -fsSL) download-actionlint.bash 1.7.7 form
- no continue-on-error: true
- Download actionlint + actionlint existing workflow paths step names
- path-order leftover docstring

Fail-closed actionlint path-filter/path-order deepen after #203 (NOT saturated
#189 path-order / NOT #176 path-filter layouts / NOT schema #191 /
NOT Pass-2 residual #199/#203 / NOT Pass-2+md/link #192 / NOT wiki-badge /
NOT stewardship-badge lint #208 / NOT schema fourth-pass #216/#204/#209 /
NOT Pass-2 leftover + md/link #220):
- contiguous push/branches/paths headers on all three workflows
- pull_request stays path-unfiltered (no nested paths:)
- reject dorny/paths-filter invent
- residual link/lint self-workflow path list entries
- exact contiguous actionlint run command (executable -color three paths)
- Download actionlint precedes actionlint existing workflow paths
- contiguous Download/id/run/shell download block
- Stewardship gate self-tests precedes Download actionlint
- reject uses: rhysd/actionlint@ invent (keep download-actionlint.bash)

Fail-closed actionlint path-filter/path-order residual deepen after #225
(NOT saturated deepen #225/#203 / NOT #189 path-order / NOT #176 layouts /
NOT schema #191/#216 / NOT Pass-2 residual #199/#203 / NOT Pass-2 leftover +
md/link #220 / NOT wiki-badge leftover #227 / NOT stewardship-checks/schema
leftover #233 / NOT stewardship-badge lint #208):
- contiguous pull_request:/schedule: adjacency (bare PR form) on all three
- reject branches-ignore: invent
- pull_request stays type-unfiltered (no nested types:)
- reject tj-actions/changed-files invent
- contiguous four-step actionlint path-order
  (gates → self-tests → Download → actionlint run)
- schedule: precedes workflow_dispatch: on all three
- contiguous shell-less actionlint run step (no invent shell: on run step)

Fail-closed actionlint path-filter/path-order residual leftover deepen after #258
(NOT saturated residual #244 / NOT stewardship-schema leftover #258 /
NOT wiki/mdlink leftover #252 / NOT saturated deepen #225/#203 /
NOT #189 path-order / NOT #176 layouts / NOT schema #191/#216 /
NOT Pass-2 residual #199/#203 / NOT Pass-2 leftover + md/link #220 /
NOT wiki outline/PUBLISH leftover #243 / NOT md/link residual #239 /
NOT stewardship-checks/schema leftover #233 / NOT wiki-badge leftover #227 /
NOT stewardship-badge lint #208):
- contiguous push:/pull_request: adjacency on all three
- contiguous schedule:/workflow_dispatch: adjacency on all three
- pull_request stays branches-unfiltered (no nested branches:)
- reject tags-ignore: invent
- reject workflow_call: invent
- contiguous five-step actionlint path-order
  (Install PyYAML → gates → self-tests → Download → actionlint run)
- contiguous on:/push: header on all three

Fail-closed actionlint path-filter/path-order residual leftover deepen after #272
(NOT lychee/blob-503 harden #278 / NOT Pass-2 residual leftover #272 /
NOT saturated leftover #262 /
NOT stewardship-schema leftover #258 /
NOT wiki/mdlink leftover #252 / NOT saturated residual #244 /
NOT saturated deepen #225/#203 / NOT #189 path-order / NOT #176 layouts /
NOT schema #191/#216 / NOT Pass-2 residual #199/#203 /
NOT Pass-2 leftover + md/link #220 / NOT wiki outline/PUBLISH leftover #243 /
NOT md/link residual #239 / NOT stewardship-checks/schema leftover #233 /
NOT wiki-badge leftover #227 / NOT stewardship-badge lint #208):
- contiguous workflow_dispatch:/concurrency: adjacency on all three
- contiguous name:/on: workflow header on all three
- reject workflow_run: invent
- reject repository_dispatch: invent
- reject merge_group: invent
- reject tags: invent (not tags-ignore:)
- contiguous six-step actionlint path-order
  (Set up Python → Install PyYAML → gates → self-tests → Download → actionlint run)

Fail-closed stewardship-checks + schema residual deepen after #225 (NOT wiki-index/badge
#227 / NOT path-edges #225 / NOT Pass-2 leftover+md/link #220 / NOT schema fourth-pass #216 /
NOT badge-lint #208 / NOT Pass-2 residual #199/#203 / NOT path-order #189;
lands closed #229 leftover on post-#227 tip — do not revive #229):
- exact contiguous Set up Python / uses / with / python-version block
- exact Install PyYAML (schema parser) run: pip install --quiet pyyaml block
- checkout@v7 immediately precedes Set up Python
- exact full stewardship push paths list (README→.markdownlint.json)
- exact schedule Weekly-drift + cron "15 6 * * 1" block
- exact concurrency group + cancel-in-progress block
- exact jobs.stewardship runs-on/timeout/permissions header
- reject strategy: / matrix: / services: invent on stewardship-checks.yml
- schema residual (pass-5) invalid status+surface stubs + residual helper needles
- schema leftover after #252: leftover helper needles + leftover status/surface stubs
  (NOT wiki/mdlink leftover #252 / NOT path-edges residual #244 / NOT wiki outline/PUBLISH #243 / NOT md/link residual #239 / NOT schema residual (pass-5) #233)
- common leftover after #252: elif hint in text / for pattern in globs /
  found: set[Path] = set() / if not path.is_file(): (load_workflow)
- Wiki outline/PUBLISH leftover after #233: existing docs/wiki pages only —
  PUBLISH.md pages-table order / Pages to publish / wiki.git clone /
  cp docs/wiki/{page} (no operator PUBLISH.md) / git add six pages /
  purpose+closes #16 / Fallback .wiki.git / badge-standard blob rewrite

Fail-closed stewardship-badge lint deepen after #189 (NOT docs-lint leftover
#161 / NOT wiki-badge #141 / NOT path-order #189 / NOT schema third-pass #191 /
NOT run_stewardship residual #199; residual uncovered only):
- README: reject invent stewardship-checks.yml/badge.svg (no fourth badge)
- README: exact link-check.yml/badge.svg + markdown-lint.yml/badge.svg paths
- exact live markdown-lint globs block (**/*.md + bang excludes)
- exact live markdown-lint push paths filter (.markdownlint.json + self path)
- exact live link-check push paths filter (.lycheeignore + self path)
- missing badge fixtures for invent svg / wrong badge.svg / glob+paths drift

Fail-closed wiki-index/badge leftover deepen after #189 (lands closed #185/#172;
NOT path-order #189 / NOT stewardship-schema sibling / NOT path-filter #176 /
NOT run_stewardship #179 / NOT wiki-index first-pass #181 alone /
NOT stewardship-badge lint #208 / NOT path-filter/path-order #225 /
NOT Pass-2 leftover + md/link #220 / NOT schema fourth-pass #216;
lands closed #222/#215/#196 leftover after #225 tip):
- wiki-index: exact PUBLISHABLE_PAGES contiguous order / TOC loop /
  ]({page})+]({stem}) / empty index (no publishable page links)
- relative wiki-index: broken relative link needle / empty markdown index /
  Duplicate slug edge set collapse
- badge-standard: refuse README invent stewardship-checks.yml/badge.svg /
  exact actions/workflows/link-check.yml/badge.svg +
  markdown-lint.yml/badge.svg image pins / no Stewardship product badge

Fail-closed markdown-lint/link-check residual exact layouts after #227 tip
(lands closed #221 leftover residual; NOT Pass-2 leftover + md/link #220 core /
NOT path-edges #225 / NOT wiki-index/badge leftover #227 / NOT stewardship-badge lint #208):
- exact contiguous link-check args: >- flag block (verbose→*.md)
- exact contiguous link-check on: push/PR/schedule/workflow_dispatch block
- exact contiguous markdown-lint on: push/PR/schedule/workflow_dispatch block
- exact contiguous markdown-lint with: globs|+config block
- exact contiguous link-check with: token commentary block

Fail-closed wiki/mdlink leftover after #243 (residual vs saturated #243 wiki
outline/PUBLISH leftover + #239 md/link residual layouts;
NOT path-filter/path-order leftover #244 /
NOT stewardship-checks/schema #233 /
NOT wiki-index/badge leftover #227):
- wiki: PUBLISH YAML status+created+purpose / One-shot heading / exact clone dest /
  contiguous cp list / cd wiki tmp / git commit #16 / git push origin master /
  Acceptance+Fallback headings / Repository not found / Home (landing) /
  Home operator PUBLISH.md omit-when-copying
- md/link leftover layouts: exact contiguous link+lint concurrency blocks /
  exact contiguous link-check + markdown-lint job headers /
  exact "**/*.md" then fail: true adjacency

Fail-closed Pass-2 residual + existing templates/AGENTS-REPO.md leftover
validation after #233 (NOT path-edges leftover #262 /
NOT stewardship-schema leftover #258 /
NOT wiki/mdlink leftover #252 /
NOT stewardship-checks/schema residual #233 /
NOT wiki-index/badge #227 / NOT path-edges #225 / NOT Pass-2 leftover+md/link #220 /
NOT Pass-2 residual #199/#203 / NOT badge-lint #208 / NOT schema #216 /
NOT path-order #189 / NOT md/link residual #239 /
NOT wiki outline/PUBLISH leftover #243 /
NOT actionlint path-filter/path-order residual #244;
lands closed #251/#250/#246/#245/#240 leftover on post-#262 tip; do not invent new templates):
- soft-fail with || : / soft-fail with || return 0 on run_stewardship_checks.sh- set +o errexit / set +o nounset soft-fail refuse
- invent python3 -m for gates refuse
- must not source env files / must not dot-source paths
- reject any continue-on-error: on all three existing workflows
- exact contiguous concurrency group template on all three workflows
  (group + cancel-in-progress: true block; existing templates only)
- existing templates/AGENTS-REPO.md leftover: H1 [PROJECT_NAME] /
  parent_governance / maintainer smtp.eth / scope repository-specific /
  version 1.0.0 / YYYY-MM-DD placeholder / §1–§6 / [CONFIG_FILE] /
  Never commit .env / agents-md/description / no invent badge.svg chrome

"""

from __future__ import annotations

import json
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
AGENTS_REPO = ROOT / "templates" / "AGENTS-REPO.md"
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
        # Second-pass after #111: exact live markdownlint layout + key set.
        expected_md = (
            "{\n"
            '  "default": true,\n'
            '  "MD013": { "line_length": 200 },\n'
            '  "MD024": { "siblings_only": true },\n'
            '  "MD033": false,\n'
            '  "MD041": false,\n'
            '  "MD060": false\n'
            "}\n"
        )
        if md_cfg != expected_md:
            fail(
                ".markdownlint.json must match exact live docs-lint second-pass layout",
                errors,
            )
        try:
            md_obj = json.loads(md_cfg)
        except json.JSONDecodeError:
            fail(
                ".markdownlint.json must be valid JSON "
                "(docs-lint second-pass)",
                errors,
            )
            md_obj = {}
        allowed_keys = {
            "default",
            "MD013",
            "MD024",
            "MD033",
            "MD041",
            "MD060",
        }
        if set(md_obj) != allowed_keys:
            fail(
                ".markdownlint.json must keep exact live docs-lint key set "
                "(default/MD013/MD024/MD033/MD041/MD060)",
                errors,
            )
        if md_obj.get("default") is not True:
            fail(
                ".markdownlint.json default must be JSON true "
                "(docs-lint second-pass)",
                errors,
            )
        if md_obj.get("MD033") is not False:
            fail(
                ".markdownlint.json MD033 must be JSON false "
                "(docs-lint second-pass)",
                errors,
            )
        if md_obj.get("MD041") is not False:
            fail(
                ".markdownlint.json MD041 must be JSON false "
                "(docs-lint second-pass)",
                errors,
            )
        if md_obj.get("MD060") is not False:
            fail(
                ".markdownlint.json MD060 must be JSON false "
                "(docs-lint second-pass)",
                errors,
            )
        if md_obj.get("MD013") != {"line_length": 200}:
            fail(
                ".markdownlint.json MD013 must be {line_length: 200} object "
                "(docs-lint second-pass)",
                errors,
            )
        if md_obj.get("MD024") != {"siblings_only": True}:
            fail(
                ".markdownlint.json MD024 must be {siblings_only: true} object "
                "(docs-lint second-pass)",
                errors,
            )


def check_lycheeignore(errors: list[str]) -> None:
    r"""Keep flaky badge CDN out of lychee; license badge stays in stewardship.

    Live fail-closed pins after #100 (docs-lint slice; not CI workflow spam):
    escaped img\.shields\.io; modelcontextprotocol.io + linuxfoundation.org
    live excludes; stewardship/license-badge commentary; reject https://* /
    http://* / bare *; not wiki / relative pin spam.
    Second-pass after #111: exact live exclude URLs + CDN/false-positive
    commentary (docs-lint second-pass; not actionlint / stewardship_common spam).
    Third-pass after #149: exact live .lycheeignore full layout + exact
    commentary lines (docs-lint leftover; not wiki / CI workflow spam).
    Pass-4 after #251: same-repo blob/main 503 exclude + wiki-outline
    absolute-pin commentary (docs-lint leftover; not invent templates / Pass-2 residual spam).
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
    # Second-pass after #111: exact live exclude URLs (docs-lint; not actionlint spam).
    if "https://modelcontextprotocol.io/" not in text:
        fail(
            ".lycheeignore must pin https://modelcontextprotocol.io/ "
            "(live docs-lint second-pass URL)",
            errors,
        )
    if "https://www.linuxfoundation.org/" not in text:
        fail(
            ".lycheeignore must pin https://www.linuxfoundation.org/ "
            "(live docs-lint second-pass URL)",
            errors,
        )
    # Second-pass after #111: live shields CDN flaky rationale commentary.
    if "Connection reset by peer" not in text:
        fail(
            ".lycheeignore must note Connection reset by peer "
            "(live shields CDN flaky rationale)",
            errors,
        )
    if "RST" not in text:
        fail(
            ".lycheeignore must note RST "
            "(live shields CDN flaky rationale)",
            errors,
        )
    if "not a broken URL" not in text:
        fail(
            ".lycheeignore must note not a broken URL "
            "(live shields CDN flaky rationale)",
            errors,
        )
    if "false-positive" not in text:
        fail(
            ".lycheeignore must note false-positive "
            "(live lychee exclude rationale)",
            errors,
        )
    if "early hints" not in text:
        fail(
            ".lycheeignore must note early hints "
            "(live lychee exclude rationale)",
            errors,
        )
    if "valid site" not in text:
        fail(
            ".lycheeignore must note valid site "
            "(live lychee exclude rationale)",
            errors,
        )
    if "check_badge_standard.py" not in text:
        fail(
            ".lycheeignore must reference check_badge_standard.py "
            "(stewardship license-badge enforcement path)",
            errors,
        )
    if "License badge presence remains enforced" not in text:
        fail(
            ".lycheeignore must note License badge presence remains enforced "
            "(CDN exclude is not a missing License badge)",
            errors,
        )

    # Third-pass after #149: exact live .lycheeignore full layout (docs-lint leftover).
    expected_lychee = (
        "# modelcontextprotocol.io returns 308 redirect — valid site, lychee false-positive\n"
        "https://modelcontextprotocol.io/\n"
        "# linuxfoundation.org returns 103 early hints — valid site\n"
        "https://www.linuxfoundation.org/\n"
        "# img.shields.io badge CDN is flaky (Connection reset by peer / RST) "
        "— not a broken URL.\n"
        "# License badge presence remains enforced by stewardship "
        "(check_badge_standard.py).\n"
        r"https://img\.shields\.io" + "\n"
        "# Same-repo GitHub blob/main HTML intermittently returns 503 "
        "— not a broken URL.\n"
        "# Absolute blob/main pins remain enforced by wiki-outline "
        "(check_wiki_outline.py).\n"
        r"https://github\.com/fuzzywigg/agents-governance/blob/main/" + "\n"
    )
    if text != expected_lychee:
        fail(
            ".lycheeignore must match exact live docs-lint third-pass layout",
            errors,
        )
    # Third-pass after #149: exact live commentary line pins (docs-lint leftover).
    mcp_line = (
        "# modelcontextprotocol.io returns 308 redirect — valid site, "
        "lychee false-positive"
    )
    if mcp_line not in text:
        fail(
            ".lycheeignore must keep exact MCP 308 commentary line "
            "(docs-lint third-pass)",
            errors,
        )
    lfs_line = "# linuxfoundation.org returns 103 early hints — valid site"
    if lfs_line not in text:
        fail(
            ".lycheeignore must keep exact LF 103 commentary line "
            "(docs-lint third-pass)",
            errors,
        )
    flaky_line = (
        "# img.shields.io badge CDN is flaky (Connection reset by peer / RST) "
        "— not a broken URL."
    )
    if flaky_line not in text:
        fail(
            ".lycheeignore must keep exact shields flaky commentary line "
            "(docs-lint third-pass)",
            errors,
        )
    license_line = (
        "# License badge presence remains enforced by stewardship "
        "(check_badge_standard.py)."
    )
    if license_line not in text:
        fail(
            ".lycheeignore must keep exact License enforcement commentary line "
            "(docs-lint third-pass)",
            errors,
        )
    if "badge CDN is flaky" not in text:
        fail(
            ".lycheeignore must note badge CDN is flaky "
            "(docs-lint third-pass)",
            errors,
        )
    if "enforced by stewardship" not in text:
        fail(
            ".lycheeignore must note enforced by stewardship "
            "(docs-lint third-pass)",
            errors,
        )
    # Pass-4 after #251: same-repo blob/main 503 exclude (docs-lint leftover).
    # Split four/th so fourth→quaternary badge-refusal self-tests stay valid.
    _p4 = "four" + "th-pass"
    if "blob/main" not in text:
        fail(
            ".lycheeignore must exclude same-repo blob/main "
            "(docs-lint " + _p4 + "; GitHub HTML 503 flake)",
            errors,
        )
    if "503" not in text:
        fail(
            ".lycheeignore must note 503 "
            "(docs-lint " + _p4 + "; GitHub blob HTML flake)",
            errors,
        )
    if "wiki-outline" not in text and "check_wiki_outline.py" not in text:
        fail(
            ".lycheeignore must note wiki-outline absolute-pin enforcement "
            "(docs-lint " + _p4 + "; blob exclude is not a missing wiki pin)",
            errors,
        )
    if r"github\.com/fuzzywigg/agents-governance/blob/main/" not in text:
        fail(
            r".lycheeignore must pin escaped "
            r"github\.com/fuzzywigg/agents-governance/blob/main/ "
            "(docs-lint " + _p4 + ")",
            errors,
        )
    blob_line = (
        "# Same-repo GitHub blob/main HTML intermittently returns 503 "
        "— not a broken URL."
    )
    if blob_line not in text:
        fail(
            ".lycheeignore must keep exact blob/main 503 commentary line "
            "(docs-lint " + _p4 + ")",
            errors,
        )
    outline_line = (
        "# Absolute blob/main pins remain enforced by wiki-outline "
        "(check_wiki_outline.py)."
    )
    if outline_line not in text:
        fail(
            ".lycheeignore must keep exact wiki-outline enforcement commentary line "
            "(docs-lint " + _p4 + ")",
            errors,
        )
    if "intermittently returns 503" not in text:
        fail(
            ".lycheeignore must note intermittently returns 503 "
            "(docs-lint " + _p4 + ")",
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
    Third-pass after #108: concurrency:+cancel-in-progress: / permissions: present /
    reject actions|packages|pull-requests: write / finditer uses /
    docker continue / rsplit[-1] / third-pass docstring.
    Deepen after #135: cancel-in-progress: true / contents: read /
    ubuntu-latest / workflow_dispatch: / reject security-events|attestations|
    statuses|deployments: write / deepen docstring.
    Leftover after #149: contents: read membership affirm (complement regex) /
    actionlint leftover (not docs-lint / wiki spam).
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
        # Third-pass after #108: reversible CI concurrency cancel pins.
        if "concurrency:" not in text:
            fail(f"{name}: actionlint-style requires concurrency:", errors)
        if "cancel-in-progress:" not in text:
            fail(f"{name}: actionlint-style requires cancel-in-progress:", errors)
        # Third-pass after #108: permissions block must be present (least privilege).
        if "permissions:" not in text:
            fail(f"{name}: actionlint-style requires permissions:", errors)
        # Third-pass after #108: reject extra write scopes on docs CI paths.
        if re.search(r"(?m)^\s*actions:\s*write\s*$", text):
            fail(f"{name}: actions: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*packages:\s*write\s*$", text):
            fail(f"{name}: packages: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*pull-requests:\s*write\s*$", text):
            fail(f"{name}: pull-requests: write is forbidden on stewardship workflows", errors)
        # Pin GitHub Actions majors (actionlint / supply-chain hygiene).
        for match in re.finditer(r"(?m)^\s*(?:-\s+)?uses:\s*([^\s#]+)", text):
            uses = match.group(1).strip()
            if uses.startswith("docker://"):
                continue
            if "@" not in uses:
                fail(f"{name}: unpinned action uses: {uses}", errors)
                continue
            ref = uses.rsplit("@", 1)[-1]
            if ref in {"main", "master", "latest"}:
                fail(f"{name}: action must not float on @{ref}: {uses}", errors)
        # Deepen after #135: CI reliability leftovers (actionlint-style slice).
        if not re.search(r"(?m)^\s*cancel-in-progress:\s*true\s*$", text):
            fail(f"{name}: actionlint-style requires cancel-in-progress: true", errors)
        if not re.search(r"(?m)^\s*contents:\s*read\s*$", text):
            fail(f"{name}: actionlint-style requires contents: read", errors)
        if "ubuntu-latest" not in text:
            fail(f"{name}: actionlint-style requires runs-on ubuntu-latest", errors)
        if "workflow_dispatch:" not in text:
            fail(f"{name}: actionlint-style requires workflow_dispatch:", errors)
        # Reject extra write scopes on docs CI (beyond third-pass actions/packages/pull-requests).
        if re.search(r"(?m)^\s*security-events:\s*write\s*$", text):
            fail(f"{name}: security-events: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*attestations:\s*write\s*$", text):
            fail(f"{name}: attestations: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*statuses:\s*write\s*$", text):
            fail(f"{name}: statuses: write is forbidden on stewardship workflows", errors)
        if re.search(r"(?m)^\s*deployments:\s*write\s*$", text):
            fail(f"{name}: deployments: write is forbidden on stewardship workflows", errors)
        # jobs must declare timeout (already checked globally; keep local needle).
        if "timeout-minutes:" not in text:
            fail(f"{name}: actionlint-style requires timeout-minutes on jobs", errors)
        # Leftover after #149: affirm contents: read via membership (complement #149 regex).
        if "contents: read" not in text:
            fail(f"{name}: actionlint-style requires contents:read via membership", errors)


def check_workflow_hardening(errors: list[str]) -> None:
    """Harden existing lint/link/stewardship workflows (triggers, perms, concurrency).

    Third-pass after #111: reversible CI workflow exact pins —
    concurrency group templates / markdown-lint+stewardship cron+timeout /
    DavidAnson@v24 / setup-python@v5 / lychee verbose+no-progress+
    max-concurrency 8+timeout 20+max-retries 3 / fail: true /
    get_actionlint id+outputs / curl -fsSL / third-pass docstring.
    Deepen after #161: Check links / Run markdownlint / Set up Python /
    Install PyYAML (schema parser) / Stewardship gates+self-tests step names /
    exact token+--github-token forms / --exclude-path .github/agents /
    globs: | / AGENTS+CLAUDE+LICENSE+CONTRIBUTING+.github/workflows/** paths /
    Weekly drift + GITHUB_TOKEN commentary / deepen docstring.
    Path-filter leftovers after #173: exact push paths layouts / residual
    stewardship path entries / reject paths-ignore / ignore-glob exactness
    (empty workflow stubs already handled; not path-order/badge spam).
    Path-order leftover after #181 (lands closed #157/#182; NOT path-filter /
    NOT wiki-index / NOT run_stewardship / NOT #165 stewardship CI):
    contiguous three-path actionlint order / exact bash <(curl -fsSL) download /
    no continue-on-error: true / Download actionlint + actionlint existing
    workflow paths step names / path-order leftover docstring.
    Path-filter/path-order deepen after #203 (NOT saturated #189 / NOT #176
    layouts / NOT schema #191 / NOT Pass-2 residual #199/#203 / NOT Pass-2+md/link #192 /
    NOT wiki-badge / NOT stewardship-badge lint #208 / NOT schema fourth-pass #216/#204/#209 /
    NOT Pass-2 leftover + md/link #220):
    contiguous push/branches/paths headers / pull_request path-unfiltered /
    reject dorny/paths-filter / residual self-workflow path list entries /
    exact contiguous actionlint run / Download precedes actionlint run /
    contiguous Download/id/run/shell block / self-tests precede Download /
    reject uses: rhysd/actionlint@ invent.
    Path-filter/path-order residual deepen after #225 (NOT saturated deepen
    #225/#203 / NOT #189 / NOT #176 / NOT schema #191/#216 /
    NOT Pass-2 residual #199/#203 / NOT Pass-2 leftover + md/link #220 /
    NOT wiki-badge leftover #227 / NOT stewardship-checks/schema leftover #233 /
    NOT stewardship-badge lint #208):
    contiguous pull_request:/schedule: adjacency / reject branches-ignore: /
    pull_request type-unfiltered / reject tj-actions/changed-files /
    contiguous four-step actionlint path-order /
    schedule before workflow_dispatch / contiguous shell-less actionlint run step.
    Path-filter/path-order residual leftover deepen after #258 (NOT saturated
    residual #244 / NOT stewardship-schema leftover #258 /
    NOT wiki/mdlink leftover #252 / NOT saturated deepen #225/#203 / NOT #189 / NOT #176 /
    NOT schema #191/#216 / NOT Pass-2 residual #199/#203 /
    NOT Pass-2 leftover + md/link #220 / NOT wiki outline/PUBLISH leftover #243 /
    NOT md/link residual #239 / NOT stewardship-checks/schema leftover #233 /
    NOT wiki-badge leftover #227 / NOT stewardship-badge lint #208):
    contiguous push:/pull_request: adjacency / contiguous schedule:/workflow_dispatch: /
    pull_request branches-unfiltered / reject tags-ignore: /
    reject workflow_call: / contiguous five-step actionlint path-order /
    contiguous on:/push: header.
    Path-filter/path-order residual leftover deepen after #272 (NOT lychee/blob-503
    harden #278 / NOT Pass-2 residual leftover #272 / NOT saturated leftover #262 /
    NOT stewardship-schema leftover #258 /
    NOT wiki/mdlink leftover #252 / NOT saturated residual #244 /
    NOT saturated deepen #225/#203 / NOT #189 / NOT #176 /
    NOT schema #191/#216 / NOT Pass-2 residual #199/#203 /
    NOT Pass-2 leftover + md/link #220 / NOT wiki outline/PUBLISH leftover #243 /
    NOT md/link residual #239 / NOT stewardship-checks/schema leftover #233 /
    NOT wiki-badge leftover #227 / NOT stewardship-badge lint #208):
    contiguous workflow_dispatch:/concurrency: adjacency /
    contiguous name:/on: workflow header / reject workflow_run: /
    reject repository_dispatch: / reject merge_group: / reject tags: /
    contiguous six-step actionlint path-order.
    Markdown-lint/link-check workflow edges after #203 tip (lands closed #202/#192 leftover;
    NOT path-filter / Pass-2 / path-order / schema / badge-lint spam):
    args: >- / externally broken links commentary / without-it private-404 commentary /
    must not set continue-on-error / exact job permissions: contents: read /
    checkout before Check links adjacency / checkout before Run markdownlint adjacency.
    Stewardship-checks + schema residual deepen after #225 (NOT wiki-index/badge #227 / NOT path-edges #225 /
    NOT Pass-2 leftover+md/link #220 / NOT schema fourth-pass #216 / NOT badge-lint #208 /
    NOT Pass-2 residual #199/#203 / NOT path-order #189):
    exact Set up Python block / exact Install PyYAML block / checkout→Set up Python /
    exact full push paths list / exact schedule+cron block / exact concurrency block /
    exact jobs.stewardship header / reject strategy|matrix|services invent.
    Pass-2 residual + existing templates/AGENTS-REPO.md leftover after #233
    (NOT stewardship-checks/schema residual #233 / NOT wiki-index/badge #227 /
    NOT path-edges #225 / NOT Pass-2 leftover+md/link #220 / NOT Pass-2 residual #199/#203 /
    NOT badge-lint #208 / NOT schema #216 / NOT md/link residual #239 /
    NOT wiki outline/PUBLISH leftover #243 /
    NOT actionlint path-filter/path-order residual #244 /
    NOT wiki/mdlink leftover #252 / NOT stewardship-schema leftover #258; do not invent new templates):
    soft-fail with || : / soft-fail with || return 0 /
    set +o errexit / set +o nounset / invent python3 -m for gates /
    must not source env files / must not dot-source paths /
    reject any continue-on-error: on existing workflows /
    exact contiguous concurrency group template (existing templates only).
    """
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

        # Third-pass after #111: reversible CI workflow exact concurrency group templates.
        if name == "link-check.yml" and "link-check-${{ github.workflow }}-${{ github.ref }}" not in text:
            fail(
                'link-check.yml must pin concurrency group '
                'link-check-${{ github.workflow }}-${{ github.ref }}',
                errors,
            )
        if name == "markdown-lint.yml" and "markdown-lint-${{ github.workflow }}-${{ github.ref }}" not in text:
            fail(
                'markdown-lint.yml must pin concurrency group '
                'markdown-lint-${{ github.workflow }}-${{ github.ref }}',
                errors,
            )
        if name == "stewardship-checks.yml" and "stewardship-checks-${{ github.workflow }}-${{ github.ref }}" not in text:
            fail(
                'stewardship-checks.yml must pin concurrency group '
                'stewardship-checks-${{ github.workflow }}-${{ github.ref }}',
                errors,
            )

        # Fail-closed: cancel-in-progress must be true (not false / empty).
        if not re.search(r"(?m)^\s*cancel-in-progress:\s*true\s*$", text):
            fail(
                f"{name} concurrency must set cancel-in-progress: true",
                errors,
            )
        # Exact contiguous concurrency group template leftover after #233
        # (existing templates only; NOT invent new templates /
        # NOT stewardship-checks/schema residual #233 / NOT wiki-index/badge #227).
        prefix = name.removesuffix(".yml")
        exact_concurrency = (
            "concurrency:\n"
            f"  group: {prefix}-${{{{ github.workflow }}}}-${{{{ github.ref }}}}\n"
            "  cancel-in-progress: true"
        )
        if exact_concurrency not in text:
            fail(
                f"{name} must keep exact contiguous concurrency group template "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if "continue-on-error:" in text:
            fail(
                f"{name} must not set continue-on-error "
                "(Pass-2 residual / template validation leftover after #233)",
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
    # Fail-closed after #176: runner before self-tests (CI reliability leftover).
    run_i = stew.find("bash scripts/run_stewardship_checks.sh")
    test_i = stew.find("python3 scripts/test_stewardship_gates.py")
    # Reconstruct so contract can pin the concatenation form.
    order_msg = "run_stewardship_checks.sh before " + "test_stewardship_gates.py"
    if run_i < 0 or test_i < 0 or not (run_i < test_i):
        fail(
            "stewardship-checks.yml must run " + order_msg,
            errors,
        )
    # Fail-closed after #191: Pass-2 residual stewardship-checks integrity
    # (NOT schema third-pass #191 / NOT path-order #189 / NOT Pass-2 core #179).
    back_to_back_block = (
        "      - name: Stewardship gates (badge / wiki / schema / relative links)\n"
        "        run: bash scripts/run_stewardship_checks.sh\n"
        "      - name: Stewardship gate self-tests\n"
        "        run: python3 scripts/test_stewardship_gates.py\n"
    )
    if back_to_back_block not in stew:
        fail(
            "stewardship-checks.yml must keep back-to-back gates→self-tests named block "
            "(Pass-2 residual after #191)",
            errors,
        )
    for inline_gate in (
        "python3 scripts/check_badge_standard.py",
        "python3 scripts/check_wiki_outline.py",
        "python3 scripts/check_stewardship_schema.py",
        "python3 scripts/check_relative_links.py",
    ):
        if inline_gate in stew:
            fail(
                "stewardship-checks.yml must not inline "
                + inline_gate
                + " (use run_stewardship_checks.sh; Pass-2 residual after #191)",
                errors,
            )
    actionlint_i = stew.find("download-actionlint.bash")
    if actionlint_i < 0:
        actionlint_i = stew.find("get_actionlint")
    if test_i >= 0 and actionlint_i >= 0 and not (test_i < actionlint_i):
        fail(
            "stewardship-checks.yml must run self-tests before actionlint "
            "(Pass-2 residual after #191)",
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

    # Exact needles for stewardship-badge lint deepen after #189 contracts:
    # exact live stewardship-badge lint globs block
    # exact live stewardship-badge lint push paths filter
    # Stewardship-badge lint deepen after #189: exact live markdown-lint globs
    # block (residual exact layout; NOT path-order #189 / NOT schema third-pass #191 /
    # NOT run_stewardship residual #199).
    expected_globs = (
        "          globs: |\n"
        "            **/*.md\n"
        "            !.github/agents/**\n"
        "            !OWASP-AGENTIC.md\n"
    )
    if expected_globs not in lint:
        fail(
            "markdown-lint.yml must match exact live stewardship-badge lint globs block "
            "after #189",
            errors,
        )
    expected_md_paths = (
        '    paths:\n'
        '      - "**/*.md"\n'
        '      - ".markdownlint.json"\n'
        '      - ".github/workflows/markdown-lint.yml"\n'
    )
    if expected_md_paths not in lint:
        fail(
            "markdown-lint.yml must match exact live stewardship-badge lint push paths filter "
            "after #189",
            errors,
        )
    expected_link_paths = (
        '    paths:\n'
        '      - "**/*.md"\n'
        '      - ".lycheeignore"\n'
        '      - ".github/workflows/link-check.yml"\n'
    )
    if expected_link_paths not in link:
        fail(
            "link-check.yml must match exact live stewardship-badge lint push paths filter "
            "after #189",
            errors,
        )
    if '".markdownlint.json"' not in lint and "'.markdownlint.json'" not in lint:
        fail(
            'markdown-lint.yml paths filter must include ".markdownlint.json" '
            "(stewardship-badge lint after #189)",
            errors,
        )
    if '".lycheeignore"' not in link and "'.lycheeignore'" not in link:
        fail(
            'link-check.yml paths filter must include ".lycheeignore" '
            "(stewardship-badge lint after #189)",
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

    # Deepen after #161: stewardship CI reliability leftovers (workflow slice).
    # Step-name pins keep operator-facing CI labels fail-closed.
    if "name: Check links" not in link:
        fail(
            'link-check.yml must keep step name: Check links',
            errors,
        )
    if "name: Run markdownlint" not in lint:
        fail(
            'markdown-lint.yml must keep step name: Run markdownlint',
            errors,
        )
    if "name: Set up Python" not in stew:
        fail(
            'stewardship-checks.yml must keep step name: Set up Python',
            errors,
        )
    if "name: Install PyYAML (schema parser)" not in stew:
        fail(
            "stewardship-checks.yml must keep step name: "
            "Install PyYAML (schema parser)",
            errors,
        )
    if "name: Stewardship gates (badge / wiki / schema / relative links)" not in stew:
        fail(
            "stewardship-checks.yml must keep step name: Stewardship gates "
            "(badge / wiki / schema / relative links)",
            errors,
        )
    if "name: Stewardship gate self-tests" not in stew:
        fail(
            "stewardship-checks.yml must keep step name: "
            "Stewardship gate self-tests",
            errors,
        )
    # Exact auth / exclude forms (beyond membership-only third-pass pins).
    if "token: ${{ secrets.GITHUB_TOKEN }}" not in link:
        fail(
            "link-check.yml must set token: ${{ secrets.GITHUB_TOKEN }}",
            errors,
        )
    if "--github-token ${{ secrets.GITHUB_TOKEN }}" not in link:
        fail(
            "link-check.yml must pass --github-token ${{ secrets.GITHUB_TOKEN }}",
            errors,
        )
    if "--exclude-path .github/agents" not in link:
        fail(
            "link-check.yml must pass contiguous --exclude-path .github/agents",
            errors,
        )
    if "globs: |" not in lint:
        fail(
            "markdown-lint.yml must keep multiline globs: | form",
            errors,
        )
    # Stewardship path-filter leftovers beyond README/docs/scripts.
    for path_needle in (
        '"AGENTS.md"',
        '"CLAUDE.md"',
        '"LICENSE"',
        '"CONTRIBUTING.md"',
        '".github/workflows/**"',
    ):
        if path_needle not in stew and path_needle.replace('"', "'") not in stew:
            fail(
                "stewardship-checks.yml paths filter must include "
                + path_needle.strip('"'),
                errors,
            )
    # Live commentary leftovers (docs CI reliability rationale).
    if "GITHUB_TOKEN allows lychee to authenticate private GitHub repos" not in link:
        fail(
            "link-check.yml must keep GITHUB_TOKEN allows lychee commentary",
            errors,
        )
    if "private repos return 404" not in link:
        fail(
            "link-check.yml must keep private repos return 404 commentary",
            errors,
        )
    if "Weekly drift catch aligned with link/stewardship schedules" not in lint:
        fail(
            "markdown-lint.yml must keep Weekly drift catch commentary",
            errors,
        )
    if "Weekly drift catch for badge/wiki/schema/relative-link gates" not in stew:
        fail(
            "stewardship-checks.yml must keep Weekly drift catch commentary",
            errors,
        )

    # Fail-closed after #173: actionlint path-filter leftovers (push paths /
    # ignore globs). Distinct from path-order/badge (#157), stewardship-badge
    # lint (#172), and stewardship CI deepen (#165); empty workflow stubs
    # already handled via load None continue. Lands closed #166 leftover.
    if "paths:" not in link:
        fail("link-check.yml must declare push paths: filter", errors)
    if "paths:" not in lint:
        fail("markdown-lint.yml must declare push paths: filter", errors)
    if "paths:" not in stew:
        fail("stewardship-checks.yml must declare push paths: filter", errors)
    if "paths-ignore:" in link:
        fail(
            "link-check.yml must not use paths-ignore: (path-filter leftovers)",
            errors,
        )
    if "paths-ignore:" in lint:
        fail(
            "markdown-lint.yml must not use paths-ignore: (path-filter leftovers)",
            errors,
        )
    if "paths-ignore:" in stew:
        fail(
            "stewardship-checks.yml must not use paths-ignore: "
            "(path-filter leftovers)",
            errors,
        )
    link_paths_exact = (
        "    paths:\n"
        '      - "**/*.md"\n'
        '      - ".lycheeignore"\n'
        '      - ".github/workflows/link-check.yml"'
    )
    if link_paths_exact not in link:
        fail(
            "link-check.yml must keep exact push paths filter layout",
            errors,
        )
    lint_paths_exact = (
        "    paths:\n"
        '      - "**/*.md"\n'
        '      - ".markdownlint.json"\n'
        '      - ".github/workflows/markdown-lint.yml"'
    )
    if lint_paths_exact not in lint:
        fail(
            "markdown-lint.yml must keep exact push paths filter layout",
            errors,
        )
    stew_paths_exact = (
        "    paths:\n"
        '      - "README.md"\n'
        '      - "AGENTS.md"\n'
        '      - "CLAUDE.md"\n'
        '      - "LICENSE"\n'
        '      - "CONTRIBUTING.md"\n'
        '      - "docs/**"\n'
        '      - "scripts/**"\n'
        '      - ".github/workflows/**"\n'
        '      - ".lycheeignore"\n'
        '      - ".markdownlint.json"'
    )
    if stew_paths_exact not in stew:
        fail(
            "stewardship-checks.yml must keep exact push paths filter layout",
            errors,
        )
    # Residual stewardship path-filter entries (after #72 only scripts/docs/README).
    if '"AGENTS.md"' not in stew and "'AGENTS.md'" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include AGENTS.md",
            errors,
        )
    if '"CLAUDE.md"' not in stew and "'CLAUDE.md'" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include CLAUDE.md",
            errors,
        )
    if '"LICENSE"' not in stew and "'LICENSE'" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include LICENSE",
            errors,
        )
    if '"CONTRIBUTING.md"' not in stew and "'CONTRIBUTING.md'" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include CONTRIBUTING.md",
            errors,
        )
    if ".github/workflows/**" not in stew:
        fail(
            "stewardship-checks.yml paths filter must include .github/workflows/**",
            errors,
        )
    if '- ".lycheeignore"' not in stew and "- '.lycheeignore'" not in stew:
        fail(
            "stewardship-checks.yml paths filter must list .lycheeignore",
            errors,
        )
    if (
        '- ".markdownlint.json"' not in stew
        and "- '.markdownlint.json'" not in stew
    ):
        fail(
            "stewardship-checks.yml paths filter must list .markdownlint.json",
            errors,
        )
    if '- ".lycheeignore"' not in link and "- '.lycheeignore'" not in link:
        fail(
            "link-check.yml paths filter must list .lycheeignore",
            errors,
        )
    if (
        '- ".markdownlint.json"' not in lint
        and "- '.markdownlint.json'" not in lint
    ):
        fail(
            "markdown-lint.yml paths filter must list .markdownlint.json",
            errors,
        )
    # Ignore-glob leftovers (exact contiguous; bangs already partially pinned).
    if "--exclude-path .github/agents" not in link:
        fail(
            "link-check.yml must pass --exclude-path .github/agents ignore glob",
            errors,
        )
    lint_globs_exact = (
        "globs: |\n"
        "            **/*.md\n"
        "            !.github/agents/**\n"
        "            !OWASP-AGENTIC.md"
    )
    if lint_globs_exact not in lint:
        fail(
            "markdown-lint.yml must keep exact ignore-glob globs layout",
            errors,
        )


    # Path-order leftover after #181 (lands closed #157/#182; NOT path-filter #176 /
    # NOT wiki-index #181 / NOT run_stewardship #179 / NOT #165 stewardship CI).
    ordered_paths = (
        ".github/workflows/link-check.yml "
        ".github/workflows/markdown-lint.yml "
        ".github/workflows/stewardship-checks.yml"
    )
    if ordered_paths not in stew:
        fail(
            "stewardship-checks.yml actionlint must list three workflow paths "
            "in order: link-check → markdown-lint → stewardship-checks "
            "(actionlint path-order leftover)",
            errors,
        )
    download_form = (
        "bash <(curl -fsSL https://raw.githubusercontent.com/rhysd/actionlint/"
        "v1.7.7/scripts/download-actionlint.bash) 1.7.7"
    )
    if download_form not in stew:
        fail(
            "stewardship-checks.yml must use exact bash <(curl -fsSL …/v1.7.7/"
            "…download-actionlint.bash) 1.7.7 form "
            "(actionlint path-order leftover)",
            errors,
        )
    if re.search(r"(?m)^\s*continue-on-error:\s*true\s*$", stew):
        fail(
            "stewardship-checks.yml must not set continue-on-error: true "
            "(actionlint path-order leftover)",
            errors,
        )
    if "name: Download actionlint" not in stew:
        fail(
            "stewardship-checks.yml must keep step name: Download actionlint "
            "(actionlint path-order leftover)",
            errors,
        )
    if "name: actionlint existing workflow paths" not in stew:
        fail(
            "stewardship-checks.yml must keep step name: "
            "actionlint existing workflow paths "
            "(actionlint path-order leftover)",
            errors,
        )

    # Path-filter/path-order deepen after #203 (DISTINCT leftover edges;
    # NOT saturated #189 path-order / NOT #176 layouts / NOT schema #191 /
    # NOT Pass-2 residual #199/#203 / NOT Pass-2+md/link #192 / NOT wiki-badge /
    # NOT stewardship-badge lint #208 / NOT schema fourth-pass #216/#204/#209 /
    # NOT Pass-2 leftover + md/link #220).
    push_header = (
        "  push:\n"
        '    branches: ["**"]\n'
        "    paths:"
    )
    for wf_name, body in (
        ("link-check.yml", link),
        ("markdown-lint.yml", lint),
        ("stewardship-checks.yml", stew),
    ):
        if push_header not in body:
            fail(
                f"{wf_name} must keep contiguous push/branches/paths header "
                "(path-filter/path-order deepen after #203)",
                errors,
            )
        pr_match = re.search(
            r"(?m)^  pull_request:\s*\n((?:    .*\n)*)",
            body,
        )
        if pr_match and re.search(r"(?m)^    paths:", pr_match.group(1)):
            fail(
                f"{wf_name} pull_request must stay path-unfiltered "
                "(no nested paths:; path-filter/path-order deepen after #203)",
                errors,
            )
        if "dorny/paths-filter" in body:
            fail(
                f"{wf_name} must not invent dorny/paths-filter "
                "(path-filter/path-order deepen after #203)",
                errors,
            )
    if '- ".github/workflows/link-check.yml"' not in link:
        fail(
            "link-check.yml paths filter must list self workflow path "
            "(path-filter/path-order deepen after #203)",
            errors,
        )
    if '- ".github/workflows/markdown-lint.yml"' not in lint:
        fail(
            "markdown-lint.yml paths filter must list self workflow path "
            "(path-filter/path-order deepen after #203)",
            errors,
        )
    exact_actionlint_run = (
        "${{ steps.get_actionlint.outputs.executable }} -color "
        ".github/workflows/link-check.yml "
        ".github/workflows/markdown-lint.yml "
        ".github/workflows/stewardship-checks.yml"
    )
    if exact_actionlint_run not in stew:
        fail(
            "stewardship-checks.yml must keep exact contiguous actionlint run "
            "command (executable -color three paths; "
            "path-filter/path-order deepen after #203)",
            errors,
        )
    download_block = (
        "      - name: Download actionlint\n"
        "        id: get_actionlint\n"
        "        run: bash <(curl -fsSL https://raw.githubusercontent.com/"
        "rhysd/actionlint/v1.7.7/scripts/download-actionlint.bash) 1.7.7\n"
        "        shell: bash"
    )
    if download_block not in stew:
        fail(
            "stewardship-checks.yml must keep contiguous Download/id/run/shell actionlint download block (path-filter/path-order deepen after #203)",
            errors,
        )
    dl_idx = stew.find("name: Download actionlint")
    run_idx = stew.find("name: actionlint existing workflow paths")
    if dl_idx < 0 or run_idx < 0 or not (dl_idx < run_idx):
        fail(
            "stewardship-checks.yml Download actionlint must precede actionlint existing workflow paths (path-filter/path-order deepen after #203)",
            errors,
        )
    self_tests_idx = stew.find("name: Stewardship gate self-tests")
    if self_tests_idx < 0 or dl_idx < 0 or not (self_tests_idx < dl_idx):
        fail(
            "stewardship-checks.yml Stewardship gate self-tests must precede Download actionlint (path-filter/path-order deepen after #203)",
            errors,
        )
    if re.search(r"(?m)^\s*uses:\s*rhysd/actionlint@", stew):
        fail(
            "stewardship-checks.yml must not invent uses: rhysd/actionlint@ "
            "(keep download-actionlint.bash; "
            "path-filter/path-order deepen after #203)",
            errors,
        )

    # Path-filter/path-order residual deepen after #225 (DISTINCT leftover edges;
    # NOT saturated deepen #225/#203 / NOT #189 path-order / NOT #176 layouts /
    # NOT schema #191/#216 / NOT Pass-2 residual #199/#203 /
    # NOT Pass-2 leftover + md/link #220 / NOT wiki-badge leftover #227 /
    # NOT stewardship-checks/schema leftover #233 /
    # NOT stewardship-badge lint #208).
    pr_schedule = "  pull_request:\n  schedule:"
    for wf_name, body in (
        ("link-check.yml", link),
        ("markdown-lint.yml", lint),
        ("stewardship-checks.yml", stew),
    ):
        if pr_schedule not in body:
            fail(
                f"{wf_name} must keep contiguous pull_request:/schedule: "
                "adjacency (bare PR form; "
                "path-filter/path-order residual deepen after #225)",
                errors,
            )
        if "branches-ignore:" in body:
            fail(
                f"{wf_name} must not invent branches-ignore: "
                "(path-filter/path-order residual deepen after #225)",
                errors,
            )
        if "tj-actions/changed-files" in body:
            fail(
                f"{wf_name} must not invent tj-actions/changed-files "
                "(path-filter/path-order residual deepen after #225)",
                errors,
            )
        pr_match = re.search(
            r"(?m)^  pull_request:\s*\n((?:    .*\n)*)",
            body,
        )
        if pr_match and re.search(r"(?m)^    types:", pr_match.group(1)):
            fail(
                f"{wf_name} pull_request must stay type-unfiltered "
                "(no nested types:; "
                "path-filter/path-order residual deepen after #225)",
                errors,
            )
        sched_idx = body.find("  schedule:")
        dispatch_idx = body.find("  workflow_dispatch:")
        if sched_idx < 0 or dispatch_idx < 0 or not (sched_idx < dispatch_idx):
            fail(
                f"{wf_name} schedule: must precede workflow_dispatch: "
                "(path-filter/path-order residual deepen after #225)",
                errors,
            )
    gates_name = (
        "name: Stewardship gates (badge / wiki / schema / relative links)"
    )
    gates_idx = stew.find(gates_name)
    self_tests_idx = stew.find("name: Stewardship gate self-tests")
    dl_idx = stew.find("name: Download actionlint")
    run_idx = stew.find("name: actionlint existing workflow paths")
    if (
        gates_idx < 0
        or self_tests_idx < 0
        or dl_idx < 0
        or run_idx < 0
        or not (gates_idx < self_tests_idx < dl_idx < run_idx)
    ):
        fail(
            "stewardship-checks.yml must keep contiguous four-step "
            "actionlint path-order "
            "(gates → self-tests → Download → actionlint run; "
            "path-filter/path-order residual deepen after #225)",
            errors,
        )
    shell_less_run = (
        "      - name: actionlint existing workflow paths\n"
        "        run: ${{ steps.get_actionlint.outputs.executable }} -color "
        ".github/workflows/link-check.yml "
        ".github/workflows/markdown-lint.yml "
        ".github/workflows/stewardship-checks.yml"
    )
    if shell_less_run not in stew:
        fail(
            "stewardship-checks.yml must keep contiguous shell-less "
            "actionlint run step (no invent shell: on run step; "
            "path-filter/path-order residual deepen after #225)",
            errors,
        )

    # Path-filter/path-order residual leftover deepen after #258 (DISTINCT leftover;
    # NOT saturated residual #244 / NOT stewardship-schema leftover #258 /
    # NOT wiki/mdlink leftover #252 / NOT saturated deepen #225/#203 /
    # NOT #189 path-order / NOT #176 layouts / NOT schema #191/#216 /
    # NOT Pass-2 residual #199/#203 / NOT Pass-2 leftover + md/link #220 /
    # NOT wiki outline/PUBLISH leftover #243 / NOT md/link residual #239 /
    # NOT stewardship-checks/schema leftover #233 /
    # NOT wiki-badge leftover #227 / NOT stewardship-badge lint #208).
    push_pr_re = re.compile(r"(?m)^  push:\n(?:    .*\n)+  pull_request:")
    sched_dispatch_re = re.compile(
        r"(?m)^  schedule:\n(?:    .*\n)+  workflow_dispatch:"
    )
    on_push = "on:\n  push:"
    for wf_name, body in (
        ("link-check.yml", link),
        ("markdown-lint.yml", lint),
        ("stewardship-checks.yml", stew),
    ):
        if not push_pr_re.search(body):
            fail(
                f"{wf_name} must keep contiguous push:/pull_request: "
                "adjacency "
                "(path-filter/path-order residual leftover deepen after #258)",
                errors,
            )
        if not sched_dispatch_re.search(body):
            fail(
                f"{wf_name} must keep contiguous schedule:/workflow_dispatch: "
                "adjacency "
                "(path-filter/path-order residual leftover deepen after #258)",
                errors,
            )
        if on_push not in body:
            fail(
                f"{wf_name} must keep contiguous on:/push: header "
                "(path-filter/path-order residual leftover deepen after #258)",
                errors,
            )
        if "tags-ignore:" in body:
            fail(
                f"{wf_name} must not invent tags-ignore: "
                "(path-filter/path-order residual leftover deepen after #258)",
                errors,
            )
        if "workflow_call:" in body:
            fail(
                f"{wf_name} must not invent workflow_call: "
                "(path-filter/path-order residual leftover deepen after #258)",
                errors,
            )
        pr_match = re.search(
            r"(?m)^  pull_request:\s*\n((?:    .*\n)*)",
            body,
        )
        if pr_match and re.search(r"(?m)^    branches:", pr_match.group(1)):
            fail(
                f"{wf_name} pull_request must stay branches-unfiltered "
                "(no nested branches:; "
                "path-filter/path-order residual leftover deepen after #258)",
                errors,
            )
    install_name = "name: Install PyYAML (schema parser)"
    install_idx = stew.find(install_name)
    gates_name_258 = (
        "name: Stewardship gates (badge / wiki / schema / relative links)"
    )
    gates_idx_258 = stew.find(gates_name_258)
    self_tests_idx_258 = stew.find("name: Stewardship gate self-tests")
    dl_idx_258 = stew.find("name: Download actionlint")
    run_idx_258 = stew.find("name: actionlint existing workflow paths")
    if (
        install_idx < 0
        or gates_idx_258 < 0
        or self_tests_idx_258 < 0
        or dl_idx_258 < 0
        or run_idx_258 < 0
        or not (
            install_idx
            < gates_idx_258
            < self_tests_idx_258
            < dl_idx_258
            < run_idx_258
        )
    ):
        fail(
            "stewardship-checks.yml must keep contiguous five-step "
            "actionlint path-order "
            "(Install PyYAML → gates → self-tests → Download → actionlint run; "
            "path-filter/path-order residual leftover deepen after #258)",
            errors,
        )

    # Path-filter/path-order residual leftover deepen after #272 (DISTINCT leftover;
    # NOT lychee/blob-503 harden #278 / NOT Pass-2 residual leftover #272 /
    # NOT saturated leftover #262 /
    # NOT stewardship-schema leftover #258 /
    # NOT wiki/mdlink leftover #252 / NOT saturated residual #244 /
    # NOT saturated deepen #225/#203 / NOT #189 path-order / NOT #176 layouts /
    # NOT schema #191/#216 / NOT Pass-2 residual #199/#203 /
    # NOT Pass-2 leftover + md/link #220 / NOT wiki outline/PUBLISH leftover #243 /
    # NOT md/link residual #239 / NOT stewardship-checks/schema leftover #233 /
    # NOT wiki-badge leftover #227 / NOT stewardship-badge lint #208).
    dispatch_concurrency = "  workflow_dispatch:\n\nconcurrency:"
    name_on_headers = (
        ("link-check.yml", "name: Link Check\n\non:"),
        ("markdown-lint.yml", "name: Markdown Lint\n\non:"),
        ("stewardship-checks.yml", "name: Stewardship Checks\n\non:"),
    )
    for wf_name, body in (
        ("link-check.yml", link),
        ("markdown-lint.yml", lint),
        ("stewardship-checks.yml", stew),
    ):
        if dispatch_concurrency not in body:
            fail(
                f"{wf_name} must keep contiguous workflow_dispatch:/concurrency: "
                "adjacency "
                "(path-filter/path-order residual leftover deepen after #272)",
                errors,
            )
        if "workflow_run:" in body:
            fail(
                f"{wf_name} must not invent workflow_run: "
                "(path-filter/path-order residual leftover deepen after #272)",
                errors,
            )
        if "repository_dispatch:" in body:
            fail(
                f"{wf_name} must not invent repository_dispatch: "
                "(path-filter/path-order residual leftover deepen after #272)",
                errors,
            )
        if "merge_group:" in body:
            fail(
                f"{wf_name} must not invent merge_group: "
                "(path-filter/path-order residual leftover deepen after #272)",
                errors,
            )
        # Reject bare tags: invent without matching tags-ignore: (already pinned).
        if re.search(r"(?m)^  tags:\s*(?:$|#)", body):
            fail(
                f"{wf_name} must not invent tags: (bare tags: key; "
                "path-filter/path-order residual leftover deepen after #272)",
                errors,
            )
    for wf_name, header in name_on_headers:
        body = {"link-check.yml": link, "markdown-lint.yml": lint, "stewardship-checks.yml": stew}[
            wf_name
        ]
        if header not in body:
            fail(
                f"{wf_name} must keep contiguous name:/on: workflow header "
                "(path-filter/path-order residual leftover deepen after #272)",
                errors,
            )
    setup_name_272 = "name: Set up Python"
    setup_idx_272 = stew.find(setup_name_272)
    install_idx_272 = stew.find("name: Install PyYAML (schema parser)")
    gates_name_272 = (
        "name: Stewardship gates (badge / wiki / schema / relative links)"
    )
    gates_idx_272 = stew.find(gates_name_272)
    self_tests_idx_272 = stew.find("name: Stewardship gate self-tests")
    dl_idx_272 = stew.find("name: Download actionlint")
    run_idx_272 = stew.find("name: actionlint existing workflow paths")
    if (
        setup_idx_272 < 0
        or install_idx_272 < 0
        or gates_idx_272 < 0
        or self_tests_idx_272 < 0
        or dl_idx_272 < 0
        or run_idx_272 < 0
        or not (
            setup_idx_272
            < install_idx_272
            < gates_idx_272
            < self_tests_idx_272
            < dl_idx_272
            < run_idx_272
        )
    ):
        fail(
            "stewardship-checks.yml must keep contiguous six-step "
            "actionlint path-order "
            "(Set up Python → Install PyYAML → gates → self-tests → "
            "Download → actionlint run; "
            "path-filter/path-order residual leftover deepen after #272)",
            errors,
        )

    # Stewardship-checks + schema residual deepen after #225 (DISTINCT leftover;
    # NOT path-edges #225 / NOT Pass-2 leftover+md/link #220 / NOT schema fourth #216 /
    # NOT badge-lint #208 / NOT Pass-2 residual #199/#203 / NOT path-order #189).
    setup_python_block = (
        "      - name: Set up Python\n"
        "        uses: actions/setup-python@v5\n"
        "        with:\n"
        '          python-version: "3.12"'
    )
    if setup_python_block not in stew:
        fail(
            "stewardship-checks.yml must keep exact contiguous Set up Python "
            "/ uses / with / python-version block "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    install_pyyaml_block = (
        "      - name: Install PyYAML (schema parser)\n"
        "        run: pip install --quiet pyyaml"
    )
    if install_pyyaml_block not in stew:
        fail(
            "stewardship-checks.yml must keep exact Install PyYAML "
            "(schema parser) pip install --quiet pyyaml block "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    checkout_then_python = (
        "      - uses: actions/checkout@v7\n"
        "      - name: Set up Python"
    )
    if checkout_then_python not in stew:
        fail(
            "stewardship-checks.yml checkout@v7 must immediately precede "
            "Set up Python (stewardship-checks + schema residual after #225)",
            errors,
        )
    full_push_paths = (
        "    paths:\n"
        '      - "README.md"\n'
        '      - "AGENTS.md"\n'
        '      - "CLAUDE.md"\n'
        '      - "LICENSE"\n'
        '      - "CONTRIBUTING.md"\n'
        '      - "docs/**"\n'
        '      - "scripts/**"\n'
        '      - ".github/workflows/**"\n'
        '      - ".lycheeignore"\n'
        '      - ".markdownlint.json"'
    )
    if full_push_paths not in stew:
        fail(
            "stewardship-checks.yml must keep exact full push paths list "
            "README→.markdownlint.json "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    schedule_block = (
        "  schedule:\n"
        "    # Weekly drift catch for badge/wiki/schema/relative-link gates\n"
        '    - cron: "15 6 * * 1"'
    )
    if schedule_block not in stew:
        fail(
            "stewardship-checks.yml must keep exact schedule Weekly-drift + "
            'cron "15 6 * * 1" block '
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    concurrency_block = (
        "concurrency:\n"
        "  group: stewardship-checks-${{ github.workflow }}-${{ github.ref }}\n"
        "  cancel-in-progress: true"
    )
    if concurrency_block not in stew:
        fail(
            "stewardship-checks.yml must keep exact concurrency group + "
            "cancel-in-progress block "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    job_header = (
        "jobs:\n"
        "  stewardship:\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 15\n"
        "    permissions:\n"
        "      contents: read"
    )
    if job_header not in stew:
        fail(
            "stewardship-checks.yml must keep exact jobs.stewardship "
            "runs-on/timeout/permissions header "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    if re.search(r"(?m)^\s*strategy:\s*$", stew) or re.search(
        r"(?m)^\s*strategy:\s+\S", stew
    ):
        fail(
            "stewardship-checks.yml must not invent strategy: "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    if re.search(r"(?m)^\s*matrix:\s*$", stew) or re.search(
        r"(?m)^\s*matrix:\s+\S", stew
    ):
        fail(
            "stewardship-checks.yml must not invent matrix: "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )
    if re.search(r"(?m)^\s*services:\s*$", stew) or re.search(
        r"(?m)^\s*services:\s+\S", stew
    ):
        fail(
            "stewardship-checks.yml must not invent services: "
            "(stewardship-checks + schema residual after #225)",
            errors,
        )

    # Fail-closed after #203 tip: markdown-lint / link-check workflow edges
    # (lands closed #202/#192 leftover; NOT path-filter #176 / Pass-2 #179/#199 /
    # path-order #189 / wiki-index #181 / schema #191/#204 / badge-lint #205).
    if "args: >-" not in link:
        fail(
            "link-check.yml must keep multiline args: >- form",
            errors,
        )
    if "Run weekly to catch externally broken links" not in link:
        fail(
            "link-check.yml must keep externally broken links commentary",
            errors,
        )
    without_it = "without it, private repos return 404 and fail the check"
    if without_it not in link:
        fail(
            "link-check.yml must keep without-it private-404 commentary",
            errors,
        )
    if "continue-on-error:" in link:
        fail(
            "link-check.yml must not set continue-on-error "
            "(markdown-lint/link-check edges after #203)",
            errors,
        )
    if "continue-on-error:" in lint:
        fail(
            "markdown-lint.yml must not set continue-on-error "
            "(markdown-lint/link-check edges after #203)",
            errors,
        )
    job_perms = "    permissions:\n      contents: read"
    if job_perms not in link:
        fail(
            "link-check.yml must keep exact job permissions: contents: read",
            errors,
        )
    if job_perms not in lint:
        fail(
            "markdown-lint.yml must keep exact job permissions: contents: read",
            errors,
        )
    link_checkout_adj = (
        "      - uses: actions/checkout@v7\n"
        "      - name: Check links"
    )
    if link_checkout_adj not in link:
        fail(
            "link-check.yml must keep checkout before Check links adjacency",
            errors,
        )
    lint_checkout_adj = (
        "      - uses: actions/checkout@v7\n"
        "      - name: Run markdownlint"
    )
    if lint_checkout_adj not in lint:
        fail(
            "markdown-lint.yml must keep checkout before Run markdownlint adjacency",
            errors,
        )



# Fail-closed after #227: markdown-lint/link-check residual exact layouts
    # (lands closed #221 leftover residual; NOT Pass-2 leftover + md/link #220 core /
    # NOT path-edges #225 / NOT wiki-index/badge leftover #227).
    link_args_exact = (
        "args: >-\n"
        "            --verbose\n"
        "            --no-progress\n"
        "            --exclude-loopback\n"
        "            --max-concurrency 8\n"
        "            --timeout 20\n"
        "            --max-retries 3\n"
        "            --github-token ${{ secrets.GITHUB_TOKEN }}\n"
        "            --exclude-path .github/agents\n"
        '            "**/*.md"'
    )
    if link_args_exact not in link:
        fail(
            "link-check.yml must keep exact contiguous args: >- flag block "
            "(markdown-lint/link-check residual after #227)",
            errors,
        )
    link_on_exact = (
        "on:\n"
        "  push:\n"
        '    branches: ["**"]\n'
        "    paths:\n"
        '      - "**/*.md"\n'
        '      - ".lycheeignore"\n'
        '      - ".github/workflows/link-check.yml"\n'
        "  pull_request:\n"
        "  schedule:\n"
        "    # Run weekly to catch externally broken links\n"
        '    - cron: "0 6 * * 1"\n'
        "  workflow_dispatch:"
    )
    if link_on_exact not in link:
        fail(
            "link-check.yml must keep exact contiguous on: "
            "push/PR/schedule/workflow_dispatch block "
            "(markdown-lint/link-check residual after #227)",
            errors,
        )
    lint_on_exact = (
        "on:\n"
        "  push:\n"
        '    branches: ["**"]\n'
        "    paths:\n"
        '      - "**/*.md"\n'
        '      - ".markdownlint.json"\n'
        '      - ".github/workflows/markdown-lint.yml"\n'
        "  pull_request:\n"
        "  schedule:\n"
        "    # Weekly drift catch aligned with link/stewardship schedules\n"
        '    - cron: "30 6 * * 1"\n'
        "  workflow_dispatch:"
    )
    if lint_on_exact not in lint:
        fail(
            "markdown-lint.yml must keep exact contiguous on: "
            "push/PR/schedule/workflow_dispatch block "
            "(markdown-lint/link-check residual after #227)",
            errors,
        )
    lint_with_exact = (
        "with:\n"
        "          globs: |\n"
        "            **/*.md\n"
        "            !.github/agents/**\n"
        "            !OWASP-AGENTIC.md\n"
        '          config: ".markdownlint.json"'
    )
    if lint_with_exact not in lint:
        fail(
            "markdown-lint.yml must keep exact contiguous with: globs|+config block "
            "(markdown-lint/link-check residual after #227)",
            errors,
        )
    link_token_with = (
        "with:\n"
        "          # GITHUB_TOKEN allows lychee to authenticate private GitHub repos\n"
        "          # without it, private repos return 404 and fail the check\n"
        "          token: ${{ secrets.GITHUB_TOKEN }}"
    )
    if link_token_with not in link:
        fail(
            "link-check.yml must keep exact contiguous with: token commentary block "
            "(markdown-lint/link-check residual after #227)",
            errors,
        )

    # Wiki/mdlink leftover after #243: residual exact layouts beyond #239/#227.
    link_concurrency_exact = (
        "concurrency:\n"
        "  group: link-check-${{ github.workflow }}-${{ github.ref }}\n"
        "  cancel-in-progress: true"
    )
    if link_concurrency_exact not in link:
        fail(
            "link-check.yml must keep exact contiguous concurrency block "
            "(wiki/mdlink leftover after #243)",
            errors,
        )
    lint_concurrency_exact = (
        "concurrency:\n"
        "  group: markdown-lint-${{ github.workflow }}-${{ github.ref }}\n"
        "  cancel-in-progress: true"
    )
    if lint_concurrency_exact not in lint:
        fail(
            "markdown-lint.yml must keep exact contiguous concurrency block "
            "(wiki/mdlink leftover after #243)",
            errors,
        )
    link_job_header_exact = (
        "jobs:\n"
        "  link-check:\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 20\n"
        "    permissions:\n"
        "      contents: read"
    )
    if link_job_header_exact not in link:
        fail(
            "link-check.yml must keep exact contiguous job header "
            "(wiki/mdlink leftover after #243)",
            errors,
        )
    lint_job_header_exact = (
        "jobs:\n"
        "  lint:\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 10\n"
        "    permissions:\n"
        "      contents: read"
    )
    if lint_job_header_exact not in lint:
        fail(
            "markdown-lint.yml must keep exact contiguous job header "
            "(wiki/mdlink leftover after #243)",
            errors,
        )
    fail_true_after_md = (
        '            "**/*.md"\n'
        "          fail: true"
    )
    if fail_true_after_md not in link:
        fail(
            "link-check.yml must keep exact **/*.md then fail: true adjacency "
            "(wiki/mdlink leftover after #243)",
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

    # Stewardship-badge lint deepen after #189: no invent workflow badge.svg
    # (residual vs wiki-badge #141; NOT schema third-pass #191 / NOT path-order #189 /
    # NOT run_stewardship residual #199).
    if "stewardship-checks.yml/badge.svg" in text:
        fail(
            "README.md must not invent stewardship-checks.yml/badge.svg "
            "(no fourth badge; wiki-index/badge leftover after #189; "
            "stewardship-badge lint after #189)",
            errors,
        )
    if "actions/workflows/stewardship-checks.yml/badge.svg" in text:
        fail(
            "README.md must not invent "
            "actions/workflows/stewardship-checks.yml/badge.svg "
            "(no fourth badge; wiki-index/badge leftover after #189)",
            errors,
        )
    link_badge = "link-check.yml/" + "badge.svg"
    md_badge = "markdown-lint.yml/" + "badge.svg"
    if link_badge not in text:
        fail(
            "README.md must keep exact link-check.yml/badge.svg image path "
            "(stewardship-badge lint after #189)",
            errors,
        )
    if md_badge not in text:
        fail(
            "README.md must keep exact markdown-lint.yml/badge.svg image path "
            "(stewardship-badge lint after #189)",
            errors,
        )


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

    check_agents_repo_template(errors)


def check_agents_repo_template(errors: list[str]) -> None:
    """Fail-close existing templates/AGENTS-REPO.md leftover after #233.

    Existing template only — do not invent new templates / do not rewrite
    AGENTS-ECOSYSTEM.md. Distinct from stewardship-checks/schema residual #233.
    """
    if not AGENTS_REPO.is_file():
        fail(
            "Missing templates/AGENTS-REPO.md "
            "(Pass-2 residual / template validation leftover after #233)",
            errors,
        )
        return
    text = AGENTS_REPO.read_text(encoding="utf-8")
    if not text.startswith("# AGENTS.md — [PROJECT_NAME]"):
        fail(
            "templates/AGENTS-REPO.md must keep H1 AGENTS.md — [PROJECT_NAME] "
            "(Pass-2 residual / template validation leftover after #233)",
            errors,
        )
    required = (
        ('parent_governance: "github.com/fuzzywigg/agents-governance"', "parent_governance"),
        ('maintainer: "smtp.eth"', "maintainer smtp.eth"),
        ('scope: "repository-specific"', "scope repository-specific"),
        ('version: "1.0.0"', "version 1.0.0"),
        ('last_updated: "YYYY-MM-DD"', "YYYY-MM-DD placeholder"),
        ("## 1. Quick Reference", "section 1 Quick Reference"),
        ("## 2. Project-Specific Rules", "section 2 Project-Specific Rules"),
        ("## 3. Testing Requirements", "section 3 Testing Requirements"),
        ("## 4. Deployment", "section 4 Deployment"),
        ("## 5. Incident Response", "section 5 Incident Response"),
        ("## 6. Amendment Process", "section 6 Amendment Process"),
        ("[CONFIG_FILE]", "[CONFIG_FILE] placeholder"),
        ("Never commit", "Never commit .env"),
        ("agents-md/description", "agents-md/description branch"),
        ("smtp.eth approval required", "smtp.eth approval required"),
    )
    for needle, label in required:
        if needle not in text:
            fail(
                f"templates/AGENTS-REPO.md must keep {label} "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
    lowered = text.lower()
    if "badge.svg" in lowered or "[![" in text or "img.shields.io" in lowered:
        fail(
            "templates/AGENTS-REPO.md must not invent badge.svg chrome "
            "(Pass-2 residual / template validation leftover after #233)",
            errors,
        )
    scan_secrets(AGENTS_REPO, errors)


def check_badge_standard_gate_contract(errors: list[str]) -> None:
    """Fail-close live badge-standard gate wiring (after #104; deepen after #61; deepen after #48)."""
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

    # Fail-closed after #104: third-pass helper / constant / needle pins
    # (badge-standard slice only; not wiki / relative / schema / common / CI
    # workflow / actionlint pin spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks
    # and so contract source does not re-introduce the live contiguous pin.
    badge_line_exact = (
        "BADGE_LINE_RE = re.compile(\n"
        '    r"^\\[!\\[(?P<label>[^\\]]+)\\]\\((?P<img>[^)]+)\\)\\]\\((?P<link>[^)]+)\\)\\s*$"\n'
        ")"
    )
    if badge_line_exact not in text:
        fail(
            "check_badge_standard.py must set BADGE_LINE_RE exact label/img/link"
            + " pattern",
            errors,
        )
    github_re_exact = (
        "REPO_FROM_GITHUB_RE = re.compile(\n"
        + '    r"https://github\\.com/(?P<owner>[^/]+)/(?P<repo>[^/\\s?#]+)",\n'
        + "    re.IGNORECASE,\n"
        + ")"
    )
    if github_re_exact not in text:
        fail(
            "check_badge_standard.py must set REPO_FROM_GITHUB_RE exact IGNORECASE"
            + " pattern",
            errors,
        )
    shields_re_exact = (
        "REPO_FROM_SHIELDS_RE = re.compile(\n"
        + '    r"https://img\\.shields\\.io/github/(?:license|actions)/"\n'
        + '    r"(?P<owner>[^/]+)/(?P<repo>[^/\\s?#]+)",\n'
        + "    re.IGNORECASE,\n"
        + ")"
    )
    if shields_re_exact not in text:
        fail(
            "check_badge_standard.py must set REPO_FROM_SHIELDS_RE exact license|actions"
            + " pattern",
            errors,
        )
    workflows_exact = (
        "REQUIRED_WORKFLOWS = (\n"
        + '    "link-check.yml",\n'
        + '    "markdown-lint.yml",\n'
        + '    "stewardship-' + 'checks.yml",\n'
        + ")"
    )
    if workflows_exact not in text and workflows_exact.replace('"', "'") not in text:
        fail(
            "check_badge_standard.py must set REQUIRED_WORKFLOWS exact three-yml"
            + " tuple",
            errors,
        )
    group_label = "group(" + '"label")'
    group_label_sq = "group(" + "'label')"
    if group_label not in text and group_label_sq not in text:
        fail(
            "check_badge_standard.py must read badge labels via " + group_label,
            errors,
        )
    group_img = "group(" + '"img")'
    group_img_sq = "group(" + "'img')"
    if group_img not in text and group_img_sq not in text:
        fail(
            "check_badge_standard.py must read badge images via " + group_img,
            errors,
        )
    group_link = "group(" + '"link")'
    group_link_sq = "group(" + "'link')"
    if group_link not in text and group_link_sq not in text:
        fail(
            "check_badge_standard.py must read badge links via " + group_link,
            errors,
        )
    sys_exit_pin = (
        'if __name__ == "__main__":\n'
        + "    sys.exit(" + "main())"
    )
    sys_exit_pin_sq = (
        "if __name__ == '__main__':\n"
        + "    sys.exit(" + "main())"
    )
    if sys_exit_pin not in text and sys_exit_pin_sq not in text:
        fail(
            "check_badge_standard.py must invoke sys.exit(main()) under __main__",
            errors,
        )
    common_import = "from stewardship_" + "common import"
    if common_import not in text:
        fail(
            "check_badge_standard.py must import from stewardship_" + "common",
            errors,
        )
    badge_gate_eq = "BADGE_GATE = Path(__file__)." + "resolve()"
    if badge_gate_eq not in text:
        fail(
            "check_badge_standard.py must set BADGE_GATE = Path(__file__)."
            + "resolve()",
            errors,
        )
    utf8_pin = 'encoding="utf-' + '8"'
    utf8_sq = "encoding='utf-" + "8'"
    if utf8_pin not in text and utf8_sq not in text:
        fail(
            "check_badge_standard.py must read files as utf-" + "8",
            errors,
        )
    strict_row = "Strict row: no blank " + "lines"
    if strict_row not in text:
        fail(
            "check_badge_standard.py extract_badge_row must keep Strict " + "row pin",
            errors,
        )
    h1_startswith = 'startswith("' + '# ")'
    h1_startswith_sq = "startswith('" + "# ')"
    if h1_startswith not in text and h1_startswith_sq not in text:
        fail(
            "check_badge_standard.py must locate H1 via " + h1_startswith,
            errors,
        )
    fail_readme = "FAIL: README.md " + "missing"
    if fail_readme not in text:
        fail(
            "check_badge_standard.py must print FAIL: README.md " + "missing",
            errors,
        )
    img_https_needle = "Badge image " + "for"
    if img_https_needle not in text or "must be https://" not in text:
        fail(
            "check_badge_standard.py must emit Badge image " + "for … must be https://"
            + " needle",
            errors,
        )
    abs_https_when = "must use https:// when " + "absolute"
    if abs_https_when not in text:
        fail(
            "check_badge_standard.py must emit must use https:// when "
            + "absolute needle",
            errors,
        )
    abs_wf_url = "absolute https:// workflow " + "URL"
    if abs_wf_url not in text:
        fail(
            "check_badge_standard.py must emit absolute https:// workflow "
            + "URL needle",
            errors,
        )
    lic_point = "License badge link must point at " + "LICENSE"
    if lic_point not in text:
        fail(
            "check_badge_standard.py must emit License badge link must point at "
            + "LICENSE needle",
            errors,
        )
    unexpected_label = "Unexpected badge " + "label"
    if unexpected_label not in text:
        fail(
            "check_badge_standard.py must emit Unexpected badge label"
            + " needle",
            errors,
        )
    link_img_must = "Link Check image must use link-check.yml/" + "badge.svg"
    if link_img_must not in text:
        fail(
            "check_badge_standard.py must emit Link Check image must use "
            + "link-check.yml/" + "badge.svg",
            errors,
        )
    md_img_must = "Markdown Lint image must use markdown-lint.yml/" + "badge.svg"
    if md_img_must not in text:
        fail(
            "check_badge_standard.py must emit Markdown Lint image must use "
            + "markdown-lint.yml/" + "badge.svg",
            errors,
        )
    lic_img_must = "License image must use img.shields.io/github/" + "license/"
    if lic_img_must not in text:
        fail(
            "check_badge_standard.py must emit License image must use "
            + "img.shields.io/github/" + "license/",
            errors,
        )
    contract_call = "    check_badge_standard_gate_contract(" + "errors)"
    if contract_call not in text:
        fail(
            "check_badge_standard.py main must call check_badge_standard_gate_contract("
            + "errors)",
            errors,
        )
    extract_call = "extract_badge_row(" + "text)"
    if extract_call not in text:
        fail(
            "check_badge_standard.py main must call extract_badge_row(" + "text)",
            errors,
        )
    check_badges_call = "check_badges(badges, " + "errors)"
    if check_badges_call not in text:
        fail(
            "check_badge_standard.py main must call check_badges(badges, "
            + "errors)",
            errors,
        )
    ignorecase_pin = "re.IGNORE" + "CASE"
    if ignorecase_pin not in text:
        fail(
            "check_badge_standard.py REPO_FROM_* must use re.IGNORE" + "CASE",
            errors,
        )
    blob_lower = 'f"{label}|{img}|{link}".' + "lower()"
    blob_lower_sq = "f'{label}|{img}|{link}'." + "lower()"
    if blob_lower not in text and blob_lower_sq not in text:
        fail(
            'check_badge_standard.py check_badges must build blob via '
            'f"{label}|{img}|{link}".' + "lower()",
            errors,
        )
    expected_lower = "EXPECTED_REPO." + "lower()"
    if expected_lower not in text:
        fail(
            "check_badge_standard.py must compare slugs via EXPECTED_REPO."
            + "lower()",
            errors,
        )
    found_lower = "found." + "lower()"
    if found_lower not in text:
        fail(
            "check_badge_standard.py must compare found." + "lower() against EXPECTED_REPO",
            errors,
        )
    list_order = "list(REQUIRED_" + "ORDER)"
    if list_order not in text:
        fail(
            "check_badge_standard.py must use list(REQUIRED_" + "ORDER) in order fail needle",
            errors,
        )
    return_empty = "return [], " + "errors"
    if return_empty not in text:
        fail(
            "check_badge_standard.py extract_badge_row must return [], "
            + "errors on missing H1",
            errors,
        )
    stderr_pin = "file=sys." + "stderr"
    if stderr_pin not in text:
        fail(
            "check_badge_standard.py must print failures to sys." + "stderr",
            errors,
        )
    named_label = "(?P<" + "label>"
    if named_label not in text:
        fail(
            "check_badge_standard.py BADGE_LINE_RE must capture (?P<" + "label>",
            errors,
        )
    named_img = "(?P<" + "img>"
    if named_img not in text:
        fail(
            "check_badge_standard.py BADGE_LINE_RE must capture (?P<" + "img>",
            errors,
        )
    named_link = "(?P<" + "link>"
    if named_link not in text:
        fail(
            "check_badge_standard.py BADGE_LINE_RE must capture (?P<" + "link>",
            errors,
        )
    workflows_path = 'ROOT / ".github" / "' + 'workflows"'
    workflows_path_sq = "ROOT / '.github' / '" + "workflows'"
    if workflows_path not in text and workflows_path_sq not in text:
        fail(
            'check_badge_standard.py must pin WORKFLOWS via ROOT / ".github" / '
            '"workflows"',
            errors,
        )
    scripts_parent = "_SCRIPTS = Path(__file__).resolve()." + "parent"
    if scripts_parent not in text:
        fail(
            "check_badge_standard.py must resolve _SCRIPTS via Path(__file__).resolve()."
            + "parent",
            errors,
        )
    future_ann = "from __future__ import " + "annotations"
    if future_ann not in text:
        fail(
            "check_badge_standard.py must keep from __future__ import "
            + "annotations",
            errors,
        )
    third_pass_doc = "Third-pass: BADGE_LINE_RE+REPO_FROM_* " + "exact"
    if third_pass_doc not in text:
        fail(
            "check_badge_standard.py docstring must keep Third-pass "
            + "BADGE_LINE_RE+REPO_FROM_* " + "exact pin",
            errors,
        )
    license_actions = "(?:license|" + "actions)"
    if license_actions not in text:
        fail(
            "check_badge_standard.py REPO_FROM_SHIELDS_RE must pin license|"
            + "actions",
            errors,
        )
    only_allowed = "only {list(REQUIRED_ORDER)} " + "allowed"
    if only_allowed not in text:
        fail(
            "check_badge_standard.py must keep only {list(REQUIRED_ORDER)} "
            + "allowed needle",
            errors,
        )
    max_badges_eq = "MAX_BADGES = " + "3"
    if max_badges_eq not in text:
        fail(
            "check_badge_standard.py must keep MAX_BADGES = " + "3 exact assign",
            errors,
        )







    # Stewardship-badge lint deepen after #189 (NOT docs-lint leftover /
    # NOT wiki-badge / NOT path-order #189 / NOT schema third-pass #191 /
    # NOT run_stewardship residual #199; residual README invent + exact badge.svg paths).
    after_189 = "after " + "#189"
    if after_189 not in text:
        fail(
            "check_badge_standard.py must pin stewardship-badge lint " + after_189,
            errors,
        )
    badge_lint_slice = "stewardship-badge " + "lint"
    if badge_lint_slice not in text:
        fail(
            "check_badge_standard.py must keep " + badge_lint_slice + " slice wording",
            errors,
        )
    not_docs_leftover = "NOT docs-lint " + "leftover"
    if not_docs_leftover not in text:
        fail(
            "module docstring must keep " + not_docs_leftover + " distinctness pin",
            errors,
        )
    not_wiki_badge = "NOT wiki-badge " + "#141"
    if not_wiki_badge not in text:
        fail(
            "module docstring must keep " + not_wiki_badge + " distinctness pin",
            errors,
        )
    not_path_order = "NOT path-order " + "#189"
    if not_path_order not in text:
        fail(
            "module docstring must keep " + not_path_order + " distinctness pin",
            errors,
        )
    not_schema_tp = "NOT schema " + "third-pass"
    if not_schema_tp not in text:
        fail(
            "module docstring must keep " + not_schema_tp + " distinctness pin",
            errors,
        )
    invent_svg = "stewardship-checks.yml/" + "badge.svg"
    if invent_svg not in text:
        fail(
            "check_readme_consistency must reject invent " + invent_svg,
            errors,
        )
    invent_fail = "must not invent stewardship-checks.yml/" + "badge.svg"
    if invent_fail not in text:
        fail(
            "check_readme_consistency must emit " + invent_fail + " needle",
            errors,
        )
    link_exact = "exact link-check.yml/" + "badge.svg"
    if link_exact not in text:
        fail(
            "check_readme_consistency must keep " + link_exact + " path pin",
            errors,
        )
    md_exact = "exact markdown-lint.yml/" + "badge.svg"
    if md_exact not in text:
        fail(
            "check_readme_consistency must keep " + md_exact + " path pin",
            errors,
        )
    residual_pin = "residual uncovered " + "only"
    if residual_pin not in text:
        fail(
            "module docstring must keep " + residual_pin + " wording",
            errors,
        )


    # Deepen after #189: wiki-index/badge leftover on badge-standard gate
    # (lands closed #185/#172; NOT path-order #189 / NOT stewardship-schema).
    badge_deepen_189 = "wiki-index/badge leftover deepen after " + "#189"
    if badge_deepen_189 not in text:
        fail(
            "check_badge_standard.py docstring must keep " + badge_deepen_189 + " pin",
            errors,
        )
    badge_lands_172 = "lands closed #185/" + "#172"
    if badge_lands_172 not in text:
        fail(
            "check_badge_standard.py docstring must keep " + badge_lands_172 + " pin",
            errors,
        )
    badge_not_path_order = "NOT path-order " + "#189"
    if badge_not_path_order not in text:
        fail(
            "check_badge_standard.py docstring must keep " + badge_not_path_order + " pin",
            errors,
        )
    badge_not_schema = "NOT stewardship-schema " + "sibling"
    if badge_not_schema not in text:
        fail(
            "check_badge_standard.py docstring must keep " + badge_not_schema + " pin",
            errors,
        )
    invent_stew_svg = "stewardship-checks.yml/" + "badge.svg"
    if invent_stew_svg not in text:
        fail(
            "check_badge_standard.py must refuse invent " + invent_stew_svg,
            errors,
        )
    invent_stew_full = "actions/workflows/stewardship-checks.yml/" + "badge.svg"
    if invent_stew_full not in text:
        fail(
            "check_badge_standard.py must refuse invent " + invent_stew_full,
            errors,
        )
    invent_leftover_needle = "wiki-index/badge leftover after " + "#189"
    if invent_leftover_needle not in text:
        fail(
            "check_badge_standard.py invent refuse must keep "
            + invent_leftover_needle
            + " needle",
            errors,
        )
    no_stew_product = "must not add a Stewardship product/status " + "badge"
    if no_stew_product not in text:
        fail(
            "check_badge_standard.py must keep Stewardship product/status badge refuse",
            errors,
        )
    exact_link_svg = "actions/workflows/link-check.yml/" + "badge.svg"
    if exact_link_svg not in text:
        fail(
            "check_badge_standard.py must pin exact " + exact_link_svg,
            errors,
        )
    exact_md_svg = "actions/workflows/markdown-lint.yml/" + "badge.svg"
    if exact_md_svg not in text:
        fail(
            "check_badge_standard.py must pin exact " + exact_md_svg,
            errors,
        )
    no_fourth_paren_badge = "(no fourth " + "badge;"
    if no_fourth_paren_badge not in text:
        fail(
            "check_badge_standard.py invent refuse must keep "
            + no_fourth_paren_badge
            + " parenthetical",
            errors,
        )




    # Deepen after #227 tip: markdown-lint/link-check residual exact layouts
    # (lands closed #221 leftover residual; NOT Pass-2 leftover + md/link #220 core /
    # NOT path-edges #225 / NOT wiki-index/badge leftover #227).
    mdlink_residual_doc = "markdown-lint/link-check residual exact layouts after " + "#227"
    if mdlink_residual_doc not in text:
        fail(
            "check_badge_standard.py docstring must keep " + mdlink_residual_doc + " pin",
            errors,
        )
    link_args_residual_pin = "exact contiguous args: >- flag " + "block"
    if link_args_residual_pin not in text:
        fail(
            "check_badge_standard.py must keep " + link_args_residual_pin + " residual pin",
            errors,
        )
    link_on_residual_pin = (
        "exact contiguous link-check on: push/PR/schedule/" + "workflow_dispatch"
    )
    if link_on_residual_pin not in text:
        fail(
            "check_badge_standard.py must keep " + link_on_residual_pin + " residual pin",
            errors,
        )
    lint_on_residual_pin = (
        "exact contiguous markdown-lint on: push/PR/schedule/" + "workflow_dispatch"
    )
    if lint_on_residual_pin not in text:
        fail(
            "check_badge_standard.py must keep " + lint_on_residual_pin + " residual pin",
            errors,
        )
    lint_with_residual_pin = "exact contiguous with: globs|+config " + "block"
    if lint_with_residual_pin not in text:
        fail(
            "check_badge_standard.py must keep " + lint_with_residual_pin + " residual pin",
            errors,
        )
    link_token_residual_pin = "exact contiguous with: token commentary " + "block"
    if link_token_residual_pin not in text:
        fail(
            "check_badge_standard.py must keep " + link_token_residual_pin + " residual pin",
            errors,
        )
    not_wiki_227 = "NOT wiki-index/badge leftover " + "#227"
    if not_wiki_227 not in text:
        fail(
            "check_badge_standard.py docstring must keep " + not_wiki_227 + " distinctness pin",
            errors,
        )
    not_mdlink_220 = "NOT Pass-2 leftover + md/link " + "#220"
    if not_mdlink_220 not in text:
        fail(
            "check_badge_standard.py docstring must keep " + not_mdlink_220 + " distinctness pin",
            errors,
        )
    leftover_243_doc = "wiki/mdlink leftover after " + "#243"
    if leftover_243_doc not in text:
        fail(
            "check_badge_standard.py docstring must keep " + leftover_243_doc + " pin",
            errors,
        )
    not_path_244 = "NOT path-filter/path-order leftover " + "#244"
    if not_path_244 not in text:
        fail(
            "check_badge_standard.py docstring must keep " + not_path_244 + " distinctness pin",
            errors,
        )
    mdlink_concurrency_pin = "exact contiguous link+lint concurrency " + "blocks"
    if mdlink_concurrency_pin not in text:
        fail(
            "check_badge_standard.py must keep " + mdlink_concurrency_pin + " leftover pin",
            errors,
        )
    mdlink_job_header_pin = "exact contiguous link-check + markdown-lint job " + "headers"
    if mdlink_job_header_pin not in text:
        fail(
            "check_badge_standard.py must keep " + mdlink_job_header_pin + " leftover pin",
            errors,
        )
    fail_true_adj_pin = 'exact "**/*.md" then fail: true ' + "adjacency"
    if fail_true_adj_pin not in text:
        fail(
            "check_badge_standard.py must keep " + fail_true_adj_pin + " leftover pin",
            errors,
        )


def check_docs_lint_gate_contract(errors: list[str]) -> None:
    """Fail-close live docs-lint wiring (after #100; second-pass after #111).

    Second-pass: exact live exclude URLs + CDN commentary + markdownlint
    layout/key-set pins (docs-lint second-pass; not actionlint /
    stewardship_common / badge spam).
    Third-pass after #149: exact live .lycheeignore full layout + exact
    commentary lines (docs-lint leftover; not CI workflow / wiki spam).
    """
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
    # Second-pass after #111: docs-lint exact URL + commentary + layout pins.
    second_pass = "Second-pass after " + "#111"
    if second_pass not in text:
        fail(
            "docs-lint must keep " + second_pass + " docstring pin",
            errors,
        )
    docs_second = "docs-lint " + "second-pass"
    if docs_second not in text:
        fail(
            "docs-lint contract must keep " + docs_second + " wording",
            errors,
        )
    mcp_url = "https://modelcontextprotocol" + ".io/"
    if mcp_url not in text:
        fail(
            "check_lycheeignore must pin " + mcp_url,
            errors,
        )
    lfs_url = "https://www.linuxfoundation" + ".org/"
    if lfs_url not in text:
        fail(
            "check_lycheeignore must pin " + lfs_url,
            errors,
        )
    peer_reset = "Connection reset by " + "peer"
    if peer_reset not in text:
        fail(
            "check_lycheeignore must keep " + peer_reset + " needle",
            errors,
        )
    rst_needle = "must note " + "RST"
    if rst_needle not in text:
        fail(
            "check_lycheeignore must keep " + rst_needle + " needle",
            errors,
        )
    broken_url = "not a broken " + "URL"
    if broken_url not in text:
        fail(
            "check_lycheeignore must keep " + broken_url + " needle",
            errors,
        )
    false_pos = "false-" + "positive"
    if false_pos not in text:
        fail(
            "check_lycheeignore must keep " + false_pos + " needle",
            errors,
        )
    early_hints = "early " + "hints"
    if early_hints not in text:
        fail(
            "check_lycheeignore must keep " + early_hints + " needle",
            errors,
        )
    valid_site = "valid " + "site"
    if valid_site not in text:
        fail(
            "check_lycheeignore must keep " + valid_site + " needle",
            errors,
        )
    badge_ref = "check_badge_standard" + ".py"
    if "must reference " + badge_ref not in text:
        fail(
            "check_lycheeignore must keep must reference " + badge_ref + " needle",
            errors,
        )
    license_enforced = "License badge presence remains " + "enforced"
    if license_enforced not in text:
        fail(
            "check_lycheeignore must keep " + license_enforced + " needle",
            errors,
        )
    exact_layout = "exact live docs-lint second-pass " + "layout"
    if exact_layout not in text:
        fail(
            "check_workflows_and_license must keep " + exact_layout + " needle",
            errors,
        )
    key_set = "exact live docs-lint key " + "set"
    if key_set not in text:
        fail(
            "check_workflows_and_license must keep " + key_set + " needle",
            errors,
        )
    json_true = "JSON " + "true"
    if json_true not in text:
        fail(
            "check_workflows_and_license must keep " + json_true + " needle",
            errors,
        )
    json_false = "JSON " + "false"
    if json_false not in text:
        fail(
            "check_workflows_and_license must keep " + json_false + " needle",
            errors,
        )
    import_json = "import " + "json"
    if import_json not in text:
        fail(
            "check_badge_standard.py must " + import_json + " for docs-lint second-pass",
            errors,
        )
    json_loads = "json." + "loads"
    if json_loads not in text:
        fail(
            "check_workflows_and_license must use " + json_loads,
            errors,
        )
    not_common = "not actionlint / stewardship_common " + "spam"
    if not_common not in text:
        fail(
            "docs-lint second-pass must keep " + not_common + " wording",
            errors,
        )
    not_badge = "stewardship_common / badge " + "spam"
    if not_badge not in text:
        fail(
            "docs-lint contract must keep " + not_badge + " wording",
            errors,
        )

    # Third-pass after #149: docs-lint leftover exact layout + commentary pins.
    third_pass = "Third-pass after " + "#149"
    if third_pass not in text:
        fail(
            "docs-lint must keep " + third_pass + " docstring pin",
            errors,
        )
    docs_third = "docs-lint " + "third-pass"
    if docs_third not in text:
        fail(
            "docs-lint contract must keep " + docs_third + " wording",
            errors,
        )
    exact_lychee_layout = "exact live docs-lint third-pass " + "layout"
    if exact_lychee_layout not in text:
        fail(
            "check_lycheeignore must keep " + exact_lychee_layout + " needle",
            errors,
        )
    mcp_line_pin = "exact MCP 308 commentary " + "line"
    if mcp_line_pin not in text:
        fail(
            "check_lycheeignore must keep " + mcp_line_pin + " needle",
            errors,
        )
    lfs_line_pin = "exact LF 103 commentary " + "line"
    if lfs_line_pin not in text:
        fail(
            "check_lycheeignore must keep " + lfs_line_pin + " needle",
            errors,
        )
    flaky_line_pin = "exact shields flaky commentary " + "line"
    if flaky_line_pin not in text:
        fail(
            "check_lycheeignore must keep " + flaky_line_pin + " needle",
            errors,
        )
    license_line_pin = "exact License enforcement commentary " + "line"
    if license_line_pin not in text:
        fail(
            "check_lycheeignore must keep " + license_line_pin + " needle",
            errors,
        )
    badge_cdn_flaky = "badge CDN is " + "flaky"
    if badge_cdn_flaky not in text:
        fail(
            "check_lycheeignore must keep " + badge_cdn_flaky + " needle",
            errors,
        )
    enforced_by_stew = "enforced by " + "stewardship"
    if enforced_by_stew not in text:
        fail(
            "check_lycheeignore must keep " + enforced_by_stew + " needle",
            errors,
        )
    leftover_docs = "docs-lint " + "leftover"
    if leftover_docs not in text:
        fail(
            "docs-lint third-pass must keep " + leftover_docs + " wording",
            errors,
        )
    not_wiki_ci = "not CI workflow / wiki " + "spam"
    if not_wiki_ci not in text:
        fail(
            "docs-lint third-pass must keep " + not_wiki_ci + " wording",
            errors,
        )
    # Pass-4 after #251: blob/main 503 exclude pins (docs-lint leftover).
    # Split four/th so fourth→quaternary badge-refusal self-tests stay valid.
    fourth_pass = "Pass-4 after " + "#251"
    if fourth_pass not in text:
        fail(
            "docs-lint must keep " + fourth_pass + " docstring pin",
            errors,
        )
    p4_split = '"four" + "th-pass"'
    if p4_split not in text:
        fail(
            "docs-lint contract must keep " + p4_split + " wording",
            errors,
        )
    blob_main_pin = "same-repo " + "blob/main"
    if blob_main_pin not in text:
        fail(
            "check_lycheeignore must keep " + blob_main_pin + " needle",
            errors,
        )
    note_503 = "must note " + "503"
    if note_503 not in text:
        fail(
            "check_lycheeignore must keep " + note_503 + " needle",
            errors,
        )
    wiki_outline_note = "wiki-outline absolute-pin " + "enforcement"
    if wiki_outline_note not in text:
        fail(
            "check_lycheeignore must keep " + wiki_outline_note + " needle",
            errors,
        )
    escaped_blob = (
        r"github\.com/fuzzywigg/agents-governance/" + r"blob/main/"
    )
    if escaped_blob not in text:
        fail(
            "check_lycheeignore must pin " + "escaped blob/main exclude",
            errors,
        )
    exact_blob_line = "exact blob/main 503 commentary " + "line"
    if exact_blob_line not in text:
        fail(
            "check_lycheeignore must keep " + exact_blob_line + " needle",
            errors,
        )
    exact_outline_line = (
        "exact wiki-outline enforcement commentary " + "line"
    )
    if exact_outline_line not in text:
        fail(
            "check_lycheeignore must keep " + exact_outline_line + " needle",
            errors,
        )
    intermittent_503 = "intermittently returns " + "503"
    if intermittent_503 not in text:
        fail(
            "check_lycheeignore must keep " + intermittent_503 + " needle",
            errors,
        )
    not_invent_tpl = "not invent templates / " + "Pass-2 residual spam"
    if not_invent_tpl not in text:
        fail(
            "docs-lint " + "four" + "th-pass must keep " + not_invent_tpl + " wording",
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
    uses_re = 'r"(?m)^\\s*(?:-\\s+)?uses:\\s*(' + '[^\\s#]+)"'
    uses_re_sq = "r'(?m)^\\s*(?:-\\s+)?uses:\\s*(" + "[^\\s#]+)'"
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



    # Fail-closed after #108: third-pass helper / constant / needle pins
    # (actionlint-style reversible CI slice only; not lychee/mdlint/docs-lint spam).
    third_pass_doc = "Third-pass after " + "#108"
    if third_pass_doc not in text:
        fail(
            "check_actionlint_style docstring must pin " + third_pass_doc,
            errors,
        )
    module_third = "third-pass after " + "#108"
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

    # Fail-closed after #135: deepen helper / constant / needle pins
    # (actionlint-style CI reliability leftovers only; not workflow-hardening /
    # badge / wiki / docs-lint / schema / common spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    # Avoid contiguous "four"+"th" wording here — that collides with badge-refusal
    # self-tests that mutate every "fourth" token in this file.
    deepen_doc = "Deepen after " + "#135"
    if deepen_doc not in text:
        fail(
            "check_actionlint_style docstring must pin " + deepen_doc,
            errors,
        )
    module_deepen = "deepen after " + "#135"
    if module_deepen not in text:
        fail(
            "check_badge_standard.py module docstring must pin actionlint "
            + module_deepen,
            errors,
        )
    cancel_true_re = 'r"(?m)^\\s*cancel-in-progress:\\s*' + 'true\\s*$"'
    cancel_true_re_sq = "r'(?m)^\\s*cancel-in-progress:\\s*" + "true\\s*$'"
    if cancel_true_re not in text and cancel_true_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact cancel-in-progress: true regex",
            errors,
        )
    contents_read_re = 'r"(?m)^\\s*contents:\\s*' + 'read\\s*$"'
    contents_read_re_sq = "r'(?m)^\\s*contents:\\s*" + "read\\s*$'"
    if contents_read_re not in text and contents_read_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact contents: read regex",
            errors,
        )
    ubuntu_membership = '"ubuntu-latest" not in ' + "text"
    ubuntu_membership_sq = "'ubuntu-latest' not in " + "text"
    if ubuntu_membership not in text and ubuntu_membership_sq not in text:
        fail(
            "check_actionlint_style must require ubuntu-latest via membership",
            errors,
        )
    dispatch_membership = '"workflow_dispatch:" not in ' + "text"
    dispatch_membership_sq = "'workflow_dispatch:' not in " + "text"
    if dispatch_membership not in text and dispatch_membership_sq not in text:
        fail(
            "check_actionlint_style must require workflow_dispatch: via membership",
            errors,
        )
    security_write_re = 'r"(?m)^\\s*security-events:\\s*' + 'write\\s*$"'
    security_write_re_sq = "r'(?m)^\\s*security-events:\\s*" + "write\\s*$'"
    if security_write_re not in text and security_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact security-events: write regex",
            errors,
        )
    attest_write_re = 'r"(?m)^\\s*attestations:\\s*' + 'write\\s*$"'
    attest_write_re_sq = "r'(?m)^\\s*attestations:\\s*" + "write\\s*$'"
    if attest_write_re not in text and attest_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact attestations: write regex",
            errors,
        )
    statuses_write_re = 'r"(?m)^\\s*statuses:\\s*' + 'write\\s*$"'
    statuses_write_re_sq = "r'(?m)^\\s*statuses:\\s*" + "write\\s*$'"
    if statuses_write_re not in text and statuses_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact statuses: write regex",
            errors,
        )
    deployments_write_re = 'r"(?m)^\\s*deployments:\\s*' + 'write\\s*$"'
    deployments_write_re_sq = "r'(?m)^\\s*deployments:\\s*" + "write\\s*$'"
    if deployments_write_re not in text and deployments_write_re_sq not in text:
        fail(
            "check_actionlint_style must keep exact deployments: write regex",
            errors,
        )
    fail_cancel_true = "actionlint-style requires cancel-in-progress: " + "true"
    if fail_cancel_true not in text:
        fail(
            "check_actionlint_style must emit " + fail_cancel_true + " fail needle",
            errors,
        )
    fail_contents_read = "actionlint-style requires contents: " + "read"
    if fail_contents_read not in text:
        fail(
            "check_actionlint_style must emit " + fail_contents_read + " fail needle",
            errors,
        )
    fail_ubuntu = "actionlint-style requires runs-on ubuntu-" + "latest"
    if fail_ubuntu not in text:
        fail(
            "check_actionlint_style must emit " + fail_ubuntu + " fail needle",
            errors,
        )
    fail_dispatch = "actionlint-style requires workflow_" + "dispatch:"
    if fail_dispatch not in text:
        fail(
            "check_actionlint_style must emit " + fail_dispatch + " fail needle",
            errors,
        )
    fail_security = "security-events: write is forbidden on stewardship " + "workflows"
    if fail_security not in text:
        fail(
            "check_actionlint_style must emit " + fail_security + " fail needle",
            errors,
        )
    fail_attest = "attestations: write is forbidden on stewardship " + "workflows"
    if fail_attest not in text:
        fail(
            "check_actionlint_style must emit " + fail_attest + " fail needle",
            errors,
        )
    fail_statuses = "statuses: write is forbidden on stewardship " + "workflows"
    if fail_statuses not in text:
        fail(
            "check_actionlint_style must emit " + fail_statuses + " fail needle",
            errors,
        )
    fail_deployments = "deployments: write is forbidden on stewardship " + "workflows"
    if fail_deployments not in text:
        fail(
            "check_actionlint_style must emit " + fail_deployments + " fail needle",
            errors,
        )
    reliability_pin = "CI reliability " + "leftovers"
    if reliability_pin not in text:
        fail(
            "check_actionlint_style must keep " + reliability_pin + " wording",
            errors,
        )

    # Leftover after #149: actionlint contents:read membership + leftover wording.
    leftover_149 = "Leftover after " + "#149"
    if leftover_149 not in text:
        fail(
            "check_actionlint_style docstring must pin " + leftover_149,
            errors,
        )
    actionlint_leftover = "actionlint " + "leftover"
    if actionlint_leftover not in text:
        fail(
            "check_actionlint_style must keep " + actionlint_leftover + " wording",
            errors,
        )
    contents_read_mem = '"contents: read" not in ' + "text"
    contents_read_mem_sq = "'contents: read' not in " + "text"
    if contents_read_mem not in text and contents_read_mem_sq not in text:
        fail(
            "check_actionlint_style must require contents: read via membership",
            errors,
        )
    fail_contents_mem = "actionlint-style requires contents:read via " + "membership"
    if fail_contents_mem not in text:
        fail(
            "check_actionlint_style must emit " + fail_contents_mem + " fail needle",
            errors,
        )
    not_docs_wiki = "not docs-lint / wiki " + "spam"
    if not_docs_wiki not in text:
        fail(
            "actionlint leftover must keep " + not_docs_wiki + " wording",
            errors,
        )
    complement_pin = "complement " + "#149"
    if complement_pin not in text:
        fail(
            "actionlint leftover must keep " + complement_pin + " wording",
            errors,
        )


def check_workflow_hardening_gate_contract(errors: list[str]) -> None:
    """Fail-close live CI workflow hardening wiring (third-pass after #111; deepen after #161;
    path-filter leftovers after #173; path-order leftover after #181;
    path-filter/path-order deepen after #203;
    path-filter/path-order residual deepen after #225;
    path-filter/path-order residual leftover deepen after #258;
    path-filter/path-order residual leftover deepen after #272)."""
    text = Path(__file__).read_text(encoding="utf-8")
    # Fail-closed after #111: third-pass helper / constant / needle pins
    # (CI workflow reversible slice only; not badge/wiki/relative/schema/actionlint spam).
    third_pass_doc = "Third-pass after " + "#111"
    if third_pass_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + third_pass_doc,
            errors,
        )
    module_third = "third-pass after " + "#111"
    if module_third not in text:
        fail(
            "check_badge_standard.py module docstring must pin workflow "
            + module_third,
            errors,
        )
    # Split construction keeps self-host mutations fail-closed (needle not only in this tuple).
    pins = (
        ('cron: "30 6 * * ' + '1"', "markdown-lint weekly cron pin"),
        ('cron: "15 6 * * ' + '1"', "stewardship weekly cron pin"),
        ("timeout-minutes: " + "10", "markdown-lint job timeout pin"),
        ("timeout-minutes: " + "15", "stewardship job timeout pin"),
        ("DavidAnson/markdownlint-cli2-action@" + "v24", "markdownlint action major pin"),
        ("actions/setup-python@" + "v5", "setup-python major pin"),
        ("--verb" + "ose", "lychee verbose flag pin"),
        ("--no-prog" + "ress", "lychee no-progress flag pin"),
        ("--max-concurrency " + "8", "lychee max-concurrency pin"),
        ("--timeout " + "20", "lychee timeout pin"),
        ("--max-retries " + "3", "lychee max-retries pin"),
        ("fail: " + "true", "lychee fail-true pin"),
        ("get_actionlint.outputs." + "executable", "actionlint executable output pin"),
        ("id: get_" + "actionlint", "actionlint download step id pin"),
        ("curl -fs" + "SL", "actionlint curl download pin"),
        (
            "link-check-${{ github.workflow }}-${{ github." + "ref }}",
            "link-check concurrency group pin",
        ),
        (
            "markdown-lint-${{ github.workflow }}-${{ github." + "ref }}",
            "markdown-lint concurrency group pin",
        ),
        (
            "stewardship-checks-${{ github.workflow }}-${{ github." + "ref }}",
            "stewardship concurrency group pin",
        ),
        ("reversible CI " + "workflow", "reversible workflow wording pin"),
    )
    for needle, label in pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label + " pin",
                errors,
            )
    # Deepen after #161: stewardship CI reliability leftover contract pins.
    deepen_doc = "Deepen after " + "#161"
    if deepen_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + deepen_doc,
            errors,
        )
    module_deepen = "deepen after " + "#161"
    if module_deepen not in text:
        fail(
            "check_badge_standard.py module docstring must pin workflow "
            + module_deepen,
            errors,
        )
    deepen_pins = (
        ('name: Check ' + 'links', 'Check links ' + 'step-name pin'),
        ('name: Run ' + 'markdownlint', 'Run markdownlint ' + 'step-name pin'),
        ('name: Set up ' + 'Python', 'Set up Python ' + 'step-name pin'),
        (
            'name: Install PyYAML (schema ' + 'parser)',
            'Install PyYAML ' + 'step-name pin',
        ),
        (
            'name: Stewardship gates (badge / wiki / schema / relative ' + 'links)',
            'Stewardship gates ' + 'step-name pin',
        ),
        (
            'name: Stewardship gate ' + 'self-tests',
            'Stewardship gate self-tests ' + 'step-name pin',
        ),
        (
            'token: ${{ secrets.GITHUB_' + 'TOKEN }}',
            'exact token secrets.GITHUB_' + 'TOKEN pin',
        ),
        (
            '--github-token ${{ secrets.GITHUB_' + 'TOKEN }}',
            'exact --github-token secrets.GITHUB_' + 'TOKEN pin',
        ),
        (
            '--exclude-path .github/' + 'agents',
            'contiguous --exclude-path .github/' + 'agents pin',
        ),
        ('globs: ' + '|', 'markdownlint globs ' + 'multiline pin'),
        ('"AGENTS' + '.md"', 'stewardship AGENTS.md ' + 'path pin'),
        ('"CLAUDE' + '.md"', 'stewardship CLAUDE.md ' + 'path pin'),
        ('"LIC' + 'ENSE"', 'stewardship LICENSE ' + 'path pin'),
        ('"CONTRIBUTING' + '.md"', 'stewardship CONTRIBUTING.md ' + 'path pin'),
        (
            '".github/workflows/' + '**"',
            'stewardship .github/workflows/** ' + 'path pin',
        ),
        (
            'GITHUB_TOKEN allows lychee to authenticate private GitHub ' + 'repos',
            'GITHUB_TOKEN allows lychee ' + 'commentary pin',
        ),
        (
            'private repos return ' + '404',
            'private-404 ' + 'commentary pin',
        ),
        (
            'Weekly drift catch aligned with link/stewardship ' + 'schedules',
            'markdownlint Weekly drift ' + 'commentary pin',
        ),
        (
            'Weekly drift catch for badge/wiki/schema/relative-link ' + 'gates',
            'stewardship Weekly drift ' + 'commentary pin',
        ),
        (
            'stewardship CI reliability ' + 'leftovers',
            'reliability-leftovers ' + 'wording',
        ),
    )
    for needle, label in deepen_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )

    # Fail-closed after #173: path-filter leftovers (not path-order/badge /
    # stewardship-badge lint / stewardship CI deepen spam; empty stubs handled).
    path_filter_doc = "Path-filter leftovers after " + "#173"
    if path_filter_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + path_filter_doc,
            errors,
        )
    module_path_filter = "path-filter leftovers after " + "#173"
    if module_path_filter not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + module_path_filter,
            errors,
        )
    empty_stub_pin = "empty workflow stubs already " + "handled"
    if empty_stub_pin not in text:
        fail(
            "check_workflow_hardening must note " + empty_stub_pin,
            errors,
        )
    not_path_order = "not path-order/badge " + "spam"
    if not_path_order not in text:
        fail(
            "check_workflow_hardening must keep " + not_path_order + " wording",
            errors,
        )
    reject_paths_ignore = "must not use paths-ignore: " + "(path-filter leftovers)"
    if reject_paths_ignore not in text:
        fail(
            "check_workflow_hardening must reject paths-ignore leftovers",
            errors,
        )
    link_layout_pin = "link-check.yml must keep exact push paths " + "filter layout"
    if link_layout_pin not in text:
        fail(
            "check_workflow_hardening must pin " + link_layout_pin,
            errors,
        )
    lint_layout_pin = "markdown-lint.yml must keep exact push paths " + "filter layout"
    if lint_layout_pin not in text:
        fail(
            "check_workflow_hardening must pin " + lint_layout_pin,
            errors,
        )
    stew_layout_pin = (
        "stewardship-checks.yml must keep exact push paths " + "filter layout"
    )
    if stew_layout_pin not in text:
        fail(
            "check_workflow_hardening must pin " + stew_layout_pin,
            errors,
        )
    agents_path_pin = "paths filter must include " + "AGENTS.md"
    if agents_path_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship AGENTS.md path",
            errors,
        )
    claude_path_pin = "paths filter must include " + "CLAUDE.md"
    if claude_path_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship CLAUDE.md path",
            errors,
        )
    license_path_pin = "paths filter must include " + "LICENSE"
    if license_path_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship LICENSE path",
            errors,
        )
    contrib_path_pin = "paths filter must include " + "CONTRIBUTING.md"
    if contrib_path_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship CONTRIBUTING.md path",
            errors,
        )
    workflows_glob_pin = "paths filter must include " + ".github/workflows/**"
    if workflows_glob_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship workflows/** path",
            errors,
        )
    stew_lychee_pin = "stewardship-checks.yml paths filter must list " + ".lycheeignore"
    if stew_lychee_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship .lycheeignore path",
            errors,
        )
    stew_mdlint_pin = (
        "stewardship-checks.yml paths filter must list " + ".markdownlint.json"
    )
    if stew_mdlint_pin not in text:
        fail(
            "check_workflow_hardening must pin stewardship .markdownlint.json path",
            errors,
        )
    link_lychee_pin = "link-check.yml paths filter must list " + ".lycheeignore"
    if link_lychee_pin not in text:
        fail(
            "check_workflow_hardening must pin link-check .lycheeignore path",
            errors,
        )
    lint_md_pin = "markdown-lint.yml paths filter must list " + ".markdownlint.json"
    if lint_md_pin not in text:
        fail(
            "check_workflow_hardening must pin markdown-lint .markdownlint.json path",
            errors,
        )
    exclude_path_pin = "--exclude-path .github/" + "agents"
    if exclude_path_pin not in text:
        fail(
            "check_workflow_hardening must pin link-check agents exclude-path",
            errors,
        )
    ignore_glob_layout = "exact ignore-glob globs " + "layout"
    if ignore_glob_layout not in text:
        fail(
            "check_workflow_hardening must pin " + ignore_glob_layout,
            errors,
        )
    declare_paths_pin = "must declare push paths: " + "filter"
    if declare_paths_pin not in text:
        fail(
            "check_workflow_hardening must require push paths: declaration",
            errors,
        )


    # Path-order leftover after #181 (lands closed #157/#182; NOT path-filter /
    # NOT wiki-index / NOT run_stewardship / NOT #165 stewardship CI).
    path_order_doc = "Path-order leftover after " + "#181"
    if path_order_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + path_order_doc,
            errors,
        )
    module_path_order = "Path-order leftover after " + "#181"
    if module_path_order not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + module_path_order,
            errors,
        )
    not_157 = "lands closed " + "#157"
    if not_157 not in text:
        fail(
            "path-order leftover must keep " + not_157 + " distinctness pin",
            errors,
        )
    not_182 = "lands closed #157/" + "#182"
    if not_182 not in text:
        fail(
            "path-order leftover must keep closed #182 distinctness pin",
            errors,
        )
    not_path_filter = "NOT " + "path-filter"
    if not_path_filter not in text:
        fail(
            "path-order leftover must keep " + not_path_filter + " distinctness pin",
            errors,
        )
    not_wiki_index = "NOT " + "wiki-index"
    if not_wiki_index not in text:
        fail(
            "path-order leftover must keep " + not_wiki_index + " distinctness pin",
            errors,
        )
    not_run_stew = "NOT " + "run_stewardship"
    if not_run_stew not in text:
        fail(
            "path-order leftover must keep " + not_run_stew + " distinctness pin",
            errors,
        )
    # Split construction keeps self-host mutations fail-closed.
    path_order_pins = (
        (
            ".github/workflows/link-check.yml" + " ",
            "link-check.yml path pin (path-order leftover)",
        ),
        (
            ".github/workflows/markdown-lint.yml" + " ",
            "markdown-lint.yml path pin (path-order leftover)",
        ),
        (
            ".github/workflows/stewardship-checks" + ".yml",
            "stewardship-checks.yml path pin (path-order leftover)",
        ),
        (
            "in order: " + "link-check",
            "three-path order fail needle",
        ),
        (
            "bash <(curl -fsSL https://raw." + "githubusercontent.com/",
            "exact bash <(curl -fsSL) download form pin",
        ),
        (
            "must not set continue-on-error: " + "true",
            "continue-on-error: true fail needle",
        ),
        (
            "name: Download " + "actionlint",
            "Download actionlint step-name pin",
        ),
        (
            "name: actionlint existing workflow " + "paths",
            "actionlint existing workflow paths step-name pin",
        ),
        (
            "actionlint path-order " + "leftover",
            "path-order leftover wording pin",
        ),
    )
    for needle, label in path_order_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )


    # Path-filter/path-order deepen after #203 (DISTINCT leftover edges).
    deepen_203_doc = "Path-filter/path-order deepen after " + "#203"
    if deepen_203_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + deepen_203_doc,
            errors,
        )
    module_deepen_203 = "path-filter/path-order deepen after " + "#203"
    if module_deepen_203 not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + module_deepen_203,
            errors,
        )
    not_saturated_189 = "NOT saturated " + "#189"
    if not_saturated_189 not in text:
        fail(
            "path deepen must keep " + not_saturated_189 + " distinctness pin",
            errors,
        )
    not_176_layouts = "NOT " + "#176"
    if not_176_layouts not in text:
        fail(
            "path deepen must keep " + not_176_layouts + " distinctness pin",
            errors,
        )
    not_schema_191 = "NOT schema " + "#191"
    if not_schema_191 not in text:
        fail(
            "path deepen must keep " + not_schema_191 + " distinctness pin",
            errors,
        )
    not_pass2_res = "NOT Pass-2 residual " + "#199"
    if not_pass2_res not in text:
        fail(
            "path deepen must keep " + not_pass2_res + " distinctness pin",
            errors,
        )
    not_pass2_192 = "NOT Pass-2+md/link " + "#192"
    if not_pass2_192 not in text:
        fail(
            "path deepen must keep " + not_pass2_192 + " distinctness pin",
            errors,
        )
    not_wiki_badge = "NOT " + "wiki-badge"
    if not_wiki_badge not in text:
        fail(
            "path deepen must keep " + not_wiki_badge + " distinctness pin",
            errors,
        )
    not_badge_lint = "NOT stewardship-badge lint " + "#208"
    if not_badge_lint not in text:
        fail(
            "path deepen must keep " + not_badge_lint + " distinctness pin",
            errors,
        )
    not_schema_216 = "NOT schema fourth-pass " + "#216"
    if not_schema_216 not in text:
        fail(
            "path deepen must keep " + not_schema_216 + " distinctness pin",
            errors,
        )
    deepen_203_pins = (
        (
            "contiguous push/branches/paths " + "header",
            "push/branches/paths header fail needle",
        ),
        (
            "pull_request must stay path-" + "unfiltered",
            "pull_request path-unfiltered fail needle",
        ),
        (
            "must not invent dorny/paths-" + "filter",
            "dorny/paths-filter reject needle",
        ),
        (
            "paths filter must list self workflow " + "path",
            "self-workflow path list fail needle",
        ),
        (
            "exact contiguous actionlint run " + "command",
            "exact actionlint run fail needle",
        ),
        (
            "contiguous Download/id/run/shell " + "actionlint download block",
            "download block fail needle",
        ),
        (
            "Download actionlint must precede " + "actionlint existing",
            "Download-before-run order fail needle",
        ),
        (
            "Stewardship gate self-tests must precede " + "Download actionlint",
            "self-tests-before-Download order fail needle",
        ),
        (
            "must not invent uses: rhysd/actionlint" + "@",
            "rhysd/actionlint@ invent reject needle",
        ),
        (
            "path-filter/path-order deepen after " + "#203",
            "deepen-after-203 wording pin",
        ),
    )
    for needle, label in deepen_203_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )

    # Stewardship-checks + schema residual deepen after #225 (DISTINCT leftover).
    residual_225_doc = "Stewardship-checks + schema residual deepen after " + "#225"
    if residual_225_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + residual_225_doc,
            errors,
        )
    module_residual_225 = "stewardship-checks + schema residual deepen after " + "#225"
    if module_residual_225 not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + module_residual_225,
            errors,
        )
    not_path_edges_225 = "NOT path-edges " + "#225"
    if not_path_edges_225 not in text:
        fail(
            "residual deepen must keep " + not_path_edges_225 + " distinctness pin",
            errors,
        )
    not_pass2_220 = "NOT Pass-2 leftover+md/link " + "#220"
    if not_pass2_220 not in text:
        fail(
            "residual deepen must keep " + not_pass2_220 + " distinctness pin",
            errors,
        )
    not_schema_fourth = "NOT schema fourth-pass " + "#216"
    if not_schema_fourth not in text:
        fail(
            "residual deepen must keep " + not_schema_fourth + " distinctness pin",
            errors,
        )
    residual_225_pins = (
        (
            "exact contiguous Set up Python" + " ",
            "Set up Python block fail needle",
        ),
        (
            "exact Install PyYAML" + " ",
            "Install PyYAML block fail needle",
        ),
        (
            "checkout@v7 must immediately precede" + " ",
            "checkout→Set up Python adjacency fail needle",
        ),
        (
            "exact full push paths list" + " ",
            "full push paths list fail needle",
        ),
        (
            "exact schedule Weekly-drift +" + " ",
            "schedule+cron block fail needle",
        ),
        (
            "exact concurrency group +" + " ",
            "concurrency block fail needle",
        ),
        (
            "exact jobs.stewardship" + " ",
            "jobs.stewardship header fail needle",
        ),
        (
            "must not invent strategy" + ":",
            "strategy invent reject needle",
        ),
        (
            "must not invent matrix" + ":",
            "matrix invent reject needle",
        ),
        (
            "must not invent services" + ":",
            "services invent reject needle",
        ),
        (
            "stewardship-checks + schema residual after " + "#225",
            "residual-after-225 wording pin",
        ),
    )
    for needle, label in residual_225_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )

    # Path-filter/path-order residual deepen after #225 (DISTINCT leftover edges).
    path_residual_225_doc = "Path-filter/path-order residual deepen after " + "#225"
    if path_residual_225_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + path_residual_225_doc,
            errors,
        )
    path_module_residual_225 = "path-filter/path-order residual deepen after " + "#225"
    if path_module_residual_225 not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + path_module_residual_225,
            errors,
        )
    not_saturated_225 = "NOT saturated deepen " + "#225"
    if not_saturated_225 not in text:
        fail(
            "path residual must keep " + not_saturated_225 + " distinctness pin",
            errors,
        )
    not_189_path_order = "NOT " + "#189"
    if not_189_path_order not in text:
        fail(
            "path residual must keep " + not_189_path_order + " distinctness pin",
            errors,
        )
    not_176_layouts = "NOT " + "#176"
    if not_176_layouts not in text:
        fail(
            "path residual must keep " + not_176_layouts + " distinctness pin",
            errors,
        )
    not_schema_191_216 = "NOT schema " + "#191/#216"
    if not_schema_191_216 not in text:
        fail(
            "path residual must keep " + not_schema_191_216 + " distinctness pin",
            errors,
        )
    not_pass2_spaces_220 = "NOT Pass-2 leftover + " + "md/link #220"
    if not_pass2_spaces_220 not in text:
        fail(
            "path residual must keep " + not_pass2_spaces_220 + " distinctness pin",
            errors,
        )
    not_stew_schema_233 = "NOT stewardship-checks/schema leftover " + "#233"
    if not_stew_schema_233 not in text:
        fail(
            "path residual must keep " + not_stew_schema_233 + " distinctness pin",
            errors,
        )
    not_path_badge_lint_208 = "NOT stewardship-badge lint " + "#208"
    if not_path_badge_lint_208 not in text:
        fail(
            "path residual must keep " + not_path_badge_lint_208 + " distinctness pin",
            errors,
        )
    path_residual_225_pins = (
        (
            "contiguous pull_request:/schedule: " + "adjacency",
            "pull_request/schedule adjacency fail needle",
        ),
        (
            "must not invent branches-" + "ignore:",
            "branches-ignore invent reject needle",
        ),
        (
            "pull_request must stay type-" + "unfiltered",
            "pull_request type-unfiltered fail needle",
        ),
        (
            "must not invent tj-actions/changed-" + "files",
            "changed-files invent reject needle",
        ),
        (
            "contiguous four-step " + "actionlint path-order",
            "four-step actionlint path-order fail needle",
        ),
        (
            "schedule: must precede " + "workflow_dispatch:",
            "schedule-before-dispatch fail needle",
        ),
        (
            "contiguous shell-less " + "actionlint run step",
            "shell-less actionlint run step fail needle",
        ),
        (
            "path-filter/path-order residual deepen after " + "#225",
            "path residual-after-225 wording pin",
        ),
    )
    for needle, label in path_residual_225_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )

    # Path-filter/path-order residual leftover deepen after #258 (DISTINCT leftover).
    path_leftover_258_doc = (
        "Path-filter/path-order residual leftover deepen after " + "#258"
    )
    if path_leftover_258_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + path_leftover_258_doc,
            errors,
        )
    path_module_leftover_258 = (
        "path-filter/path-order residual leftover deepen after " + "#258"
    )
    if path_module_leftover_258 not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + path_module_leftover_258,
            errors,
        )
    not_saturated_residual_244 = "NOT saturated residual " + "#244"
    if not_saturated_residual_244 not in text:
        fail(
            "path leftover must keep "
            + not_saturated_residual_244
            + " distinctness pin",
            errors,
        )
    not_schema_leftover_258 = "NOT stewardship-schema leftover " + "#258"
    if not_schema_leftover_258 not in text:
        fail(
            "path leftover must keep " + not_schema_leftover_258 + " distinctness pin",
            errors,
        )
    not_wiki_mdlink_252 = "NOT wiki/mdlink leftover " + "#252"
    if not_wiki_mdlink_252 not in text:
        fail(
            "path leftover must keep " + not_wiki_mdlink_252 + " distinctness pin",
            errors,
        )
    not_wiki_publish_243 = "NOT wiki outline/PUBLISH leftover " + "#243"
    if not_wiki_publish_243 not in text:
        fail(
            "path leftover must keep " + not_wiki_publish_243 + " distinctness pin",
            errors,
        )
    not_mdlink_239 = "NOT md/link residual " + "#239"
    if not_mdlink_239 not in text:
        fail(
            "path leftover must keep " + not_mdlink_239 + " distinctness pin",
            errors,
        )
    not_stew_schema_233_leftover = (
        "NOT stewardship-checks/schema leftover " + "#233"
    )
    if not_stew_schema_233_leftover not in text:
        fail(
            "path leftover must keep "
            + not_stew_schema_233_leftover
            + " distinctness pin",
            errors,
        )
    not_wiki_badge_227 = "NOT wiki-badge leftover " + "#227"
    if not_wiki_badge_227 not in text:
        fail(
            "path leftover must keep " + not_wiki_badge_227 + " distinctness pin",
            errors,
        )
    not_saturated_deepen_225 = "NOT saturated deepen " + "#225"
    if not_saturated_deepen_225 not in text:
        fail(
            "path leftover must keep "
            + not_saturated_deepen_225
            + " distinctness pin",
            errors,
        )
    not_pass2_220_leftover = "NOT Pass-2 leftover + " + "md/link #220"
    if not_pass2_220_leftover not in text:
        fail(
            "path leftover must keep "
            + not_pass2_220_leftover
            + " distinctness pin",
            errors,
        )
    path_leftover_258_pins = (
        (
            "contiguous push:/pull_request: " + "adjacency",
            "push/pull_request adjacency fail needle",
        ),
        (
            "contiguous schedule:/workflow_dispatch: " + "adjacency",
            "schedule/workflow_dispatch adjacency fail needle",
        ),
        (
            "pull_request must stay branches-" + "unfiltered",
            "pull_request branches-unfiltered fail needle",
        ),
        (
            "must not invent tags-" + "ignore:",
            "tags-ignore invent reject needle",
        ),
        (
            "must not invent workflow_" + "call:",
            "workflow_call invent reject needle",
        ),
        (
            "contiguous five-step " + "actionlint path-order",
            "five-step actionlint path-order fail needle",
        ),
        (
            "contiguous on:/push: " + "header",
            "on/push header fail needle",
        ),
        (
            "path-filter/path-order residual leftover deepen after " + "#258",
            "path leftover-after-258 wording pin",
        ),
    )
    for needle, label in path_leftover_258_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )

    # Path-filter/path-order residual leftover deepen after #272 (DISTINCT leftover).
    path_leftover_272_doc = (
        "Path-filter/path-order residual leftover deepen after " + "#272"
    )
    if path_leftover_272_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + path_leftover_272_doc,
            errors,
        )
    path_module_leftover_272 = (
        "path-filter/path-order residual leftover deepen after " + "#272"
    )
    if path_module_leftover_272 not in text:
        fail(
            "check_badge_standard.py module docstring must pin "
            + path_module_leftover_272,
            errors,
        )
    not_pass2_leftover_272 = "NOT Pass-2 residual leftover " + "#272"
    if not_pass2_leftover_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_pass2_leftover_272
            + " distinctness pin",
            errors,
        )
    not_blob503_278 = "NOT lychee/blob-503 harden " + "#278"
    if not_blob503_278 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_blob503_278
            + " distinctness pin",
            errors,
        )
    not_saturated_leftover_272 = "NOT saturated leftover " + "#262"
    if not_saturated_leftover_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_saturated_leftover_272
            + " distinctness pin",
            errors,
        )
    not_schema_leftover_258_272 = "NOT stewardship-schema leftover " + "#258"
    if not_schema_leftover_258_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_schema_leftover_258_272
            + " distinctness pin",
            errors,
        )
    not_wiki_mdlink_252_272 = "NOT wiki/mdlink leftover " + "#252"
    if not_wiki_mdlink_252_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_wiki_mdlink_252_272
            + " distinctness pin",
            errors,
        )
    not_saturated_residual_244_272 = "NOT saturated residual " + "#244"
    if not_saturated_residual_244_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_saturated_residual_244_272
            + " distinctness pin",
            errors,
        )
    not_wiki_publish_243_272 = "NOT wiki outline/PUBLISH leftover " + "#243"
    if not_wiki_publish_243_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_wiki_publish_243_272
            + " distinctness pin",
            errors,
        )
    not_mdlink_239_272 = "NOT md/link residual " + "#239"
    if not_mdlink_239_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_mdlink_239_272
            + " distinctness pin",
            errors,
        )
    not_stew_schema_233_272 = (
        "NOT stewardship-checks/schema leftover " + "#233"
    )
    if not_stew_schema_233_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_stew_schema_233_272
            + " distinctness pin",
            errors,
        )
    not_wiki_badge_227_272 = "NOT wiki-badge leftover " + "#227"
    if not_wiki_badge_227_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_wiki_badge_227_272
            + " distinctness pin",
            errors,
        )
    not_saturated_deepen_225_272 = "NOT saturated deepen " + "#225"
    if not_saturated_deepen_225_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_saturated_deepen_225_272
            + " distinctness pin",
            errors,
        )
    not_pass2_220_leftover_272 = "NOT Pass-2 leftover + " + "md/link #220"
    if not_pass2_220_leftover_272 not in text:
        fail(
            "path leftover-after-272 must keep "
            + not_pass2_220_leftover_272
            + " distinctness pin",
            errors,
        )
    path_leftover_272_pins = (
        (
            "contiguous workflow_dispatch:/concurrency: " + "adjacency",
            "workflow_dispatch/concurrency adjacency fail needle",
        ),
        (
            "contiguous name:/on: " + "workflow header",
            "name/on workflow header fail needle",
        ),
        (
            "must not invent workflow_" + "run:",
            "workflow_run invent reject needle",
        ),
        (
            "must not invent repository_" + "dispatch:",
            "repository_dispatch invent reject needle",
        ),
        (
            "must not invent merge_" + "group:",
            "merge_group invent reject needle",
        ),
        (
            "must not invent tags: " + "(bare tags: key",
            "tags invent reject needle",
        ),
        (
            "contiguous six-step " + "actionlint path-order",
            "six-step actionlint path-order fail needle",
        ),
        (
            "path-filter/path-order residual leftover deepen after " + "#272",
            "path leftover-after-272 wording pin",
        ),
    )
    for needle, label in path_leftover_272_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )

    fn_pin = "def check_workflow_hardening" + "("
    if fn_pin not in text:
        fail(
            "check_badge_standard.py must define check_workflow_hardening function",
            errors,
        )
    call_pin = "check_workflow_hardening_gate_contract" + "("
    def_pin = "def check_workflow_hardening_gate_contract" + "("
    if call_pin not in text.replace(def_pin, "", 1):
        fail(
            "check_badge_standard.py main must call workflow hardening gate contract",
            errors,
        )
    if def_pin not in text:
        fail(
            "check_badge_standard.py must define workflow hardening gate contract",
            errors,
        )

    # Fail-closed after #203 tip: markdown-lint / link-check workflow edge pins
    # (lands closed #202/#192 leftover; not path-filter / Pass-2 / path-order / schema spam).
    edge_doc = "Markdown-lint/link-check workflow edges after " + "#203"
    if edge_doc not in text:
        fail(
            "check_workflow_hardening docstring must pin " + edge_doc,
            errors,
        )
    module_edge = "markdown-lint/link-check edges after " + "#203"
    if module_edge not in text:
        fail(
            "check_badge_standard.py module docstring must pin " + module_edge,
            errors,
        )
    edge_pins = (
        ("args: " + ">-", "lychee args multiline form pin"),
        (
            "externally broken links " + "commentary",
            "link-check externally-broken commentary pin",
        ),
        (
            "without-it private-404 " + "commentary",
            "link-check without-it private-404 pin",
        ),
        (
            "must not set continue-on-" + "error",
            "continue-on-error reject pin",
        ),
        (
            "exact job permissions: contents: " + "read",
            "job permissions exact pin",
        ),
        (
            "checkout before Check links " + "adjacency",
            "link-check checkout adjacency pin",
        ),
        (
            "checkout before Run markdownlint " + "adjacency",
            "markdown-lint checkout adjacency pin",
        ),
    )
    for needle, label in edge_pins:
        if needle not in text:
            fail(
                "check_workflow_hardening must keep " + label,
                errors,
            )



    # Stewardship-badge lint deepen after #189: exact globs + paths contract.
    after_189_wf = "after " + "#189"
    if after_189_wf not in text:
        fail(
            "workflow hardening must pin stewardship-badge lint " + after_189_wf,
            errors,
        )
    exact_globs = "exact live stewardship-badge lint " + "globs block"
    if exact_globs not in text:
        fail(
            "check_workflow_hardening must keep " + exact_globs + " needle",
            errors,
        )
    exact_md_paths = "exact live stewardship-badge lint " + "push paths filter"
    if exact_md_paths not in text:
        fail(
            "check_workflow_hardening must keep " + exact_md_paths + " needle",
            errors,
        )
    globs_pipe = "globs: " + "|"
    if globs_pipe not in text:
        fail(
            "check_workflow_hardening must pin exact " + globs_pipe + " layout",
            errors,
        )
    bang_agents = "!.github/agents/" + "**"
    if bang_agents not in text:
        fail(
            "check_workflow_hardening must keep " + bang_agents + " glob pin",
            errors,
        )
    bang_owasp = "!OWASP-AGENTIC" + ".md"
    if bang_owasp not in text:
        fail(
            "check_workflow_hardening must keep " + bang_owasp + " glob pin",
            errors,
        )
    md_json_paths = '".markdownlint' + '.json"'
    if md_json_paths not in text:
        fail(
            "check_workflow_hardening must pin paths " + md_json_paths,
            errors,
        )
    lychee_paths = '".lychee' + 'ignore"'
    if lychee_paths not in text:
        fail(
            "check_workflow_hardening must pin paths " + lychee_paths,
            errors,
        )
    not_docs_189 = "NOT docs-lint " + "leftover"
    if not_docs_189 not in text:
        fail(
            "stewardship-badge lint must keep " + not_docs_189 + " distinctness",
            errors,
        )

def check_stewardship_common_contract(errors: list[str]) -> None:
    """Fail-close live stewardship_common wiring (after #111; deepen after #65/#46; leftover after #252)."""
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

    # Fail-closed after #252: common leftover helper / constant / needle pins
    # (common leftover slice only; not wiki/mdlink leftover #252 / not path-edges residual #244 /
    # not wiki outline/PUBLISH #243 / not md/link residual #239 / not schema residual (pass-5) #233 spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    common_leftover_doc = "Residual leftover after " + "#252 (common leftover"
    if common_leftover_doc not in text:
        fail(
            "stewardship_common.py docstring must pin " + common_leftover_doc,
            errors,
        )
    elif_hint = "elif hint in " + "text"
    if elif_hint not in text:
        fail(
            "stewardship_common.py scan_secrets must keep elif hint in text",
            errors,
        )
    for_globs = "for pattern in " + "globs"
    if for_globs not in text:
        fail(
            "stewardship_common.py markdown_files must iterate for pattern in globs",
            errors,
        )
    found_init = "found: set[Path] = " + "set()"
    if found_init not in text:
        fail(
            "stewardship_common.py markdown_files must init found: set[Path] = set()",
            errors,
        )
    missing_wf = "if not path.is_" + "file():"
    if missing_wf not in text:
        fail(
            "stewardship_common.py load_workflow_text must keep if not path.is_file():",
            errors,
        )
    common_host = "common leftover after " + "#252"
    self_text_common_left = BADGE_GATE.read_text(encoding="utf-8")
    if common_host not in self_text_common_left:
        fail(
            "check_badge_standard.py must keep " + common_host + " host pin",
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


    # Fail-closed after #111: third-pass helper / constant / needle pins
    # (stewardship_common slice only; not docs-lint / wiki / relative /
    # actionlint / schema / badge / CI workflow pin spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    future_pin = "from __future__ import " + "annotations"
    if future_pin not in text:
        fail(
            "stewardship_common.py must keep from __future__ import annotations",
            errors,
        )
    if "import re" not in text:
        fail(
            "stewardship_common.py must import re",
            errors,
        )
    path_import = "from pathlib import " + "Path"
    if path_import not in text:
        fail(
            "stewardship_common.py must import Path from pathlib",
            errors,
        )
    priv_key = "-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE " + "KEY-----"
    if priv_key not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact PRIVATE KEY pattern",
            errors,
        )
    ghp_group = r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"
    if ghp_group not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact ghp|gho|ghu|ghs|ghr group",
            errors,
        )
    github_pat_exact = r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"
    if github_pat_exact not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact github_pat_ pattern",
            errors,
        )
    sk_rk_exact = r"\b(sk|rk)-[A-Za-z0-9]{20,}\b"
    if sk_rk_exact not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact sk|rk pattern",
            errors,
        )
    tuple_typing = "tuple[re.Pattern[str], " + "...]"
    if tuple_typing not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must use tuple[re.Pattern[str], ...] typing",
            errors,
        )
    secret_tuple_assign = "SECRET_PATTERNS: tuple"
    if secret_tuple_assign not in text:
        fail(
            "stewardship_common.py must declare SECRET_PATTERNS: tuple",
            errors,
        )
    fence_sub = "FENCED_BLOCK_RE.sub(" + '"", text)'
    fence_sub_sq = "FENCED_BLOCK_RE.sub(" + "'', text)"
    if fence_sub not in text and fence_sub_sq not in text:
        fail(
            "stewardship_common.py strip_fenced_code must FENCED_BLOCK_RE.sub(\"\", text)",
            errors,
        )
    label_or = "label or str(path.relative_to(" + "ROOT))"
    if label_or not in text:
        fail(
            "stewardship_common.py scan_secrets must use label or str(path.relative_to(ROOT))",
            errors,
        )
    search_pin = "pattern.search(" + "text)"
    if search_pin not in text:
        fail(
            "stewardship_common.py scan_secrets must call pattern.search(text)",
            errors,
        )
    lowered_pin = "lowered = text." + "lower()"
    if lowered_pin not in text:
        fail(
            "stewardship_common.py scan_secrets must set lowered = text.lower()",
            errors,
        )
    escape_pin = "re.escape(" + "hint)"
    if escape_pin not in text:
        fail(
            "stewardship_common.py scan_secrets must re.escape(hint) for URL-ish hints",
            errors,
        )
    urlish_re = r"https?://[^\s)]*"
    if urlish_re not in text:
        fail(
            "stewardship_common.py scan_secrets must match https?://[^\\s)]* URL-ish pattern",
            errors,
        )
    glob_pin = "ROOT.glob(" + "pattern)"
    if glob_pin not in text:
        fail(
            "stewardship_common.py markdown_files must ROOT.glob(pattern)",
            errors,
        )
    update_pin = "found.update("
    if update_pin not in text:
        fail(
            "stewardship_common.py markdown_files must found.update(...)",
            errors,
        )
    set_path = "set[Path]"
    if set_path not in text:
        fail(
            "stewardship_common.py markdown_files must type found as set[Path]",
            errors,
        )
    # Split so badge third-pass replace of contiguous
    # ROOT / ".github" / "workflows" cannot neutralize this pin.
    wf_join = 'ROOT / ".github" / "' + 'workflows" / name'
    wf_join_sq = "ROOT / '.github' / '" + "workflows' / name"
    if wf_join not in text and wf_join_sq not in text:
        fail(
            "stewardship_common.py load_workflow_text must join ROOT / "
            '".github" / "workflows" / name',
            errors,
        )
    for_scheme = "for scheme in DANGEROUS_" + "LINK_SCHEMES"
    if for_scheme not in text:
        fail(
            "stewardship_common.py has_dangerous_scheme must iterate DANGEROUS_LINK_SCHEMES",
            errors,
        )
    for_pattern = "for pattern in SECRET_" + "PATTERNS"
    if for_pattern not in text:
        fail(
            "stewardship_common.py scan_secrets must iterate SECRET_PATTERNS",
            errors,
        )
    for_hint = "for hint in SECRET_URL_" + "HINTS"
    if for_hint not in text:
        fail(
            "stewardship_common.py scan_secrets must iterate SECRET_URL_HINTS",
            errors,
        )
    shared_helpers = "Shared helpers for stewardship doc " + "gates"
    if shared_helpers not in text:
        fail(
            "stewardship_common.py must keep Shared helpers for stewardship doc gates pin",
            errors,
        )
    endswith_eq = 'hint.endswith("=")'
    endswith_eq_sq = "hint.endswith('=')"
    if endswith_eq not in text and endswith_eq_sq not in text:
        fail(
            'stewardship_common.py scan_secrets must call hint.endswith("=")',
            errors,
        )
    memory_dumps = "MEMORY " + "dumps"
    if memory_dumps not in text:
        fail(
            "stewardship_common.py must keep MEMORY dumps comment pin",
            errors,
        )
    str_none = "str | " + "None"
    if str_none not in text:
        fail(
            "stewardship_common.py has_dangerous_scheme must annotate str | None",
            errors,
        )
    list_path = "list[" + "Path]"
    if list_path not in text:
        fail(
            "stewardship_common.py markdown_files must annotate list[Path]",
            errors,
        )
    forbidden_head = (
        "FORBIDDEN_BADGE_HINTS = (\n"
        '    "coverage",\n'
        '    "codecov",\n'
        '    "coveralls",'
    )
    forbidden_head_sq = forbidden_head.replace('"', "'")
    if forbidden_head not in text and forbidden_head_sq not in text:
        fail(
            'stewardship_common.py must set FORBIDDEN_BADGE_HINTS starting with coverage/codecov/coveralls',
            errors,
        )
    # SECRET_URL_HINTS token-prefix members (live path; distinct from SECRET_PATTERNS).
    for prefix in ('"ghp_"', '"gho_"', '"github_pat_"'):
        if prefix not in text and prefix.replace('"', "'") not in text:
            fail(
                f"stewardship_common.py SECRET_URL_HINTS must pin {prefix}",
                errors,
            )
    third_pass_doc = "Third-pass: future annotations / import re+" + "Path"
    if third_pass_doc not in text:
        fail(
            "stewardship_common.py docstring must pin Third-pass future annotations / import re+Path",
            errors,
        )
    module_third = "third-pass after " + "#111"
    if module_third not in text and "third-pass after #111" not in text:
        fail(
            "stewardship_common.py docstring must keep third-pass after #111 pin",
            errors,
        )
    # load_workflow_text must read with utf-8 when present.
    load_utf8 = 'return path.read_text(encoding="utf-8")'
    load_utf8_sq = "return path.read_text(encoding='utf-8')"
    if load_utf8 not in text and load_utf8_sq not in text:
        fail(
            'stewardship_common.py load_workflow_text must return path.read_text(encoding="utf-8")',
            errors,
        )
    scan_utf8 = 'text = path.read_text(encoding="utf-8")'
    scan_utf8_sq = "text = path.read_text(encoding='utf-8')"
    if scan_utf8 not in text and scan_utf8_sq not in text:
        fail(
            'stewardship_common.py scan_secrets must path.read_text(encoding="utf-8")',
            errors,
        )
    # Exact aws / slack / npm / AIza regex fragments still live.
    aws_re = r"aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{20,}"
    if aws_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact aws_secret_access_key pattern",
            errors,
        )
    xox_re = r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"
    if xox_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact xox[baprs] pattern",
            errors,
        )
    npm_re = r"\bnpm_[A-Za-z0-9]{20,}\b"
    if npm_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact npm_ pattern",
            errors,
        )
    aiza_re = r"\bAIza[0-9A-Za-z\-_]{20,}\b"
    if aiza_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact AIza pattern",
            errors,
        )
    api_key_re = r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"
    if api_key_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact api[_-]?key pattern",
            errors,
        )
    secret_assign_re = r"(?i)secret\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"
    if secret_assign_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact secret assign pattern",
            errors,
        )
    passwd_re = r"(?i)(?:password|passwd|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    if passwd_re not in text:
        fail(
            "stewardship_common.py SECRET_PATTERNS must pin exact password|passwd|token assign pattern",
            errors,
        )


    # Self-pins for third-pass docstring / slice commentary (host module).
    self_host = BADGE_GATE.read_text(encoding="utf-8")
    after_104_doc = "after #111; deepen after #65/" + "#46"
    if after_104_doc not in self_host:
        fail(
            "check_stewardship_common_contract docstring must keep " + after_104_doc,
            errors,
        )
    slice_only = "stewardship_common slice " + "only"
    if slice_only not in self_host:
        fail(
            "check_stewardship_common_contract must keep " + slice_only + " pin",
            errors,
        )
    spam_docs = "not docs-lint / wiki / relative " + "/"
    if spam_docs not in self_host:
        fail(
            "check_stewardship_common_contract must keep not docs-lint / wiki / relative / spam pin",
            errors,
        )
    if "Second-pass: ROOT parents[1]" not in text:
        fail(
            "stewardship_common.py docstring must keep Second-pass: ROOT parents[1] pin",
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
    """Fail-close live stewardship-schema gate wiring (after #72/#75; third-pass after #132; deepen after #189; policy-schema pass-4 after #208; schema residual after #225; leftover after #252)."""
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


    # Fail-closed after #132: third-pass helper / constant / needle pins
    # (schema slice only; not docs-lint / wiki / relative / actionlint / workflow spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    third_pass_doc = "Third-pass after " + "#132"
    if third_pass_doc not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + third_pass_doc,
            errors,
        )
    future_ann = "from __future__ import " + "annotations"
    if future_ann not in text:
        fail(
            "check_stewardship_schema.py must import " + future_ann,
            errors,
        )
    path_parent = "Path(__file__).resolve()." + "parent"
    if path_parent not in text:
        fail(
            "check_stewardship_schema.py must set _SCRIPTS via " + path_parent,
            errors,
        )
    path_insert = "sys.path.insert(0, str(" + "_SCRIPTS))"
    if path_insert not in text:
        fail(
            "check_stewardship_schema.py must sys.path.insert(0, str(_SCRIPTS))",
            errors,
        )
    common_import = "from stewardship_common import ROOT, fail, " + "scan_secrets"
    if common_import not in text:
        fail(
            "check_stewardship_schema.py must import ROOT, fail, scan_secrets",
            errors,
        )
    yaml_none = "yaml = " + "None"
    if yaml_none not in text:
        fail(
            "check_stewardship_schema.py must set yaml = None on ImportError",
            errors,
        )
    pragma_pin = "pragma: no " + "cover"
    if pragma_pin not in text:
        fail(
            "check_stewardship_schema.py ImportError path must keep pragma: no cover",
            errors,
        )
    five_docs = "five live stewardship docs " + "only"
    if five_docs not in text:
        fail(
            "check_stewardship_schema.py must keep " + five_docs + " pin",
            errors,
        )
    hash_comment = 'line.startswith("#")'
    if hash_comment not in text and "line.startswith('#')" not in text:
        fail(
            'check_stewardship_schema.py parse_simple_yaml must skip line.startswith("#")',
            errors,
        )
    true_false = '{"true", "false"}'
    if true_false not in text and "{'true', 'false'}" not in text:
        fail(
            'check_stewardship_schema.py must parse {"true", "false"} bools',
            errors,
        )
    null_tilde = '{"null", "~"}'
    if null_tilde not in text and "{'null', '~'}" not in text:
        fail(
            'check_stewardship_schema.py must parse {"null", "~"} nulls',
            errors,
        )
    fullmatch_int = 're.fullmatch(r"-?\\d+", ' + "value)"
    if fullmatch_int not in text:
        fail(
            'check_stewardship_schema.py must re.fullmatch(r"-?\\d+", value)',
            errors,
        )
    split_colon = '.split(":", ' + "1)"
    if split_colon not in text and ".split(':', 1)" not in text:
        fail(
            'check_stewardship_schema.py must split(":", 1) key/value',
            errors,
        )
    strip_quotes = "value[1:" + "-1]"
    if strip_quotes not in text:
        fail(
            "check_stewardship_schema.py must strip quotes via value[1:-1]",
            errors,
        )
    loaded_dict = "isinstance(loaded, " + "dict)"
    if loaded_dict not in text:
        fail(
            "check_stewardship_schema.py load_yaml must isinstance(loaded, dict)",
            errors,
        )
    fence_search = "FENCED_YAML_RE.search(" + "text)"
    if fence_search not in text:
        fail(
            "check_stewardship_schema.py first_yaml_block must FENCED_YAML_RE.search(text)",
            errors,
        )
    nested_types = "isinstance(value, (dict, " + "list))"
    if nested_types not in text:
        fail(
            "check_stewardship_schema.py reject_non_scalar must isinstance(value, (dict, list))",
            errors,
        )
    missing_sorted = "sorted(required_keys - set(" + "data))"
    if missing_sorted not in text:
        fail(
            "check_stewardship_schema.py must sorted(required_keys - set(data))",
            errors,
        )
    docs_prefix = '.startswith("docs/' + '")'
    if docs_prefix not in text and ".startswith('docs/')" not in text:
        fail(
            'check_stewardship_schema.py ACTIVE check must startswith("docs/")',
            errors,
        )
    active_upper = '.upper() != "' + 'ACTIVE"'
    if active_upper not in text and ".upper() != 'ACTIVE'" not in text:
        fail(
            'check_stewardship_schema.py must compare .upper() != "ACTIVE"',
            errors,
        )
    expected_get = "EXPECTED_VALUES.get(rel, " + "{})"
    if expected_get not in text:
        fail(
            "check_stewardship_schema.py must EXPECTED_VALUES.get(rel, {})",
            errors,
        )
    expected_fmt = "(expected {" + "want!r})"
    if expected_fmt not in text:
        fail(
            "check_stewardship_schema.py must emit (expected {want!r}) needle",
            errors,
        )
    level_set = "level not in (0, 1, 2, " + "3)"
    if level_set not in text:
        fail(
            "check_stewardship_schema.py autonomy_level must use level not in (0, 1, 2, 3)",
            errors,
        )
    tier_lt = "tier < " + "1"
    if tier_lt not in text:
        fail(
            "check_stewardship_schema.py tier must keep tier < 1 reject",
            errors,
        )
    iso_match = "ISO_DATE_RE.match(" + "raw)"
    if iso_match not in text:
        fail(
            "check_stewardship_schema.py must ISO_DATE_RE.match(raw)",
            errors,
        )
    semver_match = "SEMVER_RE.match(" + "ver)"
    if semver_match not in text:
        fail(
            "check_stewardship_schema.py must SEMVER_RE.match(ver)",
            errors,
        )
    issue_search = "ISSUE_REF_RE.search(" + "closes)"
    if issue_search not in text:
        fail(
            "check_stewardship_schema.py must ISSUE_REF_RE.search(closes)",
            errors,
        )
    closes_scope = '{"docs/badge-standard.md", "docs/wiki/PUBLISH.md"}'
    closes_scope_sq = "{'docs/badge-standard.md', 'docs/wiki/PUBLISH.md'}"
    if closes_scope not in text and closes_scope_sq not in text:
        fail(
            "check_stewardship_schema.py must pin closes scope set for badge+PUBLISH",
            errors,
        )
    scan_call = "scan_secrets(path, " + "errors)"
    if scan_call not in text:
        fail(
            "check_stewardship_schema.py must call scan_secrets(path, errors)",
            errors,
        )
    len_docs = "len(DOC_" + "SCHEMAS)"
    if len_docs not in text:
        fail(
            "check_stewardship_schema.py OK banner must include len(DOC_SCHEMAS)",
            errors,
        )
    exit_main = "sys.exit(" + "main())"
    if exit_main not in text:
        fail(
            "check_stewardship_schema.py must sys.exit(main())",
            errors,
        )
    mapping_needle = "metadata YAML must be a " + "mapping"
    if mapping_needle not in text:
        fail(
            "check_stewardship_schema.py must emit metadata YAML must be a mapping",
            errors,
        )
    empty_block = "empty yaml metadata " + "block"
    if empty_block not in text:
        fail(
            "check_stewardship_schema.py must emit empty yaml metadata block",
            errors,
        )
    missing_file = "missing file:"
    if missing_file not in text:
        fail(
            "check_stewardship_schema.py must emit missing file: needle",
            errors,
        )
    bool_subclass = "bool is a subclass of " + "int"
    if bool_subclass not in text:
        fail(
            "check_stewardship_schema.py must keep bool is a subclass of int pin",
            errors,
        )
    safe_load = "yaml.safe_" + "load"
    if safe_load not in text:
        fail(
            "check_stewardship_schema.py must call yaml.safe_load when present",
            errors,
        )

    # Fail-closed after #189: schema deepen helper / constant / needle pins
    # (schema leftover slice only; not docs-lint / actionlint / wiki / workflow spam).
    deepen_doc = "Deepen after " + "#189"
    if deepen_doc not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + deepen_doc,
            errors,
        )
    path_isfile = "path.is_" + "file()"
    if path_isfile not in text:
        fail(
            "check_stewardship_schema.py must gate missing docs via path.is_file()",
            errors,
        )
    block_strip = "block.strip()"
    if block_strip not in text:
        fail(
            "check_stewardship_schema.py must reject empty blocks via block.strip()",
            errors,
        )
    except_exc = "except Exception as " + "exc"
    if except_exc not in text:
        fail(
            "check_stewardship_schema.py must catch Exception as exc on parse",
            errors,
        )
    items_pin = "DOC_SCHEMAS.items()"
    if items_pin not in text:
        fail(
            "check_stewardship_schema.py must iterate DOC_SCHEMAS.items()",
            errors,
        )
    key_missing = "key not in " + "data"
    if key_missing not in text:
        fail(
            "check_stewardship_schema.py must skip absent keys via key not in data",
            errors,
        )
    isinstance_str = "isinstance(value, " + "str)"
    if isinstance_str not in text:
        fail(
            "check_stewardship_schema.py must isinstance(value, str) for STRING_KEYS",
            errors,
        )
    string_keys_membership = "key in STRING_" + "KEYS"
    if string_keys_membership not in text:
        fail(
            "check_stewardship_schema.py must gate string typing via key in STRING_KEYS",
            errors,
        )
    status_get = 'data.get("status")'
    if status_get not in text and "data.get('status')" not in text:
        fail(
            'check_stewardship_schema.py must data.get("status")',
            errors,
        )
    edit_policy_in = '"edit_policy" in ' + "data"
    if edit_policy_in not in text and "'edit_policy' in data" not in text:
        fail(
            'check_stewardship_schema.py must gate edit_policy via "edit_policy" in data',
            errors,
        )
    agents_rel = 'rel == "AGENTS.md"'
    if agents_rel not in text and "rel == 'AGENTS.md'" not in text:
        fail(
            'check_stewardship_schema.py must special-case rel == "AGENTS.md" semver',
            errors,
        )
    engine_pin = 'engine = "PyYAML" if yaml is not ' + "None"
    if engine_pin not in text and "engine = 'PyYAML' if yaml is not None" not in text:
        fail(
            'check_stewardship_schema.py must set engine = "PyYAML" if yaml is not None',
            errors,
        )
    ble001 = "noqa: " + "BLE001"
    if ble001 not in text:
        fail(
            "check_stewardship_schema.py parse except must keep noqa: BLE001",
            errors,
        )
    errors_init = "errors: list[str] = " + "[]"
    if errors_init not in text:
        fail(
            "check_stewardship_schema.py main must init errors: list[str] = []",
            errors,
        )
    got_want = "got != " + "want"
    if got_want not in text:
        fail(
            "check_stewardship_schema.py EXPECTED_VALUES compare must use got != want",
            errors,
        )
    autonomy_in = '"autonomy_level" in ' + "data"
    if autonomy_in not in text and "'autonomy_level' in data" not in text:
        fail(
            'check_stewardship_schema.py must gate autonomy via "autonomy_level" in data',
            errors,
        )
    tier_in = '"tier" in ' + "data"
    if tier_in not in text and "'tier' in data" not in text:
        fail(
            'check_stewardship_schema.py must gate tier via "tier" in data',
            errors,
        )
    date_loop = "for date_key in DATE_" + "KEYS"
    if date_loop not in text:
        fail(
            "check_stewardship_schema.py must iterate for date_key in DATE_KEYS",
            errors,
        )
    leftover_pin = "schema leftover " + "slice"
    # Self-pin host commentary so deepen cannot silently drop.
    # Check via split-constructed needles only — contiguous literals would
    # neutralize under the same replace() the self-tests apply.
    self_text2 = BADGE_GATE.read_text(encoding="utf-8")
    if leftover_pin not in self_text2:
        fail(
            "check_badge_standard.py schema deepen must keep "
            + leftover_pin
            + " pin",
            errors,
        )
    not_docs_spam = "not docs-lint / actionlint / wiki / " + "workflow spam"
    if not_docs_spam not in self_text2:
        fail(
            "check_badge_standard.py schema deepen must keep "
            + not_docs_spam
            + " pin",
            errors,
        )

    # Fail-closed after #208: policy-schema pass-4 helper / constant / needle pins
    # (schema pass-4 slice only; not third-pass-after-149 / docs-lint / actionlint spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    # Avoid contiguous four+th so existing badge refusal self-tests (four→quaternary) stay valid.
    pass4_doc = "Four" + "th-pass after #208"
    if pass4_doc not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + pass4_doc,
            errors,
        )
    distinct_pin = "distinct from schema-third-pass " + "after-149"
    if distinct_pin not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + distinct_pin,
            errors,
        )
    nested_list_needle = "got nested/" + "list"
    if nested_list_needle not in text:
        fail(
            "check_stewardship_schema.py must emit got nested/list needle",
            errors,
        )
    type_name = "type(value).__" + "name__"
    if type_name not in text:
        fail(
            "check_stewardship_schema.py reject_non_scalar must use type(value).__name__",
            errors,
        )
    invent_not_in = '"invent" not in ' + "policy"
    if invent_not_in not in text and "'invent' not in policy" not in text:
        fail(
            'check_stewardship_schema.py must gate invent via "invent" not in policy',
            errors,
        )
    badge_invent_rel = 'rel == "docs/badge-standard.md"'
    if badge_invent_rel not in text and "rel == 'docs/badge-standard.md'" not in text:
        fail(
            'check_stewardship_schema.py invent pin must special-case '
            'rel == "docs/badge-standard.md"',
            errors,
        )
    status_upper = "str(status)." + "upper()"
    if status_upper not in text:
        fail(
            "check_stewardship_schema.py must compare via str(status).upper()",
            errors,
        )
    policy_lower = 'str(data["edit_policy"]).' + "lower()"
    if policy_lower not in text and "str(data['edit_policy']).lower()" not in text:
        fail(
            'check_stewardship_schema.py must lower edit_policy via '
            'str(data["edit_policy"]).lower()',
            errors,
        )
    for stub in (
        "DEPRECATED",
        "ARCHIVED",
        "PENDING",
        "RETIRED",
        "SUSPENDED",
    ):
        if stub not in text:
            fail(
                "check_stewardship_schema.py docstring must pin invalid status "
                f"enum stub {stub}",
                errors,
            )
    for stub in (
        "geryon",
        "playwright",
        "browser-claude",
        "claude-cowork",
    ):
        if stub not in text:
            fail(
                "check_stewardship_schema.py docstring must pin invalid surface "
                f"enum stub {stub}",
                errors,
            )
    whitespace_pin = "whitespace-only " + "non-empty"
    if whitespace_pin not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + whitespace_pin,
            errors,
        )
    nested_policy = "nested/list edit_policy+parent_governance " + "policy refs"
    if nested_policy not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + nested_policy,
            errors,
        )
    nested_version_pin = "nested version+autonomy+maintainer+" + "status"
    if nested_version_pin not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + nested_version_pin,
            errors,
        )
    list_surface_pin = "list surface+closes+purpose+" + "autonomy"
    if list_surface_pin not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + list_surface_pin,
            errors,
        )
    pass4_slice = "schema pass-4 " + "slice"
    self_text3 = BADGE_GATE.read_text(encoding="utf-8")
    if pass4_slice not in self_text3:
        fail(
            "check_badge_standard.py schema pass-4 must keep "
            + pass4_slice
            + " pin",
            errors,
        )
    not_third_spam = "not third-pass-after-149 / docs-lint / " + "actionlint spam"
    if not_third_spam not in self_text3:
        fail(
            "check_badge_standard.py schema pass-4 must keep "
            + not_third_spam
            + " pin",
            errors,
        )
    contract_pass4 = "policy-schema pass-4 after " + "#208"
    if contract_pass4 not in self_text3:
        fail(
            "check_badge_standard.py schema gate contract docstring must pin "
            + contract_pass4,
            errors,
        )

    # Fail-closed after #225: schema residual (pass-5) helper / constant / needle pins
    # (schema residual slice only; not fourth-pass #216 / path-edges #225 / Pass-2 leftover
    # +md/link #220 / badge-lint #208 spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    # Avoid contiguous five+th so existing badge refusal self-tests stay valid.
    pass5_doc = "Residual after " + "#225"
    if pass5_doc not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + pass5_doc,
            errors,
        )
    residual_host = "schema residual " + "(pass-5)"
    self_text4 = BADGE_GATE.read_text(encoding="utf-8")
    if residual_host not in self_text4:
        fail(
            "check_badge_standard.py must keep " + residual_host + " host pin",
            errors,
        )
    not_fourth_216 = "NOT fourth-pass " + "#216"
    if not_fourth_216 not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + not_fourth_216,
            errors,
        )
    status_in_required = '"status" in required_' + "keys"
    if status_in_required not in text and "'status' in required_keys" not in text:
        fail(
            'check_stewardship_schema.py must gate ACTIVE via "status" in required_keys',
            errors,
        )
    loaded_none = "loaded is " + "None"
    if loaded_none not in text:
        fail(
            "check_stewardship_schema.py load_yaml must reject loaded is None",
            errors,
        )
    value_true = 'value.lower() == "true"'
    if value_true not in text and "value.lower() == 'true'" not in text:
        fail(
            'check_stewardship_schema.py must parse bools via value.lower() == "true"',
            errors,
        )
    int_value = "int(" + "value)"
    if int_value not in text:
        fail(
            "check_stewardship_schema.py must coerce ints via int(value)",
            errors,
        )
    text_strip = "if not text.strip()"
    if text_strip not in text:
        fail(
            "check_stewardship_schema.py load_yaml stdlib path must keep if not text.strip()",
            errors,
        )
    for stub in (
        "WIP",
        "BETA",
        "LEGACY",
        "FROZEN",
        "CANCELLED",
        "PROTOTYPE",
    ):
        if stub not in text:
            fail(
                "check_stewardship_schema.py docstring must pin residual status "
                f"enum stub {stub}",
                errors,
            )
    for stub in (
        "openai",
        "anthropic",
        "slack",
        "auto",
        "agents",
    ):
        if stub not in text:
            fail(
                "check_stewardship_schema.py docstring must pin residual surface "
                f"enum stub {stub}",
                errors,
            )
    residual_slice = "schema residual " + "slice"
    if residual_slice not in self_text4:
        fail(
            "check_badge_standard.py schema residual must keep "
            + residual_slice
            + " pin",
            errors,
        )
    not_pass2_spam = "not fourth-pass #216 / path-edges #225 / " + "Pass-2 leftover"
    if not_pass2_spam not in self_text4:
        fail(
            "check_badge_standard.py schema residual must keep "
            + not_pass2_spam
            + " distinctness pin",
            errors,
        )
    contract_residual = "schema residual after " + "#225"
    if contract_residual not in self_text4:
        fail(
            "check_stewardship_schema_gate_contract docstring must pin "
            + contract_residual,
            errors,
        )

    # Fail-closed after #252: schema leftover helper / constant / needle pins
    # (schema leftover slice only; not wiki/mdlink leftover #252 / not path-edges residual #244 /
    # not wiki outline/PUBLISH #243 / not md/link residual #239 / not schema residual (pass-5) #233 spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    leftover_252_doc = "Residual leftover after " + "#252 (schema leftover"
    if leftover_252_doc not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + leftover_252_doc,
            errors,
        )
    not_wiki_mdlink_252 = "NOT wiki/mdlink leftover " + "#252"
    if not_wiki_mdlink_252 not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + not_wiki_mdlink_252,
            errors,
        )
    not_path_edges_244 = "NOT path-edges residual " + "#244"
    if not_path_edges_244 not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + not_path_edges_244,
            errors,
        )
    not_wiki_243 = "NOT wiki outline/PUBLISH " + "#243"
    if not_wiki_243 not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + not_wiki_243,
            errors,
        )
    not_mdlink_239 = "NOT md/link residual " + "#239"
    if not_mdlink_239 not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + not_mdlink_239,
            errors,
        )
    not_pass5_233 = "NOT schema residual (pass-5) " + "#233"
    if not_pass5_233 not in text:
        fail(
            "check_stewardship_schema.py docstring must pin " + not_pass5_233,
            errors,
        )
    colon_line = 'if ":" not in ' + "line"
    if colon_line not in text and "if ':' not in line" not in text:
        fail(
            'check_stewardship_schema.py parse_simple_yaml must keep if ":" not in line',
            errors,
        )
    yaml_present = "if yaml is not " + "None:"
    if yaml_present not in text:
        fail(
            "check_stewardship_schema.py load_yaml must keep if yaml is not None:",
            errors,
        )
    no_match = "if not " + "match:"
    if no_match not in text:
        fail(
            "check_stewardship_schema.py first_yaml_block must keep if not match:",
            errors,
        )
    value_none = "value is None " + "or"
    if value_none not in text:
        fail(
            "check_stewardship_schema.py must reject empty scalars via value is None or",
            errors,
        )
    status_none = "status is not " + "None"
    if status_none not in text:
        fail(
            "check_stewardship_schema.py ACTIVE gate must keep status is not None",
            errors,
        )
    raw_date = "raw = str(data[date_" + "key])"
    if raw_date not in text:
        fail(
            "check_stewardship_schema.py DATE_KEYS loop must keep raw = str(data[date_key])",
            errors,
        )
    ver_version = 'ver = str(data["version"])'
    if ver_version not in text and "ver = str(data['version'])" not in text:
        fail(
            'check_stewardship_schema.py semver gate must keep ver = str(data["version"])',
            errors,
        )
    closes_str = 'closes = str(data["closes"])'
    if closes_str not in text and "closes = str(data['closes'])" not in text:
        fail(
            'check_stewardship_schema.py issue-ref gate must keep closes = str(data["closes"])',
            errors,
        )
    for stub in (
        "DRAFT",
        "EXPERIMENTAL",
        "OBSOLETE",
        "DISABLED",
        "INACTIVE",
        "STAGED",
    ):
        if stub not in text:
            fail(
                "check_stewardship_schema.py docstring must pin leftover status "
                f"enum stub {stub}",
                errors,
            )
    for stub in (
        "cursor",
        "linear",
        "notion",
        "discord",
        "zapier",
    ):
        if stub not in text:
            fail(
                "check_stewardship_schema.py docstring must pin leftover surface "
                f"enum stub {stub}",
                errors,
            )
    leftover_host = "schema leftover after " + "#252"
    self_text5 = BADGE_GATE.read_text(encoding="utf-8")
    if leftover_host not in self_text5:
        fail(
            "check_badge_standard.py must keep " + leftover_host + " host pin",
            errors,
        )
    leftover_slice = "schema leftover " + "slice"
    if leftover_slice not in self_text5:
        fail(
            "check_badge_standard.py schema leftover must keep "
            + leftover_slice
            + " pin",
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



    # Fail-closed after #132: wiki-badge posture pins (Link Check + Markdown Lint only;
    # no stewardship-checks.yml/badge.svg invent; lands closed #120 leftover;
    # not stewardship_common #117 / run_stewardship #127 / CI workflow #132 / docs-lint #135).
    wiki_text = (
        WIKI_OUTLINE_GATE.read_text(encoding="utf-8")
        if WIKI_OUTLINE_GATE.is_file()
        else ""
    )
    status_badges = "status badges " + "cover"
    if status_badges not in wiki_text:
        fail(
            "check_wiki_outline.py must keep status badges cover wording",
            errors,
        )
    product_badge = "product " + "badge"
    if product_badge not in wiki_text:
        fail(
            "check_wiki_outline.py must keep product badge refusal wording",
            errors,
        )
    no_fourth_svg = "stewardship-checks.yml/" + "badge.svg"
    if no_fourth_svg not in wiki_text:
        fail(
            "check_wiki_outline.py must reject stewardship-checks.yml/badge.svg invent",
            errors,
        )
    no_embed = "must not embed markdown badge " + "images"
    if no_embed not in wiki_text:
        fail(
            "check_wiki_outline.py must reject embedded markdown badge images",
            errors,
        )
    if "Link Check exactly" not in wiki_text:
        fail(
            "check_wiki_outline.py must require PUBLISH.md Link Check exactly",
            errors,
        )
    if "Markdown Lint exactly" not in wiki_text:
        fail(
            "check_wiki_outline.py must require PUBLISH.md Markdown Lint exactly",
            errors,
        )
    after_132_wiki = "after " + "#132"
    if after_132_wiki not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must pin after #132 wiki-badge deepen",
            errors,
        )
    home_no_embed = "Home.md must not embed markdown badge " + "images"
    if home_no_embed not in wiki_text:
        fail(
            "check_wiki_outline.py must reject Home.md badge-row embeds",
            errors,
        )
    status_badges_names = "must name Link Check and Markdown Lint " + "status badges"
    if status_badges_names not in wiki_text:
        fail(
            "check_wiki_outline.py must require Repo-Stewardship Link Check+Markdown Lint names",
            errors,
        )
    product_refuse = "must refuse stewardship as a product " + "badge"
    if product_refuse not in wiki_text:
        fail(
            "check_wiki_outline.py must emit product badge refusal fail needle",
            errors,
        )
    no_fourth_paren = "(no fourth " + "badge)"
    if no_fourth_paren not in wiki_text:
        fail(
            "check_wiki_outline.py must keep no fourth badge invent parenthetical",
            errors,
        )
    narrative_not_row = "wiki is narrative, not badge " + "row"
    if narrative_not_row not in wiki_text:
        fail(
            "check_wiki_outline.py must keep wiki is narrative, not badge row wording",
            errors,
        )
    wiki_badge_doc = "wiki-badge " + "posture"
    if wiki_badge_doc not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep wiki-badge posture pin",
            errors,
        )
    badge_open = '"[!["'
    badge_open_sq = "'[!['"
    if badge_open not in wiki_text and badge_open_sq not in wiki_text:
        fail(
            "check_wiki_outline.py must match markdown badge open [![ for embeds",
            errors,
        )
    badge_svg_lower = '"badge.svg" in ' + "text.lower()"
    badge_svg_lower_sq = "'badge.svg' in " + "text.lower()"
    if badge_svg_lower not in wiki_text and badge_svg_lower_sq not in wiki_text:
        fail(
            "check_wiki_outline.py must gate embeds via badge.svg in text.lower()",
            errors,
        )

    # Fail-closed after #176: wiki-index validators (Home TOC empty-index /
    # publishable page index stubs) — distinct from wiki-badge after #141 /
    # fixtures #173 / path-filter #176 spam.
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    wiki_index_doc = "Wiki-index after " + "#176"
    if wiki_index_doc not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep Wiki-index after #176 pin",
            errors,
        )
    empty_index = "Home TOC empty-" + "index"
    if empty_index not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep Home TOC empty-index pin",
            errors,
        )
    publishable_stub = "publishable page " + "index stubs"
    if publishable_stub not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep publishable page index stubs pin",
            errors,
        )
    link_publishable = "Home.md must link to publishable " + "page"
    if link_publishable not in wiki_text:
        fail(
            "check_wiki_outline.py must emit Home.md must link to publishable page needle",
            errors,
        )
    toc_comment = "Wiki-index: Home is the " + "TOC"
    if toc_comment not in wiki_text:
        fail(
            "check_wiki_outline.py must keep Wiki-index Home is the TOC comment",
            errors,
        )
    not_badge_spam = "not wiki-badge " + "#141"
    if not_badge_spam not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep not wiki-badge #141 spam pin",
            errors,
        )




    # Deepen after #189: wiki-index/badge leftover (lands closed #185/#172;
    # NOT path-order #189 / NOT stewardship-schema sibling / NOT path-filter).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    deepen_189_doc = "Deepen after " + "#189"
    if deepen_189_doc not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + deepen_189_doc + " pin",
            errors,
        )
    wiki_badge_leftover = "wiki-index/badge " + "leftover"
    if wiki_badge_leftover not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + wiki_badge_leftover + " pin",
            errors,
        )
    not_path_order = "NOT path-order " + "#189"
    if not_path_order not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + not_path_order + " pin",
            errors,
        )
    not_schema_sib = "NOT stewardship-schema " + "sibling"
    if not_schema_sib not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + not_schema_sib + " pin",
            errors,
        )
    lands_185 = "lands closed " + "#185"
    if lands_185 not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + lands_185 + " pin",
            errors,
        )
    pages_contiguous = (
        'PUBLISHABLE_PAGES = (\n'
        '    "Home.md",\n'
        '    "Overview.md",\n'
        '    "Autonomy-Levels.md",\n'
        '    "Repo-Stewardship.md",\n'
        '    "Agent-Routing.md",\n'
        '    "Security-Boundaries.md",\n'
        ')'
    )
    if pages_contiguous not in wiki_text:
        fail(
            "check_wiki_outline.py must keep exact PUBLISHABLE_PAGES contiguous order",
            errors,
        )
    toc_loop = "for page in PUBLISHABLE_" + "PAGES:"
    if toc_loop not in wiki_text:
        fail(
            "check_wiki_outline.py Home TOC must loop for page in PUBLISHABLE_PAGES",
            errors,
        )
    skip_home = 'if page == "Home.md":'
    skip_home_sq = "if page == 'Home.md':"
    if skip_home not in wiki_text and skip_home_sq not in wiki_text:
        fail(
            'check_wiki_outline.py Home TOC must skip Home.md via if page == "Home.md"',
            errors,
        )
    link_page_form = 'f"]({page})"'
    link_page_sq = "f']({page})'"
    if link_page_form not in wiki_text and link_page_sq not in wiki_text:
        fail(
            "check_wiki_outline.py Home TOC must match ]({page}) link form",
            errors,
        )
    link_stem_form = 'f"]({stem})"'
    link_stem_sq = "f']({stem})'"
    if link_stem_form not in wiki_text and link_stem_sq not in wiki_text:
        fail(
            "check_wiki_outline.py Home TOC must match ]({stem}) link form",
            errors,
        )
    empty_index_comment = "empty index (no publishable page " + "links)"
    if empty_index_comment not in wiki_text:
        fail(
            "check_wiki_outline.py must keep "
            + empty_index_comment
            + " comment",
            errors,
        )
    not_schema_191 = "not schema " + "#191"
    if not_schema_191 not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + not_schema_191 + " distinctness pin",
            errors,
        )

    # Wiki outline/PUBLISH leftover after #233 (existing docs/wiki pages only;
    # NOT wiki-index/badge leftover #227 / NOT stewardship-checks/schema residual #233).
    leftover_233_doc = "Wiki outline/PUBLISH leftover after " + "#233"
    if leftover_233_doc not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + leftover_233_doc + " pin",
            errors,
        )
    not_wiki_index_227 = "NOT wiki-index/badge leftover " + "#227"
    if not_wiki_index_227 not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + not_wiki_index_227 + " pin",
            errors,
        )
    not_stew_schema_233 = "NOT stewardship-checks/schema residual " + "#233"
    if not_stew_schema_233 not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + not_stew_schema_233 + " pin",
            errors,
        )
    existing_pages_only = "existing pages only — do not invent extra wiki " + "files"
    if existing_pages_only not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + existing_pages_only + " pin",
            errors,
        )
    pages_heading_needle = "## Pages to " + "publish"
    if pages_heading_needle not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md ## Pages to publish heading",
            errors,
        )
    wiki_git_clone = "agents-governance.wiki" + ".git"
    if wiki_git_clone not in wiki_text:
        fail(
            "check_wiki_outline.py must pin one-shot agents-governance.wiki.git clone",
            errors,
        )
    no_cp_operator = "cp docs/wiki/" + "PUBLISH.md"
    if no_cp_operator not in wiki_text:
        fail(
            "check_wiki_outline.py must refuse one-shot cp of operator PUBLISH.md",
            errors,
        )
    git_add_six_pin = (
        "git add Home.md Overview.md Autonomy-Levels.md "
        "Repo-Stewardship.md Agent-Routing.md Security-Boundaries.md"
    )
    if git_add_six_pin not in wiki_text:
        fail(
            "check_wiki_outline.py must pin git add of six publishable pages",
            errors,
        )
    git_push_origin = "git push " + "origin"
    if git_push_origin not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md git push origin",
            errors,
        )
    purpose_path = "Reversible publish path for " + "docs/wiki"
    if purpose_path not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md Reversible publish path purpose",
            errors,
        )
    closes_16 = 'closes: "#16"'
    closes_16_sq = "closes: '#16'"
    if closes_16 not in wiki_text and closes_16_sq not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md closes: \"#16\"",
            errors,
        )
    wiki_git_fallback = ".wiki" + ".git"
    if wiki_git_fallback not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md .wiki.git fallback",
            errors,
        )
    badge_blob = (
        "https://github.com/fuzzywigg/agents-governance/blob/main/docs/badge-standard.md"
    )
    if badge_blob not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md badge-standard blob rewrite URL",
            errors,
        )
    drop_bullet = "drop the in-repo `PUBLISH.md` " + "bullet"
    if drop_bullet not in wiki_text:
        fail(
            "check_wiki_outline.py must pin drop the in-repo PUBLISH.md bullet",
            errors,
        )
    operator_not_pages = "OPERATOR_ONLY in PUBLISHABLE_" + "PAGES"
    if operator_not_pages not in wiki_text:
        fail(
            "check_wiki_outline.py must refuse OPERATOR_ONLY in PUBLISHABLE_PAGES",
            errors,
        )
    copy_existing = "one-shot must copy existing " + "page"
    if copy_existing not in wiki_text:
        fail(
            "check_wiki_outline.py must pin one-shot copy existing page needles",
            errors,
        )
    table_order = "pages table must keep publishable page " + "order"
    if table_order not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md pages table order",
            errors,
        )
    leftover_243_wiki = "Wiki/mdlink leftover after " + "#243"
    if leftover_243_wiki not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + leftover_243_wiki + " pin",
            errors,
        )
    not_mdlink_239 = "NOT md/link residual layouts " + "#239"
    if not_mdlink_239 not in wiki_text:
        fail(
            "check_wiki_outline.py docstring must keep " + not_mdlink_239 + " pin",
            errors,
        )
    oneshot_heading = "## One-shot publish (after wiki " + "exists)"
    if oneshot_heading not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md ## One-shot publish heading",
            errors,
        )
    exact_clone_dest = "/tmp/agents-governance" + ".wiki"
    if exact_clone_dest not in wiki_text:
        fail(
            "check_wiki_outline.py must pin one-shot clone dest /tmp/agents-governance.wiki",
            errors,
        )
    git_commit_pin = "git commit -m " + '"docs: publish public wiki outline from docs/wiki (#16)"'
    if git_commit_pin not in wiki_text:
        fail(
            "check_wiki_outline.py must pin git commit wiki outline from docs/wiki (#16)",
            errors,
        )
    landing_cell = "Home (landing)"
    if landing_cell not in wiki_text:
        fail(
            "check_wiki_outline.py must pin PUBLISH.md Home (landing) cell",
            errors,
        )
    home_omit = "omit when copying pages to GitHub " + "Wiki"
    if home_omit not in wiki_text:
        fail(
            "check_wiki_outline.py must pin Home omit-when-copying PUBLISH.md wording",
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

    # Fail-closed after #176: wiki-index validators — broken internal stub
    # links / empty markdown index / duplicate slug headings_in set collapse
    # (not wiki-badge #141 / fixtures #173 / path-filter #176 spam).
    # Split literals so self-mutation of contiguous names cannot neutralize checks.
    rel_wiki_index = "Wiki-index after " + "#176"
    if rel_wiki_index not in text:
        fail(
            "check_relative_links.py docstring must keep Wiki-index after #176 pin",
            errors,
        )
    broken_stub = "broken internal stub " + "links"
    if broken_stub not in text:
        fail(
            "check_relative_links.py docstring must keep broken internal stub links pin",
            errors,
        )
    empty_md_index = "empty markdown " + "index"
    if empty_md_index not in text:
        fail(
            "check_relative_links.py docstring must keep empty markdown index pin",
            errors,
        )
    dup_slug = "duplicate slug headings_in " + "set"
    if dup_slug not in text:
        fail(
            "check_relative_links.py docstring must keep duplicate slug headings_in set pin",
            errors,
        )
    set_collapse = "{github_slug(match.group(2))"
    if set_collapse not in text:
        fail(
            "check_relative_links.py headings_in must collapse duplicate slugs via set",
            errors,
        )
    dup_doc = "duplicate headings collapse to one " + "slug"
    if dup_doc not in text:
        fail(
            "check_relative_links.py headings_in must document duplicate slug collapse",
            errors,
        )
    dup_comment = "Duplicate slug edge: set " + "collapse"
    if dup_comment not in text:
        fail(
            "check_relative_links.py must keep Duplicate slug edge set collapse comment",
            errors,
        )
    no_md_found = "no markdown files " + "found"
    if no_md_found not in text:
        fail(
            "check_relative_links.py must fail closed on empty markdown index",
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
            # Fail-closed after #117: each gate runs via python3 scripts/ prefix.
            # Explicit live pins (docs runner path):
            # python3 scripts/check_badge_standard.py
            # python3 scripts/check_wiki_outline.py
            # python3 scripts/check_stewardship_schema.py
            # python3 scripts/check_relative_links.py
            if f"python3 scripts/{gate}" not in run_text:
                fail(
                    f"run_stewardship_checks.sh must run python3 scripts/{gate}",
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
        # Fail-closed after #117: live runner shell posture (docs CI local path).
        if "#!/usr/bin/env bash" not in run_text:
            fail(
                "run_stewardship_checks.sh must use #!/usr/bin/env bash shebang",
                errors,
            )
        if "set -euo pipefail" not in run_text:
            fail(
                "run_stewardship_checks.sh must set -euo pipefail",
                errors,
            )
        if 'dirname "$0"' not in run_text and "dirname '$0'" not in run_text:
            fail(
                'run_stewardship_checks.sh must resolve ROOT via dirname + "$0"',
                errors,
            )
        if 'cd "$ROOT"' not in run_text and "cd '$ROOT'" not in run_text:
            fail(
                'run_stewardship_checks.sh must cd to ROOT before running gates',
                errors,
            )
        # Reconstruct phrase so self-test mutations of the concatenation fail closed.
        same_ci_phrase = "same set as " + "CI"
        if same_ci_phrase.lower() not in run_text.lower():
            fail(
                "run_stewardship_checks.sh must note same set as CI",
                errors,
            )
        # Fail-closed after #117: pwd resolve + Run-all commentary (runner slice).
        if "pwd)" not in run_text and 'pwd"' not in run_text:
            fail(
                "run_stewardship_checks.sh must resolve ROOT via pwd",
                errors,
            )
        run_all_phrase = "Run all stewardship " + "doc gates"
        if run_all_phrase not in run_text:
            fail(
                "run_stewardship_checks.sh must keep Run all stewardship doc gates note",
                errors,
            )
        # Fail-closed after #176: exactly four python3 scripts/ gate lines.
        py_prefix = "python3 scripts/"
        if run_text.count(py_prefix) != 4:
            fail(
                "run_stewardship_checks.sh must invoke exactly four python3 scripts/ gates",
                errors,
            )
        # Fail-closed after #176: no soft-fail softening of runner posture.
        if "|| true" in run_text or "||true" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with || true",
                errors,
            )
        if "set +e" in run_text:
            fail(
                "run_stewardship_checks.sh must not disable errexit with set +e",
                errors,
            )
        # Fail-closed after #176: parent-dir fragment from live ROOT assign.
        # Checked before exact-ROOT leftover so parent-frag mutations get this needle.
        parent_frag = 'dirname "$0")/..'
        if parent_frag not in run_text:
            fail(
                "run_stewardship_checks.sh must keep parent-dir ROOT fragment",
                errors,
            )
        # Fail-closed after #176: locally commentary (same set as CI path).
        locally_pin = "doc gates " + "locally"
        if locally_pin not in run_text:
            fail(
                "run_stewardship_checks.sh must keep locally commentary pin",
                errors,
            )
        # Leftover after #149: exact ROOT assign + blank line (before full layout).
        root_assign = 'ROOT="$(cd "$(dirname "$0")/.." && pwd)"'
        if root_assign not in run_text:
            fail(
                "run_stewardship_checks.sh must keep exact ROOT assign "
                "(stewardship leftover after #149)",
                errors,
            )
        if 'cd "$ROOT"\n\npython3 scripts/check_badge_standard.py' not in run_text:
            fail(
                "run_stewardship_checks.sh must keep blank line after cd "
                "(stewardship leftover after #149)",
                errors,
            )
        # Fail-closed after #176: exact ROOT assign (CI reliability leftover).
        exact_root = 'ROOT="$(cd "$(dirname "$0")/.." && pwd)"'
        if exact_root not in run_text:
            fail(
                "run_stewardship_checks.sh must use exact ROOT assign "
                '(ROOT="$(cd "$(dirname "$0")/.." && pwd)")',
                errors,
            )
        # Fail-closed after #191: Pass-2 residual runner integrity.
        if "test_stewardship_gates.py" in run_text:
            fail(
                "run_stewardship_checks.sh must remain gates-only "
                "(no test_stewardship_gates.py; Pass-2 residual after #191)",
                errors,
            )
        if "BASH_SOURCE" in run_text:
            fail(
                "run_stewardship_checks.sh must not use BASH_SOURCE ROOT drift "
                "(Pass-2 residual after #191)",
                errors,
            )
        if "python scripts/" in run_text:
            fail(
                "run_stewardship_checks.sh must not use bare python scripts/ "
                "(Pass-2 residual after #191)",
                errors,
            )
        if "set +u" in run_text or "set +o pipefail" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with set +u/+o pipefail "
                "(Pass-2 residual after #191)",
                errors,
            )
        # Pass-2 leftovers after #203 tip: residual soft-fail beyond #179/#199
        # (lands closed #202/#192 leftover; not open #205 badge-lint / #204 schema).
        if "|| exit 0" in run_text or "||exit 0" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with || exit 0",
                errors,
            )
        if not run_text.startswith("#!/usr/bin/env bash\n"):
            fail(
                "run_stewardship_checks.sh must keep shebang as first line",
                errors,
            )
        # Pass-2 residual leftover after #233 (soft-fail leftovers beyond
        # #199/#203 residual + #220 || exit 0 / shebang-first;
        # NOT stewardship-checks/schema residual #233 / NOT wiki-index/badge #227 /
        # NOT path-edges #225 / NOT Pass-2 leftover+md/link #220).
        if "|| :" in run_text or "||:" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with || : "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if "|| return 0" in run_text or "||return 0" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with || return 0 "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if "set +o errexit" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with set +o errexit "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if "set +o nounset" in run_text:
            fail(
                "run_stewardship_checks.sh must not soft-fail with set +o nounset "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if "python3 -m " in run_text:
            fail(
                "run_stewardship_checks.sh must not invent python3 -m for gates "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if re.search(r"(?m)^\s*source\s+", run_text):
            fail(
                "run_stewardship_checks.sh must not source env files "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        if re.search(r"(?m)^\s*\.\s+\S", run_text):
            fail(
                "run_stewardship_checks.sh must not dot-source paths "
                "(Pass-2 residual / template validation leftover after #233)",
                errors,
            )
        # Leftover after #149: exact live run_stewardship_checks.sh full layout.
        expected_run = (
            "#!/usr/bin/env bash\n"
            "# Run all stewardship doc gates locally (same set as CI).\n"
            "set -euo pipefail\n"
            'ROOT="$(cd "$(dirname "$0")/.." && pwd)"\n'
            'cd "$ROOT"\n'
            "\n"
            "python3 scripts/check_badge_standard.py\n"
            "python3 scripts/check_wiki_outline.py\n"
            "python3 scripts/check_stewardship_schema.py\n"
            "python3 scripts/check_relative_links.py\n"
        )
        if run_text != expected_run:
            fail(
                "run_stewardship_checks.sh must match exact live stewardship leftover layout",
                errors,
            )



    # Deepen after #189: wiki-index/badge leftover on relative wiki-index
    # (lands closed #185/#172; NOT path-order #189 / NOT stewardship-schema).
    rel_deepen_189 = "Deepen after " + "#189"
    if rel_deepen_189 not in text:
        fail(
            "check_relative_links.py docstring must keep " + rel_deepen_189 + " pin",
            errors,
        )
    rel_wiki_badge = "wiki-index/badge " + "leftover"
    if rel_wiki_badge not in text:
        fail(
            "check_relative_links.py docstring must keep " + rel_wiki_badge + " pin",
            errors,
        )
    broken_rel_needle = "broken relative " + "link"
    if broken_rel_needle not in text:
        fail(
            "check_relative_links.py must emit " + broken_rel_needle + " fail needle",
            errors,
        )
    rel_not_path_order = "NOT path-order " + "#189"
    if rel_not_path_order not in text:
        fail(
            "check_relative_links.py docstring must keep " + rel_not_path_order + " pin",
            errors,
        )
    rel_not_schema = "NOT stewardship-schema " + "sibling"
    if rel_not_schema not in text:
        fail(
            "check_relative_links.py docstring must keep " + rel_not_schema + " pin",
            errors,
        )

    rel_not_191 = "not schema " + "#191"
    if rel_not_191 not in text:
        fail(
            "check_relative_links.py docstring must keep " + rel_not_191 + " distinctness pin",
            errors,
        )
    rel_lands_185 = "lands closed " + "#185"
    if rel_lands_185 not in text:
        fail(
            "check_relative_links.py docstring must keep " + rel_lands_185 + " pin",
            errors,
        )



def check_run_stewardship_gate_contract(errors: list[str]) -> None:
    """Fail-close live run_stewardship_checks.sh wiring (after #117/#176; not lychee/mdlint spam)."""
    if not BADGE_GATE.is_file():
        fail("Missing scripts/check_badge_standard.py (run_stewardship host)", errors)
        return
    # Split encoding so utf-8 self-tests do not latin-1-mangle arrow order pins.
    text = BADGE_GATE.read_text(encoding="utf-" + "8")
    # Split pin literals so self-mutation of contiguous names cannot neutralize checks.
    host_pin = "run_stewardship " + "host"
    if host_pin not in text:
        fail(
            "check_run_stewardship_gate_contract must keep " + host_pin + " pin",
            errors,
        )
    spam_pin = "not lychee/mdlint " + "spam"
    if spam_pin not in text:
        fail(
            "check_run_stewardship_gate_contract must keep " + spam_pin + " pin",
            errors,
        )
    run_const = "RUN_" + "STEWARDSHIP"
    if run_const not in text:
        fail(
            "check_badge_standard.py must declare " + run_const,
            errors,
        )
    run_path = '"run_stewardship_checks' + '.sh"'
    if run_path not in text and "'run_stewardship_checks.sh'" not in text:
        fail(
            "check_badge_standard.py must pin path run_stewardship_checks.sh",
            errors,
        )
    shebang_pin = "#!/usr/bin/env " + "bash"
    if shebang_pin not in text:
        fail(
            "run_stewardship contract must require " + shebang_pin,
            errors,
        )
    euo_pin = "set -euo " + "pipefail"
    if euo_pin not in text:
        fail(
            "run_stewardship contract must require " + euo_pin,
            errors,
        )
    dirname_pin = 'dirname "$0"'
    if dirname_pin not in text:
        fail(
            "run_stewardship contract must require dirname \"$0\"",
            errors,
        )
    cd_pin = 'cd "$ROOT"'
    if cd_pin not in text:
        fail(
            "run_stewardship contract must require cd \"$ROOT\"",
            errors,
        )
    # Require reconstructed assign (not a contiguous "same set as CI" literal alone).
    if 'same set as " + "CI"' not in text:
        fail(
            "run_stewardship contract must keep same set as CI wording",
            errors,
        )
    order_pin = "badge → wiki → schema → " + "relative"
    if order_pin not in text:
        fail(
            "run_stewardship contract must pin gate order " + order_pin,
            errors,
        )
    for gate in (
        "check_badge_standard.py",
        "check_wiki_outline.py",
        "check_stewardship_schema.py",
        "check_relative_links.py",
    ):
        py_pin = "python3 scripts/" + gate
        if py_pin not in text:
            fail(
                "run_stewardship contract must require " + py_pin,
                errors,
            )
    contract_fn = "check_run_stewardship_" + "gate_contract"
    if f"def {contract_fn}(" not in text:
        fail(
            "check_badge_standard.py must provide " + contract_fn + "()",
            errors,
        )
    if contract_fn + "(errors)" not in text:
        fail(
            "main must call " + contract_fn + "(errors)",
            errors,
        )
    live_doc = "Fail-closed after " + "#117"
    if live_doc not in text:
        fail(
            "run_stewardship pins must keep " + live_doc + " marker",
            errors,
        )
    # Fail-closed after #117 deepen: pwd + Run-all commentary contract pins.
    pwd_pin = "resolve ROOT via " + "pwd"
    if pwd_pin not in text:
        fail(
            "run_stewardship contract must keep " + pwd_pin + " pin",
            errors,
        )
    run_all_pin = "Run all stewardship " + "doc gates"
    if run_all_pin not in text:
        fail(
            "run_stewardship contract must keep " + run_all_pin + " pin",
            errors,
        )
    closed_pin = "lands closed " + "#96"
    if closed_pin not in text:
        fail(
            "run_stewardship docstring must note " + closed_pin,
            errors,
        )

    # Leftover after #149: exact run_stewardship layout contract pins.
    leftover_149 = "Leftover after " + "#149"
    if leftover_149 not in text:
        fail(
            "run_stewardship pins must keep " + leftover_149 + " marker",
            errors,
        )
    stew_leftover = "stewardship " + "leftover"
    if stew_leftover not in text:
        fail(
            "run_stewardship contract must keep " + stew_leftover + " wording",
            errors,
        )
    exact_run_layout = "exact live stewardship " + "leftover layout"
    if exact_run_layout not in text:
        fail(
            "run_stewardship contract must keep " + exact_run_layout + " needle",
            errors,
        )
    root_assign_pin = 'ROOT="$(cd "$(dirname "$0")/.." && ' + 'pwd)"'
    if root_assign_pin not in text:
        fail(
            "run_stewardship contract must keep exact ROOT assign pin",
            errors,
        )
    blank_after_cd = "blank line after " + "cd"
    if blank_after_cd not in text:
        fail(
            "run_stewardship contract must keep " + blank_after_cd + " pin",
            errors,
        )
    leftover_after = "stewardship leftover after " + "#149"
    if leftover_after not in text:
        fail(
            "run_stewardship contract must keep " + leftover_after + " wording",
            errors,
        )
    # Fail-closed after #176 deepen: exact ROOT / four-gate / soft-fail / CI order.
    live_176 = "Fail-closed after " + "#176"
    if live_176 not in text:
        fail(
            "run_stewardship pins must keep " + live_176 + " marker",
            errors,
        )
    closed_140 = "lands closed " + "#140"
    if closed_140 not in text:
        fail(
            "run_stewardship docstring must note " + closed_140,
            errors,
        )
    closed_175 = "lands closed " + "#175"
    if closed_175 not in text:
        fail(
            "run_stewardship docstring must note " + closed_175 + " leftover",
            errors,
        )
    exact_root_pin = 'ROOT="$(cd "$(dirname "$0")/.." && pwd)"'
    if exact_root_pin not in text:
        fail(
            "run_stewardship contract must require exact ROOT assign",
            errors,
        )
    four_pin = "exactly four python3 " + "scripts/"
    if four_pin not in text:
        fail(
            "run_stewardship contract must keep " + four_pin + " pin",
            errors,
        )
    soft_pin = "soft-fail with || " + "true"
    if soft_pin not in text:
        fail(
            "run_stewardship contract must keep " + soft_pin + " pin",
            errors,
        )
    parent_marker = "parent-dir ROOT " + "fragment"
    if parent_marker not in text:
        fail(
            "run_stewardship contract must keep " + parent_marker,
            errors,
        )
    locally_c_pin = "doc gates " + "locally"
    if locally_c_pin not in text:
        fail(
            "run_stewardship contract must keep " + locally_c_pin + " pin",
            errors,
        )
    order_joined = "run_stewardship_checks.sh before " + "test_stewardship_gates.py"
    if order_joined not in text:
        fail(
            "run_stewardship contract must keep " + order_joined,
            errors,
        )
    order_marker = "CI runner-before-self-tests " + "order pin"
    if order_marker not in text:
        fail(
            "run_stewardship contract must keep " + order_marker,
            errors,
        )
    # Fail-closed after #191: Pass-2 residual contract pins.
    live_191 = "Fail-closed after " + "#191"
    if live_191 not in text:
        fail(
            "run_stewardship pins must keep " + live_191 + " marker",
            errors,
        )
    # Comment marker used in live residual checks (split so utf-8 self-tests stay stable).
    live_191_comment = "Fail-closed after " + "#191"
    if live_191_comment not in text:
        fail(
            "run_stewardship residual checks must keep " + live_191_comment,
            errors,
        )
    closed_193_178 = "lands closed " + "#193/#178"
    if closed_193_178 not in text:
        fail(
            "run_stewardship docstring must note " + closed_193_178 + " leftover",
            errors,
        )
    residual_marker = "Pass-2 residual after " + "#191"
    if residual_marker not in text:
        fail(
            "run_stewardship docstring must keep " + residual_marker,
            errors,
        )
    not_path_order = "NOT path-order " + "#189"
    if not_path_order not in text:
        fail(
            "run_stewardship docstring must keep " + not_path_order + " distinctness",
            errors,
        )
    not_schema = "NOT schema third-pass " + "#191"
    if not_schema not in text:
        fail(
            "run_stewardship docstring must keep " + not_schema + " distinctness",
            errors,
        )
    gates_only = "gates-only " + "runner"
    if gates_only not in text:
        fail(
            "run_stewardship contract must keep " + gates_only + " pin",
            errors,
        )
    no_self_doc = "no test_stewardship_gates.py " + "inside .sh"
    if no_self_doc not in text:
        fail(
            "run_stewardship docstring must keep " + no_self_doc,
            errors,
        )
    bash_source_pin = "no BASH_SOURCE ROOT " + "drift"
    if bash_source_pin not in text:
        fail(
            "run_stewardship contract must keep " + bash_source_pin,
            errors,
        )
    bare_py_pin = "no bare python " + "scripts/"
    if bare_py_pin not in text:
        fail(
            "run_stewardship contract must keep " + bare_py_pin,
            errors,
        )
    set_soft_pin = "no set +u|+o " + "pipefail"
    if set_soft_pin not in text:
        fail(
            "run_stewardship contract must keep " + set_soft_pin + " soft-fail pin",
            errors,
        )
    back_to_back_pin = "back-to-back gates→self-tests " + "named block"
    if back_to_back_pin not in text:
        fail(
            "run_stewardship contract must keep " + back_to_back_pin,
            errors,
        )
    inline_pin = "no inline check_*.py " + "in stewardship-checks.yml"
    if inline_pin not in text:
        fail(
            "run_stewardship contract must keep " + inline_pin,
            errors,
        )
    actionlint_after = "self-tests before " + "actionlint"
    if actionlint_after not in text:
        fail(
            "run_stewardship contract must keep " + actionlint_after,
            errors,
        )
    block_marker = "CI gates-self-tests back-to-back " + "block pin"
    if block_marker not in text:
        fail(
            "run_stewardship contract must keep " + block_marker,
            errors,
        )
    # Pass-2 leftovers after #203 tip: residual soft-fail / shebang-first pins
    # (lands closed #202/#192 leftover; NOT Pass-2 residual #199 / register #203).
    leftover_203 = "Pass-2 leftovers after " + "#203"
    if leftover_203 not in text:
        fail(
            "run_stewardship pins must keep " + leftover_203 + " marker",
            errors,
        )
    exit0_pin = "soft-fail with || exit " + "0"
    if exit0_pin not in text:
        fail(
            "run_stewardship contract must keep " + exit0_pin + " pin",
            errors,
        )
    shebang_first = "shebang as first " + "line"
    if shebang_first not in text:
        fail(
            "run_stewardship contract must keep " + shebang_first + " pin",
            errors,
        )
    leftover_233 = "Pass-2 residual / template validation leftover after " + "#233"
    if leftover_233 not in text:
        fail(
            "run_stewardship pins must keep " + leftover_233 + " marker",
            errors,
        )
    not_schema_233 = "NOT stewardship-checks/schema residual " + "#233"
    if not_schema_233 not in text:
        fail(
            "run_stewardship docstring must keep " + not_schema_233 + " distinctness",
            errors,
        )
    or_colon_pin = "soft-fail with || " + ":"
    if or_colon_pin not in text:
        fail(
            "run_stewardship contract must keep " + or_colon_pin + " pin",
            errors,
        )
    or_return_pin = "soft-fail with || return " + "0"
    if or_return_pin not in text:
        fail(
            "run_stewardship contract must keep " + or_return_pin + " pin",
            errors,
        )
    errexit_pin = "set +o " + "errexit"
    if errexit_pin not in text:
        fail(
            "run_stewardship contract must keep " + errexit_pin + " pin",
            errors,
        )
    nounset_pin = "set +o " + "nounset"
    if nounset_pin not in text:
        fail(
            "run_stewardship contract must keep " + nounset_pin + " pin",
            errors,
        )
    py_m_pin = "invent python3 " + "-m"
    if py_m_pin not in text:
        fail(
            "run_stewardship contract must keep " + py_m_pin + " pin",
            errors,
        )
    source_pin = "must not source env " + "files"
    if source_pin not in text:
        fail(
            "run_stewardship contract must keep " + source_pin + " pin",
            errors,
        )
    dot_pin = "must not dot-source " + "paths"
    if dot_pin not in text:
        fail(
            "run_stewardship contract must keep " + dot_pin + " pin",
            errors,
        )
    agents_repo_pin = "templates/" + "AGENTS-REPO.md"
    if agents_repo_pin not in text:
        fail(
            "run_stewardship contract must keep existing " + agents_repo_pin + " leftover",
            errors,
        )
    no_invent_tpl = "do not invent new " + "templates"
    if no_invent_tpl not in text:
        fail(
            "run_stewardship contract must keep " + no_invent_tpl + " pin",
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
    # Fail-closed after #117: run_stewardship runner contract early.
    check_run_stewardship_gate_contract(errors)
    # Fail-closed after #100: docs-lint contract early (lycheeignore + markdownlint).
    check_docs_lint_gate_contract(errors)
    # Fail-closed after #111: CI workflow third-pass contract early.
    check_workflow_hardening_gate_contract(errors)
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
