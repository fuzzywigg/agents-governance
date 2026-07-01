# OWASP Agentic AI Top 10 — fuzzywigg Ecosystem Mapping

```
version: 1.0.0
date: 2026-07-01
scope: Geryon Toborberg / OpenClaw / claw-mcp / agents-governance
reference: https://owasp.org/www-project-agentic-ai-top-10/
```

---

## Executive Summary

The Geryon ecosystem is a local-first, self-custodied AI agent stack built on OpenClaw (runtime), claw-mcp (tool server), and agents-governance (policy layer). This mapping evaluates each OWASP Agentic AI Top 10 risk against existing controls and identifies gaps where additional hardening is needed. Overall posture is moderate: strong on access scoping and kill-switch mechanics, weaker on structured memory validation, formal audit retention, and cross-agent impersonation resistance.

---

## AA01 — Agent Memory Poisoning

**Risk:** Malicious or corrupted data injected into agent memory (context documents, retrieved memories, tool outputs) that alters the agent's future behavior, values, or outputs.

**Ecosystem controls:**

- **Layered context architecture**: SOUL.md (identity, read-only), AGENTS.md (operational rules), USER.md (user profile), and daily `memory/YYYY-MM-DD.md` files are separate files with defined roles. An attacker would need to compromise multiple distinct files to alter core behavior.
- **MEMORY.md session isolation**: MEMORY.md is explicitly prohibited from loading in group chats, Discord, Slack, or shared contexts. This limits the blast radius of poisoned long-term memory by preventing exfiltration or weaponized recall in public channels.
- **SOUL.md read-only policy**: AGENTS.md specifies SOUL.md (core identity) must not be altered without explicit human approval. This creates a protected root of identity that resists drift from injected instructions.
- **Daily log granularity**: Short-lived `memory/YYYY-MM-DD.md` files contain recent context. Poisoning one day's log has limited forward persistence since logs are periodically distilled into MEMORY.md under human review.
- **Git commit history**: All memory file changes are committed to a git repository, providing a tamper-evident trail and rollback capability.

**Gaps:**

- No cryptographic signing or integrity verification on context files. A compromised filesystem write silently alters any document.
- No automated anomaly detection on memory content — injected instructions phrased as legitimate notes pass through undetected.
- MCP tool outputs (web search, file fetch) are injected into context without sanitization or structural validation, creating a live prompt-injection vector through tool results.
- No formal schema/validation for MEMORY.md entries — any text format is accepted.

**Risk Level:** 🟠 Medium-High

**Gap:** Unsigned, unvalidated context files; unsanitized MCP tool output in context window.

**Recommended next step:** Implement a memory entry schema (YAML frontmatter with `source`, `timestamp`, `trust_level`) and add a pre-commit hook that rejects entries lacking provenance metadata.

---

## AA02 — Tool / Function Abuse

**Risk:** An agent is manipulated into misusing available tools — executing destructive operations, abusing API rate limits, exfiltrating data, or taking unintended actions via tool calls.

**Ecosystem controls:**

- **`tools.deny` blocklist in openclaw.json**: Specific tools or tool patterns can be explicitly denied at the gateway level, preventing them from being invoked regardless of what the model decides.
- **Explicit permission prompts**: The Claude Code harness requires user approval for tools that are not in the `tools.allow` list, creating a human-in-the-loop gate for non-routine tool use.
- **Autonomy tiers (L0/L1/L2)**: AGENTS.md defines autonomy levels. L0 requires approval for all external actions; L1 allows routine reads; L2 permits writes within scoped boundaries. Tool abuse outside tier bounds requires escalation.
- **Hard rules in AGENTS.md**: Explicit prohibitions on destructive commands (`rm`, data exfiltration, financial transactions, sending external messages without approval) are part of the operational constitution.
- **claw-mcp tool scope**: The 37 tools in claw-mcp are organized by domain (GitHub, notifications, search). Tool access can be scoped per-session, limiting what's reachable.
- **Reversibility preference**: AGENTS.md mandates using `trash` over `rm` and preferring reversible actions, reducing blast radius.

**Gaps:**

