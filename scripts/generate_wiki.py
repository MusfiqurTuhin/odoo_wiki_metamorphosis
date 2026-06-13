#!/usr/bin/env python3
"""Generate wiki pages from odoo_module_inventory.md (Niaj scan output)."""

from __future__ import annotations

import argparse
import re
import shutil
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DEFAULT_INVENTORY = (
    ROOT / "data" / "odoo_module_inventory.md"
    if (ROOT / "data" / "odoo_module_inventory.md").exists()
    else ROOT.parent.parent / "Custom-module-Archive-wiki-Niaj" / "odoo_module_inventory.md"
)

PROJECT_HEADING = re.compile(r"^## Project: (.+)$", re.MULTILINE)
TABLE_ROW = re.compile(
    r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|",
    re.MULTILINE,
)
META_PREFIX = re.compile(r"^meta_", re.IGNORECASE)
VALID_SLUG = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")
METAMORPHOSIS_AUTHOR = re.compile(
    r"metamorphosis|niaj|ahosan|tian|rifat|joyanto|mohiuddin|sojib|tanjil|jony",
    re.IGNORECASE,
)

DISPLAY_NAMES: dict[str, str] = {
    "agile_minds_odoosh": "Agile Minds",
    "adarsha_publication": "Adarsha Publication",
    "baatighar_17_ee": "Baatighar",
    "gronthik_publication": "Gronthik Publication",
    "premier1888_odoo17": "Premier 1888",
    "shanta_life_style_17": "Shanta Life Style",
    "jamuna_classic_paint": "Jamuna Classic Paint",
    "friendship_ngo_sh": "Friendship NGO",
    "organik-chicken": "Organik Chicken",
    "pathak-samabesh": "Pathak Samabesh",
    "verity_one": "Verity One",
    "nice_software": "Nice Software",
    "curepoint": "Curepoint",
    "curepointbd_custom": "Curepoint BD",
    "colorjet": "Colorjet",
    "haj_erp_custom": "HAJ ERP",
    "idiya_17_sh": "Idiya",
    "gdfl_v18_sh": "GDFL",
    "smet-odoo-sh": "SMET",
    "tree_living_custom": "Tree Living",
    "tetra_pvt_custom": "Tetra Pvt",
    "biriyani-mahal_custom": "Biriyani Mahal",
    "precisiontex-v19-custom": "Precisiontex",
    "DISABLED_MODULES": "Disabled Modules (Archive)",
}


@dataclass(frozen=True)
class ModuleRow:
    technical_name: str
    display_name: str
    version: str
    author: str
    summary: str


def parse_inventory(path: Path) -> dict[str, list[ModuleRow]]:
    text = path.read_text(encoding="utf-8")
    projects: dict[str, list[ModuleRow]] = {}
    sections = re.split(r"\n## Project: ", text)
    for section in sections[1:]:
        project, _, block = section.partition("\n")
        project = project.strip()
        if not project:
            continue
        modules: list[ModuleRow] = []
        for match in TABLE_ROW.finditer(block):
            modules.append(
                ModuleRow(
                    technical_name=match.group(1).strip(),
                    display_name=match.group(2).strip(),
                    version=match.group(3).strip(),
                    author=match.group(4).strip(),
                    summary=match.group(5).strip(),
                )
            )
        if modules:
            if not VALID_SLUG.match(project) or "|" in project:
                print(f"Skipping invalid project slug: {project!r}")
                continue
            projects[project] = modules
    return projects


def slug_to_title(slug: str) -> str:
    if slug in DISPLAY_NAMES:
        return DISPLAY_NAMES[slug]
    return slug.replace("_", " ").replace("-", " ").title()


def infer_odoo_version(modules: list[ModuleRow]) -> str:
    versions: list[str] = []
    for mod in modules:
        m = re.match(r"^(\d+\.0)", mod.version)
        if m:
            versions.append(m.group(1))
    if not versions:
        return "TBD"
    return max(set(versions), key=versions.count)


def is_meta_owned(mod: ModuleRow) -> bool:
    return bool(META_PREFIX.match(mod.technical_name)) or bool(
        METAMORPHOSIS_AUTHOR.search(mod.author)
    )


