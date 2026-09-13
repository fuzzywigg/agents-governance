# Autonomy Levels

[← Home](Home.md)

Public summary of the autonomy framework defined in
[AGENTS-ECOSYSTEM.md §3](https://github.com/fuzzywigg/agents-governance/blob/main/AGENTS-ECOSYSTEM.md).
If this page and the policy doc disagree, **the policy doc wins**.

## Levels

| Level | Name | Human involvement | Typical use |
|-------|------|-------------------|-------------|
| L0 | Advisory | Every action | New flows, high-risk, learning |
| L1 | Bounded | Policy exceptions only | Tested flows, known-safe actions |
| L2 | Supervised | Budget/policy violations | Production with cost controls |
| L3 | Autonomous | Critical violations only | Future: proven stable systems |

This governance repository itself operates at **L1 Bounded**.

## Escalation (public)

1. Kill switch active? → **block**; human intervention required.
2. Outside policy? → escalate to Advisory (L0).
3. Outside budget? → escalate to Advisory (L0).
4. Cost ≫ budget (policy threshold)? → critical; activate kill switch.
5. Otherwise → proceed within level.

## Kill switch

- Presence of `.kill_switch` at a repo root blocks **all** agent writes.
- Only smtp.eth removes it manually after incident review.
- Details: ecosystem policy §3.3 and this repo's [AGENTS.md](https://github.com/fuzzywigg/agents-governance/blob/main/AGENTS.md).

[← Overview](Overview.md) · [Repo Stewardship →](Repo-Stewardship.md)