- No rate-limit enforcement on claw-mcp tool calls — a runaway loop can exhaust GitHub API quotas or send hundreds of Slack messages before human intervention.
- No inter-tool dependency validation — an agent could chain tools (search → write → push) in unintended ways that individually pass permission checks but collectively execute a harmful workflow.
- The `tools.allow` list in `settings.json` accumulates over time via the `fewer-permission-prompts` skill, potentially broadening the auto-approved surface area without periodic review.

**Risk Level:** 🟡 Medium

**Gap:** No rate limiting; no chain-of-tool workflow validation; `tools.allow` drift.

**Recommended next step:** Add per-tool rate limit counters to claw-mcp (e.g., max N calls/minute per tool category) and schedule a quarterly review of the `tools.allow` list.

---

## AA03 — Agent Impersonation

**Risk:** A malicious agent or external actor impersonates a trusted agent (or the human principal) to hijack workflows, escalate privileges, or extract sensitive context.

**Ecosystem controls:**

- **Single-agent architecture**: The current ecosystem runs one primary agent (Geryon) rather than a multi-agent mesh. Reducing the number of agent identities reduces impersonation surface.
- **Session origin tagging**: Subagent context blocks include a `Requester session` field identifying the spawning agent and channel. This provides lightweight provenance for task delegation.
- **Human-in-the-loop for sensitive actions**: Sending external messages, pushing code, and making financial operations require explicit human approval, making impersonation-triggered actions visible before execution.
- **SOUL.md identity anchor**: The agent's identity, values, and voice are defined in a version-controlled file. Behavioral drift (a soft form of impersonation) is detectable via git diff.

**Gaps:**

- No cryptographic authentication between the main agent and subagents. A rogue process injecting content formatted as a `[Subagent Task]` block could be treated as a legitimate delegation.
- No session token or signed nonce verifying that a `Requester session` field is authentic.
- Cross-channel impersonation is unmitigated — an attacker who can post to Slack or Discord channels the agent monitors could issue instructions formatted as legitimate agent output.
- No formal registry of known-good agent identities; the ecosystem has no way to distinguish a real Geryon subagent from a spoofed one.

**Risk Level:** 🔴 High (structural gap in multi-agent trust model)

**Gap:** No cryptographic session identity; no message-origin authentication; channel-injection impersonation possible.

**Recommended next step:** Define a signed delegation token spec for subagent spawning — even a simple HMAC over `{requester_id, task_hash, timestamp}` — and verify it in the subagent context parser.

---

## AA04 — Insufficient Access Control

**Risk:** The agent operates with excessive permissions — reading files it shouldn't, calling APIs beyond task scope, or persisting credentials available to all sessions.

**Ecosystem controls:**

- **Tier/Autonomy system (L0/L1/L2)**: Defined in per-repo AGENTS.md files. Each repo can declare its own autonomy level, scoping what the agent is permitted to do within that context without human approval.
- **Per-repo AGENTS.md**: Governance rules are co-located with the code they govern, making it easy to audit and diff what permissions apply per project.
- **MEMORY.md group-chat restriction**: Sensitive long-term memory is withheld from group channels, enforcing a coarse-grained access boundary between session types.
- **`tools.deny` and `tools.allow` in settings**: Explicit allowlist/denylist at the harness level constrains what the agent can call.
- **Hard-coded prohibitions**: AGENTS.md lists categories of action (financial, destructive, external messaging) that require escalation regardless of tier.

**Gaps:**

- Tier assignments in AGENTS.md are advisory text, not machine-enforced — there is no runtime that reads the autonomy level and enforces it programmatically. Compliance depends on the model following instructions.
- No attribute-based access control (ABAC) — permissions are coarse (L0/L1/L2) rather than fine-grained (e.g., "can read issues but not push to main").
- claw-mcp grants access to all 37 tools unless individually denied; there is no allowlist-by-default posture.
- Subagents inherit tool access from the parent session; there is no privilege reduction when spawning a restricted subagent.

**Risk Level:** 🟡 Medium

**Gap:** Autonomy tiers are model-enforced, not runtime-enforced; claw-mcp is denylist-by-default rather than allowlist-by-default; subagents are not privilege-reduced.

