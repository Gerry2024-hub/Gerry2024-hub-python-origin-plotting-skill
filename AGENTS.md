# Agent Instructions

This repository packages a reusable workflow for Python-driven OriginPro plotting. It is intended for Codex, OpenClaw/ClawHub, Hermes-style agents, and other coding agents that can read repository instructions.

When a user asks to generate or refine OriginPro figures from Excel or CSV data:

1. Read `skills/python-origin-plotting/SKILL.md` first.
2. Use `skills/python-origin-plotting/scripts/originpro_plot_template.py` as the starting script for new projects.
3. Read `skills/python-origin-plotting/references/originpro-workflow.md` when implementing chart-specific logic.
4. Read `skills/python-origin-plotting/references/troubleshooting.md` when OriginPro, COM, export, Chinese-path, or locked-file problems occur.
5. Keep private data out of commits and published skill bundles.

Do not upload or commit `.xlsx`, `.xls`, `.xlsm`, `.csv`, `.opju`, `.opj`, generated image files, or local Origin output folders unless the user explicitly asks and confirms they are safe to publish.

This skill requires a local Windows machine with OriginPro and the Python `originpro` package available. If those prerequisites are missing, explain the limitation instead of fabricating Origin output with another plotting library.
