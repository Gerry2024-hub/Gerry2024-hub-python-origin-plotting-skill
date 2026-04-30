# OriginPro Workflow Notes

## Script Shape

Prefer this structure:

1. Constants for paths, column names/indexes, colors, and output names.
2. `load_data()` or `prepare_data()` for pandas cleanup.
3. Small graph helper functions such as `style_layer()`, `export_graph()`, and `save_project()`.
4. One function per figure.
5. `main()` that creates output folders, writes audit CSV, starts Origin, builds workbooks/graphs, saves project, and exits Origin.

Keep project-specific labels and plotting requirements near the top of the script so another user can adapt the file quickly.

## Data Preparation

- Use `pd.read_excel(..., sheet_name="...")` or `pd.read_csv(...)`.
- Drop rows missing required plotting fields with `dropna(subset=[...])`.
- Sort before plotting so Origin receives the exact visual order.
- Add short display labels such as `G1`, `P01`, or sample IDs for the X axis.
- Preserve long process descriptions in separate worksheet columns for auditability.
- Write `origin_input_data_sorted.csv` with `utf-8-sig` so Excel opens Chinese text cleanly.

## Workbook Setup

Typical pattern:

```python
wb = op.new_book(lname="Project_Data")
wks = wb[0]
wks.from_df(df)
wks.cols_axis("xnnYYYY", c1=0, repeat=False)
wks.set_label(col_index, "Delta Rs", "L")
wks.set_label(col_index, "%", "U")
```

Use `cols_axis` only after the final DataFrame column order is stable.

## Chart Recipes

Column chart:

```python
gp = op.new_graph(lname="Origin_Rs_Percent_Bar")
gl = gp[0]
p = gl.add_plot(wks, coly=4, colx=0, type="c")
p.color = "#36536F"
gl.axis("x").title = "Group"
gl.axis("y").title = "Delta Rs (%)"
gl.rescale()
```

Grouped metrics:

```python
p1 = gl.add_plot(wks, coly=4, colx=0, type="c")
p2 = gl.add_plot(wks, coly=5, colx=0, type="c")
p3 = gl.add_plot(wks, coly=6, colx=0, type="c")
p1.color = "#4E6E8E"
p2.color = "#D9903D"
p3.color = "#2F8F83"
```

Set colors after adding plots. If Origin grouping overwrites manual colors, avoid grouping or reapply colors after `group(...)`.

Dual-axis chart:

```python
gp = op.new_graph(lname="Origin_Dual_Axis")
left = gp[0]
bar = left.add_plot(wks, coly=4, colx=0, type="c")
right = gp.add_layer(2)
line = right.add_plot(wks, coly=5, colx=0, type="l")
left.axis("y").title = "Left metric"
right.axis("y2").title = "Right metric"
```

When zero baselines must align, explicitly set left and right Y limits.

## Styling

- Use Origin APIs for basic titles and ranges.
- Use LabTalk for details such as legend refresh, grid lines, font size, tick rotation, and layer labels.
- Prefer page long names and exported filenames over graph titles when titles collide with the plot area.
- Use a restrained palette with enough contrast between metrics.

Examples:

```python
gl.lt_exec("layer.grid.majorY.show=1; layer.grid.majorY.color=15; layer.grid.majorY.lineStyle=2;")
gl.lt_exec("layer.x.label.fsize=16; layer.x.label.rotate=45;")
gp.lt_exec("legend -r; legend.fsize=18;")
```

## Export and Save

Export figures through Origin:

```python
gp.save_fig(str(tmp_file), type="png", width=1800)
```

Save `.opju` through Origin:

```python
op.save(str(tmp_opju))
```

Use an ASCII temp directory first, then copy to the final folder. This avoids many path encoding and export issues on Windows.
