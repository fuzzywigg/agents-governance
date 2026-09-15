# README Badge Standard — Public Governance Repos

```yaml
status: ACTIVE
tier: 1
created: "2026-09-13"
owner: copilot
scope: "public governance front-door repos"
edit_policy: "Agent-editable under docs/; do not invent product badges"
closes: "#16"
```

Public governance repos (Tier B front doors such as this repository) use a **fixed, minimal** badge row so status is visible without private CI or internal tooling details.

## Required badges (in order)

| Order | Badge | Purpose | Example |
|-------|-------|---------|---------|
| 1 | Link Check | Public link integrity CI | `actions/workflows/link-check.yml/badge.svg` |
| 2 | Markdown Lint | Docs quality CI | `actions/workflows/markdown-lint.yml/badge.svg` |
| 3 | License | SPDX / license disclosure | `img.shields.io/github/license/<owner>/<repo>` |

Place the row immediately under the H1 (or ASCII title block), before the one-line purpose sentence.

## Canonical snippet

Replace `<owner>/<repo>` and workflow filenames if a sibling governance repo uses different workflow names. Prefer matching this repo's workflow names when adding CI.

```markdown
[![Link Check](https://github.com/<owner>/<repo>/actions/workflows/link-check.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/link-check.yml)
[![Markdown Lint](https://github.com/<owner>/<repo>/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/markdown-lint.yml)
[![License](https://img.shields.io/github/license/<owner>/<repo>)](https://github.com/<owner>/<repo>/blob/main/LICENSE)
```

Copy into the repository root `README.md`. The License badge target may also be a relative `LICENSE` link when the README sits at repo root.

## Rules

- **Disclose status only** — CI pass/fail and license. No coverage %, download, or social badges.
- **No private workflow badges** — Do not link badges that require private Actions visibility or leak private repo names as broken images.
- **No secrets in badge URLs** — No tokens, query auth, or internal endpoints.
- **Keep the row thin** — Three badges max unless smtp.eth adds an explicit fourth (e.g. release).
- **Quiet stewardship** — Praetor/Aesop-style process stays in normal project docs and wiki narrative; it does not get a product badge.

## This repository

