#!/usr/bin/env bash
# Push wiki to canonical org repo and personal Pages mirror.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "→ Pushing to org (canonical): metamorphosisbd/odoo_wiki_metamorphosis"
git push origin main

echo "→ Pushing to personal (Pages): MusfiqurTuhin/odoo_wiki_metamorphosis"
git push pages main

echo "Done. Site will build at https://musfiqurtuhin.github.io/odoo_wiki_metamorphosis/"
