# Changelog

All notable changes to the agents-governance framework are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

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
