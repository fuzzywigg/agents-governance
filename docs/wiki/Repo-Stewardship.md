# Repo Stewardship

[← Home](Home.md)

How public governance repos in this ecosystem are kept trustworthy without
exposing private project machinery.

## Front-door duties

- Keep [README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md) accurate: purpose, document map, badge row.
- Follow the [badge standard](../badge-standard.md).
- Prefer reversible docs/stewardship PRs; no invent-product work.
- Never delete scratchpad history; append and mark `[x]` when done.

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
