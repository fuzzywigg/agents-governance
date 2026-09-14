# Changelog

All notable changes to the agents-governance framework are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- TOKENMAXX stewardship-schema third-pass + deepen pins after #165: expand
  self-tests to 3145 cases (was 2957) fail-closing live schema integrity —
  future annotations / Path parent / yaml=None / five live docs / true+false /
  null+~ / fullmatch / split+strip quotes / FENCED search / nested reject /
  ACTIVE / EXPECTED get / closes scope / path.is_file / block.strip /
  Exception as exc / STRING_KEYS / engine PyYAML / BLE001 / got != want /
  DATE_KEYS / deepen docstring — schema leftover slice only (not docs-lint /
  actionlint / wiki / stewardship-CI / workflow spam); no invent-product; no
  fourth badge. Distinct from stewardship CI deepen (#165), leftover combo
  (#161), actionlint (#149), wiki-badge (#141), and docs-lint (#135). Does
  **not** revive closed #142/#147/#153/#163 siblings.

- TOKENMAXX stewardship CI deepen pins after #161: expand self-tests to
  2957 cases (was 2885) fail-closing live stewardship CI reliability leftovers —
  Check links / Run markdownlint / Set up Python / Install PyYAML (schema parser) /
  Stewardship gates+self-tests step names / exact `token`+`--github-token` forms /
  `--exclude-path .github/agents` / `globs: |` / AGENTS+CLAUDE+LICENSE+CONTRIBUTING+
  `.github/workflows/**` path filters / Weekly drift + GITHUB_TOKEN commentary /
  named-step `uses:` scan broaden / deepen docstring + gate-contract needles —
  stewardship CI workflow slice only (not actionlint / badge / wiki / docs-lint /
  schema / common spam); no invent-product; no fourth badge. Lands closed #158
  leftover on post-#161 main (do **not** revive #158/#113).

- TOKENMAXX leftover docs-lint/stewardship/actionlint pins after #149: expand
  self-tests to 2885 cases (was 2761) fail-closing live leftover integrity —
  docs-lint third-pass exact `.lycheeignore` full layout + commentary lines /
  actionlint leftover `contents: read` membership affirm (complement #149
  regex) / stewardship leftover exact `run_stewardship_checks.sh` full layout —
  leftover docs-lint/stewardship/actionlint slice only (not wiki / badge / CI
  workflow / relative / schema spam); no invent-product; no fourth badge.
  Distinct from actionlint deepen (#149), docs-lint second-pass (#135), and
  wiki-badge (#141). Does **not** revive closed #150/#146/#154 siblings.

- TOKENMAXX actionlint-style deepen pins after #135/#141: expand self-tests to
  2761 cases (was 2689) fail-closing live actionlint CI reliability leftovers —
  `cancel-in-progress: true` / `contents: read` / `ubuntu-latest` /
  `workflow_dispatch:` / reject `security-events|attestations|statuses|
  deployments: write` / deepen docstring + gate-contract needles —
  actionlint-style slice only (not workflow-hardening / badge / wiki /
  docs-lint / schema / common spam); no invent-product; no fourth badge.
  New draft after #141 (do **not** revive closed #139/#145/#113).

- TOKENMAXX wiki-badge posture pins after #132/#135: expand self-tests to
  2689 cases (was 2593) fail-closing live wiki badge posture — status badges
  cover Link Check+Markdown Lint / product badge refusal / reject stewardship
  workflow badge invent / reject embedded markdown badge images / PUBLISH
  Link Check+Markdown Lint exactly / Home no badge-row embeds, plus
  `check_wiki_outline_gate_contract` wiki-badge pins in `check_badge_standard.py`
  — wiki-badge slice only (not docs-lint #135 / common / run_stewardship /
  actionlint / relative / CI workflow spam); no invent-product; no fourth badge.
  Lands closed #120/#131 leftovers on post-#135 main (do not revive #131/#134).

- TOKENMAXX CI workflow third-pass pins after #111/#117/#127: expand self-tests to
  2491 cases (was 2419) fail-closing live reversible CI workflow integrity —
  exact concurrency group templates / markdown-lint+stewardship cron+timeout /
  DavidAnson@v24 / setup-python@v5 / lychee verbose+no-progress+max-concurrency 8+
  timeout 20+max-retries 3 / fail: true / get_actionlint id+outputs /
  curl -fsSL / `check_workflow_hardening_gate_contract` — CI workflow third-pass
  slice only; no invent-product; no fourth badge. New draft after #127 (do not revive #85/#124/#129).

- TOKENMAXX run_stewardship runner pins after #117: expand self-tests to
  2419 cases (was 2331) fail-closing live local runner integrity —
  `#!/usr/bin/env bash` / `set -euo pipefail` / `dirname "$0"` + `pwd` ROOT /
  `cd "$ROOT"` / same set as CI / `python3 scripts/<gate>` for four gates /
  badge→wiki→schema→relative order / Run all stewardship doc gates note, plus
  `check_run_stewardship_gate_contract` in `check_badge_standard.py` —
  run_stewardship slice only (not common/actionlint/docs-lint/wiki/badge spam);
  no invent-product; no fourth badge. Lands closed #122/#96 leftover on
  post-#117 main (do **not** revive #119).

- TOKENMAXX stewardship_common third-pass pins after #111: expand self-tests to
  2331 cases (was 2223) fail-closing live shared-helper integrity — future
  annotations / import re+Path / exact PRIVATE KEY+gh-family+sk|rk patterns /
  SECRET_PATTERNS tuple typing / FENCED_BLOCK_RE.sub / label or relative_to /
  pattern.search / lowered=text.lower / re.escape / https? URL-ish /
  ROOT.glob+found.update / set[Path] / workflows path join / scheme+pattern+hint
  loops / Shared helpers doc / hint.endswith(=) / MEMORY dumps /
  str|None+list[Path] / FORBIDDEN_BADGE_HINTS head / SECRET_URL_HINTS
  gh-family prefix members, plus `check_stewardship_common_contract`
  third-pass pins in `check_badge_standard.py` — stewardship_common third-pass
  slice only (not badge/actionlint/docs-lint/wiki/relative spam); no
  invent-product; no fourth badge. Lands open #112 leftover on post-#111 main.
- TOKENMAXX docs-lint second-pass pins after #132: expand self-tests to
  2593 cases (was 2491) fail-closing live docs-lint integrity —
  exact `.lycheeignore` exclude URLs (`https://modelcontextprotocol.io/`,
  `https://www.linuxfoundation.org/`) / Connection reset by peer + RST /
  false-positive + early hints + valid site commentary /
  `check_badge_standard.py` reference / License badge presence remains enforced /
  exact `.markdownlint.json` layout + key set + `json.loads` true/false object pins,
  plus `check_docs_lint_gate_contract` second-pass pins in
  `check_badge_standard.py` — docs-lint second-pass slice only (not actionlint /
  stewardship_common / badge / wiki / relative spam); no invent-product; no fourth badge.
  Distinct from stewardship_common (#117) and closed #116 leftover.

- TOKENMAXX actionlint-style third-pass pins after #108: expand self-tests to
  2223 cases (was 2151) fail-closing live reversible CI workflow integrity —
  `concurrency:` + `cancel-in-progress:` / `permissions:` present /
  reject `actions|packages|pull-requests: write` / `re.finditer` uses /
  docker `continue` / `rsplit("@", 1)[-1]` / third-pass docstring, plus
  `check_actionlint_style_gate_contract` third-pass pins in
  `check_badge_standard.py` — actionlint third-pass slice only (not
  badge/docs-lint/wiki/relative spam); no invent-product; no fourth badge.
  Lands closed #105/#109 leftover on post-#108 main (do not revive #85).

- TOKENMAXX badge-standard third-pass pins after #104: expand self-tests to
  2151 cases (was 2079) fail-closing live badge-standard integrity —
  `BADGE_LINE_RE`+`REPO_FROM_*` exact / `REQUIRED_WORKFLOWS` exact /
  `group(label|img|link)` / `sys.exit` / stewardship_common / `BADGE_GATE` /
  utf-8 / Strict row / H1 startswith / FAIL README / https image+link needles /
  absolute workflow URL / License point / Unexpected label /
  extract+check_badges / `contract(errors)` / IGNORECASE / `blob.lower` /
  `EXPECTED_REPO.lower` — badge-standard third-pass slice only (not docs-lint /
  wiki / relative / actionlint / schema / common / CI workflow pin spam); no
  invent-product; no fourth badge; lands closed #103 leftover on post-#104 main

- TOKENMAXX docs-lint pins after #100: expand self-tests to 2079 cases (was 1971)
  fail-closing live docs-lint integrity — `.lycheeignore` escaped
  `img\.shields\.io` / `modelcontextprotocol.io` / `linuxfoundation.org` /
  stewardship+308+103 commentary / reject `https://*`+`http://*`+`*` /
  exact MD013+MD024 objects / MD033+MD041+MD060 false / `default: true` /
  LYCHEEIGNORE+MARKDOWNLINT_CONFIG ROOT assigns / `check_workflows_and_license`
  and CDN-exclude needle / `check_docs_lint_gate_contract` — docs-lint slice
  only (not wiki / relative / actionlint / schema / badge / common / CI
  workflow pin spam); no invent-product; no fourth badge; lands closed #101
  leftover on post-#100 main

- TOKENMAXX wiki-outline third-pass pins after #90/#94: expand self-tests to 1971
  cases (was 1899) fail-closing live wiki-outline integrity — WIKI exact /
  `removesuffix` / `glob("*.md")` / `sorted(unexpected)` / Link Check+
  Markdown Lint+No secrets / Home invent+secrets+kill needles /
  Repo-Stewardship relative+invent+actionlint+run_script needles /
  `startswith("//")`+`http://` / `group(2)` / utf-8 / `sys.exit` /
  stewardship_common / invent-chrome social special-cases / shields host /
  markdown-badge open / badge-in-lowered gate / README+badge hint paths /
  pages+operator OK / intentional PUBLISH pin / `PAGE_TOPIC_HINTS.get` /
  `strip_fenced_code(text)` / `has_dangerous_scheme(target)` /
  `scan_secrets` calls, plus wiki-outline gate contract pins in
  `check_badge_standard.py` — wiki-outline third-pass slice only (not
  relative / actionlint / markdownlint+lycheeignore / schema / badge /
  common / CI workflow pin spam); no invent-product; no fourth badge

- TOKENMAXX relative-link third-pass pins after #90: expand self-tests
  to 1899 cases (was 1827) fail-closing live relative-link integrity —
  `MD_LINK_RE`+`ATX_HEADING_RE` exact / `SKIP_*` exact assigns /
  OK+FAILED banners / empty+http+protocol-relative+dangerous needles /
  utf-8 / `as_posix` / `.md` suffix / `ValueError` / `sorted` / UNICODE /
  space-to-dash slug / Percent-decode+Cap nested / empty () fail-closed /
  `sys.exit` / `urllib.unquote` / `group(2)` / `startswith#` / `split#` /
  files scanned / stewardship_common import / title attr / `#{1,6}` /
  slug punctuation / Offline+lychee docstring / `path.parent`, plus
  relative-link gate contract pins in `check_badge_standard.py` —
  relative-link third-pass slice only (not schema / badge / wiki /
  common / CI workflow / actionlint pin spam); no invent-product; no
  fourth badge

- TOKENMAXX actionlint-style second-pass pins after #83/#86: expand self-tests
  to 1827 cases (was 1755) fail-closing live actionlint-style integrity —
  exact `name:` / `uses:` regexes / write-all+contents+id-token regexes /
  `startswith("docker://")` / `"@" not in uses` / `rsplit("@", 1)` /
  `match.group(1).strip()` / fail needles / least-privilege+OIDC+majors
  comments / `REQUIRED_WORKFLOWS` loop, plus actionlint-style gate contract
  pins in `check_badge_standard.py` — actionlint-style second-pass slice only
  (not schema / badge / wiki / relative / common / CI workflow pin spam); no
  invent-product; no fourth badge

- TOKENMAXX stewardship-schema second-pass pins after #79: expand self-tests
  to 1755 cases (was 1683) fail-closing live schema integrity —
  `FENCED_YAML_RE` exact / `ISO_DATE_RE` / `SEMVER_RE` / `ISSUE_REF_RE` /
  `DATE_KEYS` exact / Tiny YAML subset / scalar+non-empty+string needles /
  ACTIVE status / positive tier / 0..3 autonomy / ISO-8601 / invent wording /
  semver / closes #N / FAILED+OK banners / stdlib-subset+PyYAML /
  bool subclass / `match.group(1)` / missing metadata keys / utf-8 /
  `STRING_KEYS` members, plus stewardship-schema gate contract pins in
  `check_badge_standard.py` — schema second-pass slice only (not badge /
  wiki / relative / common / CI workflow / actionlint pin spam); no
  invent-product; no fourth badge

- TOKENMAXX actionlint-style gate pins after #75: expand self-tests to 1683
  cases (was 1612) fail-closing live actionlint-style integrity — top-level
  `name:` / `jobs.*.runs-on` / `jobs.*.steps` / `timeout-minutes` / no
  `pull_request_target` / no `permissions: write-all` / no `contents: write` /
  no `id-token: write` / `@`-pin float set `main|master|latest` / `docker://`
  skip / unpinned reject, plus actionlint-style gate contract pins in
  `check_badge_standard.py` — actionlint-style gate contract slice only (not
  CI workflow / common / relative-link / schema-scalar / badge / wiki-outline
  / fixture-reject spam); no invent-product; no fourth badge

- TOKENMAXX stewardship_common second-pass pins after #65: expand self-tests to
  1540 cases (was 1468) fail-closing live shared-helper integrity — ROOT
  `parents[1]` / `FENCED_BLOCK_RE` DOTALL / helper doc pins / scan_secrets
  needles / `relative_to` / `strip().lower()` / `startswith` /
  `errors.append` / `password|passwd|token` / OPENSSH+EC / Public docs /
  invent-product surface / social chrome / Link schemes / `is_file`+`sorted` /
  workflows path / `return None` / exact `DANGEROUS_LINK_SCHEMES` +
  `SECRET_URL_HINTS` head, plus stewardship_common contract pins in
  `check_badge_standard.py` — common second-pass slice only (not badge /
  wiki / relative / schema / CI workflow pin / fixture-reject spam); no
  invent-product; no fourth badge

- TOKENMAXX badge-standard second-pass pins after #61: expand self-tests to 1468
  cases (was 1396) fail-closing live badge-standard integrity —
  `REQUIRED_ORDER`+`EXPECTED_REPO` exact assigns / README+LICENSE+
  badge-standard+CONTRIBUTING+AGENTS+lycheeignore+markdownlint paths /
  contract+main fns / `actions/workflows/*.yml/badge.svg` /
  exactly+order+contiguous+H1+unexpected+forbidden+secret+FAILED+OK needles /
  endswith+/./LICENSE / `load_workflow_text` / invent-product doc /
  intentionally / quiet stewardship / selftest+relative AGENTS pins /
  img https startswith / http link reject, plus badge-standard gate contract
  pins in `check_badge_standard.py` — badge-standard second-pass slice only
  (not wiki / relative / schema / common / CI workflow pin / fixture-reject
  spam); no invent-product; no fourth badge

- TOKENMAXX wiki-outline second-pass pins after #59: expand self-tests to 1396
  cases (was 1324) fail-closing live wiki-outline integrity — `OPERATOR_ONLY` /
  docs/wiki / `_reject_invent_badge_chrome` / autonomy+governance+public+kill+
  secret+surface+routing+`run_stewardship_checks.sh`+badge topic pins /
  `](Home.md)` backlink / Unexpected+Missing+FAILED needles / angle+image RE /
  Do-not-push / README blob / badge-standard hint / stars+forks+followers /
  invent-chrome needle / Home.md table row, plus wiki-outline gate contract
  pins in `check_badge_standard.py` — wiki-outline second-pass slice only
  (not relative / schema-scalar / badge-standard / common / CI workflow pin /
  fixture-reject spam); no invent-product; no fourth badge

- TOKENMAXX relative-link second-pass pins after #55: expand self-tests to 1324
  cases (was 1253) fail-closing live relative-link integrity — `MD_LINK_RE` /
  `SKIP_PARTS` / `SKIP_PREFIXES` / `SKIP_FILES` / `_MAX_UNQUOTE_PASSES = 4` /
  `should_skip` / `iter_markdown` / `headings_in` / `check_file` / mailto+tel
  allow / NUL / angle-bracket strip / image-link RE / escapes+broken+missing
  needles / rglob + no-markdown fail-closed, plus relative-link gate contract
  pins in `check_badge_standard.py` — relative-link second-pass slice only
  (not schema-scalar / badge-standard / common / wiki-outline / CI workflow
  pin / fixture-reject spam); no invent-product; no fourth badge

- TOKENMAXX stewardship-schema scalar / live pins after #53: expand self-tests
  to 1253 cases (was 1182) fail-closing live schema integrity — `STRING_KEYS` /
  `reject_non_scalar` / empty yaml metadata / bool pretending to be
  autonomy_level or tier ints, plus live EXPECTED_VALUES for badge
  `scope` / `closes #16` and PUBLISH `purpose` / `closes #16`, plus
  stewardship-schema gate contract pins in `check_badge_standard.py` —
  schema gate scalar / live-pin slice only (not badge-standard / common /
  wiki-outline / relative-link / CI workflow pin / fixture-reject spam); no
  invent-product; no fourth badge

- TOKENMAXX badge-standard gate pins after #48: expand self-tests to 1182
  cases (was 1114) fail-closing live badge-standard integrity — REQUIRED_ORDER
  Link Check → Markdown Lint → License / MAX_BADGES = 3 / EXPECTED_REPO /
  REQUIRED_WORKFLOWS / badge.svg + shields license / contiguous row /
  invent-product / fourth-badge refusal / Stewardship product badge reject,
  plus badge-standard gate contract pins in `check_badge_standard.py` —
  badge-standard gate contract slice only (not common / schema / wiki-outline /
  relative-link / CI workflow pin / fixture-reject spam); no invent-product;
  no fourth badge

- TOKENMAXX stewardship_common gate pins after #46: expand self-tests to 1114
  cases (was 1045) fail-closing live shared-helper integrity — SECRET_PATTERNS /
  SECRET_URL_HINTS / FORBIDDEN_BADGE_HINTS / DANGEROUS_LINK_SCHEMES /
  `strip_fenced_code` / `scan_secrets` / invent-product wording, plus
  stewardship_common contract pins in `check_badge_standard.py` — common helper
  contract slice only (not schema / wiki-outline / relative-link / CI workflow
  pin / fixture-reject spam); no invent-product; no fourth badge

- TOKENMAXX stewardship-schema gate pins after #45: expand self-tests to 1045
  cases (was 974) fail-closing live schema integrity — DOC_SCHEMAS /
  EXPECTED_VALUES / SEMVER / ISO-8601 / closes `#N` / invent edit_policy /
  issue-backlog owner `copilot` / `scan_secrets`, plus stewardship-schema gate
  contract pins in `check_badge_standard.py` — schema gate contract slice only
  (not wiki-outline / relative-link / CI workflow pin / fixture-reject spam);
  no invent-product; no fourth badge

- TOKENMAXX wiki-outline gate pins after #43: expand self-tests to 974 cases
  (was 903) fail-closing live wiki outline integrity — PUBLISHABLE_PAGES
  L0–L3 / credential / copilot topic hints, `strip_fenced_code` before link
  scan, protocol-relative `//` reject, Home kill-switch callout, plus
  wiki-outline gate contract pins in `check_badge_standard.py` — wiki-outline
  gate contract slice only (not relative-link / CI workflow pin /
  badge-wiki-schema fixture-reject spam); no invent-product; no fourth badge

- TOKENMAXX relative-link gate pins after #41: expand self-tests to 903 cases
  (was 836) fail-closing live relative-link integrity — `OWASP-AGENTIC.md` /
  `.github/agents` / `node_modules` / `.git` skips, `strip_fenced_code`,
  `fully_unquote` nested percent-decode, empty `path#` fragments, query-string
  reject on relative targets, protocol-relative / http:// / dangerous-scheme
  still-needles, `run_stewardship_checks.sh` invokes badge→wiki→schema→relative
  in order, AGENTS.md relative mention — relative-link gate contract slice
  only (not CI workflow pin / badge-wiki-schema fixture-reject spam); no
  invent-product; no fourth badge

- TOKENMAXX CI workflow pins after #39: expand self-tests to 836 cases
  (was 774) fail-closing live `actions/checkout@v7` on all three workflows,
  `lycheeverse/lychee-action@v2`, job `timeout-minutes` 20/10/15, weekly
  crons `0 6` / `30 6` / `15 6`, `ubuntu-latest`, stewardship `pip --quiet`
  and `shell: bash` and actionlint `-color`, plus actionlint float/unpinned/
  write-all/contents:write/pull_request_target edges, workflow cancel/
  schedule/dispatch/concurrency/permissions, link-check fail/loopback/
  github-token/token/concurrency/timeout/retries, markdown-lint cli2@v24/
  DavidAnson/config/OWASP/agents excludes, markdownlint MD033/MD041/MD060/
  line_length:200/default:true still, stewardship setup-python@v5 /
  get_actionlint id+outputs /v1.7.7/ / 3.12 / rhysd / curl -fsSL /
  raw.githubusercontent still, lycheeignore https://*/http://*/shields
  still — CI workflow pin slice only (not badge/wiki/schema/relative
  fixture-reject spam); no invent-product; no fourth badge

- TOKENMAXX stewardship fixtures after #38: expand self-tests to 774 cases
  (was 712) covering `.markdownlint.json` `MD033`/`MD041`/`MD060`: false,
  markdownlint-cli2-action `@v24`, stewardship `actions/setup-python@v5` +
  `id: get_actionlint`, pull_request_target on markdown-lint, contents:write/
  write-all on link-check/stewardship, checkout@main float, cancel-in-
  progress:false on stewardship, missing schedule/workflow_dispatch, badge
  coverage/stars/discord/npm/token/http-image/four-badge/three-max, relative
  HtTpS/Javascript/Data / hash slug / parent broken / angle MailTo / empty
  parens / protocol-relative, wiki Home→Routing / coveralls/producthunt/npm/
  pypi chrome / DATA: / PUBLISH Security-Boundaries / actionlint+relative
  still, schema empty edit_policy/maintainer/created / missing parent+
  autonomy / DRAFT badge / autonomy 2 / wrong CLAUDE parent / closes without
  #, common ghs_/ghu_/rk-/aws / coverage+stars hints / ghs scan / FILE:
  casefold, plus default:true / max-concurrency 8 /v1.7.7/ /
  get_actionlint.outputs / codecov/http / tier 0 still-needles

- TOKENMAXX stewardship fixtures after #37: expand self-tests to 712 cases
  (was 650) covering `.markdownlint.json` `default: true`, stewardship
  `get_actionlint.outputs.executable` + actionlint download path `/v1.7.7/`,
  lychee `--max-concurrency 8` / `--timeout 20` / `--max-retries 3`,
  pull_request_target on stewardship, contents:write/write-all on markdown-
  lint/link-check, checkout@latest float, cancel-in-progress:false on
  link-check, missing concurrency/timeout, badge codecov/downloads/
  followers/pypi/apikey/http-image/four-badge/fourth-refusal still, relative
  HTTPS/VbScript/File / ampersand slug / sibling broken / angle tel / bare
  `#` / nested %2e escape, wiki Home→Overview / discord/twitter/stars/forks
  chrome / JAVASCRIPT / PUBLISH Autonomy-Levels / CI+badge topic still, schema
  empty scope / missing maintainer+repo / empty closes / DRAFT publish /
  autonomy -1 / wrong scope / semver prerelease, common github_pat_/xoxb-/RSA
  key / buymeacoffee+opencollective hints / xoxb scan / vbscript casefold,
  plus DavidAnson/--github-token/line_length:200/raw.githubusercontent/
  coveralls/http / tier 0 still-needles

- TOKENMAXX stewardship fixtures after #36: expand self-tests to 650 cases
  (was 588) covering `.markdownlint.json` MD013 `line_length: 200` + MD024
  `siblings_only: true`, stewardship `raw.githubusercontent.com` + curl `-fsSL`,
  pull_request_target on markdown-lint, contents:write/write-all on link-check/
  stewardship, checkout@main float, cancel-in-progress:false on stewardship,
  missing schedule/workflow_dispatch, badge coverage/stars/discord/npm/token/
  http-image/four-badge/three-max, relative HtTpS/Javascript/Data / hash slug /
  parent broken / angle MailTo / empty parens / protocol-relative, wiki
  Home→Routing / coveralls/producthunt/npm/pypi chrome / DATA: / PUBLISH
  Security-Boundaries / actionlint+relative still, schema empty edit_policy/
  maintainer/created / missing parent+autonomy / DRAFT badge / autonomy 2 /
  wrong CLAUDE parent / closes without #, common ghs_/ghu_/rk-/aws /
  coverage+stars hints / ghs scan / FILE: casefold, plus cli2/lycheeverse/
  siblings_only/rhysd/twitter/http / tier 0 / data: still-needles

- TOKENMAXX stewardship fixtures after #35: expand self-tests to 588 cases
  (was 526) covering `.markdownlint.json` MD024 `siblings_only`, stewardship
  `rhysd/actionlint` + `curl` download, lychee-action `with: token:`,
  pull_request_target on link-check, contents:write/write-all on stewardship/
  link-check, checkout@latest float, cancel-in-progress:false on markdown-lint,
  missing concurrency/timeout, badge buymeacoffee/opencollective/coveralls/
  x.com/client_secret/http-image/four-badge/fourth-refusal still, relative
  Mailto/VbScript/FILE / underscore slug / sibling broken / angle tel / bare
  `#` / nested %2e escape, wiki Home→Overview / discord/twitter/stars/forks
  chrome / JAVASCRIPT / PUBLISH Autonomy-Levels / CI+badge topic still, schema
  empty scope/owner/closes / missing maintainer+repo / DRAFT publish / autonomy
  -1 / wrong scope / semver prerelease, common github_pat_/xoxb-/RSA key /
  buymeacoffee+opencollective hints / xoxb scan / vbscript casefold, plus
  DavidAnson/--github-token/MD024/download-actionlint/producthunt/http /
  tier 0 / javascript / https://* lycheeignore still-needles

- TOKENMAXX stewardship fixtures after #34: expand self-tests to 526 cases
  (was 464) covering `DavidAnson/markdownlint-cli2-action`, lychee
  `--github-token`, `.markdownlint.json` MD024, stewardship
  `download-actionlint.bash`, pull_request_target on stewardship,
  contents:write/write-all on markdown-lint, checkout@main float,
  cancel-in-progress:false on link-check, missing schedule/workflow_dispatch,
  badge followers/forks/npm/pypi/apikey/http-image/blank-row/three-max still,
  relative TEL/JavaScript/DATA / asterisk slug / nested broken / angle https /
  empty parens / %2e traversal, wiki Home→Security / buymeacoffee/opencollective/
  codecov/downloads chrome / FILE: / PUBLISH Overview / actionlint+invent still,
  schema empty owner/scope/purpose / missing version+surface / DRAFT status /
  autonomy 4 / wrong CLAUDE repo / closes without #, common ghr_/gho_/sk-/EC key /
  followers+forks hints / AIza scan / JAVASCRIPT casefold, plus cli2/lycheeverse/
  line_length/pip/twitter/Http:// / data: / tier 0 / data: still-needles

- TOKENMAXX stewardship fixtures after #33: expand self-tests to 464 cases
  (was 404) covering `lycheeverse/lychee-action`, `markdownlint-cli2-action`,
  `.markdownlint.json` MD013 `line_length`, stewardship `pip install` PyYAML,
  pull_request_target on markdown-lint, contents:write/write-all on link-check,
  checkout@latest float, cancel-in-progress:false on stewardship, missing
  concurrency/timeout needles, badge coverage/stars/token/http-license/four-badge
  and fourth-refusal still, relative HTTPS/MAILTO uppercase / File: / tilde slug /
  parent missing / angle mailto / protocol-relative, wiki Home→Repo-Stewardship /
  coveralls/producthunt/npm/pypi chrome / HTTP:// / vbscript / PUBLISH
  stewardship row / relative hint still, schema empty closes/version /
  missing autonomy+parent / empty last_updated / whitespace scope / tier -1 /
  wrong maintainer, common ghs_/ghu_/rk-/aws/OPENSSH / coveralls+producthunt
  hints / npm scan / FILE: casefold, plus lychee-action/MD013/checkout/PyYAML/
  discord/HTTP:// / javascript / tier 0 / VBSCRIPT still-needles

- TOKENMAXX stewardship fixtures after #32: expand self-tests to 404 cases
  (was 345) covering link-check/markdown-lint `actions/checkout`, `lychee-action`,
  `.markdownlint.json` MD013, pull_request_target on link-check, contents:write on
  markdown-lint, write-all on stewardship, cancel-in-progress:false reject, badge
  twitter/codecov/downloads/github_pat/ghp/producthunt + Markdown-Lint-first order +
  missing AGENTS.md + three-badges-max doc still, relative JavaScript/DATA mixed-case /
  tel+title / colon slug / nested image / LICENSE from docs / HTTP:// casefold, wiki
  Home→Overview / discord+buymeacoffee+opencollective chrome / javascript: / PUBLISH
  Autonomy+Security+Routing rows / actionlint+data still, schema empty edit_policy/
  CLAUDE owner / missing version+edit_policy+last_updated / tier 0 / empty created /
  autonomy 3 vs expected 1, common npm_/AIza/xoxb/github_pat/twitter+codecov hints +
  javascript+data schemes, plus verbose/no-progress/checkout/config/lycheeignore still

- TOKENMAXX stewardship fixtures after #31: expand self-tests to 345 cases
  (was 289) covering lychee `--verbose` / `--no-progress`, stewardship
  `actions/checkout`, cancel-in-progress:true on markdown-lint, pull_request_target
  / unpinned setup-python, badge coveralls/buymeacoffee/opencollective/npm/pypi/
  followers/x.com/forks + apikey/client_secret/gho_ + wrong license slug +
  missing stewardship workflow + badge-doc License label, relative .git skip /
  VBSCRIPT / nested %2e escape / underscore slug / docs nested fragment, wiki
  L0/secret/surface/governance/public / Home→Autonomy / followers+x.com chrome /
  PUBLISH Home row / file: / run_stewardship_checks.sh, schema CLAUDE surface+
  repo keys / backlog owner / empty purpose+scope / autonomy 0 / publish closes /
  closes without #, common hint registry + gho_ / apikey scan, plus markdown
  **/*.md / exclude-loopback / Python 3.12 / stewardship schedule still-needles

- TOKENMAXX stewardship fixtures after #30: expand self-tests to 289 cases
  (was 233) covering stewardship Python `3.12` / `python-version` pin,
  cancel-in-progress:true on link-check, setup-python @master/@latest float,
  stewardship contents:write / timeout / markdown-lint dispatch, lycheeignore
  bare `*`, link-check `**/*.md` not txt, badge discord/producthunt/api_key/
  access_token/http-license/license-first/stars + badge-doc snippets + missing
  link-check workflow, relative node_modules skip / uppercase schemes / nested
  escape / numbered slug / mailto+https / parent relative, wiki Home invent+
  secrets / L1 / kill / downloads / Security link / PUBLISH Overview / data:
  / badge topic / twitter, schema CLAUDE owner/autonomy / backlog DRAFT /
  empty scope / missing closes/purpose / autonomy drift+float / semver
  prerelease, common commerce hints / sk- / casefold / token= / file:, plus
  markdown-lint OWASP + stewardship timeout + write-all needles

- TOKENMAXX stewardship fixtures after #29: expand self-tests to 233 cases
  (was 182) covering `cancel-in-progress: true`, link-check `.github/agents`
  exclude, markdown-lint `**/*.md` glob, lycheeignore `http://*`, actionlint
  markdown-lint path + unpinned/float setup-python, schedule/concurrency/
  permissions edges, relative/absolute badge link + ./LICENSE + coverage/
  token= + four-badge + badge-doc label/shields, relative angle-bracket/
  nested/image-title/percent-escape/slug backticks, wiki actionlint/autonomy/
  routing/out-of-scope/forks/codecov/home-routing/PUBLISH secret/table,
  schema badge status/tier/closes/empty/tier-string/autonomy-range/non-
  mapping/date, extended common secret-url/forbidden/private-key/tilde/
  ghp helpers, fail:true + PyYAML needles

- TOKENMAXX stewardship fixtures after #28: expand self-tests to 182 cases
  (was 134) covering cancel-in-progress / `**/*.md` link-check glob, actionlint
  timeout + docker:// pin skip, badge-standard/CONTRIBUTING missing-file,
  license image path/slug, README secret, AGENTS workflow needles, badge-doc
  invent/three-max/fourth-refusal, lycheeignore `https://*`, relative
  angle-bracket/LICENSE/ampersand-slug/whitespace, wiki PUBLISH Link
  Check/Markdown Lint/secrets + Overview/Security topics + stars chrome +
  missing wiki dir, schema scope/parent/repo/publish/backlog/autonomy-string/
  date/YAML parse, extended secret/forbidden-hint helpers, markdown-lint
  config + actionlint path needles, stewardship workflow_dispatch

- TOKENMAXX stewardship fixtures after #27: expand self-tests to 134 cases
  (was 89) covering actionlint write-all/@master/@latest/name/steps, link-check
  GITHUB_TOKEN / lychee / exclude-path / concurrency / timeout needles,
  markdown-lint OWASP/agents excludes, stewardship actionlint 1.7.7 + all three
  workflow path targets, lycheeignore literal/regex positives, relative
  tel/NUL/bare-hash/title/image, wiki PUBLISH/badge/home/relative/invent edges,
  schema maintainer/parent/owner/secret negatives

- TOKENMAXX stewardship fixtures after #26: expand self-tests to 89 cases
  (was 50) covering lycheeignore shields exclude, actionlint-style workflow
  harden (no pull_request_target / contents:write / unpinned@main), markdown-
  link empty/file/vbscript/mailto/agents-skip/image/slug fixtures, wiki/schema
  positive + missing-page/yaml/file negatives
- Stewardship Checks CI: run pinned actionlint v1.7.7 on the three existing
  workflow paths (link-check / markdown-lint / stewardship-checks)

- TOKENMAXX stewardship gate burn after #24: 50 negative/positive self-test
  fixtures (was 14) covering http badges, dangerous link schemes, percent-
  encoded path escape, tilde fences, wiki invent chrome / http / secrets,
  schema semver / closes / empty values, workflow_dispatch / fail:true /
  schedule / concurrency / PyYAML wiring
- Stewardship gate hardening after #23: expanded negative self-tests, workflow
  `timeout-minutes` / `workflow_dispatch` / markdown-lint weekly schedule, lychee
  `--max-retries`, fenced-code-aware relative links, schema date/surface/tier
  constraints, CONTRIBUTING + AGENTS self-test callouts
- `docs/badge-standard.md` — required README badge row for public governance repos
  (Link Check, Markdown Lint, License)
- `docs/wiki/` — public wiki outline (Home, Overview, Autonomy Levels, Repo
  Stewardship, Agent Routing, Security Boundaries) plus `PUBLISH.md` path to
  GitHub Wiki (#16)
- README Documents table links to badge standard and wiki Home
- `scripts/check_badge_standard.py`, `scripts/check_wiki_outline.py`,
  `scripts/check_stewardship_schema.py`, `scripts/run_stewardship_checks.sh` —
  executable gates for badge/wiki/schema stewardship standards
- `.github/workflows/stewardship-checks.yml` — CI job for stewardship scripts
- `scripts/check_relative_links.py` — offline relative markdown link + heading
  fragment integrity (complements lychee)
- `scripts/stewardship_common.py` — shared secret-pattern helpers for public docs
- `scripts/test_stewardship_gates.py` — negative/positive self-tests for gates

### Changed

- Badge/stewardship gates after #30: require stewardship-checks Python
  `python-version` + `3.12` pin; wiki Home must retain invent-product **and**
  secrets out-of-scope wording (not either/or)
- Badge/stewardship gates after #29: require concurrency `cancel-in-progress: true`
  (value, not just key); link-check exclude-path must target `.github/agents`;
  markdown-lint must scan `**/*.md`; lycheeignore rejects `http://*` as well as
  `https://*`; Repo-Stewardship must call out actionlint
- Badge/stewardship gates after #28: require concurrency `cancel-in-progress` on
  all three workflows; link-check must scan `**/*.md`; badge-standard doc that
  mentions stewardship-checks must refuse a fourth badge explicitly
- Badge/stewardship gates after #27: require link-check `GITHUB_TOKEN`, stewardship
  actionlint pin `1.7.7`, and actionlint targets for all three existing workflow
  filenames (link-check / markdown-lint / stewardship-checks)
- Badge/stewardship gates: require `.lycheeignore` + shields CDN exclude (after
  #26), `.markdownlint.json` present, actionlint needle in stewardship-checks,
  link-check paths filter references `.lycheeignore`
- Relative links: catch empty `()` targets (markdown-link fail-closed)
- Link Check: exclude `img.shields.io` in `.lycheeignore` so transient badge
  CDN RST / Connection-reset blips do not fail the gate; keep lychee `fail: true`
  for real broken doc links (after #25 flake)
- Badge workflow hardening: require `workflow_dispatch` + weekly `schedule` on
  all three CI workflows; lychee `fail: true` + `--exclude-loopback`;
  markdown-lint `.markdownlint.json` + `.github/agents` exclusion; stewardship
  setup-python + PyYAML install needles
- Relative links: reject `javascript:` / `data:` / `vbscript:` / `file:`,
  insecure `http://`, protocol-relative `//`, percent-encoded `..` escapes;
  strip `~~~` fences as well as ` ``` `
- Wiki outline: reject invent-product badge chrome, insecure http, dangerous
  schemes on publishable pages
- Schema: AGENTS semver, `closes` issue refs, non-empty required metadata
- README: private `claw-mcp` listed without a public URL (avoids Link Check 404)
- `.markdownlint.json`: disable MD060 (false positives on compact tables after
  markdownlint v0.41)
- Markdown Lint workflow: exclude long-form `OWASP-AGENTIC.md` from lint globs
- Markdown Lint + Link Check: always run on pull_request; push path filters also
  cover config/workflow files
- `AGENTS.md` §3 Testing Requirements: document markdownlint-cli2, lychee, and
  stewardship scripts (replace stale npx link-check notes)
- Strengthened stewardship gates: README↔badge-standard consistency, repo slug
  checks, wiki CI callouts, metadata value constraints, secret URL hints
- Link Check: concurrency group, `--max-concurrency 8`, `--timeout 20`,
  `--max-retries 3`, exclude `.github/agents`; job `timeout-minutes` +
  `workflow_dispatch`
- Stewardship Checks: run via `run_stewardship_checks.sh`, weekly schedule,
  self-tests step; job `timeout-minutes` + `workflow_dispatch`
- Markdown Lint: concurrency group, weekly schedule, `timeout-minutes`,
  `workflow_dispatch`
- README / CONTRIBUTING / wiki Repo-Stewardship: document local stewardship
  runner + self-tests

---

## [2.3.0] — 2026-04-19

### Added

- AGENTS-ECOSYSTEM.md §2.1 expanded to full 23-repo, 4-tier portfolio
  (Tier A Active, Tier B Governance, Tier C Infrastructure, Tier D Dormant)
  plus a Tier Summary
- AGENTS-ECOSYSTEM.md §2.1.1: reference to `fuzzywigg/project-template` as the
  canonical AGENTS.md v1.0 template (4 execution modes, implementation-plan
  requirement, agent routing convention, Tier-1/Tier-2 governance structure,
  7 flavor branches)
- Appendix B: Caveman context compression — optional
  `project-template/scripts/compress-context.py` for ~40% governance-file
  token reduction
- README.md: ecosystem snapshot table, project-template usage flow,
  compression note

### Changed

- AGENTS-ECOSYSTEM.md front matter: version bumped to 2.3.0, `last_updated`
  2026-04-19, added `ecosystem_size` and `template_source` keys
- Domain Portfolio table extended to include `meromhouse.org`, `g0p.us`,
  `g0p.ai` with tier annotations
- README.md version stamp bumped to 2.3.0

---

## [Pre-2.3.0 Unreleased]

### Added

- `CLAUDE.md` — Copilot surface rules and critical file registry
- `AGENTS.md` — Repo-specific governance instance (using own template)
- `LICENSE` — MIT license file (previously only stated in README)
- `CONTRIBUTING.md` — Contribution guidelines and approval matrix
- `SECURITY.md` — Vulnerability reporting and severity levels
- `scratchpad/ecosystem.txt` — Ecosystem-wide inter-agent coordination state
- `scratchpad/incidents.txt` — Active incident log
- `docs/agent-hydration.md` — Full hydration findings report
- `.github/ISSUE_TEMPLATE/` — Issue templates (governance-gap, documentation-error, feature-request)
- `.github/pull_request_template.md` — Standardized PR template
- `.github/CODEOWNERS` — Code ownership for protected files
- `.github/workflows/markdown-lint.yml` — CI: markdownlint on all .md files
- `.github/workflows/link-check.yml` — CI: weekly + PR broken link detection
- `.markdownlint.json` — Lint configuration (line-length relaxed, HTML allowed)

---

## [2.2.0] — 2025-12-13

### Added

- Enhanced Section 6: Multi-Agent Coordination (Goose Protocol)
- Ecosystem-wide architecture diagram
- MCP Server Registry table
- Scratchpad hierarchy documentation
- Cross-project coordination protocol
- Recipe governance rules
- Audit requirements for Goose
- Appendix A: Goose Protocol Resources
- Appendix B: Quick Commands

---

## [2.1.0] — 2025-12-13

### Added

- Initial ecosystem governance document (`AGENTS-ECOSYSTEM.md`)
- Repository-specific template (`templates/AGENTS-REPO.md`)
- README with usage documentation

---

## [2.0.0] — 2025-12-13

### Changed

- Separated ecosystem governance from repo-specific AGENTS.md
