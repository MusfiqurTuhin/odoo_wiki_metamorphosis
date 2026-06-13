# Requirements — manual input still needed

Auto-generation covers **~80%** from Niaj's scan. The items below cannot be inferred reliably and need owners.

## Critical (blocks accurate wiki)

| # | Item | Owner | Notes |
|---|------|-------|-------|
| 1 | **Git remote URLs** per project | Dev / Niaj | `project.yaml` → `git.remote_url` — run `git remote -v` in each repo |
| 2 | **Folder → client legal name** mapping | PM | e.g. `basb`, `mm_project`, `odoo17_custom` → real client names |
| 3 | **Client contacts** (name, email, role) | PM / Account manager | `project.yaml` → `client.contacts` |
| 4 | **Project brief** (2–5 sentences) | Project lead | Replace auto-generated `brief` in `project.yaml` |

## Per module (quality, not blocking)

| # | Item | Owner | Notes |
|---|------|-------|-------|
| 5 | **Version history + what's new** | Module author | Replace "Seeded from scan" rows; use git log on `__manifest__.py` |
| 6 | **Confirmed contributors** | Module author | Manifest `author` is a hint only — confirm via `git shortlog` |
| 7 | **marketing_summary** | Dev + marketing | Plain-language pitch; set `reusable: true` for productizable modules |
| 8 | **Module dependencies** | Module author | `depends[]` in front matter — from manifest `depends` |
| 9 | **Curated flag** | Reviewer | Set `curated: true` after review (generator will not overwrite) |

## Infrastructure

| # | Item | Owner | Notes |
|---|------|-------|-------|
| 10 | **GitHub repo** for wiki | Musfiq / DevOps | Update `repo_url` in `mkdocs.yml` |
| 11 | **Deploy target** | DevOps | GitHub Pages (private) or internal nginx |
| 12 | **Python 3.10+** on CI | DevOps | `pip install -r requirements.txt && mkdocs build` |
| 13 | **Scheduled scan** | Niaj | Cron weekly: `scan_modules.py` → commit `data/odoo_module_inventory.md` → `generate_wiki.py` |

## Optional enhancements

| # | Item | Benefit |
|---|------|---------|
| 14 | `enrich_git.py` — git log on manifests | Auto version history |
| 15 | Pre-commit in addon repos | Wiki stays in sync on release |
| 16 | Odoo version per project confirm | Some folders mix versions |
| 17 | Excel export from wiki YAML | Management reports without duplicate data entry |
| 18 | SSO on deployed site | Management access |

## Developer checklist (each team member)

1. Run `python scripts/scan_modules.py` from your addons root (same filters as Niaj).
2. Send `odoo_module_inventory.md` diff or PR to wiki repo `data/`.
3. For modules you own: open `docs/projects/<project>/modules/<name>.md`, fix brief, contributors, versions, set `curated: true`.
4. For projects you lead: fill `project.yaml` client + git fields.

## What is already done

- [x] Parse full `odoo_module_inventory.md` (38 projects)
- [x] Generate `project.yaml` + `index.md` per project
- [x] Generate 2,327 module pages with manifest data
- [x] Auto `catalog.md` (808 unique `meta_*`)
- [x] Auto `reuse-matrix.md` (cross-project duplicates)
- [x] MkDocs nav for all projects
- [x] `scan_modules.py` + `generate_excel.py` in `scripts/`
- [x] 3 curated Agile Minds modules preserved
