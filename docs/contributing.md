# Contributing

Goal: **≤ 5 minutes** per module when you ship a change.

## When to update

| Event | Action |
|-------|--------|
| New custom module | Add `projects/<project>/modules/<technical_name>.md` from template |
| Version bump in `__manifest__.py` | Append row to module **Version history** table |
| Module reused in another project | Add project slug to `used_in` in module YAML; update reuse matrix |
| New client project | Copy `templates/project.yaml` → `projects/<slug>/project.yaml` |

## File layout

```text
module-wiki/
  docs/
    projects/<project_slug>/
      project.yaml          # client + brief + git root
      index.md              # project landing (generated or hand-written)
      modules/
        <technical_name>.md # one page per module
  _schema/                  # JSON Schema for validation
  scripts/                  # scan + build (future)
```

## Module page checklist

Each module page must answer:

1. **What** — business purpose (not only manifest summary)
2. **Who** — primary developer(s) and reviewers
3. **Where** — technical name, git path, Odoo version
4. **When** — version history with release notes

Use [templates/module.md](https://github.com) (see `templates/module.md` in repo root).

## Regenerate from inventory

```bash
python scripts/scan_modules.py          # on server; copy to data/
python scripts/generate_wiki.py           # skips curated: true pages
pip install -r requirements.txt
mkdocs serve
```

## Validation (local)

```bash
pip install -r requirements.txt
mkdocs serve   # http://127.0.0.1:8000
mkdocs build --strict
```

## Ownership

| Role | Responsibility |
|------|----------------|
| Module author | Version history + “what’s new” on each release |
| Project lead | `project.yaml` client details and module list accuracy |
| Wiki maintainer | Schema, scan scripts, deploy pipeline |
