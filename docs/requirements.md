# Requirements — manual input still needed

See the full list in the repository: [REQUIREMENTS.md](https://github.com/metamorphosisbd/odoo_wiki_metamorphosis/blob/main/REQUIREMENTS.md).

## Critical

**Git remote URLs** per project (Dev/Niaj), **folder → client legal name** mapping (PM), **client contacts** (PM), **project brief** text (project lead).

## Per module

**Version history + what's new**, confirmed **contributors**, **marketing_summary**, manifest **depends**, set **curated: true** after review.

## Infrastructure

GitHub repo for wiki, deploy target (GitHub Pages or internal), Python 3.11+ on CI, weekly scheduled scan on server.

## Developer checklist

1. Run `python scripts/scan_modules.py` from addons root.
2. PR updated `data/odoo_module_inventory.md`.
3. Curate modules you own; set `curated: true`.
4. Project leads fill `project.yaml`.
