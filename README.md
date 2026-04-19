# agents-governance

**Canonical AI governance documents for the smtp.eth ecosystem.**

This repository contains the source-of-truth governance framework for all AI agents operating across smtp.eth's **22 repositories + 1 gist** of personal digital sovereignty infrastructure.

## Documents

| Document | Purpose |
|----------|---------|
| [AGENTS-ECOSYSTEM.md](AGENTS-ECOSYSTEM.md) | Ecosystem-wide governance: identity, trust, finances, multi-user, compliance, full repo tier map |
| [templates/AGENTS-REPO.md](templates/AGENTS-REPO.md) | Legacy per-project template (kept for historical reference) |
| [`fuzzywigg/project-template`](https://github.com/fuzzywigg/project-template) | **Canonical AGENTS.md template (v1.0)** + 7 flavor branches — recommended starting point for new repos |

## Usage

### For New Projects (Recommended)

1. Clone or fork [`fuzzywigg/project-template`](https://github.com/fuzzywigg/project-template)
2. Choose the appropriate flavor branch for your stack (Python, Next.js, Cloudflare Worker, MCP server, etc.)
3. Customize the placeholders in the bundled `AGENTS.md` (v1.0 — includes 4 execution modes, implementation-plan requirement, agent routing convention, Tier-1 / Tier-2 governance structure)
4. Reference this repo from your `AGENTS.md` header:
   ```yaml
   parent_governance: "github.com/fuzzywigg/agents-governance"
   ```

### For Existing Projects

Add to your project's `AGENTS.md` header:

```yaml
parent_governance: "github.com/fuzzywigg/agents-governance"
```

For the full ecosystem rules (autonomy levels, kill switch, MCP security, financial controls), see [AGENTS-ECOSYSTEM.md](AGENTS-ECOSYSTEM.md).

## Ecosystem Snapshot

The full 22-repo ecosystem is mapped in [AGENTS-ECOSYSTEM.md §2.1](AGENTS-ECOSYSTEM.md#21-project-portfolio). Summary:

| Tier | Count | Description |
|------|-------|-------------|
| **A — Active Strategic** | 8 | Primary value-creation surfaces (PikoClaw, agents, claw-mcp, etc.) |
| **B — Governance & Standards** | 3 + 1 gist | Source-of-truth docs (this repo, agents-standard, ai vision repo, Agent OS gist) |
| **C — Infrastructure & Utilities** | 5 | Sites and CLI tooling (praetor, godaddy-toolkit, fuzzywigg-ai, fuzzywigg.com, meromhouse.org) |
| **D — Dormant / Reference Only** | 6 | Read-only; do not refactor (g0p.us, nft2.me, g0p.ai, menu_planner, math-pentathlon, Backlink, g0p-agents) |

## Optional: Caveman Context Compression

Tier A repos with large `AGENTS.md` files can use the optional compression script in `project-template/scripts/compress-context.py` to reduce governance-file token usage by **~40%**. See [Appendix B](AGENTS-ECOSYSTEM.md#appendix-b-caveman-context-compression-optional) for details.

## Philosophy

**Local-first. Privacy-preserving. Self-custodied.**

This governance framework ensures AI agents:
- Respect human authority (kill switch, approval tiers)
- Protect sensitive data (PHI guard, zone-based routing)
- Operate within defined boundaries (budgets, policies)
- Maintain audit trails (blockchain logging)
- Support multi-user families (delegation, permissions)

## Contributing

1. Fork this repository
2. Create branch: `amendment/description`
3. Submit PR with rationale
4. smtp.eth reviews and merges

Structural changes to `AGENTS-ECOSYSTEM.md` and `templates/` require Andrew approval. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Version

Current: **2.3.0** (2026-04-19)

## License

MIT

---

*Maintained by smtp.eth*