def parse_contributors(author: str) -> list[str]:
    if not author or author.upper() == "N/A":
        return []
    parts = re.split(r",|\band\b", author)
    names = [p.strip() for p in parts if p.strip()]
    cleaned: list[str] = []
    for name in names:
        name = re.sub(r"\s+from\s+Metamorphosis.*$", "", name, flags=re.I).strip()
        name = re.sub(r"\s+Metamorphosis.*$", "", name, flags=re.I).strip()
        if name and name.lower() not in ("metamorphosis", "metamorphosis ltd", "metamorphosis ltd."):
            cleaned.append(name)
    return cleaned[:5]


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def module_front_matter(project: str, mod: ModuleRow) -> str:
    reusable = bool(META_PREFIX.match(mod.technical_name))
    contributors = parse_contributors(mod.author)
    contributor_lines = "\n".join(
        f"  - name: {yaml_quote(n)}\n    role: author"
        for n in contributors
    ) or '  - name: "TBD"\n    role: author'
    odoo_ver = "TBD"
    m = re.match(r"^(\d+\.0)", mod.version)
    if m:
        odoo_ver = m.group(1)
    summary = mod.summary.replace("\n", " ").strip() or "TBD"
    return textwrap.dedent(
        f"""\
        ---
        technical_name: {mod.technical_name}
        display_name: {yaml_quote(mod.display_name)}
        project_slug: {project}
        curated: false
        reusable: {"true" if reusable else "false"}
        marketing_summary: {yaml_quote(summary[:300])}
        odoo_version: {yaml_quote(odoo_ver)}
        category: TBD
        git:
          repo_url: ""
          path: {project}/{mod.technical_name}
          branch: main
        contributors:
        {contributor_lines}
        depends: []
        used_in:
          - {project}
        versions:
          - version: {yaml_quote(mod.version)}
            date: {yaml_quote(str(date.today()))}
            odoo_version: {yaml_quote(odoo_ver)}
            whats_new: "Seeded from manifest scan. Update with release notes."
        ---
        """
    )


def render_module_page(project: str, mod: ModuleRow) -> str:
    contributors = parse_contributors(mod.author)
    contrib_table = (
        "\n".join(f"| {n} | author |" for n in contributors)
        if contributors
        else "| TBD | author |"
    )
    body = textwrap.dedent(
        f"""\
        # {mod.display_name}

        `{mod.technical_name}`

        ## Module brief

        {mod.summary or "_No summary in manifest. Please add a business-purpose description._"}

        ## Who worked on this module

        | Name | Role |
        |------|------|
        {contrib_table}

        _Source: `__manifest__.py` author field. Confirm and extend via git history._

        ## Technical details

        | Field | Value |
        |-------|-------|
        | Technical name | `{mod.technical_name}` |
        | Current version | `{mod.version}` |
        | Project | [{slug_to_title(project)}](../index.md) |
        | Git path | `{project}/{mod.technical_name}` |
        | Manifest author | {mod.author} |

        ## Version history

        | Version | Date | What's new |
        |---------|------|------------|
        | {mod.version} | {date.today().isoformat()} | Seeded from scan — add release notes |

        !!! note "Needs review"
            This page was auto-generated. Set `curated: true` in front matter after manual review.
        """
    )
    return module_front_matter(project, mod) + "\n" + body


def render_project_yaml(project: str, modules: list[ModuleRow]) -> str:
    meta_count = sum(1 for m in modules if META_PREFIX.match(m.technical_name))
    return textwrap.dedent(
        f"""\
        slug: {project}
        display_name: {yaml_quote(slug_to_title(project))}
        status: active
        brief: >
          Odoo custom addons for {slug_to_title(project)}. {len(modules)} modules in scan
          ({meta_count} meta_*). Update this brief with project scope and delivery notes.
        odoo_version: {yaml_quote(infer_odoo_version(modules))}
        hosting: TBD

        client:
          name: {yaml_quote(slug_to_title(project))}
          legal_name: ""
          industry: TBD
          country: Bangladesh
          website: ""
          contacts: []

        git:
          remote_url: ""
          default_branch: main
          root_path: {project}/

        team: []

        modules:
        {chr(10).join(f"  - {m.technical_name}" for m in sorted(modules, key=lambda x: x.technical_name))}

        tags:
          - auto-generated
        """
    )


