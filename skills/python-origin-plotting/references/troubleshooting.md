# Troubleshooting

## `ModuleNotFoundError: originpro`

Install or expose the `originpro` Python package that matches the local Origin/OriginPro installation. On some systems it is easiest to run the script with Origin's bundled or configured Python.

## Origin COM Launch Failure

Open Origin manually once, close dialogs, then rerun the script. Check that Python and Origin bitness match and that Origin is licensed and allowed to run interactively.

## Exports Fail on Chinese Paths

Write figures and `.opju` files to an ASCII temp directory such as `E:/origin_tmp`, then copy to the final Chinese path with `shutil.copy2`.

## Exported PNG Is Missing or Empty

Check the return value of `gp.save_fig(...)`, verify that the temp file exists, and confirm the graph page has at least one plot. Call `gl.rescale()` after adding plots.

## Manual Colors Revert

Origin grouping can overwrite plot colors. Either avoid grouping after assigning colors, or group first and then set colors again.

## Destination OPJU Is Locked

Save to a timestamped temp `.opju`, then copy to the final name. If copying raises `PermissionError`, copy to a versioned filename such as `project_20260430_160000.opju`.

## Hidden Origin Sessions Remain Running

Always use:

```python
try:
    ...
finally:
    op.exit()
```

If a previous run crashed, close leftover Origin processes manually before rerunning.
