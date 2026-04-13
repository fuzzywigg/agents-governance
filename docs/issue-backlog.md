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

**Status:** ✅ RESOLVED — Created during hydration on 2026-04-13:
- `.github/workflows/markdown-lint.yml`
- `.github/workflows/link-check.yml`
- `.markdownlint.json`

---

### [P2-2] [copilot] Add CONTRIBUTING.md and SECURITY.md

**Status:** ✅ RESOLVED — Created during hydration on 2026-04-13.

---

### [P2-3] [copilot] Add .github/CODEOWNERS

**Status:** ✅ RESOLVED — `.github/CODEOWNERS` created during hydration on 2026-04-13.

---

### [P2-4] [claude-cowork] Populate projects registry and align downstream repos

**Status:** 🔜 PENDING — Requires Andrew decision on project table (nft2.me, owl-visuals status).

**Problem:** `README.md` lists `nft2.me` as "Pending" and `owl-visuals` as "Planned" in the "Projects Using This Governance" table. Neither has an active AGENTS.md. The table is aspirational, not factual.

**Proposed Solution:**
1. Update README table to distinguish between repos with active AGENTS.md vs. planned ones
2. Open tracking issues in each downstream repo to adopt the template
3. Add `fuzzywigg-ai` AGENTS.md link to README (it's listed as Active with ✅)

**Acceptance Criteria:**
- [ ] README table accurately reflects which repos have an active AGENTS.md
- [ ] fuzzywigg-ai AGENTS.md URL linked
- [ ] nft2.me and owl-visuals have tracking issues opened

**Routing:** claude-cowork | P2 | Branch: amendment/update-projects-registry | Deps: none

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

**Problem:** `AGENTS-ECOSYSTEM.md` Appendix B references `python scripts/validate_recipes.py` but the `scripts/` directory and this script do not exist. Any agent following Appendix B instructions will encounter a file-not-found error.

**Proposed Solution:**
1. Create `scripts/validate_recipes.py` as a stub that validates Goose recipe YAML format
2. Validate: `name`, `recipe.version`, `recipe.settings.autonomy_level`, `recipe.settings.network_zone` fields
3. Add usage to Appendix B in AGENTS-ECOSYSTEM.md

**Acceptance Criteria:**
- [ ] `python scripts/validate_recipes.py` exits 0 for valid YAML, non-zero for invalid
- [ ] Script validates all required Goose recipe fields per §6.2
- [ ] Appendix B command in AGENTS-ECOSYSTEM.md points to correct path

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
| 2 | [P2-4] Projects registry | claude-cowork | 🔜 Pending |
| 2 | [P2-5] Branch protection | human | 🔜 HITL |
| 3 | [P3-1] Notion sync | claude-cowork | 🔜 HITL |
| 3 | [P3-2] CHANGELOG | copilot | ✅ Done |
| 3 | [P3-3] Recipe validator | copilot | 🔜 Pending |
| 3 | [P3-4] Contract address | human | 🔜 HITL |
