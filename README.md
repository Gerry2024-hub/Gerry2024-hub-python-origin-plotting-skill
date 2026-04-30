# Python Origin Plotting Skill

This repository packages a Codex skill for Python-driven OriginPro plotting. It helps Codex create reproducible `originpro` scripts, build Origin workbooks and graph pages, export publication figures, and save `.opju` projects from Excel or CSV data.

## Repository Layout

```text
python-origin-plotting-skill/
  README.md
  skills/
    python-origin-plotting/
      SKILL.md
      agents/openai.yaml
      scripts/originpro_plot_template.py
      references/originpro-workflow.md
      references/troubleshooting.md
```

## Install Locally

Copy the skill folder into your Codex skills directory.

PowerShell:

```powershell
$repo = (Get-Location).Path
$dest = "$env:USERPROFILE\.codex\skills\python-origin-plotting"
New-Item -ItemType Directory -Force -Path (Split-Path $dest)
Copy-Item -Recurse -Force "$repo\skills\python-origin-plotting" $dest
```

macOS/Linux:

```bash
repo="/path/to/python-origin-plotting-skill"
dest="${CODEX_HOME:-$HOME/.codex}/skills/python-origin-plotting"
mkdir -p "$(dirname "$dest")"
cp -R "$repo/skills/python-origin-plotting" "$dest"
```

Restart Codex after installing, then try:

```text
Use $python-origin-plotting to make an OriginPro grouped bar chart from this Excel file and save PNG plus OPJU outputs.
```

## Use the Template Script

The bundled script is a starting point for new OriginPro automation:

```powershell
python .\skills\python-origin-plotting\scripts\originpro_plot_template.py .\data.xlsx --sheet "Sheet1" --out .\plots_origin --show
```

For real work, adapt `prepare_data()` and `build_origin_project()` to the target columns and graph types.

## Validate the Skill

From this repository root:

```powershell
python D:\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\python-origin-plotting
python -m py_compile .\skills\python-origin-plotting\scripts\originpro_plot_template.py
```

The first command checks skill metadata and structure. The second catches Python syntax issues without needing Origin to be installed.

## Publish to GitHub for the First Time

1. Create a new empty repository on GitHub, for example `python-origin-plotting-skill`. Do not add a README on GitHub if this local folder already has one.
2. Open PowerShell in this folder:

```powershell
cd "path\to\python-origin-plotting-skill"
git init
git add .
git commit -m "Add python-origin-plotting Codex skill"
git branch -M main
git remote add origin https://github.com/<your-name>/python-origin-plotting-skill.git
git push -u origin main
```

3. Replace `<your-name>` with your GitHub username. If Git asks you to sign in, follow the browser prompt or use a personal access token.

## Recommended Release Checklist

- Keep private data files, unpublished figures, and generated `.opju` outputs out of the repo.
- Commit only the reusable skill, template script, and documentation.
- Add screenshots to the GitHub README only if they are safe to publish.
- Tag a first version after the initial push:

```powershell
git tag v0.1.0
git push origin v0.1.0
```
