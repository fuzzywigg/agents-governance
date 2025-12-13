# agents-governance

**Canonical AI governance documents for the smtp.eth ecosystem.**

This repository contains the source-of-truth governance framework for all AI agents operating within smtp.eth's personal digital sovereignty infrastructure.

## Documents

| Document | Purpose |
|----------|---------|
| [AGENTS-ECOSYSTEM.md](AGENTS-ECOSYSTEM.md) | Ecosystem-wide governance: identity, trust, finances, multi-user, compliance |
| [templates/AGENTS-REPO.md](templates/AGENTS-REPO.md) | Template for project-specific AGENTS.md files |

## Usage

### For New Projects

1. Fork this repository (or use as submodule)
2. Copy `templates/AGENTS-REPO.md` to your project root as `AGENTS.md`
3. Customize for your project's specific needs
4. Reference `AGENTS-ECOSYSTEM.md` for ecosystem-wide rules

### For Existing Projects

Add to your project's AGENTS.md header:

```yaml
parent_governance: "github.com/fuzzywigg/agents-governance"
```

## Projects Using This Governance

| Project | AGENTS.md Status |
|---------|------------------|
| [fuzzywigg-ai](https://github.com/fuzzywigg/fuzzywigg-ai) | ✅ Active |
| nft2.me | 🔜 Pending |
| owl-visuals | 📋 Planned |

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

## Version

Current: **2.1.0** (2025-12-13)

## License

MIT

---

*Maintained by smtp.eth*