def render_project_index(project: str, modules: list[ModuleRow]) -> str:
    meta_mods = [m for m in modules if META_PREFIX.match(m.technical_name)]
    other_mods = [m for m in modules if not META_PREFIX.match(m.technical_name)]
    lines = [
        f"# {slug_to_title(project)}",
        "",
        f"**Slug:** `{project}` · **Modules:** {len(modules)} · "
        f"**Odoo:** {infer_odoo_version(modules)} · **meta_*:** {len(meta_mods)}",
        "",
        "## Project brief",
        "",
        f"Odoo custom deployment for **{slug_to_title(project)}**. "
        "Edit `project.yaml` for client legal name, contacts, and git remote.",
        "",
        "## Client details",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Client | {slug_to_title(project)} _(map to legal name in project.yaml)_ |",
        "| Industry | TBD |",
        "| Country | Bangladesh |",
        "",
        "## Modules — Metamorphosis (`meta_*`)",
        "",
        "| Module | Name | Version | Author |",
        "|--------|------|---------|--------|",
    ]
    for mod in sorted(meta_mods, key=lambda m: m.technical_name):
        author = mod.author.replace("|", "\\|")[:60]
        lines.append(
            f"| [`{mod.technical_name}`](modules/{mod.technical_name}.md) "
            f"| {mod.display_name} | {mod.version} | {author} |"
        )
    if not meta_mods:
        lines.append("| _none_ | | | |")

    lines.extend(["", "## Modules — Third-party / other", "", "| Module | Name | Version | Author |", "|--------|------|---------|--------|"])
    for mod in sorted(other_mods, key=lambda m: m.technical_name):
        author = mod.author.replace("|", "\\|")[:60]
        lines.append(
            f"| [`{mod.technical_name}`](modules/{mod.technical_name}.md) "
            f"| {mod.display_name} | {mod.version} | {author} |"
        )
    return "\n".join(lines) + "\n"


def render_projects_index(projects: dict[str, list[ModuleRow]]) -> str:
    lines = [
        "# Projects",
        "",
        f"**{len(projects)}** project folders · **{sum(len(m) for m in projects.values())}** modules _(Niaj scan)_",
        "",
        "| Project | Display name | Modules | meta_* | Odoo |",
        "|---------|--------------|---------|--------|------|",
    ]
    for slug in sorted(projects.keys(), key=str.lower):
        mods = projects[slug]
        meta_n = sum(1 for m in mods if META_PREFIX.match(m.technical_name))
        lines.append(
            f"| [{slug}]({slug}/index.md) | {slug_to_title(slug)} | {len(mods)} | {meta_n} | {infer_odoo_version(mods)} |"
        )
    return "\n".join(lines) + "\n"


def render_reuse_matrix(projects: dict[str, list[ModuleRow]]) -> str:
    by_name: dict[str, list[tuple[str, ModuleRow]]] = defaultdict(list)
    for project, modules in projects.items():
        for mod in modules:
            by_name[mod.technical_name].append((project, mod))

    multi = [(name, locs) for name, locs in by_name.items() if len(locs) > 1]
    multi.sort(key=lambda x: (-len(x[1]), x[0]))

    lines = [
        "# Cross-project reuse matrix",
        "",
        f"Modules appearing in **more than one** project folder ({len(multi)} technical names).",
        "",
        "| Technical name | Projects | Count | meta_* | Sample version |",
        "|----------------|----------|-------|--------|----------------|",
    ]
    for name, locs in multi[:200]:
        projs = ", ".join(f"`{p}`" for p, _ in locs)
        is_meta = "yes" if META_PREFIX.match(name) else "no"
        lines.append(
            f"| `{name}` | {projs} | {len(locs)} | {is_meta} | {locs[0][1].version} |"
        )
    if len(multi) > 200:
        lines.append(f"\n_…and {len(multi) - 200} more. Regenerate via `python scripts/generate_wiki.py`._")
    return "\n".join(lines) + "\n"


def render_catalog(projects: dict[str, list[ModuleRow]]) -> str:
    seen: dict[str, tuple[str, ModuleRow]] = {}
    for project, modules in projects.items():
        for mod in modules:
            if not META_PREFIX.match(mod.technical_name):
                continue
            if mod.technical_name not in seen:
                seen[mod.technical_name] = (project, mod)

    lines = [
        "# Reusable module catalog (`meta_*`)",
        "",
        f"**{len(seen)}** unique Metamorphosis module technical names across all projects.",
        "",
        "| Module | Display name | Version (sample) | Primary project | Used in # projects |",
        "|--------|--------------|------------------|-----------------|-------------------|",
    ]
    usage_count: dict[str, int] = defaultdict(int)
    for project, modules in projects.items():
        for mod in modules:
            usage_count[mod.technical_name] += 1

    for name in sorted(seen.keys()):
        project, mod = seen[name]
        count = usage_count[name]
        link = f"../projects/{project}/modules/{name}.md"
        lines.append(
            f"| [`{name}`]({link}) | {mod.display_name} | {mod.version} | "
            f"[{slug_to_title(project)}](../projects/{project}/index.md) | {count} |"
        )
    return "\n".join(lines) + "\n"


