# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the governance framework (e.g., a policy gap that could allow unauthorized agent action, a secret inadvertently committed, or a trust-boundary bypass):

**Do not open a public issue.**

Contact smtp.eth directly:
- GitHub: [@fuzzywigg](https://github.com/fuzzywigg)
- ENS: smtp.eth

Please include:
1. Description of the vulnerability
2. Affected file(s) and section(s)
3. Potential impact
4. Suggested remediation (if known)

## Response Timeline

| Severity | Response | Resolution Target |
|----------|----------|-------------------|
| SEV-1 (Critical) | Immediate | Same day |
| SEV-2 (High) | < 1 hour | < 48 hours |
| SEV-3 (Medium) | < 24 hours | Next sprint |
| SEV-4 (Low) | Next sprint | Best effort |

## Scope

This repository contains governance documentation, not executable code. Security concerns relevant here include:

- **Policy gaps** — Governance rules that fail to protect sensitive data or prevent unauthorized agent actions
- **Trust boundary violations** — Rules that allow agents to escalate privileges beyond their autonomy level
- **Secret handling** — Any `.env` patterns, credentials, or PII inadvertently included in documents
- **Scratchpad integrity** — Anything that could corrupt the append-only coordination state

## Out of Scope

- Hypothetical future vulnerabilities without a concrete current gap
- Suggestions for stricter policy beyond what the ecosystem needs

## Disclosure

smtp.eth follows responsible disclosure. Once a fix is merged, the vulnerability may be documented in the CHANGELOG with appropriate detail.
