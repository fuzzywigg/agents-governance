# AGENTS.md — [PROJECT_NAME]

```yaml
version: "1.0.0"
last_updated: "YYYY-MM-DD"
maintainer: "smtp.eth"
scope: "repository-specific"
parent_governance: "github.com/fuzzywigg/agents-governance"
```

> **This document governs AI agent behavior within this repository.**
> For ecosystem-wide governance, see [AGENTS-ECOSYSTEM.md](https://github.com/fuzzywigg/agents-governance).

---

## 1. Quick Reference

### Critical Files

| File | Purpose | Edit Restrictions |
|------|---------|-------------------|
| `[CONFIG_FILE]` | Main configuration | Human approval required |
| `.env` | Secrets | Never commit |

### Autonomy Level

This project operates at **Level [0/1/2]** autonomy:
- [ ] L0 Advisory: Human confirms every action
- [ ] L1 Bounded: Auto-approve within policy
- [ ] L2 Supervised: Auto-approve within policy + budget

---

## 2. Project-Specific Rules

### 2.1 [Section Title]

[Add project-specific governance rules here]

### 2.2 [Section Title]

[Add project-specific governance rules here]

---

## 3. Testing Requirements

```bash
# Run tests
[test command]

# Required coverage
[coverage requirements]
```

---

## 4. Deployment

### Environments

| Environment | Platform | Status |
|-------------|----------|--------|
| Development | Local | ✅ |
| Staging | [Platform] | [Status] |
| Production | [Platform] | [Status] |

---

## 5. Incident Response

Follow ecosystem incident protocol from [AGENTS-ECOSYSTEM.md](https://github.com/fuzzywigg/agents-governance).

Severity levels:
- SEV-1: Immediate response
- SEV-2: < 1 hour
- SEV-3: < 24 hours
- SEV-4: Next sprint

---

## 6. Amendment Process

1. Create branch: `agents-md/description`
2. Edit this file
3. Submit PR with rationale
4. smtp.eth approval required

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial version |

---

**End of Document**

*See [agents-governance](https://github.com/fuzzywigg/agents-governance) for ecosystem rules.*
