# AGENTS.md — agents-governance

```yaml
version: "1.0.0"
last_updated: "2026-04-13"
maintainer: "smtp.eth"
scope: "repository-specific"
parent_governance: "github.com/fuzzywigg/agents-governance"
autonomy_level: 1
```

> **This document governs AI agent behavior within the agents-governance repository.**
> For ecosystem-wide governance, see [AGENTS-ECOSYSTEM.md](./AGENTS-ECOSYSTEM.md).

---

## 1. Quick Reference

### Critical Files

| File | Purpose | Edit Restrictions |
|------|---------|-------------------|
| `AGENTS-ECOSYSTEM.md` | Ecosystem-wide policy | Andrew approval required |
| `templates/AGENTS-REPO.md` | Per-project template | Andrew approval required |
| `AGENTS.md` | This file | Agent-editable |
| `CLAUDE.md` | Copilot surface rules | Agent-editable |
| `scratchpad/ecosystem.txt` | Cross-project state | Append-only |
| `scratchpad/incidents.txt` | Active incidents | Append-only |

### Autonomy Level

This project operates at **Level 1** autonomy (Bounded):
- [x] L1 Bounded: Auto-approve within policy
- [ ] L0 Advisory: Human confirms every action
- [ ] L2 Supervised: Auto-approve within policy + budget

---

## 2. Project-Specific Rules

### 2.1 Governance Document Integrity

`AGENTS-ECOSYSTEM.md` and `templates/AGENTS-REPO.md` are the canonical governance artifacts. No agent may modify these without an explicit Andrew-approved PR. Rationale: downstream projects depend on these documents as their source of truth.

### 2.2 Scratchpad Protocol

The `scratchpad/` directory implements ecosystem-wide inter-agent coordination state per [AGENTS-ECOSYSTEM.md §6.3](./AGENTS-ECOSYSTEM.md).

Rules:
- **APPEND-ONLY** — never delete or rewrite entries
- Mark completed steps with `[x]`
- Add timestamps in ISO-8601 format
- Tag blocked items with `← BLOCKED (reason)`

### 2.3 Issue and PR Conventions

All issues must follow the title format: `[agent-surface] Descriptive title`

All PRs must reference the issue they address and follow the PR template.

### 2.4 Kill Switch

If `.kill_switch` exists at repo root, all agent writes are blocked until smtp.eth removes it manually.

---

## 3. Testing Requirements

This is a documentation-only repository. There is no application code to test.

```bash
# Lint markdown (when markdownlint-cli is installed)
npx markdownlint-cli "**/*.md" --ignore node_modules

# Check for broken links (when markdown-link-check is installed)
npx markdown-link-check README.md AGENTS-ECOSYSTEM.md
```

---

## 4. Deployment

This repository is not deployed. It is referenced by downstream repos via:
```yaml
parent_governance: "github.com/fuzzywigg/agents-governance"
```

---

## 5. Incident Response

Follow ecosystem incident protocol from [AGENTS-ECOSYSTEM.md §10.4](./AGENTS-ECOSYSTEM.md).

Severity levels:
- SEV-1: Governance document corrupted or deleted
- SEV-2: Scratchpad state lost
- SEV-3: Broken links or template errors
- SEV-4: Documentation quality issues

---

## 6. Amendment Process

1. Create branch: `amendment/description`
2. Edit target file
3. Submit PR with rationale
4. smtp.eth approval required for `AGENTS-ECOSYSTEM.md` and `templates/`
5. Agent-editable files (AGENTS.md, CLAUDE.md, docs/, scratchpad/) may be merged by copilot surface after review

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial AGENTS.md created during repo hydration |

---

**End of Document**

*See [AGENTS-ECOSYSTEM.md](./AGENTS-ECOSYSTEM.md) for ecosystem-wide rules.*
