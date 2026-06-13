# Schema reference

Wiki content is **Markdown + YAML** so developers can edit in IDE or GitHub without a CMS.

## Project (`project.yaml`)

| Field | Required | Purpose |
|-------|----------|---------|
| `slug` | yes | URL path, folder name |
| `display_name` | yes | Human title |
| `brief` | yes | Project brief (management) |
| `client.*` | yes | Client details block |
| `odoo_version` | yes | Target Odoo series |
| `git.*` | yes | Source repo + addons path |
| `modules[]` | no | List of technical names |
| `team[]` | no | Delivery team |

See `_schema/project.schema.yaml`.

## Module (YAML front-matter in `modules/*.md`)

| Field | Required | Purpose |
|-------|----------|---------|
| `technical_name` | yes | Odoo module directory name |
| `display_name` | yes | Manifest name |
| `project_slug` | yes | Parent project |
| `contributors[]` | yes | Who worked on it |
| `git.path` | yes | Path inside repo |
| `versions[]` | yes | Version history + what's new |
| `reusable` | no | Show in marketing catalog |
| `used_in[]` | no | Cross-project deployments |
| `marketing_summary` | no | Non-technical pitch |

See `_schema/module.schema.yaml`.

## Mapping to your 6 requirements

| Requirement | Wiki location |
|-------------|---------------|
| 1. Project brief | `project.yaml` → `brief` + project `index.md` |
| 2. Client details | `project.yaml` → `client` |
| 3. Modules list | project `index.md` table + `modules[]` |
| 4. Brief per module | module front-matter + **Module brief** section |
| 5. Who worked | `contributors[]` + **Who worked** table |
| 6. Technical name, git, versions, what's new | front-matter `git`, `versions[]`, **Technical details** |
