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
plus stewardship-schema second-pass after #72: `FENCED_YAML_RE`
MULTILINE|DOTALL / ISO+SEMVER+ISSUE regexes / `DATE_KEYS` exact /
`STRING_KEYS` frozenset / parse_simple_yaml null~+bool+int /
unsupported+empty-key / no-fenced / scalar+non-empty+string msgs /
ACTIVE `docs/` / autonomy 0..3 + `tier < 1` / ISO-8601 date-prefixed /
invent edit_policy / semver X.Y.Z / closes #N / FAILED+OK banners /
`sys.path`+ImportError / ROOT/fail/scan_secrets import / badge+PUBLISH
closes pair / PyYAML|stdlib-subset).
A fourth “Stewardship Checks” badge is intentionally **not** added — quiet
stewardship stays in CI/docs, not as invent-product chrome.
Flaky `img.shields.io` hosts stay out of lychee via `.lycheeignore`; license
badge presence remains stewardship-enforced.

## Related

- Public wiki outline: [wiki/Home.md](./wiki/Home.md)
- Wiki publish path: [wiki/PUBLISH.md](./wiki/PUBLISH.md)
- Testing commands: [AGENTS.md §3](../AGENTS.md#3-testing-requirements)
