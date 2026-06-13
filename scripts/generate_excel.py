import os
import ast
import re
import pandas as pd

OUTPUT_FILE = "odoo_module_inventory.xlsx"
ROOT_DIR = "."

# Compiled regex for path filtering
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

def parse_manifest(manifest_path):
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find actual dictionary content
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
    if not author:
        return False
    a = str(author).lower().strip()
    odoo_authors = ['odoo', 'odoo s.a.', 'odoo sa', 'odoo s. a.']
    if any(oa == a for oa in odoo_authors):
        return True
    if 'odoo s.a.' in a or 'odoo sa' in a:
         if len(a) < 25: 
             return True
    return False

def main():
    data_list = []
    
    print(f"Scanning for Odoo modules to export to Excel...")
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if "__manifest__.py" in files or "__openerp__.py" in files:
            m_file = "__manifest__.py" if "__manifest__.py" in files else "__openerp__.py"
            manifest_path = os.path.join(root, m_file)
            module_dir_name = os.path.basename(root)
            
            rel_path = os.path.relpath(root, ROOT_DIR)
            path_parts = rel_path.split(os.sep)
            
            if is_excluded_path(path_parts):
                continue
            
            # Filter by Module Name (l10*)
            if is_excluded_module_name(module_dir_name):
                continue

            if len(path_parts) >= 1:
                project_name = path_parts[0]
                if project_name == '.': continue 
            else:
                project_name = "Root"

            manifest_data = parse_manifest(manifest_path)
            if manifest_data:
                author = manifest_data.get('author', 'N/A')
                
                if is_excluded_author(author):
                    continue

                module_info = {
                    'Project': project_name,
                    'Module Directory': module_dir_name,
                    'Module Name (Manifest)': manifest_data.get('name', 'N/A'),
                    'Version': manifest_data.get('version', 'N/A'),
                    'Author': author,
                    'Summary': str(manifest_data.get('summary') or manifest_data.get('description') or 'N/A')[:300].replace('\n', ' ')
                }
                data_list.append(module_info)

    print(f"Found {len(data_list)} modules. Creating Excel file...")
    
    if not data_list:
        print("No modules found matching the criteria.")
        return

    df = pd.DataFrame(data_list)
    
    # Sort by Project then Module Name
    df.sort_values(by=['Project', 'Module Directory'], inplace=True)
    
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"Successfully created {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error creating Excel file: {e}")

if __name__ == "__main__":
    main()