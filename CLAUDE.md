# CLAUDE.md — agents-governance

```yaml
repo: agents-governance
owner: fuzzywigg (smtp.eth)
surface: copilot
autonomy_level: 1
last_updated: "2026-04-13"
parent_governance: "github.com/fuzzywigg/agents-governance/AGENTS-ECOSYSTEM.md"
```

## Purpose

This is the **canonical governance repository** for the smtp.eth AI ecosystem. It contains:

- `AGENTS-ECOSYSTEM.md` — Ecosystem-wide governance (source of truth)
- `templates/AGENTS-REPO.md` — Template for per-project AGENTS.md files
- `AGENTS.md` — This repo's own governance instance
- `scratchpad/` — Ecosystem-wide inter-agent coordination state

## Agent Operating Rules (This Repo)

### What agents may do autonomously (L1 Bounded)

- Edit `AGENTS.md`, `CLAUDE.md`, `README.md`, and files in `docs/` and `scratchpad/`
- Create or update `.github/ISSUE_TEMPLATE/` and `.github/pull_request_template.md`
- Append to `scratchpad/ecosystem.txt` and `scratchpad/incidents.txt`
- Create new issues and PRs

### What requires Andrew approval (structural changes)

- Any change to `AGENTS-ECOSYSTEM.md`
- Any change to `templates/AGENTS-REPO.md`
- Adding or removing files at repo root
- Merging own PRs
- Changing branch protection rules

### Kill Switch

If `.kill_switch` exists in repo root, ALL agent writes are blocked.

```bash
# Check
ls -la .kill_switch 2>/dev/null && echo "ACTIVE" || echo "inactive"
```

## Critical Files

| File | Purpose | Edit Restrictions |
|------|---------|-------------------|
| `AGENTS-ECOSYSTEM.md` | Ecosystem-wide governance | Andrew approval required |
| `templates/AGENTS-REPO.md` | Per-project AGENTS.md template | Andrew approval required |
| `AGENTS.md` | This repo's governance | Agent-editable |
| `CLAUDE.md` | This file | Agent-editable |
| `scratchpad/ecosystem.txt` | Cross-project task state | Append-only |
| `scratchpad/incidents.txt` | Active incidents | Append-only |

## Routing Matrix

| Task | Surface | Notes |
|------|---------|-------|
| Single-file edits, CI fixes, doc updates | copilot | Default surface |
| Multi-file structural changes | geryon | Long-running |
| Notion sync, cross-platform coordination | claude-cowork | Policy truth |
| GitHub Settings UI | browser-claude | Repo settings |
| E2E verification | playwright | Automated QA |

## Conventions

- Branch naming: `amendment/description` for governance changes, `copilot/description` for agent work
- Issue title format: `[agent-surface] Descriptive title`
- Scratchpad updates: append-only, mark complete with `[x]`, never delete entries
- All changes on a working branch — never commit to `main`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial CLAUDE.md created during repo hydration |