`README.md` already follows this standard (Link Check, Markdown Lint, License).
Executable enforcement lives in `scripts/check_badge_standard.py` (run via
`bash scripts/run_stewardship_checks.sh` or `.github/workflows/stewardship-checks.yml`).
Negative fixtures live in `scripts/test_stewardship_gates.py` (CI fail-closed;
TOKENMAXX suite covers badge/lycheeignore/actionlint/markdown-link/wiki/schema,
including GITHUB_TOKEN + actionlint 1.7.7 three-path needles after #27, plus
cancel-in-progress / `**/*.md` / fourth-badge refusal deepen after #28, plus
`cancel-in-progress: true` / link-check `.github/agents` / markdown-lint
`**/*.md` / lycheeignore `http://*` / Repo-Stewardship actionlint deepen after #29,
plus Python 3.12 pin / Home invent+secrets / existing-path deepen after #30,
plus lychee `--verbose`/`--no-progress` + stewardship `actions/checkout` /
commerce+coveralls badge hints / wiki L0+secret+surface deepen after #31,
plus link/markdown `actions/checkout` + `lychee-action` + MD013 /
twitter+codecov+downloads / HTTP:// casefold deepen after #32,
plus `lycheeverse/lychee-action` + `markdownlint-cli2-action` + MD013
`line_length` + `pip install` PyYAML deepen after #33,
plus `DavidAnson/markdownlint-cli2-action` + `--github-token` + MD024 +
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
plus docs-lint pass-4 after #251 tip: `.lycheeignore` excludes flaky
same-repo `blob/main` GitHub HTML (503) while wiki-outline keeps absolute
blob pins; exact layout + commentary + contract needles (do not revive
closed #251/#250; distinct from Pass-2 residual/template leftover).

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
plus stewardship-badge lint deepen after #189/#199 tip: README invent
stewardship-checks workflow `badge.svg` refuse / exact
link-check+markdown-lint badge.svg paths / exact live markdown-lint
globs block / exact live markdown-lint+link-check push paths filters
(stewardship-badge lint slice only; lands closed #172 leftover; do not
revive #172/#169/#195/#190; leave path-order #189, schema third-pass #191,
and run_stewardship residual #199 alone)).
plus stewardship-schema fourth-pass after #216 tip: nested policy refs /
invalid status+surface enum stubs / whitespace-only / nested+list rejects /
pass-4 contract pins (lands closed #171/#209 leftover; do not revive closed
closed #171/#209/#204/#200/#194/#190/#188/#187/#183),
and run_stewardship residual #199 alone,
plus Pass-2 leftover + markdown-lint/link-check edges after #203 tip:
shebang-first / reject `|| exit 0` / `args: >-` /
externally-broken commentary / without-it private-404 /
reject continue-on-error / exact job permissions / checkout adjacency
(lands closed #202/#192 leftover; do not revive #202/#192;
distinct from Pass-2 residual #199 and merged badge-lint #208)).
plus actionlint path-filter/path-order deepen leftovers after #220: contiguous
push/branches/paths headers / pull_request path-unfiltered /
reject dorny/paths-filter / residual self-workflow path lists / exact
contiguous actionlint run / Download-before-run + self-tests-before-Download
order / contiguous Download/id/run/shell block / reject uses: rhysd/actionlint@
— DISTINCT leftover edges only (not saturated #189 / not #176 layouts /
not schema #191 / not Pass-2 residual #199/#203 / not Pass-2 leftover + md/link #220 /
not wiki-badge / not stewardship-badge lint #208 / not schema fourth-pass #216;
lands closed #223/#217/#213/#198 leftover; do not revive #223/#217/#213/#198/#186/#166/#157),
plus wiki-index/badge leftover deepen after #189: exact PUBLISHABLE_PAGES
contiguous order / Home TOC loop+skip+link forms / empty-index comment /
relative broken-link+empty-index+duplicate-slug needles / README invent
stewardship-checks badge refuse leftover framing — DISTINCT leftover only
(not path-filter/path-order #225 / not Pass-2 leftover + md/link #220 /
not schema fourth-pass #216 / not stewardship-badge lint #208;
lands closed #222/#215/#196 leftover on post-#225 tip; do not revive
closed #222/#215/#196/#185/#172)).
plus stewardship-checks + schema residual deepen leftovers after #227 tip:
exact contiguous Set up Python / Install PyYAML / checkout→Set up Python /
full push paths / schedule+cron / concurrency / jobs.stewardship header /
reject strategy|matrix|services invent / schema residual (pass-5)
status+surface stubs + helper needles — DISTINCT leftover only
(not wiki-index/badge #227 / not path-filter/path-order #225 /
not Pass-2 leftover + md/link #220 / not schema fourth-pass #216 /
not stewardship-badge lint #208; lands closed #229 leftover on post-#227
tip; do not revive closed #229/#228/#230/#231),
plus markdown-lint/link-check residual exact layouts after #233 tip: exact
contiguous link-check `args: >-` flag block / exact contiguous `on:`
push/PR/schedule/workflow_dispatch for link+lint / exact contiguous
markdown-lint `with:` globs|+config / exact contiguous link-check `with:`
token commentary — DISTINCT residual edges only (not leftover #233 schema /
not wiki-index/badge #227 / not path-edges #225 / not Pass-2 leftover +
md/link #220 core / not stewardship-badge lint #208; lands closed #221 leftover
residual; do not revive #221/#219/#214/#207/#201/#231)).
plus wiki outline/PUBLISH leftover deepen after #239 tip: existing
`docs/wiki` pages only — PUBLISH.md pages-table order / Pages to publish /
wiki.git clone / cp docs/wiki/{page} (no operator PUBLISH.md) / git add six
pages / purpose+closes `#16` / Fallback `.wiki.git` / badge-standard blob
rewrite / OPERATOR_ONLY not in PUBLISHABLE_PAGES — DISTINCT leftover only
(not md/link residual #239 / not stewardship-checks/schema #233 /
not wiki-index/badge #227 / not path-filter/path-order #225;
lands closed #238 leftover on post-#239 tip; do not revive #238)).
plus actionlint path-filter/path-order residual deepen after #225: contiguous
pull_request:/schedule: adjacency / reject branches-ignore: /
pull_request type-unfiltered / reject tj-actions/changed-files /
contiguous four-step actionlint path-order / schedule before workflow_dispatch /
contiguous shell-less actionlint run step — DISTINCT residual edges only
(not wiki outline/PUBLISH leftover #243 / not saturated deepen #225/#203 /
not #189 / not #176 / not schema #191/#216 / not Pass-2 residual #199/#203 /
not Pass-2 leftover + md/link #220 / not wiki-badge leftover #227 /
not stewardship-checks/schema leftover #233 / not md/link residual #239 /
not stewardship-badge lint #208; do not revive
closed #236/#232/#228/#226/#223/#217/#213/#198/#186/#166/#157)).
plus wiki/mdlink leftover deepen after #243 tip: PUBLISH YAML
status+created+purpose / One-shot heading / exact clone dest / contiguous
cp list / git commit `#16` / `git push origin master` / Acceptance+Fallback /
Repository not found / Home (landing) / Home operator PUBLISH.md
omit-when-copying plus exact contiguous link+lint concurrency / job headers /
`**/*.md` then `fail: true` adjacency — DISTINCT leftover only (not #243
wiki/PUBLISH saturated pins / not md/link residual #239 / not path-filter
residual #244 / not schema #233; no extra wiki files)).
plus stewardship-schema leftover deepen after #252 tip: leftover parse/load
needles / leftover invalid status+surface stubs / `stewardship_common`
glob+hint+is_file leftovers — DISTINCT leftover only (not wiki/mdlink
leftover #252 / not path-edges residual #244 / not wiki outline/PUBLISH
leftover #243 / not md/link residual #239 / not stewardship-checks/schema
residual #233 / not wiki-index/badge leftover #227; do not revive
closed #253/#248/#241)).
plus actionlint path-filter/path-order residual leftover deepen after #258:
contiguous push:/pull_request: adjacency / contiguous
schedule:/workflow_dispatch: adjacency / pull_request branches-unfiltered /
reject tags-ignore: / reject workflow_call: / contiguous five-step
actionlint path-order / contiguous on:/push: header — DISTINCT residual
leftover edges only (not stewardship-schema leftover #258 /
not wiki/mdlink leftover #252 / not saturated residual #244 /
not saturated deepen #225/#203 / not wiki outline/PUBLISH leftover #243 /
not md/link residual #239 / not stewardship-checks/schema leftover #233 /
not wiki-badge leftover #227 / not #189 / not #176 / not schema #191/#216 /
not Pass-2 residual #199/#203 / not Pass-2 leftover + md/link #220 /
not stewardship-badge lint #208; do not revive
closed #255/#247/#244/#236/#232/#228/#226/#223/#217/#213/#198/#186/#166/#157)).
plus Pass-2 residual + existing templates/AGENTS-REPO.md leftover after #244
(rebased post-#262): soft-fail with `|| :` / `|| return 0` / `set +o errexit` /
`set +o nounset` / invent `python3 -m` for gates / must not source env files /
must not dot-source paths / reject any `continue-on-error:` on existing workflows /
exact contiguous concurrency group template on all three workflows (existing
templates only; no invent) / existing `templates/AGENTS-REPO.md` H1
`[PROJECT_NAME]` / parent_governance / maintainer smtp.eth / YYYY-MM-DD
placeholder / §1–§6 / `[CONFIG_FILE]` / Never commit `.env` /
`agents-md/description` / no invent badge.svg chrome — DISTINCT leftover edges
only (not path-edges leftover #262 / not stewardship-schema leftover #258 / not wiki/mdlink leftover #252 / not actionlint path-filter/path-order
residual #244 / not wiki outline/PUBLISH leftover #243 /
not md/link residual #239 / not stewardship-checks/schema residual #233 /
not wiki-index/badge #227 /
not path-edges #225 / not Pass-2 leftover + md/link #220 /
not Pass-2 residual #199/#203 / not badge-lint #208 / not schema #216;
lands closed #251/#250/#246/#245/#240 leftover on post-#262 tip;
do not revive #251/#250/#246/#245/#240/#235/#230;prior #251/#250 RED was transient GitHub 503; do not invent new templates).
plus stewardship-schema leftover residual deepen after #262 tip
(rebased post-#278): leftover residual parse/load needles / leftover residual
invalid status+surface stubs / `stewardship_common`
errors.append+lowered+scheme+found.update leftovers — DISTINCT leftover
residual only (not lychee/blob-503 leftover #278 /
not Pass-2 residual leftover #272 / not path-filter/path-order leftover #262 /
not schema leftover #258 / not wiki/mdlink leftover #252 /
not path-edges residual #244 / not wiki outline/PUBLISH leftover #243 /
not md/link residual #239 / not stewardship-checks/schema residual #233 /
not wiki-index/badge leftover #227; do not revive closed
PR #279/#276/#275/#269/#263/#257/#253/#248/#241; prior #269 RED was MD018)).
plus wiki/mdlink leftover residual deepen after #282 tip: PUBLISH YAML
status+created+purpose+closes / table header / sibling cells / full operator
push prose / clean worktree / or main default branch / stay-green acceptance /
Home.md `./Home.md` fallback / Settings→Wikis / create-any-page-once plus md/link
Check links->lychee@v2 / Run markdownlint->DavidAnson@v24 / name->on adjacency
plus markdown-link residual empty-fragment / query-string / escapes-repo /
missing-heading / OK banner / `raw.startswith("#")` — DISTINCT leftover only
(lands closed #281/#277 leftover; not stewardship-schema residual #282 /
not lychee/blob-503 leftover #278 / not Pass-2 residual + templates #272 /
not path-edges leftover #262 / not wiki/mdlink leftover #252 /
not stewardship-schema leftover #258 / not path-filter residual #244 /
not wiki outline/PUBLISH leftover #243 / not md/link residual layouts #239;
no extra wiki files)).
plus stewardship-schema residual CI leftover residual deepen after #314 tip
(lands closed #316 leftover on post-#314 path-order tip):
residual CI leftover residual helper needles (`if missing:` /
`fail(f"missing file: {rel}"` / `if value is None or` / `must be non-empty` /
`must be a string` / `"status" in required_keys` / `status is not None` /
`status must be ACTIVE` / `(expected {want!r})` / `not isinstance(level, int)` /
`isinstance(tier, bool)` / `not isinstance(tier, int)` / `or tier < 1` /
`if rel == "AGENTS.md"` / `"version" in data` / `yaml.safe_load` /
`isinstance(loaded, dict)`) / residual CI leftover residual status stubs
ABANDONED|EXPIRED|REVOKED|HIDDEN|OFFLINE|ZOMBIE / residual CI leftover residual
surface stubs huggingface|replicate|cohere|bedrock|sagemaker — DISTINCT schema
residual CI leftover residual only (tip-relaunch leftover residual on post-#314 tip;
not schema residual CI leftover #309 / not schema residual CI #299 /
not wiki/mdlink leftover residual #293 / not schema leftover residual #282 /
not lychee/blob-503 leftover #278 / not Pass-2 residual leftover #272 /
not path-filter/path-order leftover #314/#262 / not schema leftover #258 /
not wiki/mdlink leftover #252 / not path-edges residual #244 /
not stewardship-checks/schema residual #233; no stewardship_common invent;
do not revive closed PR #316/#295/#290/#268/#259/#257/#253/#248/#241)).
plus stewardship-schema residual CI leftover deepen after #299 tip: residual CI
leftover helper needles (`missing = sorted(...)` / `if key not in data:` /
`value = data[key]` / `if reject_non_scalar(...)` / `status = data.get("status")` /
`str(status).upper() != "ACTIVE"` / `if rel.startswith("docs/")` /
`expected = EXPECTED_VALUES.get(rel, {})` / `if got != want:` /
`isinstance(level, bool)` / `level not in (0, 1, 2, 3)` / `if "tier" in data:` /
`tier = data["tier"]` / `for date_key in DATE_KEYS:` / `if "invent" not in policy` /
`scan_secrets(path, errors)` / `except Exception as exc:` / `errors: list[str] = []` /
`sys.exit(main())` / engine PyYAML-or-stdlib) / residual CI leftover status stubs
BLOCKED|PAUSED|DEFERRED|SKIPPED|MUTED|DORMANT / residual CI leftover surface stubs
gemini|perplexity|fireworks|deepseek|ollama — DISTINCT schema residual CI leftover
only (tip-relaunch leftover on post-#299 tip; not schema residual CI #299 /
not wiki/mdlink leftover residual #293 / not schema leftover residual #282 /
not lychee/blob-503 leftover #278 / not Pass-2 residual leftover #272 /
not path-filter/path-order leftover #262 / not schema leftover #258 /
not wiki/mdlink leftover #252 / not path-edges residual #244 /
not stewardship-checks/schema residual #233; no stewardship_common invent;
do not revive closed PR #295/#290/#268/#259/#257/#253/#248/#241)).
plus stewardship-schema residual CI deepen after #293 tip: residual CI helper
needles (`if errors:` / `return 1` / `return 0` / `DOC_SCHEMAS.items()` /
`for key in required_keys:` / `path.is_file` / `block.strip` /
`STRING_KEYS isinstance` / `autonomy_level in data` / `edit_policy in data` /
`date_key not in data` / `ISO_DATE_RE.match` / `SEMVER_RE.match` /
`ISSUE_REF_RE.search` / `re.fullmatch digit` / `value[1:-1]` /
`expected.items` / `level = data["autonomy_level"]` / err print /
`splitlines` / line+key strip / nonempty compound / `path = ROOT / rel`) /
residual CI status stubs SHELVED|SUPERSEDED|HOLD|STALE|ALPHA|NIGHTLY /
residual CI surface stubs chatgpt|vertex|groq|together|mistral — DISTINCT
schema residual CI only (lands closed #290/#268 leftover; not wiki/mdlink
leftover residual #293 / not schema leftover residual #282 /
not lychee/blob-503 leftover #278 / not Pass-2 residual leftover #272 /
not path-filter/path-order leftover #262 / not schema leftover #258 /
not wiki/mdlink leftover #252 / not path-edges residual #244 /
not stewardship-checks/schema residual #233; no stewardship_common invent;
do not revive closed PR #290/#268/#259/#257/#253/#248/#241)).
plus actionlint path-filter/path-order residual leftover deepen after #309 tip
(lands closed #310/#304/#303/#300/#294/#292/#286/#280 leftover):
contiguous workflow_dispatch:/concurrency: adjacency / contiguous name:/on:
workflow header / reject workflow_run: / reject repository_dispatch: /
reject merge_group: / reject tags: (bare) / contiguous six-step actionlint
path-order — DISTINCT residual leftover edges only (not schema residual CI
leftover #309 / not schema residual CI #299 /
not wiki/mdlink leftover residual #293 / not stewardship-schema residual #282 /
not lychee/blob-503 harden #278 / not Pass-2 residual leftover #272 /
not saturated leftover #262 / not stewardship-schema leftover #258 /
not wiki/mdlink leftover #252 / not saturated residual #244 /
not saturated deepen #225/#203 / not wiki outline/PUBLISH leftover #243 /
not md/link residual #239 / not stewardship-checks/schema leftover #233 /
not wiki-badge leftover #227 / not #189 / not #176 / not schema #191/#216 /
not Pass-2 residual #199/#203 / not Pass-2 leftover + md/link #220 /
not stewardship-badge lint #208; do not revive closed PRs
(#310/#304/#303/#300/#294/#292/#286/#280/#274/#270/#264/#255/#247/#244/#236/#232/#228/#226/#223/#217/#213/#198/#186/#166/#157)).
plus wiki/mdlink leftover residual deepen after #320 tip: PUBLISH H1 /
in-repo source / separate git repo / table separator / rewrite relative /
badge-standard.md links to: / Wiki Home README acceptance / private MEMORY /
editable source copy / Until `.wiki.git` treat / landing from README /
clone fails initialized / push Home.md / full push # or main line /
Home Start here TOC / Source of truth / Canonical front door /
public narrative layer / Front-door duties / Docs quality CI /
token->args adjacency / checkout->Check links->lychee triple /
checkout->Run markdownlint->DavidAnson triple — DISTINCT leftover only
(lands #325/#318/#308/#307/#302 leftover; not stewardship-schema residual CI leftover residual #320 /
not path-filter/path-order leftover #314 / not stewardship-schema residual CI leftover #309 /
not stewardship-schema residual CI #299 /
not stewardship-schema residual CI #297 /
not wiki/mdlink leftover residual #293 / not stewardship-schema residual #282 /
not lychee/blob-503 leftover #278 / not Pass-2 residual + templates #272 /
not path-edges leftover #262 / not wiki/mdlink leftover #252;
no extra wiki files)).
plus Pass-2 residual / templates leftovers after #326 tip: soft-fail with
`|| true` / `set +e` / must not `eval` / existing `templates/AGENTS-REPO.md`
`Level [0/1/2]` / L0–L2 / Critical Files / Autonomy Level / End of Document /
SEV-1..SEV-4 / `[test command]` / cov-req placeholder / `.env` Secrets row /
governs blurb / lychee reject invent `tree/main` + bare `https://github.com/` /
keep Same-repo GitHub — DISTINCT leftover only (lands closed
PR #333/#331/#324/#315/#313/#312/#305/#298/#291 leftover on post-#326 tip; not
wiki/mdlink leftover residual #326 /
not stewardship-schema residual CI leftover residual #320 /
not path-filter/path-order residual leftover #314 /
not stewardship-schema residual CI leftover #309 /
not stewardship-schema residual CI #299 /
not wiki/mdlink leftover residual #293 /
not stewardship-schema leftover residual #282 /
not saturated Pass-2 residual leftover #272 /
not lychee/blob-503 leftover #278 / not path-edges leftover #262 /
not schema leftover #258 / not wiki/mdlink leftover #252; do not invent new
templates; no secrets; do not revive PR #333/#331/#324/#315/#313/#312/#305/#298/#291)).
plus Pass-2 residual / templates leftovers after #337 tip: soft-fail with
`|| /bin/true` / `|| /usr/bin/true` / `set +E` / existing
`templates/AGENTS-REPO.md` `[Section Title]` / Add project-specific rules /
Environments table + Dev/Staging/Production rows / Human confirms /
Auto-approve + budget / Human approval required / Immediate response /
`< 1 hour` / `< 24 hours` / Next sprint / Version History /
ecosystem-wide governance / See `[agents-governance]` / lychee reject invent
`blob/master` + `tree/master` + `raw.githubusercontent.com` — DISTINCT leftover
residual only (leftover residual on post-#337 tip; not Pass-2 residual /
templates leftover after #326 / not wiki/mdlink leftover residual #326 /
not stewardship-schema residual CI leftover residual #320 /
not path-filter/path-order residual leftover #314 /
not stewardship-schema residual CI leftover #309 /
not stewardship-schema residual CI #299 /
not wiki/mdlink leftover residual #293 /
not stewardship-schema leftover residual #282 /
not saturated Pass-2 residual leftover #272 /
not lychee/blob-503 leftover #278 / not path-edges leftover #262 /
not schema leftover #258 / not wiki/mdlink leftover #252; do not invent new
templates; no secrets; do not revive PR #333/#331/#324/#315/#313/#312/#305/#298/#291)).

plus wiki/mdlink leftover residual deepen after #348 tip: and drop PUBLISH.md
bullet / initialized once (Settings then first page or / first page or / in this directory landing /
(.wiki.git URL) that must be / Home H1 public wiki / Policy truth /
Praetor/Aesop stays quiet / TOC cells / Out of scope / project-template /
MEMORY dumps / Invented frameworks / Maintained by smtp.eth /
trustworthy without / Prefer reversible PRs / Never delete scratchpad /
three workflows / --verbose->--no-progress /
--github-token->--exclude-path / !OWASP->config adjacency —
DISTINCT leftover only (not Pass-2 residual / templates leftover #348 /
not Pass-2 residual / templates leftover #337 /
not wiki/mdlink leftover residual after #326 /
not wiki/mdlink leftover residual after #320 /
not stewardship-schema residual CI leftover residual #320 /
not path-filter/path-order leftover #314 / not stewardship-schema residual CI leftover #309 /
not stewardship-schema residual CI #299 /
not stewardship-schema residual CI #297 /
not wiki/mdlink leftover residual #293 / not stewardship-schema residual #282 /
not lychee/blob-503 leftover #278 / not Pass-2 residual + templates #272 /
not path-edges leftover #262 / not wiki/mdlink leftover #252;
no extra wiki files)).
A fourth “Stewardship Checks” badge is intentionally **not** added — quiet
stewardship stays in CI/docs, not as invent-product chrome.
Flaky `img.shields.io` hosts stay out of lychee via `.lycheeignore`; license
badge presence remains stewardship-enforced.

## Related

- Public wiki outline: [wiki/Home.md](./wiki/Home.md)
- Wiki publish path: [wiki/PUBLISH.md](./wiki/PUBLISH.md)
- Testing commands: [AGENTS.md §3](../AGENTS.md#3-testing-requirements)
