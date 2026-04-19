# Changelog

All notable changes to the agents-governance framework are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [2.3.0] — 2026-04-19

### Added

- AGENTS-ECOSYSTEM.md §2.1 expanded to full 22-repo, 4-tier portfolio
  (Tier A Active, Tier B Governance, Tier C Infrastructure, Tier D Dormant)
  plus a Tier Summary
- AGENTS-ECOSYSTEM.md §2.1.1: reference to `fuzzywigg/project-template` as the
  canonical AGENTS.md v1.0 template (4 execution modes, implementation-plan
  requirement, agent routing convention, Tier-1/Tier-2 governance structure,
  7 flavor branches)
- Appendix B: Caveman context compression — optional
  `project-template/scripts/compress-context.py` for ~40% governance-file
  token reduction
- README.md: ecosystem snapshot table, project-template usage flow,
  compression note

### Changed

- AGENTS-ECOSYSTEM.md front matter: version bumped to 2.3.0, `last_updated`
  2026-04-19, added `ecosystem_size` and `template_source` keys
- Domain Portfolio table extended to include `meromhouse.org`, `g0p.us`,
  `g0p.ai` with tier annotations
- README.md version stamp bumped to 2.3.0

---

## [Pre-2.3.0 Unreleased]

### Added

- `CLAUDE.md` — Copilot surface rules and critical file registry
- `AGENTS.md` — Repo-specific governance instance (using own template)
- `LICENSE` — MIT license file (previously only stated in README)
- `CONTRIBUTING.md` — Contribution guidelines and approval matrix
- `SECURITY.md` — Vulnerability reporting and severity levels
- `scratchpad/ecosystem.txt` — Ecosystem-wide inter-agent coordination state
- `scratchpad/incidents.txt` — Active incident log
- `docs/agent-hydration.md` — Full hydration findings report
- `.github/ISSUE_TEMPLATE/` — Issue templates (governance-gap, documentation-error, feature-request)
- `.github/pull_request_template.md` — Standardized PR template
- `.github/CODEOWNERS` — Code ownership for protected files
- `.github/workflows/markdown-lint.yml` — CI: markdownlint on all .md files
- `.github/workflows/link-check.yml` — CI: weekly + PR broken link detection
- `.markdownlint.json` — Lint configuration (line-length relaxed, HTML allowed)

---

## [2.2.0] — 2025-12-13

### Added

- Enhanced Section 6: Multi-Agent Coordination (Goose Protocol)
- Ecosystem-wide architecture diagram
- MCP Server Registry table
- Scratchpad hierarchy documentation
- Cross-project coordination protocol
- Recipe governance rules
- Audit requirements for Goose
- Appendix A: Goose Protocol Resources
- Appendix B: Quick Commands

---

## [2.1.0] — 2025-12-13

### Added

- Initial ecosystem governance document (`AGENTS-ECOSYSTEM.md`)
- Repository-specific template (`templates/AGENTS-REPO.md`)
- README with usage documentation

---

## [2.0.0] — 2025-12-13

### Changed

- Separated ecosystem governance from repo-specific AGENTS.md
