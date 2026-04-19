# AGENTS-ECOSYSTEM.md — smtp.eth Governance Framework

```yaml
version: "2.3.0"
last_updated: "2026-04-19"
maintainer: "smtp.eth"
scope: "ecosystem-wide"
repository: "github.com/fuzzywigg/agents-governance"
goose_protocol: true
ecosystem_size: "22 repos + 1 gist"
template_source: "github.com/fuzzywigg/project-template"
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
6. [Multi-Agent Coordination (Goose Protocol)](#6-multi-agent-coordination-goose-protocol) ← **ENHANCED**
7. [Data Governance](#7-data-governance)
8. [Family & Multi-User Model](#8-family--multi-user-model)
9. [Hardware & Infrastructure](#9-hardware--infrastructure)
10. [Compliance & Audit](#10-compliance--audit)
11. [Domain Portfolio](#11-domain-portfolio)
12. [Amendment Process](#12-amendment-process)

Appendices:

- [Appendix A: Goose Protocol Resources](#appendix-a-goose-protocol-resources)
- [Appendix B: Caveman Context Compression (Optional)](#appendix-b-caveman-context-compression-optional)
- [Appendix C: Quick Commands](#appendix-c-quick-commands)

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

The smtp.eth ecosystem currently contains **22 repositories + 1 gist**, organized into four tiers by strategic role. Each tier has different governance expectations and agent autonomy defaults.

#### Tier A — Active Development, Strategic (8 repos)

Primary value-creation surfaces. Receive the most agent attention; require AGENTS.md compliance; tracked in ecosystem scratchpad.

| Repo | Language | Stage | Pipeline Role |
|------|----------|-------|---------------|
| PikoClaw | Python + Next.js | GREEN | Frontend + API, primary Panathenea demo |
| Q_Willow_HCL | Python | Pre-alpha | Quantum swarm, potential second demo |
| agents | Python + Solidity | Working v3.x | Agent orchestration brain |
| QFZZ | Python | GREEN | Discord control |
| claw-mcp | Python | GREEN | MCP tooling |
| project-template | TypeScript | Active | Project factory (7 flavor branches) |
| matrix-workers | TypeScript | Beta | CF primitives reference (fork-only) |
| openclaw_geryon | Python | RED (security) | Agent executor (needs remediation) |

#### Tier B — Governance & Standards (3 repos + 1 gist)

Source-of-truth documents. Structural changes require Andrew approval (see §12).

| Repo | Purpose |
|------|---------|
| agents-governance | Fork-this-repo governance templates (THIS REPO) |
| agents-standard | Public agent behavior protocols |
| ai | Vision repo (dormant, L1-L4 concepts) |
| Gist `8dc0d7482f...` | Agent OS Google Workspace operational spec |

#### Tier C — Infrastructure & Utilities (5 repos)

Supporting infrastructure, websites, and CLI tooling. L1 autonomy by default.

| Repo | Purpose |
|------|---------|
| praetor | TypeScript scaffold |
| godaddy-toolkit | Python CLI for DNS management |
| fuzzywigg-ai | Next.js portfolio site |
| fuzzywigg.com | Static site |
| meromhouse.org | Static site |

#### Tier D — Dormant / Reference Only (6 repos)

No active development. Agents should NOT refactor or fork these unless explicitly directed.

| Repo | Purpose |
|------|---------|
| g0p.us | Static HTML |
| nft2.me | Static HTML |
| g0p.ai | Static HTML (wrong default branch) |
| menu_planner | Personal Python tool |
| math-pentathlon | Educational |
| Backlink | DJ_GPT orchestration |
| g0p-agents | Reference data only — do NOT fork or refactor |

#### Tier Summary

| Tier | Count | Default Autonomy | Agent Behavior |
|------|-------|------------------|----------------|
| A — Active Strategic | 8 | L1 Bounded | Full agent loop with PR review |
| B — Governance | 3 + 1 gist | L0 Advisory | Andrew approval on structural change |
| C — Infrastructure | 5 | L1 Bounded | Auto-merge low-risk PRs allowed |
| D — Dormant | 6 | L0 Advisory | Read-only by default; no refactors |

### 2.1.1 Universal AGENTS.md Template (v1.0)

The **canonical AGENTS.md template** for new repositories now lives at
[`fuzzywigg/project-template`](https://github.com/fuzzywigg/project-template).
It supersedes `templates/AGENTS-REPO.md` in this repo (which remains for legacy reference).

The v1.0 template defines:

- **4 execution modes** — Advisory, Generative, Transformative, Operational
- **Implementation plan requirement** — every non-trivial PR ships a plan-of-record
- **Agent routing convention** — issue label prefix standard (e.g. `agent:copilot`, `agent:geryon`, `agent:claude-cowork`) so the right surface picks up the work
- **Tier-1 / Tier-2 governance structure** — Tier-1 = mandatory ecosystem rules, Tier-2 = repo-specific overrides
- **7 flavor branches** in `project-template` for common stack choices (Python, Next.js, Cloudflare Worker, MCP server, etc.)

**Recommended for new repos:** clone `project-template`, choose the appropriate flavor branch, customize the `AGENTS.md` placeholders, and link `parent_governance` back to this repo.

### 2.2 Technology Stack

```text
┌─────────────────────────────────────────────────────┐
│                    Applications                      │
│  (Dashboard, Mobile Companion, CLI, Integrations)   │
├─────────────────────────────────────────────────────┤
│                  Orchestration Layer                 │
│         (Goose Protocol + fuzzywigg-ai)             │
│    [Recipes] [Scratchpad] [MCP Router] [Governance] │
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

