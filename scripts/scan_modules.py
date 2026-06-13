import os
import ast
import collections
import re

OUTPUT_FILE = "odoo_module_inventory.md"
ROOT_DIR = "."

# Compiled regex for path filtering
# Matches: odoo12-ce, odoo12_ce, odoo12ce, odoo-server, enterprise, and standard odoo folders (e.g. odoo14)
# but avoids excluding folders like odoo14-custom.
EXCLUDED_DIR_PATTERN = re.compile(r'^odoo\d*[-_]?(ce|ent(erprise)?)$|^odoo-server$|^enterprise$|^odoo\d+$', re.IGNORECASE)

# Top-level directories to skip entirely (not our repos / not custom)
EXCLUDED_DIRS = {
    'precisiontex-qd-global',  # v14 OCA mirror, not ours
    'psae-mediastar-limited',  # no longer a client
    'odoo17_theme',            # Odoo official theme repo
    'toptenbd',                # not our client
}

# Compiled regex for l10n modules and other l10 patterns
L10N_PATTERN = re.compile(r'^l10.*', re.IGNORECASE)

PROGRESS_FILE = "scan_progress.log"

def log_progress(message):
    with open(PROGRESS_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

def parse_manifest(manifest_path):
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Clean content slightly if it starts with # or something non-dict
            # (Heuristic: look for the first '{' and last '}')
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                content = content[start:end+1]
            try:
                manifest_data = ast.literal_eval(content)
                if not isinstance(manifest_data, dict):
                    return None
                return manifest_data
            except (SyntaxError, ValueError):
                return None
    except Exception:
        return None

def is_excluded_path(path_parts):
    """
    Check if any part of the path matches the exclusion patterns or explicit list.
    """
    if path_parts and path_parts[0] in EXCLUDED_DIRS:
        return True
    for part in path_parts:
        if EXCLUDED_DIR_PATTERN.match(part):
            return True
    return False

def is_excluded_module_name(name):
    """
    Check if module dir name starts with l10
    """
    return bool(L10N_PATTERN.match(name))

def is_excluded_author(author):
    """
    Check if author is Odoo official.
    """
    if not author:
        return False
    
    # Normalize
    a = str(author).lower().strip()
    
    # Common Odoo author variations
    odoo_authors = ['odoo', 'odoo s.a.', 'odoo sa', 'odoo s. a.']
    if any(oa == a for oa in odoo_authors):
        return True
        
    if 'odoo s.a.' in a or 'odoo sa' in a:
         # Heuristic: if "Odoo S.A." is in the string and it's short, it's likely official
         if len(a) < 25:
             return True
             
    return False

def main():
    projects = collections.defaultdict(list)
    
    # Reset log file
    with open(PROGRESS_FILE, "w") as f:
        f.write(f"Starting scan at {os.popen('date').read()}")
    
    log_progress(f"Scanning for CUSTOM Odoo modules in {os.path.abspath(ROOT_DIR)}...")
    
    count = 0
    skipped_path = 0
    skipped_author = 0
    skipped_l10n = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if "__manifest__.py" in files or "__openerp__.py" in files:
            m_file = "__manifest__.py" if "__manifest__.py" in files else "__openerp__.py"
            manifest_path = os.path.join(root, m_file)
            module_dir_name = os.path.basename(root)
            
            # Relative path components
            rel_path = os.path.relpath(root, ROOT_DIR)
            path_parts = rel_path.split(os.sep)
            
            # 1. Filter by Directory Path
            if is_excluded_path(path_parts):
                skipped_path += 1
                continue

            # 2. Filter by Module Name (l10*)
            if is_excluded_module_name(module_dir_name):
                skipped_l10n += 1
                continue

            # Determine Project Name
            if len(path_parts) >= 1:
                # If path_parts[0] is one of the excluded patterns, skip (already handled by is_excluded_path)
                # We want the first directory level to be the project.
                project_name = path_parts[0]
                if project_name == '.': continue 
            else:
                project_name = "Root"

            # Parse Manifest
            data = parse_manifest(manifest_path)
            if data:
                author = data.get('author', 'N/A')
                
                # 3. Filter by Author
                if is_excluded_author(author):
                    skipped_author += 1
                    continue

                module_info = {
                    'dir_name': module_dir_name,
                    'name': data.get('name', 'N/A'),
                    'version': data.get('version', 'N/A'),
                    'author': author,
                    'summary': str(data.get('summary') or data.get('description') or 'N/A')[:150].replace('\n', ' ')
                }
                projects[project_name].append(module_info)
                count += 1
                if count % 100 == 0:
                    log_progress(f"Found {count} custom modules...")

    log_progress(f"Scan Complete.")
    log_progress(f"Total Custom Modules: {count}")
    log_progress(f"Skipped by Path: {skipped_path}")
    log_progress(f"Skipped by Author: {skipped_author}")
    log_progress(f"Skipped by l10* Name: {skipped_l10n}")
    log_progress(f"Writing results to {OUTPUT_FILE}...")


    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Odoo Custom Module Inventory\n")
        f.write(f"Generated on: {os.popen('date').read().strip()}\n")
        f.write(f"**Filters Applied:**\n")
        f.write(f"- Excluded Paths: `odoo*-ce`, `odoo*-ent`, `odoo-server`, `enterprise`\n")
        f.write(f"- Excluded Authors: `Odoo`, `Odoo S.A.`\n")
        f.write(f"- Excluded Modules: `l10n_*`\n\n")
        
        for project in sorted(projects.keys()):
            modules = projects[project]
            f.write(f"## Project: {project}\n\n")
            f.write(f"| Module Dir | Name | Version | Author | Summary |\n")
            f.write(f"| :--- | :--- | :--- | :--- | :--- |\n")
            
            for mod in sorted(modules, key=lambda x: x['dir_name']):
                name = str(mod['name']).replace('|', '\\|')
                # limit summary length further for table readability
                summary = str(mod['summary']).replace('|', '||')
                author = str(mod['author']).replace('|', '\\|')
                
                f.write(f"| `{mod['dir_name']}` | {name} | {mod['version']} | {author} | {summary} |\n")
            
            f.write("\n")

    log_progress("Done.")

if __name__ == "__main__":
    main()