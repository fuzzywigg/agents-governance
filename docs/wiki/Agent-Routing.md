# Agent Routing

[← Home](Home.md)

Public routing matrix for work against this repository. Surfaces are **labels /
operators**, not installable frameworks.

## Routing matrix

| Task | Surface | Notes |
|------|---------|-------|
| Single-file edits, CI fixes, doc updates | copilot | Default surface |
| Multi-file structural changes | geryon | Long-running |
| Notion sync, cross-platform coordination | claude-cowork | Policy truth elsewhere |
| GitHub Settings UI | browser-claude / human | Repo settings |
| E2E verification | playwright | Automated QA |

## Conventions

- Branch naming: `amendment/…` for governance amendments, `docs/…` or agent-surface prefixes for stewardship work.
- Issue label prefixes such as `agent:copilot` help the right surface pick up work.
- Label `docs:wiki` / `docs:readme` mark documentation surfaces; they do not grant extra autonomy.

## What not to route here

- Private template implementation (`project-template` internals)
- Application feature work belonging in Tier A product repos
- Secret rotation or credential storage

Canonical detail: [CLAUDE.md](https://github.com/fuzzywigg/agents-governance/blob/main/CLAUDE.md) and
[AGENTS-ECOSYSTEM.md](https://github.com/fuzzywigg/agents-governance/blob/main/AGENTS-ECOSYSTEM.md).

[← Repo Stewardship](Repo-Stewardship.md) · [Security Boundaries →](Security-Boundaries.md)
