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
`//` reject, Home kill-switch callout).
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
