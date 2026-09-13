# Publishing this wiki outline to GitHub Wiki

```yaml
status: ACTIVE
created: "2026-09-13"
purpose: "Reversible publish path for docs/wiki → GitHub Wiki"
closes: "#16"
```

The Markdown under `docs/wiki/` is the **in-repo source** for the public wiki
outline. GitHub Wiki is a separate git repo
(`https://github.com/fuzzywigg/agents-governance.wiki.git`) that must be
initialized once (Settings → Features → Wikis, then create the first page or
push `Home.md`).

## Pages to publish

| Source file | Wiki page |
|-------------|-----------|
| `Home.md` | Home (landing) |
| `Overview.md` | Overview |
| `Autonomy-Levels.md` | Autonomy-Levels |
| `Repo-Stewardship.md` | Repo-Stewardship |
| `Agent-Routing.md` | Agent-Routing |
| `Security-Boundaries.md` | Security-Boundaries |

Do **not** push `PUBLISH.md` to the wiki (operator instructions only).

When copying `Home.md` / `Repo-Stewardship.md` to the wiki, rewrite relative
`../badge-standard.md` links to:

`https://github.com/fuzzywigg/agents-governance/blob/main/docs/badge-standard.md`

and drop the in-repo `PUBLISH.md` bullet from Home.

## One-shot publish (after wiki exists)

```bash
# From a clean worktree of agents-governance
git clone https://github.com/fuzzywigg/agents-governance.wiki.git /tmp/agents-governance.wiki
cp docs/wiki/Home.md \
   docs/wiki/Overview.md \
   docs/wiki/Autonomy-Levels.md \
   docs/wiki/Repo-Stewardship.md \
   docs/wiki/Agent-Routing.md \
   docs/wiki/Security-Boundaries.md \
   /tmp/agents-governance.wiki/
cd /tmp/agents-governance.wiki
git add Home.md Overview.md Autonomy-Levels.md Repo-Stewardship.md Agent-Routing.md Security-Boundaries.md
git commit -m "docs: publish public wiki outline from docs/wiki (#16)"
git push origin master   # or main — match the wiki default branch
```

If clone fails with "Repository not found", the wiki has never been initialized:
create any page once in the GitHub UI, then re-run the clone.

## Acceptance checks

- [ ] Wiki Home links back to the repository [README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)
- [ ] No secrets, private MEMORY, or private-template internals in published pages
- [ ] In-repo `docs/wiki/` remains the editable source; wiki push is a copy
- [ ] Link Check and Markdown Lint stay green on the PR that updates sources

## Fallback

Until the `.wiki.git` remote exists, treat
[Home.md](./Home.md) in this directory as the public landing page linked from the README.
