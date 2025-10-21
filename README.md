# markdown-toc-creator

This is a command-line tool to create table of contents from markdown files.

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. Why should you use this tool?](#1-why-should-you-use-this-tool)
- [2. How to use this tool?](#2-how-to-use-this-tool)
  - [2.1. As a command-line tool](#21-as-a-command-line-tool)
  - [2.2. As a pre-commit hook](#22-as-a-pre-commit-hook)
- [3. Configuration options](#3-configuration-options)
  - [3.1. `--style`](#31---style)
  - [3.2. `--exclude`](#32---exclude)
  - [3.3. `--in-place`](#33---in-place)
  - [3.4. `--quiet` (or `-q`)](#34---quiet-or--q)
  - [3.5. `--skip-first-n-lines`](#35---skip-first-n-lines)
  - [3.6. `--proactive`](#36---proactive)
  - [3.7. `--add-toc-title`](#37---add-toc-title)
  - [3.8. `--toc-title`](#38---toc-title)
  - [3.9. `--add-horizontal-rules`](#39---add-horizontal-rules)
- [4. Compatibility with other formatters](#4-compatibility-with-other-formatters)
  - [4.1. With `markdown-heading-numbering`](#41-with-markdown-heading-numbering)
  - [4.2. With `mdformat`](#42-with-mdformat)

______________________________________________________________________

<!--TOC-->

## 1. Why should you use this tool?

Adding a table of contents to your markdown file can make it much easier to
navigate the file content (especially if the file is long).

But it's inconvenient and error-prone to manually create and maintain a table
of contents, as section titles and numbering could change in the future.

This tool can automate this process for you, saving your time and energy for
the truly important task: the content itself.

## 2. How to use this tool?

### 2.1. As a command-line tool

Install this tool:

```commandline
pip install markdown-toc-creator
```

And then run this command:

```commandline
markdown-toc-creator <PATH_TO_FOLDER_OR_FILE>
```

A table of contents will be put between `<!--TOC-->`.

### 2.2. As a pre-commit hook

Add something like this into your `.pre-commit-config.yaml` file:

```yaml
  - repo: https://github.com/jsh9/markdown-toc-creator
    rev: <REPLACE_WITH_LATEST_VERSION>
    hooks:
      - id: markdown-toc-creator
        args:
          - --proactive=False
          - --add-toc-title=True
```

(You can change the args yourself. Check out the following section.)

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

### 3.6. `--proactive`

If `True` (default), the tool creates a table of contents even when the
`<!--TOC-->` placeholders are missing. When disabled, files without
placeholders are left untouched.

If `False`, this tool will only create tables of contents in markdown files
with the following placeholder pairs:

```markdown
<!--TOC-->

<!--TOC-->
```

The ToC will be created within the placeholder pair.

### 3.7. `--add-toc-title`

If `True` (default), insert a bolded title line after the opening placeholder.
Combine with `--toc-title` to customise the text.

### 3.8. `--toc-title`

The text to use for the table-of-contents title when `--add-toc-title` is
enabled. Defaults to `"Table of Contents"` and supports arbitrary Unicode
strings (for example, emojis or non-English phrases).

This config option has no effect if `--add-toc-title` is `False`.

### 3.9. `--add-horizontal-rules`

If `True` (default), wrap the generated entries between horizontal rules
(`---`) for additional separation. (The ToC title, if added, will be within the
horizontal rules)

## 4. Compatibility with other formatters

### 4.1. With [`markdown-heading-numbering`](https://github.com/jsh9/markdown-heading-numbering/)

If you are also using my other markdown formatter
[`markdown-heading-numbering`](https://github.com/jsh9/markdown-heading-numbering/)
as a pre-commit hook to for create tables of contents in your markdown files,
it's better to use that hook **before** this one.

### 4.2. With [`mdformat`](https://github.com/hukkin/mdformat)

This tool is fully compatible with
[`mdformat`](https://github.com/hukkin/mdformat) as pre-commit hooks.
