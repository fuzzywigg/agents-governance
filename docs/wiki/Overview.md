# Overview

[← Home](Home.md)

## What this repository is

`agents-governance` is the **public source of truth** for AI agent governance across the smtp.eth / fuzzywigg ecosystem. Downstream repos point here via:

```yaml
parent_governance: "github.com/fuzzywigg/agents-governance"
```

## What this repository is not

- Not an application runtime or agent framework to install
- Not a substitute for each project's own `AGENTS.md`
- Not a place to publish private templates, credentials, or MEMORY

## Public operating model (short)

1. **Policy** lives in [AGENTS-ECOSYSTEM.md](https://github.com/fuzzywigg/agents-governance/blob/main/AGENTS-ECOSYSTEM.md).
2. **Per-repo rules** live in that repo's `AGENTS.md` / `CLAUDE.md`.
3. **Coordination state** uses append-only `scratchpad/` files (no history deletes).
4. **Human authority** is absolute: kill switch, approval tiers, and structural amend process.

## Documents map

| Document | Role |
|----------|------|
| README | Public front door + badges |
| AGENTS-ECOSYSTEM.md | Ecosystem-wide governance (Andrew approval to change) |
| templates/AGENTS-REPO.md | Legacy template (historical; Andrew approval to change) |
| docs/ | Agent-editable stewardship docs (this wiki source, badge standard, etc.) |

See the [README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md) for install/usage pointers and the live ecosystem snapshot.

[← Home](Home.md) · [Autonomy Levels →](Autonomy-Levels.md)
