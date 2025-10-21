# Repository Summary

- CLI tool `markdown_toc_creator` builds Markdown tables of contents either
  in-place or via stdout.
- `main.py` wires the Click-based interface, walks provided paths, filters
  markdown files, and delegates to `createToc`; options include proactive
  inserts, toggles for ToC title/horizontal rules, and a customizable
  `--toc-title` string.
- `create_toc.py` parses headings, enforces header-level continuity, renders
  indented links with optional GitHub/GitLab styles, writes content between
  `<!--TOC-->` tags, and keeps runs idempotent by refreshing existing
  placeholders in place.
- `toc_entry.py` encapsulates anchor generation, deduplication, and rendering
  rules; tested via `tests/test_toc_entry.py`.
- Automated coverage relies on `pytest` suites in `tests/`, while packaging
  metadata lives in `pyproject.toml` with optional `tox` workflows.