**Recommended next step:** Add a machine-readable `autonomy.json` schema (parseable by OpenClaw) that maps L0/L1/L2 to specific tool permission sets, and enforce it at the gateway level rather than relying on model instruction-following.

---

## AA05 — Insufficient Kill Switch

**Risk:** No reliable mechanism exists to stop, pause, or roll back an agent that is misbehaving or executing an unintended action chain.

**Ecosystem controls:**

- **`tools.deny` in openclaw.json**: Specific tools can be added to the deny list in the gateway config, taking effect on the next request. This is a soft kill for targeted tool categories.
- **`openclaw gateway restart`**: Documented in AGENTS.md as an emergency stop mechanism. Restarting the gateway terminates active sessions and clears in-flight context.
- **Human approval gates**: Sensitive actions require explicit user confirmation before execution — the human can deny at any approval prompt, which functions as an inline kill switch for that action.
- **`/stop` and `/pause` compliance**: AGENTS.md states the agent must obey stop/pause/audit commands and never bypass safeguards — this is a behavioral kill-switch backed by identity (SOUL.md).
- **No auto-push / no-force-push policy**: The agent will not push to remote repositories without explicit instruction, preventing runaway commits.
- **Reversibility preference**: Actions taken before a kill are more likely to be undoable (trash vs rm, draft vs send).

**Gaps:**

- Kill is not atomic. Between a human issuing a stop and the gateway restart completing, in-flight tool calls (e.g., a GitHub push, a Slack message) may complete. There is no pre-emptive tool-call cancellation.
- No `SIGTERM` handler in claw-mcp — a kill signal to the gateway does not cancel pending HTTP requests to external APIs.
- No "circuit breaker" pattern — if a tool call fails repeatedly, there is no automatic throttle or halt; the agent can be prompted to retry indefinitely.
- The kill switch (gateway restart) requires shell access to the WSL host. If the host is unavailable or the agent has spawned background processes, the kill is incomplete.
- No audit event emitted on kill — there is no record of when and why the gateway was restarted.

**Risk Level:** 🟡 Medium

**Gap:** Non-atomic kill; no in-flight cancellation; no circuit breaker; kill requires local host access.

**Recommended next step:** Add a `/api/emergency-stop` endpoint to the OpenClaw gateway that (1) sets a global halt flag checked before each tool dispatch, (2) emits an audit event, and (3) returns 503 for all subsequent tool calls until manually cleared.

---

## AA06 — Excessive Data Exposure

**Risk:** The agent leaks PII, secrets, or sensitive context to unauthorized parties — via tool outputs, log files, group channels, or injected memory.

**Ecosystem controls:**

- **MEMORY.md group-chat restriction**: The most sensitive long-term memory file is explicitly prohibited from loading in group contexts. This is the single most important data exposure control in the ecosystem.
- **Session-type awareness**: AGENTS.md distinguishes main (1:1), group chat, heartbeat, and cron session types with different data loading rules per type.
- **No secrets in repos**: TOOLS.md and AGENTS.md explicitly prohibit committing API keys or credentials to any repository.
- **`wrangler secret put` pattern**: Secrets are pushed to Workers KV rather than stored in plaintext files accessible to the agent.
- **SOUL.md data-handling ethics**: The agent's identity includes a commitment to privacy preservation and local-first data handling.
- **PII tiers (emerging)**: The ecosystem references PII sensitivity tiers (IDEM sensitivity) though these are not yet formally codified.

**Gaps:**

- No automated PII detection in outbound messages. The agent can forward PII from context documents to Slack/Discord without a scrubbing step.
- Daily memory files (`memory/YYYY-MM-DD.md`) are written in plaintext and committed to git with no field-level encryption. A compromised repo leaks all logged context.
- claw-mcp tool responses (e.g., GitHub issue bodies, email content) are passed into the context window without a data-minimization step — full payloads are ingested even when only metadata is needed.
- No formal data retention or deletion policy for memory files — stale PII can persist indefinitely.
- Group-chat restriction on MEMORY.md is a behavioral rule, not a technical enforcement — if the model ignores the instruction, the data loads.

**Risk Level:** 🟠 Medium-High

