# OWASP Agentic Top 10 — smtp.eth Compliance Mapping

> **Canonical source:** [OWASP Agentic AI Top 10 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
> **Mapped against:** AGENTS-ECOSYSTEM.md v2.3.0 (2026-04-19)
> **Stack:** smtp.eth / OpenClaw / Geryon / Goose Protocol

This document maps each OWASP Agentic Top 10 threat to its concrete manifestation within the smtp.eth ecosystem, the controls already in place, and identified gaps.

---

## AA01 — Prompt Injection

**What it means here:** Malicious content in emails, Discord messages, Notion pages, or MCP tool responses could hijack agent instructions — e.g., a crafted email body telling Geryon to forward credentials or modify the scratchpad.

**Controls in place:**
- Network zone trust model (§2.3): Cloud and Public zones carry lower trust; content from these zones is not automatically elevated to instruction-level authority
- Autonomy levels (§3.1): L0/L1 agents require human approval for novel or high-risk actions, limiting the blast radius of injected instructions
- MCP tool allowlist (§6.7): Only declared tools can be invoked, preventing injected commands from reaching arbitrary capabilities

**Gaps:**
- No explicit prompt-content sanitizer or instruction-boundary enforcement (e.g., structural separation of system vs. user content) at the orchestration layer
- Scratchpad is append-only but not cryptographically signed — a compromised agent could write injection payloads that are read and acted on by other agents

**Priority:** HIGH — the multi-agent Goose Protocol makes lateral injection a concrete attack path across all 23 repos

---

## AA02 — Insecure Output Handling

**What it means here:** Agent-generated content (code, shell commands, MCP payloads) passed downstream without validation could trigger unintended execution — e.g., generated shell code auto-run by a CI hook or Goose recipe step.

**Controls in place:**
- Autonomy gates (§3.1): L0/L1 destructive or novel outputs require human approval before execution
- Audit trail captures output hashes (§10.1): Every action logs input/output hash, enabling post-hoc detection of anomalous outputs
- Kill switch (§3.3): Triggers on governance violation, halting further output processing across the ecosystem

**Gaps:**
- No declared output schema validation for MCP tool responses before agents act on returned data
- Tier C repos allow auto-merge for "low-risk PRs" without explicit output-safety checks on agent-generated code

**Priority:** MEDIUM — approval gates provide meaningful mitigation; schema validation is the primary gap

---

## AA03 — Agent Memory Poisoning

**What it means here:** The ecosystem scratchpad (`agents-governance/scratchpad/ecosystem.txt`) and per-repo scratchpads are the shared memory fabric of the Goose Protocol. Corrupted or maliciously written entries could persist bad state across agents and sessions.

**Controls in place:**
- Scratchpad is append-only with audit logging (§6.7, §10.1): `log_scratchpad_updates: true` creates a record of all writes
- Scratchpad corruption is classified SEV-2 (§10 incident taxonomy), triggering mandatory human escalation
- MEMORY.md security rule (AGENTS.md §2): Never loaded in group chats or shared contexts — limits personal memory exposure

**Gaps:**
- No cryptographic signing of scratchpad entries — a compromised agent can write arbitrary state that other agents will trust
- No TTL or expiry on scratchpad tasks; stale or poisoned entries persist until manually cleared
- The MEMORY.md isolation rule is a policy control, not a technical enforcement boundary

**Priority:** HIGH — the scratchpad is the Goose Protocol's nervous system; poisoning it propagates across all coordinated agents

---

## AA04 — Privilege Escalation

**What it means here:** An agent operating at L1 (Bounded) autonomy attempting to invoke absolute-tier operations (kill switch deactivation, governance amendments, key rotation) or impersonating higher-trust identities like `wife.smtp.eth`.

**Controls in place:**
- Trust hierarchy (§4.1): Four-tier model (absolute / high / medium / low) with explicit operation-to-tier binding; kill switch deactivation and governance amendments are `absolute` — smtp.eth only
- Sub-identity scope (§1.2): `agent.smtp.eth` is declared as a low-trust identity; it cannot self-elevate by design
- Kill switch requires physical file removal (§3.3): No API call can deactivate it — requires direct local human action, making remote escalation impossible

**Gaps:**
- Trust hierarchy is enforced by policy documentation, not by a cryptographic capability system or runtime RBAC enforcement
- If `wife.smtp.eth` (high trust) identity were spoofed or compromised, an agent could obtain `new_integration_approval` rights and introduce hostile integrations
- No runtime check that the declared actor identity matches a cryptographic proof

**Priority:** HIGH — the trust model is well-designed but relies entirely on policy compliance, not technical enforcement

---

## AA05 — Excessive Agency

**What it means here:** Agents taking actions beyond their sanctioned scope — spending money autonomously, sending external messages without approval, pushing directly to production branches, or modifying Tier D dormant repos.

**Controls in place:**
- Kill switch protocol (§3.3): Triggers on cost exceeding 10x budget, critical governance violation, or detected security breach — halts all agent action ecosystem-wide
- Autonomy framework (§3.1): L1 agents handle only policy exceptions with human involvement; L2 requires escalation on budget or policy violations
- Hard rules (AGENTS.md §5): "NEVER run destructive commands unprompted. NEVER delete without approval."
- Financial controls (§5): Budget caps with automatic escalation thresholds
- Tier D repos explicitly marked read-only for agents (§2.1): "Agents should NOT refactor or fork these unless explicitly directed"

**Gaps:**
- L3 (Autonomous) mode is described as future/planned — guardrails and safety criteria for it are not yet specified in any document
- No automated enforcement preventing agents from direct branch pushes vs. required PR draft workflow

**Priority:** MEDIUM — multiple overlapping controls are in place; the main gap is the unspecified L3 future-mode guardrails

---

## AA06 — Prompt Leakage

**What it means here:** System prompts, SOUL.md identity content, MEMORY.md personal data, governance instructions, or family context leaking into agent outputs, external API calls (Claude, OpenAI, Gemini), or Discord messages.

**Controls in place:**
- MEMORY.md security rule (AGENTS.md §2): NEVER loaded in group chats, Discord, or shared contexts — explicit architectural leak prevention
- PHI/PII redaction before cloud transmission (§7.2): Email, phone, SSN, credit card, and IP addresses are all replaced with tokens before leaving the home zone
- Network zone model (§2.3): Sensitive data routes to Home zone; cloud zone only receives PII-stripped context
- `phi_guard: true` required on all Goose recipes with `network_zone: cloud` (§7.2)

**Gaps:**
- SOUL.md and AGENTS.md content could be exfiltrated if an agent is tricked into including governance files in a tool call or API request — no technical block exists
- Redaction relies on a fixed token list (§7.2) — novel PII patterns not on the list pass through undetected
- No automated scanning of outbound LLM API payloads for governance document content or system prompt fragments

**Priority:** MEDIUM — PHI guard is well-specified; system-prompt leakage has no technical enforcement layer

---

## AA07 — Insecure Plugin/Tool Design

**What it means here:** MCP servers (claw-mcp, AuditMCP, HealthMCP, ContractMCP) exposing excessive capabilities, missing authentication, or lacking rate limits — providing agents or attackers a foothold to chain tool calls into harmful operations.

**Controls in place:**
- MCP security requirements (§6.7): Authentication required (`bearer_token` or `mtls`); `tool_allowlist: true`; `rate_limiting: true`; `zone_binding: true`; all calls logged with timestamps and sensitive fields redacted
- HealthMCP is restricted to `health-agents` with `phi_guard_for_cloud: true` (§6.5), limiting PHI exposure surface
- Tool allowlist prevents invocation of undeclared tools — no open proxy to arbitrary shell execution

**Gaps:**
- `openclaw_geryon` (the primary agent executor) is currently flagged RED for security and requires remediation (§2.1) — any tool it invokes inherits its unresolved risk
- AuditMCP and HealthMCP are marked "Planned" — security requirements are defined but production hardening is not yet complete
- No specification of tool input validation schemas beyond allowlisting tool names by string match

**Priority:** HIGH — Geryon executor is RED status; planned tools are not yet production-hardened

---

## AA08 — Sensitive Data Exposure

**What it means here:** Private keys, API keys, session tokens, PHI, or family member data (wife.smtp.eth, kid1/kid2) written to logs, git history, cloud APIs, or shared scratchpads.

**Controls in place:**
- Credential management policy (§4.2): Wallet keys in hardware wallet only; API keys in local encrypted vault with quarterly rotation; session tokens in memory only, never persisted; none may appear in git or cloud LLM payloads
- PHI/PII redaction pipeline (§7.2): Structured redaction applied before any cloud-zone transmission
- Data residency policy (§7.3): 7-year retention with automated compliance; PHI remains in the home zone
- Network zone model (§2.3) enforces data class routing — each zone has an explicit data policy

**Gaps:**
- "Local encrypted vault" for API keys is referenced but the vault implementation is not specified — encryption quality and access controls are undocumented
- HealthMCP manages family PHI (kid1/kid2 health data) but is still in "Planned" status — PHI controls are not yet enforced in production
- Blockchain audit logs on Polygon/Optimism are public by design — action metadata (actor, type, timestamps) is permanently and publicly visible on-chain

**Priority:** MEDIUM — credential hygiene policy is strong; implementation gaps in vault spec and planned MCP tooling remain

---

## AA09 — Insufficient Logging & Monitoring

**What it means here:** Agent actions occurring without an auditable trail — making incident response, compliance audits, and anomaly detection impossible across 23 repos and multiple LLM providers.

**Controls in place:**
- Comprehensive audit trail (§10.1): Every action logged with timestamp, actor identity, action type, input hash, output hash, governance decision, chain/zone, Recipe ID, and Scratchpad task ID
- Blockchain logging (§10.2): Immutable on-chain audit records on Polygon for cost efficiency; Ethereum for critical financial actions
- Incident severity classification: SEV-1 (kill switch, breach, fund loss) → immediate response; SEV-2 (scratchpad corruption) → human escalation
- Goose Protocol mandates Recipe ID on all coordinated actions — provides cross-agent trace correlation

**Gaps:**
- AuditMCP is "Planned" — blockchain logging is designed but not yet live in production; current audit trail is file/log-based only
- No named centralized log aggregation or alerting system (SIEM equivalent) — incidents may rely on manual review rather than automated detection
- `log_all_calls: true` is a declared requirement in §6.7 but no tooling enforces this uniformly across all MCP servers

**Priority:** MEDIUM — audit design is thorough; production deployment of AuditMCP is the critical implementation gap

---

## AA10 — Supply Chain Vulnerabilities

**What it means here:** Compromised third-party LLM providers (Claude API, OpenAI, Gemini), malicious or backdoored MCP servers, hostile skill/recipe updates, or poisoned dependencies in the 23 repos infecting the agent pipeline.

**Controls in place:**
- Skill Scanner in CI pipeline: Proposed skills go through a structured review workflow before reaching live agent context — prevents hostile skill injection into OpenClaw
- `tool_allowlist: true` in MCP security (§6.7): Only pre-approved tools can be invoked, limiting blast radius of a compromised MCP server
- LiteLLM gateway abstracts provider switching (§2.2): Compromise of one LLM provider does not grant it direct system access — it only affects inference output, which still passes through autonomy gates
- Tier B governance repos require Andrew approval for structural changes (§12): Prevents unauthorized modification of the canonical trust anchor documents

**Gaps:**
- No pinned or hashed dependency versions mentioned across the 23 repos — supply chain attacks via npm/pip package compromise are unaddressed
- Ollama local models (gemma4:e4b, qwen3 family) pulled from public registries without documented integrity verification
- `fuzzywigg/project-template` (private) is the canonical AGENTS.md source; if compromised, all new repos inherit hostile governance from the ground up
- Third-party LLM providers are treated as Medium-trust but their model fine-tuning, system-prompt behaviors, and infrastructure security are entirely out of scope for local controls

**Priority:** HIGH — dependency pinning absent; canonical template is a high-value single point of compromise

---

## CI / Compliance Checklist

Run this checklist at PR review time and on any governance amendment. Agents MUST verify all passing items before declaring a feature or integration compliant.

### Identity & Trust (→ AA04)
- [ ] Action actor is identified and maps to a declared trust level (§4.1)
- [ ] No automated agent claims `absolute` or `high` trust for any operation
- [ ] `agent.smtp.eth` sub-identity used for all automated operations, never the primary `smtp.eth` identity

### Prompt & Input Safety (→ AA01, AA03)
- [ ] No user-supplied or external content is treated as system-level instruction without explicit sanitization
- [ ] Scratchpad writes are scoped to the agent's declared task; no writes to other agents' namespaces
- [ ] MCP tool inputs are validated against declared schemas before dispatch
- [ ] Kill switch file (`.kill_switch`) is absent at session start

### Output Safety (→ AA02)
- [ ] Agent-generated code or commands require human approval before execution in L0/L1 contexts
- [ ] Tier C auto-merge is blocked if agent-generated content includes shell commands or infra changes
- [ ] Output hash logged to audit trail per §10.1

### Data Handling (→ AA06, AA08)
- [ ] All cloud-zone transmissions pass through PHI redaction (§7.2 token list verified)
- [ ] No API keys, session tokens, or private keys appear in logs, git diff, or MCP payloads
- [ ] Goose recipes with `network_zone: cloud` have `phi_guard: true` set
- [ ] MEMORY.md is NOT loaded in group chat, Discord, or non-1:1 sessions

### Autonomy & Scope (→ AA05)
- [ ] Declared autonomy level does not exceed L1 without explicit smtp.eth approval
- [ ] No Tier D repo is modified, forked, or refactored without explicit direction
- [ ] Financial operations stay within approved budget; >10x triggers kill switch (§3.3)
- [ ] L3 (Autonomous) mode not used until guardrails are formally specified

### MCP / Plugin Security (→ AA07)
- [ ] All MCP servers present bearer token or mTLS credential before tool calls are accepted
- [ ] Tool allowlist reviewed; no undeclared tools invoked during this session
- [ ] `openclaw_geryon` is NOT used in production until RED security status is resolved (§2.1)
- [ ] AuditMCP status confirmed — if still "Planned", note the monitoring gap in the PR description

### Logging & Audit (→ AA09)
- [ ] Every agent action produces an audit record with all §10.1 required fields
- [ ] Recipe ID and Scratchpad task ID included for all Goose Protocol coordinated actions
- [ ] Incident classification applied if any SEV-1/SEV-2 condition is observed during this session

### Supply Chain (→ AA10)
- [ ] New MCP servers reviewed against §6.7 requirements before being added to tool allowlist
- [ ] Skill proposals pass Skill Scanner review before activation in OpenClaw
- [ ] Changes to `project-template` require Andrew approval (Tier B governance, §12)
- [ ] New third-party dependencies have pinned versions; document any waiver explicitly
- [ ] Ollama model pulls are from the expected registry and version

---

*Generated: 2026-06-30 | Based on AGENTS-ECOSYSTEM.md v2.3.0 | Maintained by smtp.eth*
