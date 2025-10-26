# Repository Summary

- CLI tool `markdown_toc_creator` generates Markdown tables of contents either
  in-place (default) or via stdout, making it suitable for scripts or CI.
- `markdown_toc_creator/main.py` exposes a Click CLI that discovers markdown
  files (with `--exclude`, `--skip-first-n-lines`, proactive insertion, stdout
  vs in-place, quiet mode) and forwards configuration to the ToC builder.
- `markdown_toc_creator/create_toc.py` parses headings, validates level flow,
  applies GitHub/GitLab anchor styles, renders indented entries, and refreshes
  the `<!--TOC-->` blocks with optional titles and horizontal rules that match
  mdformat or Prettier.
- `markdown_toc_creator/toc_entry.py` encapsulates anchor creation,
  deduplication, and text rendering; edge cases are covered by
  `tests/test_toc_entry.py`, while CLI behaviour lives in `tests/test_main.py`.
- `pyproject.toml` defines the package metadata, dependencies, CLI entry point,
  and dev extras; `tox.ini` and `requirements.dev` support lint/test workflows,
  and `.pre-commit-config.yaml` offers local hook integration.