**Gap:** No outbound PII scrubbing; plaintext memory at rest; no data minimization on tool responses; behavioral-only enforcement of MEMORY.md restriction.

**Recommended next step:** Add a pre-send content filter (regex + LLM classifier) that scans outbound message content for PII patterns before the `message` tool dispatches to any channel.

---

## AA07 — Insufficient Tool Chain Oversight (MCP Security)

**Risk:** MCP-connected tool servers expose broad capabilities without adequate inspection, sandboxing, or logging of what tools were called, with what arguments, and what they returned.

**Ecosystem controls:**

- **claw-mcp server**: 37 tools organized by domain (GitHub, notifications, search, file ops, etc.). The server is locally hosted, reducing the attack surface compared to a third-party MCP provider.
- **Tool-level permissions**: Tool access can be denied at the gateway level via `tools.deny`. Specific tool names can be individually blocked.
- **Local-first posture**: claw-mcp runs on the same host as the gateway, so network exposure is minimal — no internet-accessible MCP endpoint exists by default.
- **Tool manifest awareness**: The agent knows the tool list (visible in system-reminder at session start), enabling it to reason about what is available.

**Gaps:**

- No per-tool argument schema validation — claw-mcp accepts arguments as passed by the model without input sanitization. A prompt-injected tool call with malicious arguments (e.g., a `shell_exec` path traversal) is not blocked at the server level.
- No structured logging of tool calls with full arguments and responses in a queryable audit log. Tool calls appear in daily memory files only if the agent explicitly records them.
- claw-mcp tools have no concept of "dry run" — there is no way to preview what a tool call will do before it executes.
- No tool call signing — the MCP server cannot verify that a tool invocation originated from the trusted OpenClaw gateway vs. a spoofed client.
- Tool return values are passed to the model context without size-capping or sensitivity classification — a large, PII-rich tool response fills the context window and is available to all subsequent reasoning.

**Risk Level:** 🟠 Medium-High

**Gap:** No argument sanitization; no structured tool audit log; no MCP-level authentication; no response size/sensitivity controls.

**Recommended next step:** Add structured JSON logging to claw-mcp (one log line per tool call: timestamp, tool name, arguments hash, response size, latency) and ship logs to a local append-only file for audit review.

---

## AA08 — Insecure Credential Handling

**Risk:** API keys, signing keys, or session tokens are stored, logged, or transmitted in ways that expose them to compromise — in plaintext files, git history, logs, or agent context.

**Ecosystem controls:**

- **No secrets in repos (hard rule)**: TOOLS.md and AGENTS.md prohibit committing credentials to any repository. This is reinforced as a "hard rule" in the agent constitution.
- **`wrangler secret put` pattern**: Cloudflare Workers secrets are pushed via the CLI rather than stored in `wrangler.toml` or env files committed to git.
- **MEMORY.md session isolation**: MEMORY.md (which might reference credential locations) is not loaded in group chats, limiting surface area for credential context leakage.
- **Keyring workaround**: Where OS keyring integration is available, credentials are stored outside the filesystem and out of the agent's direct read path.
- **SIGNING_KEY policy**: A documented policy exists for signing key handling, informed by a prior ETH key incident that established the "no keys in repos" rule as a hard lesson.
- **`gh auth` integration**: GitHub credentials are managed via the `gh` CLI credential store rather than plaintext tokens in config files.

**Gaps:**

- No automated secret scanning on commits (e.g., `git-secrets`, `truffleHog`, or GitHub secret scanning on the private repos). The no-secrets rule is behavioral, not technically enforced pre-commit.
- The agent can read any file on the WSL filesystem, including `.env` files, `.netrc`, browser credential stores, and SSH keys. If prompted or injected, it could log these to memory.
- claw-mcp has no mechanism to detect or redact secrets in tool arguments or responses — an API key in a GitHub issue body or Slack message passes through in plaintext.
- No credential rotation schedule or TTL enforcement. Long-lived tokens accumulate without review.
- Daily memory logs could capture partial credential context (e.g., a command output that echoes a masked token) without detection.

**Risk Level:** 🟡 Medium

**Gap:** No pre-commit secret scanning; agent has read access to local credential files; no secret redaction in tool pipeline; no rotation policy.

