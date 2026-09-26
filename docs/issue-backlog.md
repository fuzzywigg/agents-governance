# Issue Backlog — agents-governance

```yaml
status: ACTIVE
tier: 1
created: "2026-04-13"
owner: copilot
edit_policy: "Agent-editable; structural changes require Andrew approval"
note: "Issues below are ready to be created in GitHub. Agent surface: copilot can create them on next run with write credentials."
```

---

## Phase 1 — Foundation (P1)

### [P1-1] [copilot] Add LICENSE file

**Status:** ✅ RESOLVED — `LICENSE` (MIT) was created during hydration on 2026-04-13.

---

### [P1-2] [copilot] Create scratchpad/ directory with ecosystem.txt and incidents.txt

**Status:** ✅ RESOLVED — `scratchpad/ecosystem.txt` and `scratchpad/incidents.txt` created during hydration on 2026-04-13.

---

### [P1-3] [copilot] Add GitHub issue templates and PR template

**Status:** ✅ RESOLVED — Created during hydration on 2026-04-13:

- `.github/ISSUE_TEMPLATE/governance-gap.md`
- `.github/ISSUE_TEMPLATE/documentation-error.md`
- `.github/ISSUE_TEMPLATE/feature-request.md`
- `.github/pull_request_template.md`

---

## Phase 2 — Hardening (P2)

### [P2-1] [copilot] Add CI/CD: markdown lint and broken link checking

**Status:** ✅ RESOLVED — Created during hydration on 2026-04-13; tip now also runs
stewardship gates (ECO-017+). Live workflows (do not claim absent):

- `.github/workflows/markdown-lint.yml` — `checkout@v7` + `markdownlint-cli2-action@v24`
- `.github/workflows/link-check.yml` — `checkout@v7` + `lychee-action@v2` (not markdown-link-check)
- `.github/workflows/stewardship-checks.yml` — `checkout@v7` + `setup-python@v5` (intentional pin)
- `.markdownlint.json`

---

### [P2-2] [copilot] Add CONTRIBUTING.md and SECURITY.md

**Status:** ✅ RESOLVED — Created during hydration on 2026-04-13.

---

### [P2-3] [copilot] Add .github/CODEOWNERS

**Status:** ✅ RESOLVED — `.github/CODEOWNERS` created during hydration on 2026-04-13.

---

### [P2-4] [claude-cowork] Populate projects registry and align downstream repos

**Status:** 🔜 PENDING HITL — Requires Andrew decision on portfolio registry
(nft2.me / owl-visuals naming if they should appear anywhere).

**Problem:** Tip `README.md` does **not** have a "Projects Using This Governance"
table claiming `nft2.me` "Pending" / `owl-visuals` "Planned" — do **not** reopen
that claim. Tip README uses the Ecosystem Snapshot tiers instead (`nft2.me` appears
only under Tier D dormant wording; `owl-visuals` is absent from tip README).
Remaining work is HITL registry alignment (AGENTS-ECOSYSTEM §2.1 / downstream
adoption), not inventing a README projects table overnight.

**Proposed Solution:**

1. Andrew decides whether `nft2.me` / `owl-visuals` need registry or tracking updates
   (ecosystem map vs. leave dormant / omit)
2. If adoption tracking is wanted: open issues in the relevant downstream repos
3. Optionally link live AGENTS.md URLs for Active Tier C surfaces (e.g. fuzzywigg-ai)
   — only when a real public URL exists; do not invent rows

**Acceptance Criteria:**

- [ ] Tip honesty: backlog never claims README has a Pending/Planned "Projects Using
      This Governance" table
- [ ] Andrew decision recorded for nft2.me / owl-visuals (keep dormant / omit / track)
- [ ] Any README or ecosystem-map edits match live tip (no invented project rows)

**Routing:** claude-cowork | P2 | Branch: amendment/update-projects-registry | Deps: Andrew HITL

---

### [P2-5] [human] Enable branch protection on main

**Status:** 🔜 PENDING HITL — Requires Andrew to configure via GitHub Settings.

**Problem:** `main` branch has no protection rules. Any agent with push access could directly commit to `main`, bypassing the PR + review requirement stated in AGENTS-ECOSYSTEM.md §12.1.

**Proposed Solution:**

- Require PRs before merging to `main`
- Require at least 1 approval
- Dismiss stale approvals on new commits
- Block force pushes

**Acceptance Criteria:**