```text
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

## 6. Multi-Agent Coordination (Goose Protocol)

> **Goose** is Block's open-source AI agent framework, donated to the Linux Foundation.
> The smtp.eth ecosystem adopts Goose patterns for standardized inter-agent coordination.

### 6.1 Architecture Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                     Goose Orchestrator                       │
│  (Ecosystem-wide coordination across all smtp.eth projects) │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐   ┌────────────────┐   ┌──────────────┐ │
│  │ fuzzywigg-ai   │   │  health-agents │   │  home-node   │ │
│  │  recipes/      │   │   recipes/     │   │  recipes/    │ │
│  └───────┬────────┘   └───────┬────────┘   └──────┬───────┘ │
│          │                    │                   │         │
│          ▼                    ▼                   ▼         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Ecosystem Scratchpad (Shared State)        │   │
│  │   github.com/fuzzywigg/agents-governance/scratchpad  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                  MCP Server Network                          │
│  [WalletMCP] [CalendarMCP] [SmartHomeMCP] [HealthMCP]       │
│  [OllamaMCP] [ContractMCP] [NotificationMCP] [AuditMCP]     │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Goose Recipe Standard

All recipes across the ecosystem follow this format:

```yaml
# Standard Goose Recipe Format for smtp.eth ecosystem
name: descriptive_recipe_name
recipe:
  version: 1.0.0
  title: Human-Readable Title
  
  settings:
    goose_provider: "anthropic"           # or "openai", "ollama"
    goose_model: "claude-sonnet-4"        # or specific model
    autonomy_level: 1                     # Maps to Section 3.1
    network_zone: "home"                  # Maps to Section 2.3
  
  instructions: |
    High-level context for the orchestrating agent.
    References AGENTS-ECOSYSTEM.md governance rules.
  
  prompt: |
    Specific numbered steps to execute.
    Must update scratchpad at each checkpoint.
  
  extensions:
    - type: builtin
      name: developer
      timeout: 300
    - type: mcp
      name: service_name
      uri: http://localhost:PORT
      network_zone: home  # MUST specify zone
```

### 6.3 The Scratchpad Pattern

The **scratchpad** is the ecosystem-wide state machine for inter-agent coordination.

**Hierarchy:**

```text
agents-governance/
└── scratchpad/
    ├── ecosystem.txt      # Cross-project coordination
    └── incidents.txt      # Active incidents

fuzzywigg-ai/
└── agentic_flows/
    └── scratchpad.txt     # Repo-specific tasks

health-agents/
└── scratchpad.txt         # Repo-specific tasks
```

**Format:**

```markdown
# Scratchpad - [Scope] State
# Last updated: ISO-8601 timestamp

## Active Tasks

### [TASK-XXX] Title - Scheduled Time
- [x] AgentA: Completed step
  - [x] Substep with note (value ✓)