**Recommended next step:** Add `detect-secrets` as a pre-commit hook to the workspace repo and configure the Claude Code harness to deny `Read` tool calls targeting known credential file paths (`.env`, `~/.netrc`, `~/.ssh/id_*`).

---

## AA09 — Inadequate Audit Trail

**Risk:** Insufficient logging of agent decisions, tool invocations, memory reads/writes, and approval events makes it impossible to reconstruct what the agent did, why, and with whose authorization.

**Ecosystem controls:**

- **Daily memory files (`memory/YYYY-MM-DD.md`)**: Raw notes, task summaries, and events are logged per-day. This provides a human-readable narrative audit trail.
- **Git commit history**: All workspace file changes are committed to git with timestamps and commit messages. This is a tamper-evident (but not append-only) record.
- **Slack delivery logs**: Outbound messages sent via the `message` tool are recorded in Slack's own audit trail.
- **OpenClaw session labels**: Sessions carry labels (e.g., `owasp-governance`, `main`) that provide basic context for what session produced an output.
- **Requester session tagging**: Subagent context includes `Requester session` and `Requester channel`, enabling basic attribution of delegated actions.

**Gaps:**

- Memory files are narrative prose, not structured logs. They cannot be reliably parsed, queried, or aggregated for forensic analysis.
- Tool call arguments and return values are not systematically recorded — the audit trail shows "agent did X" but not "agent called tool Y with arguments Z and got response W."
- No immutable log store. Daily memory files can be edited or deleted; git history can be rewritten (`git push --force`). There is no append-only audit sink.
- No coverage of tool calls that happen within a session but are not mentioned in the day's memory note — silent tool executions leave no trace.
- No approval event logging — when a human approves or denies a tool call, that decision is not persisted anywhere outside the conversation transcript (which is ephemeral).
- No retention policy or SLA — old memory files accumulate indefinitely with no archival or deletion schedule.

**Risk Level:** 🔴 High (forensic gap)

**Gap:** Prose-only logs not queryable; no tool-call audit log; no immutable store; approval events not persisted; silent tool executions untracked.

**Recommended next step:** Implement a structured `audit.jsonl` append-only log at the OpenClaw gateway layer that captures: session_id, timestamp, tool_name, args_hash, response_size, approval_status, and user_id for every tool dispatch.

---

## AA10 — Unverified Skills / Plugins

**Risk:** Third-party or newly created agent skills/plugins are installed and executed without adequate review, allowing malicious or buggy extensions to compromise agent behavior.

**Ecosystem controls:**

- **Skill Workshop review process**: New skills go through a proposal → review → apply lifecycle. Generated skills are pending proposals by default and cannot be activated without explicit user approval.
- **`action=apply` requires explicit user request**: The `skill_workshop` tool's `apply` action is gated behind explicit user confirmation — the agent cannot self-install skills.
- **Skill proposal visibility**: Proposals are stored as files that can be inspected before applying. The content is visible to the user before activation.
- **No auto-update of installed skills**: Skills are applied at a point in time; they do not auto-update from a remote registry.
- **Local-first skill store**: Skills are stored locally in the workspace, not pulled from a third-party registry that could be compromised.

**Gaps:**

- No cryptographic signing of skill proposals — a compromised workspace write could alter a proposal file between review and apply without detection.
- No automated static analysis of skill content before apply (e.g., checking for shell injection patterns, excessive permission requests, or hardcoded credentials in the skill body).
- No skill isolation or sandboxing — once applied, a skill runs with the same process permissions as the main agent. A malicious skill has full tool access.
- No provenance tracking of skill origin — there is no record of who authored a skill, from what source, or whether it matches a known-good hash.
- Third-party MCP skills (future integration risk) would bypass the Skill Workshop if installed via `npx` or direct config edit rather than through the review pipeline.

**Risk Level:** 🟡 Medium

**Gap:** Unsigned proposals; no static analysis pre-apply; no sandbox; no origin provenance; direct MCP install bypasses review.

**Recommended next step:** Add a SHA-256 hash of each approved proposal to the skill's metadata at apply-time, and verify the hash matches at load-time — detecting tampering between approval and execution.

