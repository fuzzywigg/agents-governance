# AGENTS-ECOSYSTEM.md — smtp.eth Governance Framework

```yaml
version: "2.1.0"
last_updated: "2025-12-13"
maintainer: "smtp.eth"
scope: "ecosystem-wide"
repository: "github.com/fuzzywigg/agents-governance"
```

> **This document establishes governance principles for all AI agents operating within the smtp.eth ecosystem.**
> For repository-specific rules, see AGENTS.md in individual project repos.

---

## Table of Contents

1. [Identity & Sovereignty](#1-identity--sovereignty)
2. [Ecosystem Architecture](#2-ecosystem-architecture)
3. [Autonomy Framework](#3-autonomy-framework)
4. [Security & Trust Boundaries](#4-security--trust-boundaries)
5. [Financial Controls](#5-financial-controls)
6. [Multi-Agent Coordination](#6-multi-agent-coordination)
7. [Data Governance](#7-data-governance)
8. [Family & Multi-User Model](#8-family--multi-user-model)
9. [Hardware & Infrastructure](#9-hardware--infrastructure)
10. [Compliance & Audit](#10-compliance--audit)
11. [Domain Portfolio](#11-domain-portfolio)
12. [Amendment Process](#12-amendment-process)

---

## 1. Identity & Sovereignty

### 1.1 Primary Identity

| Attribute | Value |
|-----------|-------|
| ENS Identity | `smtp.eth` |
| Governance Model | Personal Digital Sovereignty |
| Philosophy | Local-first, privacy-preserving, self-custodied |

### 1.2 Sub-Identities

```yaml
family:
  - wife.smtp.eth    # Spouse - trusted co-administrator
  - kid1.smtp.eth    # Child 1 - supervised access
  - kid2.smtp.eth    # Child 2 - supervised access

agents:
  - agent.smtp.eth   # Autonomous agent identity
  - home.smtp.eth    # Home infrastructure identity
```

### 1.3 Identity Principles

1. **Self-Custody**: All keys, credentials, and identity materials remain under smtp.eth control
2. **Verifiable**: Actions can be cryptographically attributed to identity
3. **Delegatable**: Sub-identities can be granted scoped permissions
4. **Revocable**: Any delegation can be revoked unilaterally by smtp.eth

---

## 2. Ecosystem Architecture

### 2.1 Project Portfolio

| Project | Purpose | Status | AGENTS.md |
|---------|---------|--------|-----------|
| fuzzywigg-ai | Core agent orchestration | Active | ✅ |
| nft2.me | NFT minting platform | Active | Pending |
| owl-visuals | Visual generation | Planned | Pending |
| health-agents | Health data management | Planned | Pending |
| home-node | Sovereign infrastructure | Sprint 16 | Pending |

### 2.2 Technology Stack

```
┌─────────────────────────────────────────────────────┐
│                    Applications                      │
│  (Dashboard, Mobile Companion, CLI, Integrations)   │
├─────────────────────────────────────────────────────┤
│                  Orchestration Layer                 │
│    (fuzzywigg-ai: Flows, Governance, MCP Router)    │
├─────────────────────────────────────────────────────┤
│                    LLM Gateway                       │
│     (LiteLLM: Claude, ChatGPT, Gemini, Ollama)     │
├─────────────────────────────────────────────────────┤
│                  Infrastructure                      │
│   (Home Node, Cloud Fallback, Mobile, IoT/Pi)       │
├─────────────────────────────────────────────────────┤
│                    Blockchain                        │
│     (Ethereum, Polygon, Optimism, Base)             │
└─────────────────────────────────────────────────────┘
```

### 2.3 Network Zones

| Zone | Examples | Trust Level | Data Policy |
|------|----------|-------------|-------------|
| Home | Raspberry Pi, Arduino, NAS | High | Full context |
| Device | Mobile phone, laptop | High | Full context |
| Cloud | Claude API, OpenAI, Zapier | Medium | PII stripped |
| Public | Block explorers, public APIs | Low | Minimal data |

---

## 3. Autonomy Framework

### 3.1 Autonomy Levels

| Level | Name | Human Involvement | Use Case |
|-------|------|-------------------|----------|
| L0 | Advisory | Every action | New flows, high-risk, learning |
| L1 | Bounded | Policy exceptions only | Tested flows, known safe actions |
| L2 | Supervised | Budget/policy violations | Production with cost controls |
| L3 | Autonomous | Critical violations only | Future: proven stable systems |

### 3.2 Escalation Matrix

```
Action Request
     │
     ▼
┌─────────────┐
│ Kill Switch │──Yes──▶ BLOCK (human intervention required)
│   Active?   │
└──────┬──────┘
       │ No
       ▼
┌─────────────┐
│  In Policy? │──No───▶ Escalate to Advisory
└──────┬──────┘
       │ Yes
       ▼
┌─────────────┐
│ Within      │──No───▶ Escalate to Advisory
│ Budget?     │
└──────┬──────┘
       │ Yes
       ▼
┌─────────────┐
│ Cost > 10x  │──Yes──▶ CRITICAL: Activate Kill Switch
│ Budget?     │
└──────┬──────┘
       │ No
       ▼
   APPROVED
```

### 3.3 Kill Switch Protocol

**Triggers:**
- Cost exceeds 10x allocated budget
- Critical governance violation flagged
- Manual activation by smtp.eth
- Security breach detected

**Behavior:**
- File-based lock (`.kill_switch` in repo root)
- ALL agent actions blocked
- Human must physically remove file
- Incident logged and postmortem required

---

## 4. Security & Trust Boundaries

### 4.1 Trust Hierarchy

```yaml
trust_levels:
  absolute:     # smtp.eth only
    - kill_switch_deactivation
    - governance_amendments
    - key_rotation
    
  high:         # smtp.eth + wife.smtp.eth
    - budget_increases
    - new_integration_approval
    - security_camera_control
    
  medium:       # Family members
    - calendar_management
    - smart_home_control
    - spending_under_limits
    
  low:          # Agents (automated)
    - logging
    - notifications
    - read-only queries
```

### 4.2 Credential Management

| Credential Type | Storage | Rotation | Never |
|-----------------|---------|----------|-------|
| Wallet private keys | Hardware wallet | Annual | Cloud, logs |
| API keys | Local encrypted vault | Quarterly | Git, cloud LLMs |
| ENS ownership | On-chain | Never | Delegate |
| Session tokens | Memory only | Per session | Persist |

### 4.3 Network Security

```yaml
routing_rules:
  banking:
    require: "cloud"  # Never process banking on home network
    reason: "Liability protection"
    
  medical:
    prefer: "home"
    fallback: "cloud_with_phi_guard"
    reason: "HIPAA-adjacent protection"
    
  smart_home:
    require: "home"
    reason: "Physical security"
```

---

## 5. Financial Controls

### 5.1 Transaction Classification

| Tier | Amount (USD) | Examples | Approval |
|------|--------------|----------|----------|
| Trivial | < $1 | Logs, tests | Auto |
| Low | $1 - $50 | Smart home, utilities | Auto within daily limit |
| Medium | $50 - $500 | Subscriptions, services | Human review |
| High | $500 - $5,000 | Major purchases | Human + delay |
| Critical | > $5,000 | Investments, transfers | 2x approval + 24hr |

### 5.2 Budget Management

```yaml
budgets:
  daily:
    auto_approve_limit: 50 USD
    alert_threshold: 100 USD
    hard_cap: 500 USD
    
  monthly:
    operational: 500 USD
    infrastructure: 200 USD
    experiments: 100 USD
    
  per_action:
    llm_api_calls: 0.50 USD
    blockchain_tx: 10 USD (gas)
    external_api: 1 USD
```

### 5.3 Chain Selection by Action

| Action Type | Primary Chain | Fallback | Rationale |
|-------------|---------------|----------|-----------|
| Critical financial | Ethereum | None | Security, finality |
| Permissions/access | Ethereum | Polygon | Immutability |
| Audit logs | Polygon | Optimism | Cost efficiency |
| IoT/smart home | Optimism | Polygon | Speed, cost |
| Ephemeral/test | Polygon | — | Burn after use |

---

## 6. Multi-Agent Coordination

### 6.1 MCP (Model Context Protocol)

The ecosystem uses MCP for inter-agent communication:

```yaml
mcp_servers:
  home:
    - raspberry_pi_smart_home
    - arduino_garage
    - nest_hub
    
  cloud:
    - anthropic_claude
    - openai_chatgpt
    - zapier_automation
    
  device:
    - mobile_local
    - ollama_local
```

### 6.2 Distributed Locking

```yaml
locking:
  enabled: true
  default_duration: 300 seconds
  resources:
    calendar: "single_writer"
    smart_home: "multi_reader_single_writer"
    wallet: "exclusive"
```

### 6.3 Conflict Resolution

| Conflict Type | Resolution |
|---------------|------------|
| Resource lock timeout | Release lock, notify owner |
| Concurrent edits | Last-write-wins + audit trail |
| Budget contention | FIFO queue, advisory mode |
| Agent disagreement | Escalate to human |

---

## 7. Data Governance

### 7.1 Classification

| Level | Examples | Handling |
|-------|----------|----------|
| Public | Blog posts, open source | No restrictions |
| Internal | Calendar, task lists | Family access |
| Confidential | Financial, medical | smtp.eth only |
| Restricted | Private keys, passwords | Never transmit |

### 7.2 PHI/PII Protection

**Always Redact Before Cloud Transmission:**
- Email addresses → `[EMAIL]`
- Phone numbers → `[PHONE]`
- SSN → `[SSN]`
- Credit cards → `[CREDIT_CARD]`
- IP addresses → `[IPV4]`

### 7.3 Data Residency

```yaml
residency:
  default: "home"
  
  exceptions:
    - type: "cloud_llm_context"
      allowed: true
      condition: "pii_stripped"
      
    - type: "blockchain_audit"
      allowed: true
      condition: "hashed_identifiers"
```

### 7.4 Retention

| Data Type | Retention | Deletion |
|-----------|-----------|----------|
| Audit logs | 7 years | Automated |
| Session context | End of session | Immediate |
| Conversation history | 90 days | On request |
| Financial records | 7 years | Per regulations |

---

## 8. Family & Multi-User Model

### 8.1 Permission Matrix

| Resource | smtp.eth | wife.smtp.eth | kid1.smtp.eth | kid2.smtp.eth |
|----------|----------|---------------|---------------|---------------|
| All systems | ✅ Full | ✅ Full | — | — |
| Calendar | ✅ | ✅ | 👁️ View | 👁️ View |
| Smart lights | ✅ | ✅ | 🏠 Own room | 🏠 Own room |
| Thermostat | ✅ | ✅ | — | — |
| Security cameras | ✅ | 👁️ View | — | — |
| Purchases | ✅ | ✅ | ≤$50 | ≤$50 |

### 8.2 Delegation Rules

```yaml
delegation:
  - from: smtp.eth
    to: kid1.smtp.eth
    actions:
      - purchase_request
    constraints:
      max_amount: 50 USD
      requires_parent_approval: true
      
  - from: smtp.eth
    to: wife.smtp.eth
    actions:
      - "*"  # Full delegation
    constraints:
      except:
        - kill_switch_deactivation
        - governance_amendment
```

### 8.3 Onboarding Flow

New family member onboarding:
1. Create sub-identity ENS (e.g., `newmember.smtp.eth`)
2. Assign permission tier
3. Configure device access
4. Set spending limits
5. Verify understanding of governance
6. Enable audit logging

---

## 9. Hardware & Infrastructure

### 9.1 Home Node Vision

**Target: Sprint 16 (Dec 2025)**

```yaml
home_node:
  form_factor: "Single 2-3GB image"
  supported_hardware:
    - Raspberry Pi 4/5
    - x86 mini PC
    
  pre_installed:
    - Docker
    - Ollama (local LLM)
    - Fuzzywigg agent stack
    
  first_boot:
    - WiFi setup wizard
    - Wallet connect (MetaMask/WalletConnect)
    - Family member enrollment
```

### 9.2 Device Hierarchy

```
smtp.eth (Owner)
    │
    ├── Home Node (Primary)
    │   ├── Raspberry Pi MCP Server
    │   ├── Arduino Garage Controller
    │   └── NAS Storage
    │
    ├── Cloud (Fallback)
    │   ├── Claude API
    │   ├── OpenAI API
    │   └── Zapier Integrations
    │
    └── Mobile (On-the-go)
        ├── Tauri Companion App
        └── Local Ollama (when available)
```

### 9.3 Resilience

| Scenario | Primary | Fallback | Degradation |
|----------|---------|----------|-------------|
| Home internet down | Home node | Cloud via mobile | Full |
| Cloud API down | Cloud | Home node + Ollama | Reduced capability |
| Power outage | Home node | Cloud only | Graceful |
| All systems down | — | SMS alerts only | Emergency only |

---

## 10. Compliance & Audit

### 10.1 Audit Trail

Every action logged with:
- Timestamp (UTC)
- Actor (identity)
- Action type
- Input hash
- Output hash
- Governance decision
- Chain/zone

### 10.2 Blockchain Logging

```yaml
audit_logging:
  enabled: true
  min_severity: "medium"  # medium, high, critical
  chain: "polygon"
  contract: "0x..."  # Audit log contract
```

### 10.3 Compliance Targets

| Standard | Status | Target |
|----------|--------|--------|
| SOC 2 Type II | 🔄 In progress | Q2 2026 |
| GDPR | ✅ Designed in | Active |
| HIPAA | ⚠️ Best effort | N/A (personal use) |
| FedRAMP | 📋 Planned | Q4 2026 |

### 10.4 Incident Response

**Severity Levels:**
- SEV-1: Kill switch activated, breach, fund loss → Immediate
- SEV-2: Production down, critical failure → < 1 hour
- SEV-3: Degraded performance → < 24 hours
- SEV-4: Minor issue → Next sprint

**Postmortem Required:** SEV-1 and SEV-2 incidents

---

## 11. Domain Portfolio

### 11.1 Active Domains

| Domain | Purpose | Registrar | Renewal |
|--------|---------|-----------|---------|
| smtp.eth | Primary identity | ENS | Perpetual |
| nft2.me | NFT platform | — | Annual |
| fuzzywigg.com | Brand/marketing | — | Annual |

### 11.2 Domain Security

- DNSSEC enabled where supported
- Registrar lock on all domains
- 2FA on all registrar accounts
- Annual audit of domain portfolio

---

## 12. Amendment Process

### 12.1 Proposing Changes

1. Fork `agents-governance` repository
2. Create branch: `amendment/description`
3. Edit relevant `.md` file
4. Submit PR with rationale
5. smtp.eth reviews and merges (or rejects with reason)

### 12.2 Version History

| Version | Date | Summary |
|---------|------|---------|
| 2.1.0 | 2025-12-13 | Initial ecosystem governance document |
| 2.0.0 | 2025-12-13 | Separated from repo-specific AGENTS.md |

### 12.3 Review Schedule

- **Quarterly**: Budget limits, permission matrix
- **Semi-annual**: Trust hierarchy, compliance status
- **Annual**: Full document review, roadmap alignment

---

## Appendix A: Related Documents

| Document | Location | Purpose |
|----------|----------|---------|
| AGENTS.md (fuzzywigg-ai) | [fuzzywigg-ai repo](https://github.com/fuzzywigg/fuzzywigg-ai/AGENTS.md) | Repo-specific rules |
| ROADMAP.md | fuzzywigg-ai/docs/planning/ | Sprint backlog |
| config.yaml | fuzzywigg-ai/.fuzzywigg/ | MCP configuration |
| postmortems/ | Per-repo | Incident documentation |

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| MCP | Model Context Protocol - inter-agent communication standard |
| PHI | Protected Health Information |
| PII | Personally Identifiable Information |
| ENS | Ethereum Name Service |
| Kill Switch | Emergency stop mechanism blocking all agent actions |
| Home Node | Self-hosted infrastructure running agent stack |

## Appendix C: Contact

- **Primary**: smtp.eth
- **GitHub**: [fuzzywigg](https://github.com/fuzzywigg)
- **Governance Repo**: [agents-governance](https://github.com/fuzzywigg/agents-governance)

---

**End of Document**

*This document governs the smtp.eth ecosystem. Individual projects should maintain their own AGENTS.md that references this document and adds project-specific rules.*