- [ ] AgentB: Pending step
  - [ ] Substep ← BLOCKED (reason)
- [ ] AgentC: Future step

## Completed (Archive after 7 days)
```

**Rules:**

1. Each agent owns its section (identified by name)
2. Progress tracked as `[x]` complete, `[ ]` pending
3. **APPEND-ONLY**: Never delete, only mark complete
4. Markers: `← BLOCKED`, `← FAILED`, `← TIMEOUT`, `← APPROVAL`
5. Archive completed tasks weekly

### 6.4 MCP Server Registry

All MCP servers in the ecosystem must be registered:

| Server | Zone | Purpose | Owner | Status |
|--------|------|---------|-------|--------|
| WalletMCP | home | Web3 transactions | fuzzywigg-ai | 🔄 Planned |
| CalendarMCP | cloud | Google Calendar | Zapier | ✅ Active |
| SmartHomeMCP | home | IoT control | home-node | 🔄 In Progress |
| HealthMCP | home | Health data (PHI) | health-agents | 📋 Planned |
| OllamaMCP | home | Local LLM | fuzzywigg-ai | ✅ Active |
| ContractMCP | home | Smart contracts | fuzzywigg-ai | 🔄 Planned |
| NotificationMCP | cloud | Push/email | Zapier | ✅ Active |
| AuditMCP | home | Blockchain logging | fuzzywigg-ai | 🔄 Planned |

**Adding New MCP Servers:**

1. Define in project's `.fuzzywigg/config.yaml`
2. Register in this table (PR to agents-governance)
3. Document tools in server README
4. Add to allowlist after security review

### 6.5 Sub-Recipe Composition

Complex workflows span multiple projects via sub-recipes:

```yaml
# Ecosystem-level orchestration example
name: weekly_family_summary
recipe:
  version: 1.0.0
  title: Weekly Family Dashboard Update
  
  sub_recipes:
    # Health data from health-agents
    - name: collect_health
      project: health-agents
      path: ./recipes/weekly_health.yaml
      timeout: 120
    
    # Smart home metrics from home-node
    - name: collect_home_metrics
      project: home-node
      path: ./recipes/weekly_metrics.yaml
      timeout: 60
    
    # Calendar summary from fuzzywigg-ai
    - name: calendar_summary
      project: fuzzywigg-ai
      path: ./agentic_flows/recipes/calendar_summary.yaml
      timeout: 60
    
    # Generate unified report
    - name: generate_dashboard
      project: fuzzywigg-ai
      path: ./agentic_flows/recipes/dashboard_update.yaml
      timeout: 90
      depends_on: [collect_health, collect_home_metrics, calendar_summary]
```

### 6.6 Cross-Project Coordination Protocol

When agents from different projects need to coordinate:

1. **Initiating project** creates task in `agents-governance/scratchpad/ecosystem.txt`
2. **Target project** agent reads ecosystem scratchpad
3. **Target agent** executes and updates its repo-specific scratchpad
4. **Target agent** reports completion to ecosystem scratchpad
5. **Initiating project** reads result and continues

**Example:**

```markdown
# agents-governance/scratchpad/ecosystem.txt

### [ECO-001] Cross-Project Health Report - 2025-12-15
- [x] fuzzywigg-ai/OrchestratorAgent: Initiated
- [ ] health-agents/CollectorAgent: Gather metrics
  - [ ] Awaiting response ← PENDING
- [ ] fuzzywigg-ai/ReportAgent: Generate unified report
```

### 6.7 MCP Security Requirements

All MCP servers must comply with:

```yaml
mcp_security:
  authentication:
    required: true
    methods: ["bearer_token", "mtls"]
    
  authorization:
    tool_allowlist: true  # Only declared tools can be called
    rate_limiting: true
    
  network:
    zone_binding: true    # Server must declare zone
    phi_guard_for_cloud: true
    
  audit:
    log_all_calls: true
    include_timestamps: true
    redact_sensitive: true
```

### 6.8 Distributed Locking

```yaml
locking:
  enabled: true
  default_duration: 300 seconds
  
  resources:
    calendar: "single_writer"
    smart_home: "multi_reader_single_writer"
    wallet: "exclusive"
    scratchpad: "append_only"  # No locks needed
    
  conflict_resolution:
    timeout: "release_and_notify"
    concurrent_edit: "last_write_wins_with_audit"
    budget_contention: "fifo_queue"
