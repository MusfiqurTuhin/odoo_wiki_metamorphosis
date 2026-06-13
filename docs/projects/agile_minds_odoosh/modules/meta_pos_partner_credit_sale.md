---
technical_name: meta_pos_partner_credit_sale
display_name: Partner Wise Credit Sale in POS
project_slug: agile_minds_odoosh
curated: true
reusable: true
marketing_summary: >
  Sell on credit from the Point of Sale with per-partner limits, date-range
  controls, automatic receivable journal entries, and credit reporting —
  built for membership and B2B retail in Bangladesh.
odoo_version: "17.0"
category: Point of Sale / Accounting
git:
  repo_url: ""  # TODO
  path: agile_minds_odoosh/meta_pos_partner_credit_sale
  branch: main
contributors:
  - name: Md. Niaj Shahriar Shishir
    role: author
    email: niaj@metamorphosis.com.bd
depends:
  - point_of_sale
  - account
used_in:
  - agile_minds_odoosh
versions:
  - version: "17.0.0.4"
    date: "2026-06-01"
    odoo_version: "17.0"
    whats_new: >
      Reporting improvements and credit date-range validation hardening.
    git_tag: ""
    contributors: [Md. Niaj Shahriar Shishir]
  - version: "17.0.0.3"
    date: "2025-11-15"
    odoo_version: "17.0"
    whats_new: >
      Receivable journal entry automation on credit POS orders.
    contributors: [Md. Niaj Shahriar Shishir]
  - version: "17.0.0.1"
    date: "2025-08-01"
    odoo_version: "17.0"
    whats_new: >
      Initial release — partner credit limit and POS credit sale flow.
    contributors: [Md. Niaj Shahriar Shishir]
---

# Partner Wise Credit Sale in POS

`meta_pos_partner_credit_sale`

## Module brief

Extends Odoo Point of Sale so cashiers can complete sales **on credit** for selected partners. Enforces credit limits, optional date windows for credit eligibility, posts receivable journal entries, and exposes reporting for finance teams.

**Manifest summary:** Make sales in POS with Credit Limit, Control date range of Credit sales, Create Receivable Journal Entries, Reporting etc.

## Who worked on this module

| Name | Role |
|------|------|
| Md. Niaj Shahriar Shishir | Author / maintainer |

## Technical details

| Field | Value |
|-------|-------|
| Technical name | `meta_pos_partner_credit_sale` |
| Current version | `17.0.0.4` |
| Odoo version | 17.0 |
| Git path | `agile_minds_odoosh/meta_pos_partner_credit_sale` |
| Reusable | Yes — candidate for other POS + credit clients |

## Version history

| Version | Date | What's new |
|---------|------|------------|
| 17.0.0.4 | 2026-06-01 | Reporting improvements; credit date-range validation |
| 17.0.0.3 | 2025-11-15 | Automatic receivable JE on credit POS orders |
| 17.0.0.1 | 2025-08-01 | Initial credit limit + POS credit sale workflow |

## Marketing notes

- **Target buyers:** Retail, membership clubs, distributors using Odoo POS
- **Differentiator:** End-to-end POS credit with accounting integration (not just a UI flag)
- **Demo ask:** POS session with partner over limit + date-range block scenarios
