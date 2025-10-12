# Change Log

## [0.0.11] - 2025-10-12

- Fixed
  - A bug where special characters would trigger errors on Windows system
- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.10...0.0.11

## [0.0.10] - 2024-12-25

- Fixed
  - Fixed dashes for GitHub style
- Changed
  - Using "modern" type annotations (e.g., `str | int | None`, `list[str]`)
- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.9...0.0.10

## [0.0.9] - 2024-12-25

- Changed
  - No longer produce consecutive dashes for Github style, because Github's
    behavior has changed (which becomes the same as Gitlab's)
- Removed
  - Removed Python 3.8 support
- Added
  - Added checks for Python 3.12 and 3.13
- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.8...0.0.9

## [0.0.8] - 2024-09-16

- Changed
  - Strip links inside headings before including them in ToC
- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.7...0.0.8

## [0.0.7] - 2024-09-12

- Changed
  - Rendered hyperlinks as texts only
- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.6...0.0.7

## [0.0.6] - 2024-01-08

- Fixed
  - Fixed a bug where dashes within backtick ("`") pairs are removed
- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.5...0.0.6

## [0.0.5] - 2023-11-08

- Fixed

  - Fixed a bug that does not ignore `#` in code blocks

- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.4...0.0.5

## [0.0.4] - 2023-07-20

- Fixed

  - Fixed how underscores are handled in anchor links

- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.3...0.0.4

## [0.0.3] - 2023-07-19

- Added

  - File type filter in pre-commit hook definition

- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.2...0.0.3

## [0.0.2] - 2023-07-19

- Fixed

  - Fixed pre-commit hooks
  - Fixed how ToC display texts are rendered

- Full diff
  - https://github.com/jsh9/markdown-toc-creator/compare/0.0.1...0.0.2

## [0.0.1] - 2023-07-19

Initial release
