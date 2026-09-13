# Changelog

All notable changes to the agents-governance framework are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

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