def is_curated(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "curated: true" in text[:800]


def clean_stale_projects(valid: set[str]) -> int:
    removed = 0
    root = DOCS / "projects"
    for path in root.iterdir():
        if not path.is_dir() or path.name in valid:
            continue
        shutil.rmtree(path)
        removed += 1
        print(f"Removed stale project: {path.name}")
    return removed


def generate(inventory: Path, dry_run: bool = False) -> dict[str, int]:
    projects = parse_inventory(inventory)
    stats = {"projects": 0, "modules_written": 0, "modules_skipped": 0, "stale_removed": 0}

    if dry_run:
        return {"projects": len(projects), "modules": sum(len(m) for m in projects.values())}

    stats["stale_removed"] = clean_stale_projects(set(projects.keys()))

    (DOCS / "projects").mkdir(parents=True, exist_ok=True)

    for project, modules in sorted(projects.items()):
        proj_dir = DOCS / "projects" / project
        mod_dir = proj_dir / "modules"
        mod_dir.mkdir(parents=True, exist_ok=True)

        (proj_dir / "project.yaml").write_text(render_project_yaml(project, modules), encoding="utf-8")
        (proj_dir / "index.md").write_text(render_project_index(project, modules), encoding="utf-8")
        stats["projects"] += 1

        for mod in modules:
            mod_path = mod_dir / f"{mod.technical_name}.md"
            if is_curated(mod_path):
                stats["modules_skipped"] += 1
                continue
            mod_path.write_text(render_module_page(project, mod), encoding="utf-8")
            stats["modules_written"] += 1

    (DOCS / "projects" / "index.md").write_text(render_projects_index(projects), encoding="utf-8")
    (DOCS / "modules" / "reuse-matrix.md").write_text(render_reuse_matrix(projects), encoding="utf-8")
    (DOCS / "modules" / "catalog.md").write_text(render_catalog(projects), encoding="utf-8")

    return stats


def write_mkdocs_nav(projects: dict[str, list[ModuleRow]]) -> None:
    """Append project links to mkdocs.yml (top projects by module count)."""
    mkdocs_path = ROOT / "mkdocs.yml"
    text = mkdocs_path.read_text(encoding="utf-8")

    ranked = sorted(projects.items(), key=lambda x: len(x[1]), reverse=True)
    nav_lines = ["  - Projects:", "      - Overview: projects/index.md"]
    for slug, mods in ranked:
        title = slug_to_title(slug)
        if len(title) > 40:
            title = title[:37] + "..."
        nav_lines.append(f"      - \"{title}\": projects/{slug}/index.md")

    nav_lines.extend(
        [
            "  - Modules:",
            "      - Reusable Catalog: modules/catalog.md",
            "      - Cross-Project Matrix: modules/reuse-matrix.md",
            "  - Schema Reference: schema.md",
            "  - Requirements: requirements.md",
        ]
    )

    new_nav = "nav:\n  - Home: index.md\n  - How to Contribute: contributing.md\n" + "\n".join(nav_lines) + "\n"
    text = re.sub(r"nav:.*", new_nav.rstrip(), text, flags=re.DOTALL)
    mkdocs_path.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate wiki from Niaj inventory")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-nav", action="store_true", default=True)
    args = parser.parse_args()

    if not args.inventory.exists():
        raise SystemExit(f"Inventory not found: {args.inventory}")

    if args.dry_run:
        result = generate(args.inventory, dry_run=True)
        print(f"Would generate: {result['projects']} projects, {result['modules']} modules")
        return

    stats = generate(args.inventory)
    projects = parse_inventory(args.inventory)
    if args.update_nav:
        write_mkdocs_nav(projects)

    print(
        f"Done: {stats['projects']} projects, "
        f"{stats['modules_written']} modules written, "
        f"{stats['modules_skipped']} curated preserved, "
        f"{stats.get('stale_removed', 0)} stale removed"
    )


if __name__ == "__main__":
    main()
