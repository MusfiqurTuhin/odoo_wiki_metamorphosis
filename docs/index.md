# Metamorphosis Module Wiki

Central inventory of **38 Odoo projects** and **2,330+ custom modules** — generated from Niaj's server scan, enriched with per-module pages for delivery, reuse, and marketing.

## Status

| Item | Count |
|------|-------|
| Projects | 38 |
| Module pages | 2,327 auto-generated + 3 curated |
| Unique `meta_*` modules | 808 |
| Cross-project duplicates | See [reuse matrix](modules/reuse-matrix.md) |

## Quick links

- [All projects](projects/index.md)
- [meta_* catalog](modules/catalog.md) — marketing / reuse
- [Reuse matrix](modules/reuse-matrix.md) — same module in multiple repos
- [Contributing](contributing.md)
- [Requirements list](requirements.md) — what still needs manual input

## Regenerate from scan

```bash
# 1. Update inventory (on Odoo server or local addons root)
python scripts/scan_modules.py

# 2. Copy odoo_module_inventory.md to data/

# 3. Regenerate wiki (preserves pages with curated: true)
python scripts/generate_wiki.py

# 4. Preview
pip install -r requirements.txt
mkdocs serve
```

## Data source

Inventory: `data/odoo_module_inventory.md` from **Md. Niaj Shahriar Shishir** (`scan_modules.py`, Jun 2026).

Filters: excludes Odoo core, `l10n_*`, enterprise trees, Odoo S.A. authors.