```

### 6.9 Recipe Governance Rules

| Autonomy Level | Recipe Restrictions |
|----------------|---------------------|
| L0 (Advisory) | All recipes require human approval per step |
| L1 (Bounded) | Only pre-approved recipes can auto-execute |
| L2 (Supervised) | Recipes execute within budget, escalate violations |
| L3 (Autonomous) | Future: proven recipes only, kill switch monitored |

**Recipe Approval Process:**

1. Submit recipe PR to project repo
2. Security review (credentials, network access)
3. Test in Advisory mode (L0)
4. Graduate to Bounded (L1) after 5 successful runs
5. Graduate to Supervised (L2) after 20 successful runs

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

**Goose Recipe Requirement:** Any recipe with `network_zone: cloud` MUST have `phi_guard: true` in settings.

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
      
    - type: "goose_scratchpad"
      allowed: "home_only"
      condition: "never_sync_to_cloud"
```

### 7.4 Retention

| Data Type | Retention | Deletion |
|-----------|-----------|----------|
| Audit logs | 7 years | Automated |
| Session context | End of session | Immediate |
| Conversation history | 90 days | On request |
| Financial records | 7 years | Per regulations |
| Scratchpad archives | 90 days | Automated |

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
| Goose Recipes | ✅ Create | ✅ Create | Run only | Run only |
| Scratchpad | ✅ Full | ✅ Full | Read only | Read only |

### 8.2 Delegation Rules

```yaml
delegation:
  - from: smtp.eth
    to: kid1.smtp.eth
    actions:
      - purchase_request
      - run_recipe  # NEW: Can run pre-approved recipes
    constraints:
      max_amount: 50 USD
      requires_parent_approval: true
      recipe_allowlist:
        - "smart_lights_bedroom"
        - "homework_timer"
      
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
5. **Assign recipe permissions** (new)
6. Verify understanding of governance
7. Enable audit logging

---

## 9. Hardware & Infrastructure

### 9.1 Home Node Vision

Target: Sprint 16 (Dec 2025)

```yaml
home_node:
  form_factor: "Single 2-3GB image"
  supported_hardware:
    - Raspberry Pi 4/5
    - x86 mini PC
    
  pre_installed:
    - Docker
    - Ollama (local LLM)
    - Goose CLI
    - Fuzzywigg agent stack
    - MCP server runtime
    
  first_boot:
    - WiFi setup wizard
    - Wallet connect (MetaMask/WalletConnect)
    - Family member enrollment
    - Goose recipe sync
```

### 9.2 Device Hierarchy

```text
smtp.eth (Owner)
    │
    ├── Home Node (Primary)
    │   ├── Goose Orchestrator
    │   ├── Raspberry Pi MCP Server
    │   ├── Arduino Garage Controller
    │   ├── Local Scratchpad
    │   └── NAS Storage
    │
    ├── Cloud (Fallback)
    │   ├── Claude API
    │   ├── OpenAI API
    │   └── Zapier Integrations
    │
    └── Mobile (On-the-go)
        ├── Tauri Companion App
        ├── Local Ollama (when available)
        └── Recipe trigger UI
```

### 9.3 Resilience

| Scenario | Primary | Fallback | Degradation |
|----------|---------|----------|-------------|
| Home internet down | Home node | Cloud via mobile | Full |
| Cloud API down | Cloud | Home node + Ollama | Reduced capability |
| Power outage | Home node | Cloud only | Graceful |
| All systems down | — | SMS alerts only | Emergency only |
| Goose orchestrator down | Local recipes | Manual execution | Advisory mode |

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
- **Recipe ID** (if via Goose)
- **Scratchpad task ID** (if coordinated)

### 10.2 Blockchain Logging

```yaml
audit_logging:
  enabled: true
  min_severity: "medium"  # medium, high, critical
  chain: "polygon"
  contract: "0x..."  # Audit log contract
  
  goose_specific:
    log_recipe_executions: true
    log_scratchpad_updates: true
    log_mcp_calls: true
