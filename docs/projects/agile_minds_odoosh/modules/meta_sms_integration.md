---
technical_name: meta_sms_integration
display_name: Meta SMS Integration
project_slug: agile_minds_odoosh
curated: true
reusable: true
marketing_summary: >
  Unified SMS sending layer for Odoo — configurable templates and provider
  hooks used across POS, membership, and sales workflows.
odoo_version: "17.0"
category: Technical / Integration
git:
  path: agile_minds_odoosh/meta_sms_integration
contributors:
  - name: Md. Niaj Shahriar Shishir
    role: author
used_in:
  - agile_minds_odoosh
  - odoo17_custom
versions:
  - version: "17.0.0.1"
    date: "2025-10-01"
    whats_new: Initial Meta SMS integration module.
---

# Meta SMS Integration

`meta_sms_integration`

## Module brief

Central SMS integration for Metamorphosis Odoo projects. Other modules (`meta_membership_sms`, `meta_pos_credit_sms_notification`, etc.) depend on or extend this base.

## Who worked on this module

| Name | Role |
|------|------|
| Md. Niaj Shahriar Shishir | Author |

## Technical details

| Field | Value |
|-------|-------|
| Technical name | `meta_sms_integration` |
| Current version | `17.0.0.1` |
| Reusable | **Yes** — deployed in multiple repos per scan |
| Also used in | `odoo17_custom` |

## Version history

| Version | Date | What's new |
|---------|------|------------|
| 17.0.0.1 | 2025-10-01 | Initial provider integration and send API |
