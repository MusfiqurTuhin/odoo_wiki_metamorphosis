# Deploying the wiki

## GitHub repo

https://github.com/metamorphosisbd/odoo_wiki_metamorphosis

## GitHub Pages (recommended when available)

The org plan must support **GitHub Pages** for this repository.

1. Repo → **Settings** → **Pages** → Source: **GitHub Actions**
2. Re-enable deploy job in `.github/workflows/wiki-deploy.yml` (template below) or upgrade org plan
3. Site URL: `https://metamorphosisbd.github.io/odoo_wiki_metamorphosis/`

Current status: Pages API returns *plan does not support GitHub Pages* — CI builds the site and uploads `mkdocs-site` artifact instead.

## Local preview

```bash
pip install -r requirements.txt
python scripts/generate_wiki.py
mkdocs serve
```

## Internal server (nginx)

```bash
python scripts/generate_wiki.py
mkdocs build
rsync -av site/ user@wiki.internal:/var/www/odoo-wiki/
```

## Download CI artifact

After each push to `main`, download **mkdocs-site** from the [Actions](https://github.com/metamorphosisbd/odoo_wiki_metamorphosis/actions) run and host the `site/` folder on any static file server.

## When Pages is enabled

Uncomment and use `wiki-deploy.yml` or merge deploy steps back into `wiki.yml` with `actions/deploy-pages@v4`.