```

### 10.3 Compliance Targets

| Standard | Status | Target |
|----------|--------|--------|
| SOC 2 Type II | 🔄 In progress | Q2 2026 |
| GDPR | ✅ Designed in | Active |
| HIPAA | ⚠️ Best effort | N/A (personal use) |
| FedRAMP | 📋 Planned | Q4 2026 |
| Goose Protocol | ✅ Compliant | Active |

### 10.4 Incident Response

**Severity Levels:**

- SEV-1: Kill switch activated, breach, fund loss → Immediate
- SEV-2: Production down, critical failure → < 1 hour
- SEV-3: Degraded performance → < 24 hours
- SEV-4: Minor issue → Next sprint

**Postmortem Required:** SEV-1 and SEV-2 incidents

**Goose-Specific Incidents:**

- Recipe failure cascade → SEV-2
- Scratchpad corruption → SEV-2
- MCP server compromise → SEV-1

---

## 11. Domain Portfolio

### 11.1 Active Domains

| Domain | Purpose | Registrar | Renewal |
|--------|---------|-----------|---------|
| smtp.eth | Primary identity | ENS | Perpetual |
| nft2.me | NFT platform (Tier D) | — | Annual |
| fuzzywigg.com | Brand/marketing (Tier C) | — | Annual |
| meromhouse.org | Static site (Tier C) | — | Annual |
| g0p.us | Static (Tier D) | — | Annual |
| g0p.ai | Static (Tier D) | — | Annual |

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
| 2.3.0 | 2026-04-19 | Expanded §2.1 to full 22-repo / 4-tier portfolio; added §2.1.1 referencing project-template AGENTS.md v1.0; added Appendix B for caveman compression |
| 2.2.0 | 2025-12-13 | Added Goose Protocol integration (Section 6 major update) |
| 2.1.0 | 2025-12-13 | Initial ecosystem governance document |
| 2.0.0 | 2025-12-13 | Separated from repo-specific AGENTS.md |

### 12.3 Review Schedule

- **Quarterly**: Budget limits, permission matrix, MCP server registry
- **Semi-annual**: Trust hierarchy, compliance status, recipe approvals
- **Annual**: Full document review, roadmap alignment, Goose protocol updates

---

## Appendix A: Goose Protocol Resources

- [Goose Documentation](https://block.github.io/goose/) — Official Goose docs
- [MCP Specification](https://modelcontextprotocol.io/) — Model Context Protocol
- [Linux Foundation Announcement](https://www.linuxfoundation.org/) — Goose donation
- [fuzzywigg-ai Recipes](https://github.com/fuzzywigg/fuzzywigg-ai/tree/main/agentic_flows/recipes) — Example recipes

## Appendix B: Caveman Context Compression (Optional)

For repos with large governance files (`AGENTS.md`, `AGENTS-ECOSYSTEM.md`, long
scratchpads), a context compression script is available at:

```text
project-template:scripts/compress-context.py
```

Known as **"caveman compression"** — an optional optimization that reduces
governance-file token usage by **~40%** by stripping markdown decoration,
collapsing whitespace, and abbreviating recurring scaffolding while preserving
all semantic content.

**When to use:**

- AGENTS.md exceeds ~8K tokens
- Repo loads multiple governance files into context per agent turn
- Cost or latency on large-context models is a concern

**When NOT to use:**

- Files are already small (overhead exceeds savings)
- Human readability of the source is the primary goal (this is an output-time
  transform; keep the readable original in git)

**Status:** optional but recommended for Tier A repos with heavy AGENTS.md surface area. See `project-template/scripts/compress-context.py` for usage.

---

## Appendix C: Quick Commands

```bash
# Validate all recipes in a project
python scripts/validate_recipes.py

# Check ecosystem scratchpad
cat agents-governance/scratchpad/ecosystem.txt

# Run a recipe (Goose CLI)
goose run ./agentic_flows/recipes/my_recipe.yaml

# Check MCP server status
curl http://localhost:3000/health

# Activate kill switch
touch .kill_switch

# Check kill switch status
ls -la .kill_switch 2>/dev/null && echo "ACTIVE" || echo "inactive"
```

---

End of Document

*This is the canonical ecosystem governance document. Individual projects reference this and add repo-specific rules in their own AGENTS.md files.*
