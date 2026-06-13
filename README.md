# Metamorphosis Module Wiki

Odoo custom module inventory wiki — **38 projects**, **2,330+ modules**, built from Niaj's scan.

## Quick start

```bash
cd module-wiki
pip install -r requirements.txt
mkdocs serve
# http://127.0.0.1:8000
```

## Structure

```
module-wiki/
  data/odoo_module_inventory.md   # Niaj scan output
  docs/                           # MkDocs content
  scripts/
    scan_modules.py               # rescan addons tree
    generate_excel.py             # Excel export
    generate_wiki.py              # inventory → wiki pages
  _schema/                        # YAML validation schemas
  REQUIREMENTS.md                 # manual input still needed
```

## Regenerate

```bash
python scripts/generate_wiki.py
```

Pages with `curated: true` in front matter are **not** overwritten.

## Deploy

Repo: https://github.com/metamorphosisbd/odoo_wiki_metamorphosis

CI builds on every push. **GitHub Pages** requires org plan support — see [DEPLOY.md](DEPLOY.md).

```bash
mkdocs build   # or download mkdocs-site artifact from Actions
```