- [ ] Direct pushes to `main` are blocked
- [ ] PRs require at least 1 review
- [ ] Branch protection visible in GitHub Settings > Branches

**Routing:** human (browser-claude can assist with GitHub Settings UI) | P2 | Deps: none

---

## Phase 3 — Optimization (P3)

### [P3-1] [claude-cowork] Sync repo findings to Notion Master Index

**Status:** 🔜 PENDING HITL — Requires Notion credentials and Master Index parent page ID.

**Problem:** Per the hydration protocol, Notion is the truth for policies/decisions. This repo has no Notion page under the Master Index. Cross-system alignment is incomplete.

**Proposed Solution:**

1. claude-cowork searches Notion workspace for existing agents-governance page
2. If absent: creates page under Active Sprint Work with metadata header
3. Links to GitHub hydration report, roadmap issue, and CHANGELOG

**Acceptance Criteria:**

- [ ] Notion page exists for agents-governance under Master Index
- [ ] Page links to GitHub (not duplicates content)
- [ ] Page includes metadata header per governance standard

**Routing:** claude-cowork | P3 | Deps: none

---

### [P3-2] [copilot] Add CHANGELOG.md

**Status:** ✅ RESOLVED — `CHANGELOG.md` created during hydration on 2026-04-13.

---

### [P3-3] [copilot] Add recipe validation script stub (scripts/validate_recipes.py)

**Status:** 🔜 PENDING — Low priority.

**Problem:** `AGENTS-ECOSYSTEM.md` Appendix B references `python scripts/validate_recipes.py`,
but that script is **not** on tip. Do **not** claim `scripts/` is absent — tip already has a
live stewardship `scripts/` tree (`run_stewardship_checks.sh`, `test_stewardship_gates.py`,
`check_*.py`, etc.). Agents following Appendix B's recipe-validator command still hit
file-not-found for `validate_recipes.py` only.

**Proposed Solution:**

1. Create `scripts/validate_recipes.py` as a stub that validates Goose recipe YAML format
   (alongside existing stewardship scripts — do not invent a second `scripts/` tree)
2. Validate: `name`, `recipe.version`, `recipe.settings.autonomy_level`, `recipe.settings.network_zone` fields
3. Add usage to Appendix B in AGENTS-ECOSYSTEM.md

**Acceptance Criteria:**

- [ ] `python scripts/validate_recipes.py` exits 0 for valid YAML, non-zero for invalid
- [ ] Script validates all required Goose recipe fields per §6.2
- [ ] Appendix B command in AGENTS-ECOSYSTEM.md points to correct path
- [ ] Tip honesty: backlog never claims the whole `scripts/` directory is missing

**Routing:** copilot | P3 | Branch: copilot/add-recipe-validator | Deps: Andrew approval for AGENTS-ECOSYSTEM.md edit

---

### [P3-4] [copilot] Resolve blockchain audit contract address placeholder

**Status:** 🔜 PENDING HITL — Requires Andrew.

**Problem:** `AGENTS-ECOSYSTEM.md §10.2` shows `contract: "0x..."` as a placeholder. If this is meant to be a real deployed contract, the placeholder creates ambiguity for agents reading audit requirements.

**Proposed Solution:** Either populate with a real address or add a note explicitly marking it as TBD/planned.

**Routing:** human | P3 | Deps: Andrew to provide address or confirm not-yet-deployed

---

## Roadmap Summary

| Phase | Issue | Surface | Status |
|-------|-------|---------|--------|
| 1 | [P1-1] LICENSE | copilot | ✅ Done |
| 1 | [P1-2] scratchpad/ | copilot | ✅ Done |
| 1 | [P1-3] Issue/PR templates | copilot | ✅ Done |
| 2 | [P2-1] CI/CD workflows | copilot | ✅ Done |
| 2 | [P2-2] CONTRIBUTING + SECURITY | copilot | ✅ Done |
| 2 | [P2-3] CODEOWNERS | copilot | ✅ Done |
| 2 | [P2-4] Projects registry | claude-cowork | 🔜 HITL |
| 2 | [P2-5] Branch protection | human | 🔜 HITL |
| 3 | [P3-1] Notion sync | claude-cowork | 🔜 HITL |
| 3 | [P3-2] CHANGELOG | copilot | ✅ Done |
| 3 | [P3-3] Recipe validator | copilot | 🔜 Pending |
| 3 | [P3-4] Contract address | human | 🔜 HITL |
