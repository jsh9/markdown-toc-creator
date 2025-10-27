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
  - [3.1. `--proactive` (default: `True`)](#31---proactive-default-true)
    - [3.1.1. If `--proactive=True`](#311-if---proactivetrue)
    - [3.1.2. If `--proactive=False`](#312-if---proactivefalse)
  - [3.2. `--style` (default: "github")](#32---style-default-github)
  - [3.3. `--exclude` (default: '.git|.tox|.pytest_cache')](#33---exclude-default-gittoxpytest_cache)
  - [3.4. `--in-place` (default: `True`)](#34---in-place-default-true)
  - [3.5. `--quiet` (or `-q` ,default: `False`)](#35---quiet-or--q-default-false)
  - [3.6. `--skip-first-n-lines` (default: 1)](#36---skip-first-n-lines-default-1)
  - [3.7. `--add-toc-title` (default: `True`)](#37---add-toc-title-default-true)
  - [3.8. `--toc-title` (default: `'Table of Contents'`)](#38---toc-title-default-table-of-contents)
  - [3.9. `--add-horizontal-rules` (default: `True`)](#39---add-horizontal-rules-default-true)
  - [3.10. `--horizontal-rule-style` (default: `'mdformat'`)](#310---horizontal-rule-style-default-mdformat)
  - [3.11. `--config` (default: `'pyproject.toml'`)](#311---config-default-pyprojecttoml)
- [4. Compatibility with other formatters](#4-compatibility-with-other-formatters)
  - [4.1. With `markdown-heading-numbering`](#41-with-markdown-heading-numbering)
  - [4.2. With `mdformat`](#42-with-mdformat)

______________________________________________________________________

<!--TOC-->

## 1. Why should you use this tool?

Tables of contents (ToC) make markdown documents easier to understand and to
navigate.

But generating them (and more importantly, keeping them updated) is tedious and
error prone. This tool can automate this process for you, saving your time and
energy for the truly important task: the document's content itself.

Additional, I've written another tool,
[`markdown-heading-numbering`](https://github.com/jsh9/markdown-heading-numbering/)
to help you add numbering to markdown headers. You are welcome to try it out
too. ([More notes below](#41-with-markdown-heading-numbering).)

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

*(Config options are introduced in the
[seciton below](#3-configuration-options).)*

By default, a table of contents will be generated below Line 1 of every
markdown file in your path (or in your specified files).

If you want to manually control which markdown file will have ToC generated
(and where in the file the ToC is), check out the
[`--proactive`](#31---proactive) config option below.

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

*(You can change the args yourself. Check out the following section for all
possible args.)*

## 3. Configuration options

### 3.1. `--proactive` (default: `True`)

#### 3.1.1. If `--proactive=True`

If `True` (default), the tool creates a table of contents below Line 1 of every
markdown file in your specified path.

A pair of HTML comments will be added to the file, and the table of contents
are generated within it:

```markdown
<!--TOC-->

<!--TOC-->
```

#### 3.1.2. If `--proactive=False`

The tool would not be in the "proactive" mode.

In this mode, if you want tables of contents auto-generated for some markdown
files, you'll need to put the HTML comment pair (double `<!--TOC-->`) into
those files, and then a ToC will be generated between the comments.

### 3.2. `--style` (default: "github")

Pick between "gitlab" or "github" (default).

### 3.3. `--exclude` (default: '.git|.tox|.pytest_cache')

Regex of file/folder name patterns to exclude, default:
`'\.git|\.tox|\.pytest_cache'`

### 3.4. `--in-place` (default: `True`)

Whether to actually add the table of contents into the original markdown file.
Default: `True`.

### 3.5. `--quiet` (or `-q` ,default: `False`)

If `True`, the generated table of contents will not be printed to the terminal.
Default: `False`.

### 3.6. `--skip-first-n-lines` (default: 1)

How many lines of the markdown file (starting from the top) to skip. This is
useful because usually the initial line of markdown file is H1 (header level 1,
with a `#`), and we don't want it to be included in the table of content.

### 3.7. `--add-toc-title` (default: `True`)

If `True` (default), insert a bolded title line after the opening placeholder.
Combine with `--toc-title` to customise the text.

### 3.8. `--toc-title` (default: `'Table of Contents'`)

The text to use for the table-of-contents title when `--add-toc-title` is
enabled. Defaults to `"Table of Contents"` and supports arbitrary Unicode
strings (for example, emojis or non-English phrases).

This config option has no effect if `--add-toc-title` is `False`.

### 3.9. `--add-horizontal-rules` (default: `True`)

If `True` (default), wrap the generated entries between horizontal rules for
additional separation (the ToC title, if added, will be inside the rules). Pair
this with `--horizontal-rule-style` to pick which thematic break format to use.

### 3.10. `--horizontal-rule-style` (default: `'mdformat'`)

Controls the style of the horizontal rules inserted when
`--add-horizontal-rules` is enabled:

- `mdformat` (default): uses 70 underscores to match `mdformat`'s style
- `prettier`: uses `---` to match Prettier's style

### 3.11. `--config` (default: `'pyproject.toml'`)

Use this option to load default values for the other flags from a TOML file.

- By default the CLI looks for `[tool.markdown_toc_creator]` in file
  `pyproject.toml`. You can point to another file with
  `markdown-toc-creator --config <MY_TOML_FILE_NAME> <paths>`.
- Keys inside the section use the same kebab-case flag names:

```toml
[tool.markdown_toc_creator]
proactive = false
add-toc-title = false
horizontal-rule-style = "prettier"
skip-first-n-lines = 2
```

- The TOML file must exist and contain the `[tool.markdown_toc_creator]`
  section, otherwise the command exits with an error.
- Explicit CLI arguments will override the values loaded from the config file

## 4. Compatibility with other formatters

### 4.1. With [`markdown-heading-numbering`](https://github.com/jsh9/markdown-heading-numbering/)

If you are also using my other markdown formatter
[`markdown-heading-numbering`](https://github.com/jsh9/markdown-heading-numbering/)
as a pre-commit hook to for create tables of contents in your markdown files,
it's better to use that hook **before** this one.

### 4.2. With [`mdformat`](https://github.com/hukkin/mdformat)

This tool is fully compatible with
[`mdformat`](https://github.com/hukkin/mdformat) as pre-commit hooks.
