# Repo Stewardship

[← Home](Home.md)

How public governance repos in this ecosystem are kept trustworthy without
exposing private project machinery.

## Front-door duties

- Keep [README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md) accurate: purpose, document map, badge row.
- Follow the [badge standard](../badge-standard.md).
- Prefer reversible docs/stewardship PRs; no invent-product work.
- Never delete scratchpad history; append and mark `[x]` when done.

## Docs quality CI

Public front-door trust rests on three workflows (status badges cover Link Check and
Markdown Lint only — stewardship stays in CI/docs, not as a product badge):

| Workflow | What it enforces |
|----------|------------------|
| `markdown-lint.yml` | Markdownlint on docs |
| `link-check.yml` | External + markdown link integrity (lychee) |
| `stewardship-checks.yml` | Badge row, wiki outline, metadata schemas, relative links + self-tests |

Locally: `bash scripts/run_stewardship_checks.sh` then
`python3 scripts/test_stewardship_gates.py` (heavy negative/positive fixtures:
badge order/http/secrets/lycheeignore shields, relative schemes/escapes/fragments,
wiki invent chrome, schema value/date/semver, workflow/actionlint hardening needles,
link-check GITHUB_TOKEN + actionlint 1.7.7 three-path targets after #27, plus
cancel-in-progress / `**/*.md` / fourth-badge refusal deepen after #28, plus
`cancel-in-progress: true` / `.github/agents` exclude / markdown-lint `**/*.md` /
lycheeignore `http://*` / actionlint callout deepen after #29, plus Python 3.12
pin / Home invent+secrets / existing-path deepen after #30, plus lychee
`--verbose`/`--no-progress` + stewardship `actions/checkout` / wiki L0+secret
deepen after #31, plus link/markdown `actions/checkout` + `lychee-action` +
MD013 / HTTP:// casefold deepen after #32, plus `lycheeverse/lychee-action` +
`markdownlint-cli2-action` + MD013 `line_length` / pip install deepen after #33,
plus `DavidAnson/markdownlint-cli2-action` + `--github-token` + MD024 /
`download-actionlint.bash` deepen after #34,
plus MD024 `siblings_only` + `rhysd/actionlint` + `curl` download +
lychee-action `with: token:` deepen after #35,
plus MD013 `line_length: 200` + MD024 `siblings_only: true` +
`raw.githubusercontent.com` + curl `-fsSL` deepen after #36,
plus markdownlint `default: true` + `get_actionlint.outputs.executable` +
actionlint `/v1.7.7/` path + lychee `--max-concurrency 8` / `--timeout 20` /
`--max-retries 3` deepen after #37,
plus MD033/MD041/MD060 `false` + `markdownlint-cli2-action@v24` +
`actions/setup-python@v5` + `id: get_actionlint` deepen after #38,
plus `actions/checkout@v7` + `lychee-action@v2` + job timeouts 20/10/15 +
weekly crons + `ubuntu-latest` + `pip --quiet` + `shell: bash` +
actionlint `-color` deepen after #39,
plus relative-link gate contract pins after #41: OWASP/agents/node_modules
skip, `fully_unquote`, empty `path#` fragments, query-string reject,
`run_stewardship_checks.sh` order badge→wiki→schema→relative,
plus wiki-outline gate contract pins after #43: PUBLISHABLE_PAGES L0–L3 /
credential / copilot topic hints, `strip_fenced_code`, protocol-relative
`//` reject, Home kill-switch callout,
plus stewardship-schema gate contract pins after #45: DOC_SCHEMAS /
EXPECTED_VALUES / SEMVER / ISO-8601 / closes `#N` / invent edit_policy /
issue-backlog owner `copilot` / `scan_secrets`,
plus stewardship_common contract pins after #46: SECRET_PATTERNS /
SECRET_URL_HINTS / FORBIDDEN_BADGE_HINTS / DANGEROUS_LINK_SCHEMES /
`strip_fenced_code` / `scan_secrets` / invent-product wording,
plus badge-standard gate contract pins after #48: REQUIRED_ORDER /
MAX_BADGES = 3 / EXPECTED_REPO / REQUIRED_WORKFLOWS / badge.svg + shields
license / contiguous row / invent-product / fourth-badge refusal /
Stewardship product badge reject,
plus stewardship-schema scalar / `STRING_KEYS` / empty-yaml / bool-int
rejects and live badge scope / PUBLISH purpose / closes `#16` pins after #53,
plus relative-link second-pass after #55: `MD_LINK_RE` / `SKIP_*` /
`_MAX_UNQUOTE_PASSES = 4` / `should_skip` / `iter_markdown` / `headings_in` /
`check_file` / mailto+tel allow / NUL / angle brackets / image links /
escapes+broken+missing needles / rglob fail-closed,
plus wiki-outline second-pass after #59: `OPERATOR_ONLY` / docs/wiki /
`_reject_invent_badge_chrome` / autonomy+governance+public+kill+secret+
surface+routing+`run_stewardship_checks.sh`+badge topic pins / `](Home.md)`
backlink / Unexpected+Missing+FAILED needles / angle+image RE /
Do-not-push / README blob / badge-standard hint / social special-case
pins / invent-chrome needle / Home.md table row,
plus badge-standard second-pass after #61: `REQUIRED_ORDER`+`EXPECTED_REPO`
exact assigns / README+LICENSE+badge-standard+CONTRIBUTING+AGENTS+
lycheeignore+markdownlint paths / contract+main fns /
`actions/workflows/*.yml/badge.svg` / exactly+order+contiguous+H1+
unexpected+forbidden+secret+FAILED+OK needles / endswith+/./LICENSE /
`load_workflow_text` / invent-product doc / intentionally / quiet
stewardship / selftest+relative AGENTS pins / img https startswith /
http link reject,
plus stewardship_common second-pass after #65: ROOT `parents[1]` /
`FENCED_BLOCK_RE` DOTALL / helper doc pins / scan_secrets needles /
`relative_to` / `strip().lower()` / `startswith` / `errors.append` /
`password|passwd|token` / OPENSSH+EC / Public docs / invent-product
surface / social chrome / Link schemes / `is_file`+`sorted` /
workflows path / `return None` / exact `DANGEROUS_LINK_SCHEMES` +
`SECRET_URL_HINTS` head,
plus actionlint-style gate contract pins after #75: top-level `name:` /
`jobs.*.runs-on` / `jobs.*.steps` / `timeout-minutes` / no
`pull_request_target` / no `write-all` / no `contents: write` / no
`id-token: write` / `@`-pin float set `main|master|latest` / `docker://`
skip / unpinned reject,
plus stewardship-schema second-pass after #72/#75: `FENCED_YAML_RE` exact /
`ISO_DATE_RE` / `SEMVER_RE` / `ISSUE_REF_RE` / `DATE_KEYS` / Tiny YAML /
scalar+non-empty+string / ACTIVE / tier / 0..3 / ISO-8601 / invent /
semver / closes #N / FAILED+OK / stdlib-subset+PyYAML / bool subclass /
`match.group(1)` / missing keys / utf-8 / `STRING_KEYS` members,
plus actionlint-style second-pass after #83/#86: exact `name:`/`uses:`
regexes / write-all+contents+id-token regexes / `docker://` startswith /
`@` not in uses / `rsplit` / `group(1).strip()` / fail needles /
least-privilege+OIDC+majors comments / `REQUIRED_WORKFLOWS` loop),
plus relative-link third-pass after #90: `MD_LINK_RE`+`ATX_HEADING_RE`
exact / `SKIP_*` exact / OK+FAILED banners / empty+http+proto+dangerous
needles / utf-8 / `as_posix` / `.md` suffix / `ValueError` / `sorted` /
UNICODE / space-dash / Percent-decode+Cap / empty () / `sys.exit` /
`urllib.unquote` / `group(2)` / `startswith#` / `split#` / files scanned /
stewardship_common / title / `#{1,6}` / slug punct / Offline+lychee /
`path.parent`,
plus wiki-outline third-pass after #90/#94: WIKI exact / `removesuffix` /
`glob("*.md")` / `sorted(unexpected)` / Link Check+Markdown Lint+No secrets /
Home invent+secrets+kill needles / Repo-Stewardship relative+invent+
actionlint+run_script needles / `startswith("//")`+`http://` / `group(2)` /
utf-8 / `sys.exit` / stewardship_common / invent-chrome social special-cases /
shields host / markdown-badge open / badge-in-lowered gate /
README+badge hint paths / pages+operator OK / intentional PUBLISH pin /
`PAGE_TOPIC_HINTS.get` / `strip_fenced_code(text)` /
`has_dangerous_scheme(target)` / `scan_secrets` calls,
plus docs-lint pins after #100: `.lycheeignore` escaped `img\.shields\.io` /
`modelcontextprotocol.io` / `linuxfoundation.org` / stewardship+308+103
commentary / reject `https://*`+`http://*`+`*` / exact MD013+MD024 objects /
MD033+MD041+MD060 false / `default: true` / ROOT path assigns /
`check_workflows_and_license` + CDN-exclude needle /
`check_docs_lint_gate_contract`,
plus badge-standard third-pass after #104: `BADGE_LINE_RE`+`REPO_FROM_*`
exact / `REQUIRED_WORKFLOWS` exact / `group(label|img|link)` / `sys.exit` /
stewardship_common / `BADGE_GATE` / utf-8 / Strict row / H1 startswith /
FAIL README / https image+link needles / absolute workflow URL / License
point / Unexpected label / extract+check_badges / `contract(errors)` /
IGNORECASE / `blob.lower` / `EXPECTED_REPO.lower`,
plus actionlint-style third-pass after #108: `concurrency:` +
`cancel-in-progress:` / `permissions:` present / reject
`actions|packages|pull-requests: write` / `re.finditer` / docker continue /
`rsplit[-1]` / third-pass docstring,
plus stewardship_common third-pass after #111: future annotations / import
re+Path / exact PRIVATE KEY+gh-family+sk|rk patterns / SECRET_PATTERNS
tuple typing / FENCED_BLOCK_RE.sub / label or relative_to / pattern.search /
lowered=text.lower / re.escape / https? URL-ish / ROOT.glob+found.update /
set[Path] / workflows path join / scheme+pattern+hint loops / Shared helpers
doc / hint.endswith(=) / MEMORY dumps / str|None+list[Path] /
FORBIDDEN_BADGE_HINTS head / SECRET_URL_HINTS gh-family prefix members,
plus run_stewardship runner pins after #117: `#!/usr/bin/env bash` /
`set -euo pipefail` / `dirname "$0"`+`pwd` ROOT / `cd "$ROOT"` / same set as
CI / `python3 scripts/<gate>` ×4 / badge→wiki→schema→relative order /
`check_run_stewardship_gate_contract` (lands closed #122/#96 leftover; do not
revive #119),
plus CI workflow third-pass after #111/#117/#127: concurrency templates /
cron+timeout / DavidAnson@v24 / setup-python@v5 / lychee verbose+
concurrency+timeout+retries / fail:true / get_actionlint / curl -fsSL,
plus docs-lint second-pass after #132: exact live exclude URLs /
Connection-reset+RST+false-positive+early-hints+valid-site commentary /
`check_badge_standard.py` reference / License badge presence remains enforced /
exact `.markdownlint.json` layout+key-set+`json.loads` pins /
`check_docs_lint_gate_contract` second-pass,
plus wiki-badge posture after #132/#135: status badges cover Link Check+Markdown
Lint / product badge refusal / reject stewardship-checks workflow badge invent /
reject embedded markdown badge images / PUBLISH Link Check+Markdown Lint
exactly / Home no badge-row embeds,
plus actionlint-style deepen after #135/#141: `cancel-in-progress: true` /
`contents: read` / `ubuntu-latest` / `workflow_dispatch:` / reject
`security-events|attestations|statuses|deployments: write` / deepen docstring,
plus leftover docs-lint/stewardship/actionlint pins after #149: docs-lint
third-pass exact `.lycheeignore` full layout + commentary lines /
actionlint leftover `contents: read` membership affirm (complement #149
regex) / stewardship leftover exact `run_stewardship_checks.sh` full layout,
plus stewardship CI deepen after #161: Check links / Run markdownlint /
Set up Python / Install PyYAML (schema parser) / Stewardship gates+self-tests
step names / exact token+`--github-token` forms / `--exclude-path .github/agents` /
`globs: |` / AGENTS+CLAUDE+LICENSE+CONTRIBUTING+`.github/workflows/**` paths /
Weekly drift + GITHUB_TOKEN commentary / deepen docstring,
plus overnight stewardship/CI/schema/wiki fixture deepen after #165: residual
schema/wiki/relative/common/badge policy edge fixtures via existing `_seed_*`
harnesses only — not actionlint / docs-lint / stewardship-CI pin / path-filter /
schema-third-pass pin spam; lands closed #167 leftover; do not revive
closed #167/#168/#169,
plus actionlint path-filter leftovers after #173: exact push `paths:` layouts /
residual stewardship path entries / reject `paths-ignore:` / ignore-glob
exactness — empty stubs already handled; distinct from path-order/badge and
stewardship-badge lint; lands closed #166 leftover; do not revive #166/#157,
plus run_stewardship Pass-2 after #176: exact ROOT assign / exactly four
`python3 scripts/` / no `|| true` soft-fail / `dirname "$0")/..` fragment /
doc gates locally / CI runner before self-tests /
`check_run_stewardship_gate_contract` Pass-2 (lands closed #175/#140 leftover;
do not revive #175/#140/#122),
plus wiki-index validators after #176: Home TOC empty-index / publishable
page index stubs / broken internal stub links / empty markdown index /
duplicate slug `headings_in` set collapse — lands closed #177/#168/#170 leftover;
do not revive #177/#168/#170; distinct from path-filter #176 and run_stewardship #179,
plus actionlint path-order leftover after #181: contiguous three-path
actionlint order / exact bash <(curl -fsSL) download /
reject continue-on-error: true / Download actionlint + actionlint existing
workflow paths step names / path-order leftover docstring,
plus stewardship-schema third-pass + deepen after #189: future annotations /
Path parent / yaml=None / five live docs / parse pins / path.is_file /
block.strip / STRING_KEYS / BLE001 / DATE_KEYS / deepen docstring
(lands closed #187/#188 leftover; do not revive #187/#188/#183/#164;
distinct from path-order #189),
plus run_stewardship Pass-2 residual after #191: gates-only runner /
no BASH_SOURCE / no bare python / no set +u|+o pipefail /
back-to-back gates→self-tests block / no inline check_*.py /
self-tests before actionlint (lands closed #193/#178 leftover; do not
revive #193/#178/#175/#140; distinct from schema third-pass #191 and
path-order #189),
plus stewardship-schema fourth-pass after #199/#203 tip: nested policy refs /
invalid status+surface enum stubs / whitespace-only / nested+list rejects /
pass-4 contract pins (lands closed #171/#200/#204 leftover; do not revive
closed #171/#200/#204/#194/#190/#188/#187/#183; leave open md/link #206 alone).
Stewardship CI also runs `actionlint` on the three existing workflow paths.

## What agents may edit (this repo, L1)

- `AGENTS.md`, `CLAUDE.md`, `README.md`
- Files under `docs/` and append-only `scratchpad/`
- Issue / PR templates under `.github/`

## What requires smtp.eth (Andrew) approval

- Changes to `AGENTS-ECOSYSTEM.md` or `templates/AGENTS-REPO.md`
- Adding or removing files at repo root
- Merging own PRs / changing branch protection

## Quiet stewardship

Praetor/Aesop-style process is **quiet governance**: it supports normal project
docs and routing; it is not marketed as a separate product in the public wiki.
Link to living policy and README instead of inventing frameworks.

## Issue / PR hygiene

- Issue titles: `[agent-surface] Descriptive title`
- PRs reference the issue they address and use the PR template
- Working branches only — never commit stewardship directly to `main`

[← Autonomy Levels](Autonomy-Levels.md) · [Agent Routing →](Agent-Routing.md)