---

## Gap Summary Table

| Risk | ID | Status | Priority | Biggest Gap | Next Action |
|------|----|--------|----------|-------------|-------------|
| Memory Poisoning | AA01 | 🟡 Partial | High | Unsigned context files; unsanitized tool output | Memory entry provenance schema |
| Tool Abuse | AA02 | 🟡 Partial | Medium | No rate limiting; tools.allow drift | Per-tool rate limits in claw-mcp |
| Agent Impersonation | AA03 | 🔴 Weak | High | No session authentication; channel injection | Signed delegation tokens |
| Access Control | AA04 | 🟡 Partial | High | Tiers are model-enforced, not runtime-enforced | Machine-readable autonomy.json |
| Kill Switch | AA05 | 🟢 Good | Low | Non-atomic kill; no in-flight cancellation | `/api/emergency-stop` endpoint |
| Data Exposure | AA06 | 🟡 Partial | High | No outbound PII scrubbing; plaintext memory at rest | Pre-send PII content filter |
| MCP Tool Chain | AA07 | 🟡 Partial | High | No arg sanitization; no tool audit log | Structured claw-mcp audit log |
| Credential Handling | AA08 | 🟢 Good | Medium | No pre-commit secret scanning; agent reads filesystem | detect-secrets pre-commit hook |
| Audit Trail | AA09 | 🔴 Weak | Critical | Prose-only logs; no immutable store; silent tool calls | `audit.jsonl` at gateway layer |
| Skills / Plugins | AA10 | 🟡 Partial | Medium | Unsigned proposals; no sandbox; no provenance | SHA-256 hash verification at apply |

**Legend:** 🟢 Good (controls in place, minor gaps) | 🟡 Partial (meaningful controls, notable gaps) | 🔴 Weak (structural gap, controls insufficient)

---

## Implementation Roadmap

Ordered by risk reduction impact:

### 1. AA09 — Structured Audit Log (Critical)
Implement `audit.jsonl` at the OpenClaw gateway layer. Every tool dispatch writes one JSON line: `{ts, session_id, tool, args_hash, response_size_bytes, approved_by, latency_ms}`. This alone closes the single largest forensic gap — the inability to reconstruct what the agent actually did in a session. Cost: medium (gateway middleware change). Impact: unlocks all future audit and forensics work.

### 2. AA03 — Subagent Delegation Authentication (High)
Define and implement signed delegation tokens for subagent spawning. A simple HMAC-SHA256 over `{requester_session, task_hash, timestamp, nonce}` using a locally-stored gateway secret key. Subagent context parser rejects unsigned or expired delegation blocks. This closes the highest-severity structural gap (agent impersonation) with a self-contained, low-dependency implementation.

### 3. AA04 — Machine-Readable Autonomy Enforcement (High)
Convert AGENTS.md autonomy tiers (L0/L1/L2) to a `autonomy.json` schema parseable by OpenClaw gateway. Map each tier to an explicit `{tools_allowed, tools_denied, requires_approval}` policy. Gateway enforces this at dispatch time, removing reliance on model instruction-following for access control. This transforms the biggest "behavioral" control into a technical one.

### 4. AA01 / AA07 — Memory Provenance + Tool Audit Log (High)
Combined: (a) add YAML frontmatter with `source`, `timestamp`, and `trust_level` to all memory entries, with a pre-commit hook rejecting entries lacking provenance; (b) add JSON logging to claw-mcp for every tool call. These two changes together dramatically improve both memory integrity and tool chain visibility.

### 5. AA06 — Outbound PII Filter (Medium-High)
Add a pre-send content filter that classifies outbound message content before the `message` tool dispatches. Use a fast regex layer for common PII patterns (email, phone, SSN, API key patterns) plus an optional LLM classifier for higher-confidence screening. Applies to all `message` tool invocations targeting external channels. Closes the most user-visible data exposure vector.

---

*This document represents the ecosystem posture as of 2026-07-01. Controls marked 🔴 represent structural gaps that should be addressed before expanding agent autonomy or onboarding additional MCP tool servers.*

*Geryon 🦀 — From the deep.*
