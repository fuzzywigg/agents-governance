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
Negative fixtures live in `scripts/test_stewardship_gates.py` (CI fail-closed).
A fourth “Stewardship Checks” badge is intentionally **not** added — quiet
stewardship stays in CI/docs, not as invent-product chrome.

## Related

- Public wiki outline: [wiki/Home.md](./wiki/Home.md)
- Wiki publish path: [wiki/PUBLISH.md](./wiki/PUBLISH.md)
- Testing commands: [AGENTS.md §3](../AGENTS.md#3-testing-requirements)
