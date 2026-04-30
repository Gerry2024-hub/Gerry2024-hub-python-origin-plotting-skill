---
name: python-origin-plotting
description: Automate OriginPro figure generation from Excel or CSV data through Python originpro. Use when Codex needs to create, reproduce, or refine Origin/OriginPro .opju projects, publication PNG/TIFF exports, worksheet import pipelines, grouped bar charts, dual-axis charts, scatter/line plots, or chart styling scripts using Python-driven Origin automation.
---

# Python Origin Plotting

Use this skill to turn tabular data and plotting requirements into reproducible OriginPro projects driven by Python `originpro`.

## First Pass

1. Locate existing artifacts before writing code:
   - `*origin*.py`, `*.opju`, `*.opj`, `plots_origin/`, exported `Origin_*.png`
   - PowerShell: `Get-ChildItem -Recurse -File -Include *origin*.py,*.opju,*.opj,*.png`
2. Identify the input file, sheet name, required columns, desired chart types, output folder, and whether Origin should be visible.
3. Reuse any existing project script style first, especially workbook setup, LabTalk styling, export naming, and temp-path handling.
4. For a new project, copy and adapt `scripts/originpro_plot_template.py`.

## Standard Workflow

1. Load and clean data with `pandas`.
   - Read Excel or CSV.
   - Drop rows missing required plotting columns.
   - Sort data in the expected visual order.
   - Create short axis labels while preserving long labels in separate worksheet columns.
   - Export an audit CSV such as `origin_input_data_sorted.csv` with `encoding="utf-8-sig"`.

2. Start a clean Origin project.
   - `import originpro as op`
   - `op.set_show(True)` when the user should see Origin.
   - `op.new()` before creating new workbooks and graph pages.
   - Create a workbook with `op.new_book(...)`, write the DataFrame with `wks.from_df(df)`, then set column designations and labels.

3. Create graphs in Origin.
   - Use Origin graph pages and layers rather than matplotlib when the user asks for Origin output.
   - Add plots with `gl.add_plot(wks, coly=..., colx=..., type=...)`.
   - For dual-axis charts, add a second layer and explicitly manage right-Y axis titles and limits.

4. Style through Origin APIs and LabTalk.
   - Set axis titles with `gl.axis("x").title` and `gl.axis("y").title`.
   - Use `gl.lt_exec(...)` or `gp.lt_exec(...)` for labels, legends, grids, tick rotation, and template-specific styling.
   - Call `gl.rescale()` after adding plots.
   - Avoid graph titles when they overlap exports; prefer page long names and filenames.

5. Export figures and save the Origin project.
   - Export PNG/TIFF with `gp.save_fig(...)`.
   - Save `.opju` with `op.save(...)`.
   - If output paths contain Chinese characters or Origin refuses direct export, save first to an ASCII temp directory, then copy to the final path.
   - Use timestamped or versioned `.opju` names if the final project file may be locked.

6. Close Origin cleanly.
   - Put save/export logic in `try`.
   - Put `op.exit()` in `finally`.
   - Do not leave hidden Origin COM sessions running.

## References

Read these only when needed:

- `references/originpro-workflow.md`: detailed implementation patterns, chart recipes, and script structure.
- `references/troubleshooting.md`: common `originpro`, COM, Chinese-path, export, and locked-file failures.

## Validation Checklist

- The script runs without Python exceptions on the target machine.
- Output folder contains an audit CSV, exported figure files, and a saved `.opju`.
- Figure files are non-empty and have recent modification times.
- The `.opju` opens in Origin and contains the worksheet plus graph pages.
- If Origin or `originpro` is not installed, say so clearly and do not fake Origin output with matplotlib unless the user asks for a fallback.
