# Deploying the wiki

## Architecture (best practice)

| Role | Repository | URL |
|------|------------|-----|
| **Source of truth** (team edits) | [metamorphosisbd/odoo_wiki_metamorphosis](https://github.com/metamorphosisbd/odoo_wiki_metamorphosis) | Private org repo |
| **Public site** (GitHub Pages) | [MusfiqurTuhin/odoo_wiki_metamorphosis](https://github.com/MusfiqurTuhin/odoo_wiki_metamorphosis) | https://musfiqurtuhin.github.io/odoo_wiki_metamorphosis/ |

Edit links in the wiki point to the **org repo**. The personal repo is a public mirror for hosting only.

## After making changes

```bash
./scripts/push_all.sh
```

Or manually:

```bash
git push origin main    # org — canonical
git push pages main     # personal — triggers Pages deploy
```

## Git remotes

```bash
git remote -v
# origin → metamorphosisbd/odoo_wiki_metamorphosis
# pages  → MusfiqurTuhin/odoo_wiki_metamorphosis
```

## CI

| Repo | Workflow | Purpose |
|------|----------|---------|
| Org | `wiki.yml` | Build + upload artifact (no Pages on org plan) |
| Personal | `pages.yml` | Build + deploy GitHub Pages |

## Optional: auto-deploy from org only

Add org secret `PERSONAL_GITHUB_TOKEN` (fine-grained PAT with write access to `MusfiqurTuhin/odoo_wiki_metamorphosis`). Then enable `.github/workflows/deploy-external-pages.yml` on the org repo so a single `git push origin main` updates the live site.

## Internal server alternative

```bash
python scripts/generate_wiki.py
mkdocs build
# rsync site/ to nginx
```
