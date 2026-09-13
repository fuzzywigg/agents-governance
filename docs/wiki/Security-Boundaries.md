# Security Boundaries

[← Home](Home.md)

Public summary only. Full rules live in
[AGENTS-ECOSYSTEM.md §4](https://github.com/fuzzywigg/agents-governance/blob/main/AGENTS-ECOSYSTEM.md)
and [SECURITY.md](https://github.com/fuzzywigg/agents-governance/blob/main/SECURITY.md).

## Trust hierarchy (summary)

| Level | Who | Examples |
|-------|-----|----------|
| Absolute | smtp.eth | Kill switch deactivation, governance amendments, key rotation |
| High | smtp.eth + designated family principals | Budget increases, new integration approval |
| Medium | Family members | Calendar / smart-home within limits |
| Low | Agents | Logging, notifications, read-only queries |

## Credentials (public rules)

- **Never** commit wallet keys, API secrets, or session tokens to git.
- API keys stay in local encrypted vaults; rotate on the policy schedule.
- Session tokens are memory-only; do not persist to docs or wikis.
- This wiki and `docs/` must not contain private MEMORY or private-repo secrets.

## Network routing (high level)

- Banking-class work: cloud path per policy (liability protection).
- Medical / PHI-adjacent: prefer home; cloud only with PHI guard.
- Smart-home control: home network.

Do not publish hostnames, vault paths, or private MCP endpoints here.

## Reporting

See [SECURITY.md](https://github.com/fuzzywigg/agents-governance/blob/main/SECURITY.md) for how to report security issues.

[← Agent Routing](Agent-Routing.md) · [Home](Home.md)
