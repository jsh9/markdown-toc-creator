# markdown-toc-creator

This is a command-line tool to create table of contents from markdown files.

<!--TOC-->

<!--TOC-->

## 1. Installation

```commandline
pip install markdown-toc-creator
```

## 2. Usage

In the markdown files that you would like to generate tables of contents, put
this placeholder at where you would like to the table of contents to go:

```markdown
<!--TOC-->

<!--TOC-->
```

And then run this command:

```commandline
markdown-toc-creator <PATH_TO_FOLDER_OR_FILE>
```

A table of contents will be put between `<!--TOC-->`.

Or, to use it as a pre-commit hook, add this into your
`.pre-commit-config.yaml` file:

```
  - repo: https://github.com/jsh9/markdown-toc-creator
    rev: <REPLACE_WITH_LATEST_VERSION>
    hooks:
      - id: markdown-toc-creator
```

## 3. Configuration options

### 3.1. `--style`

Pick between "gitlab" or "github" (default).

### 3.2. `--exclude`

Regex of file/folder name patterns to exclude, default:
`'\.git|\.tox|\.pytest_cache'`

### 3.3. `--in-place`

Whether to actually add the table of contents into the original markdown file.
Default: `True`.

### 3.4. `--quiet` (or `-q`)

If `True`, the generated table of contents will not be printed to the terminal.
Default: `False`.

### 3.5. `--skip-first-n-lines`

How many lines of the markdown file (starting from the top) to skip. This is
useful because usually the initial line of markdown file is H1 (header level 1,
with a `#`), and we don't want it to be included in the table of content.
