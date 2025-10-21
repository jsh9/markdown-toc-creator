from pathlib import Path
from shutil import copyfile

import pytest
from click.testing import CliRunner

from markdown_toc_creator.main import createToc, main

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'test_data'
PROACTIVE_DATA = DATA_DIR / 'proactive'
ADD_TOC_TITLE_DATA = DATA_DIR / 'add_toc_title'
ADD_HORIZONTAL_RULES_DATA = DATA_DIR / 'add_horizontal_rules'
TOC_TITLE_DATA = DATA_DIR / 'toc_title'


@pytest.mark.parametrize(
    'style',
    ['github', 'gitlab'],
)
def testCreateToc(style: str) -> None:
    tocLines = createToc(
        filename=DATA_DIR / 'test1.md',
        skip_first_n_lines=3,
        quiet=False,
        in_place=False,
        style=style,
    )
    expected = {
        'github': [
            '- [This header has spaces in it](#this-header-has-spaces-in-it)',
            '  - [This header has a :thumbsup: in it](#this-header-has-a-thumbsup-in-it)',  # noqa: E501
            '- [This header has Unicode in it: 中文](#this-header-has-unicode-in-it-中文)',  # noqa: E501
            '  - [This header has spaces in it](#this-header-has-spaces-in-it-1)',  # noqa: E501
            '    - [This header has spaces in it](#this-header-has-spaces-in-it-2)',  # noqa: E501
            '  - [This header has 3.5 in it (and parentheses)](#this-header-has-35-in-it-and-parentheses)',  # noqa: E501
            "    - [What day is today? I don't know.](#what-day-is-today-i-dont-know)",  # noqa: E501
            '  - [This header has     consecutive spaces in it](#this-header-has-----consecutive-spaces-in-it)',  # noqa: E501
            '    - [Hello _world_](#hello-world)',
            '    - [Hello *world*](#hello-world-1)',
            '    - [Hello __world__](#hello-world-2)',
            '    - [Hello **world**](#hello-world-3)',
            '    - [Hello _**world**_](#hello-world-4)',
            '    - [Hello *__world__*](#hello-world-5)',
            '  - [Here is `hello_?and!_world`](#here-is-hello_and_world)',
            '  - [🌻 This is a sunflower](#-this-is-a-sunflower)',
            '  - [This is a link to pypi](#this-is-a-link-to-pypi)',
            "  - [5. `ABC`,:! There shouldn't be two consecutive dashes here](#5-abc-there-shouldnt-be-two-consecutive-dashes-here)",  # noqa: E501
            '  - [7. ABC: This is great](#7-abc-this-is-great)',
            '  - [8. DEF:: This is better](#8-def-this-is-better)',
        ],
        'gitlab': [
            '- [This header has spaces in it](#this-header-has-spaces-in-it)',
            '  - [This header has a :thumbsup: in it](#this-header-has-a-in-it)',  # noqa: E501
            '- [This header has Unicode in it: 中文](#this-header-has-unicode-in-it-中文)',  # noqa: E501
            '  - [This header has spaces in it](#this-header-has-spaces-in-it-1)',  # noqa: E501
            '    - [This header has spaces in it](#this-header-has-spaces-in-it-2)',  # noqa: E501
            '  - [This header has 3.5 in it (and parentheses)](#this-header-has-35-in-it-and-parentheses)',  # noqa: E501
            "    - [What day is today? I don't know.](#what-day-is-today-i-dont-know)",  # noqa: E501
            '  - [This header has     consecutive spaces in it](#this-header-has-consecutive-spaces-in-it)',  # noqa: E501
            '    - [Hello _world_](#hello-world)',
            '    - [Hello *world*](#hello-world-1)',
            '    - [Hello __world__](#hello-world-2)',
            '    - [Hello **world**](#hello-world-3)',
            '    - [Hello _**world**_](#hello-world-4)',
            '    - [Hello *__world__*](#hello-world-5)',
            '  - [Here is `hello_?and!_world`](#here-is-hello_and_world)',
            '  - [🌻 This is a sunflower](#-this-is-a-sunflower)',
            '  - [This is a link to pypi](#this-is-a-link-to-pypi)',
            "  - [5. `ABC`,:! There shouldn't be two consecutive dashes here](#5-abc-there-shouldnt-be-two-consecutive-dashes-here)",  # noqa: E501
            '  - [7. ABC: This is great](#7-abc-this-is-great)',
            '  - [8. DEF:: This is better](#8-def-this-is-better)',
        ],
    }
    assert tocLines == expected[style]


def _assert_cli_result(
        tmp_path: Path,
        base_dir: Path,
        before_filename: str,
        after_filename: str,
        cli_args: list[str],
) -> None:
    runner = CliRunner()
    before_path = base_dir / 'before' / before_filename
    expected_path = base_dir / 'after' / after_filename
    target = tmp_path / before_path.name
    copyfile(before_path, target)

    result = runner.invoke(main, [*cli_args, str(target)])
    assert result.exit_code == 0

    actual_content = target.read_text(encoding='utf-8')
    expected_content = expected_path.read_text(encoding='utf-8')
    assert actual_content == expected_content


def _count_placeholders(content: str) -> int:
    return content.count('<!--TOC-->')


@pytest.mark.parametrize(
    ('before_filename', 'after_filename', 'cli_args'),
    [
        ('with_heading.md', 'with_heading_default.md', []),
        (
            'with_heading.md',
            'with_heading_no_title.md',
            ['--add-toc-title', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_no_rules.md',
            ['--add-horizontal-rules', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_minimal.md',
            ['--add-toc-title', 'False', '--add-horizontal-rules', 'False'],
        ),
        (
            'with_extra_placeholders.md',
            'with_extra_placeholders.md',
            [],
        ),
        (
            'no_heading.md',
            'no_heading_default.md',
            [],
        ),
        ('with_placeholder.md', 'with_placeholder_default.md', []),
        (
            'with_placeholder.md',
            'with_placeholder_no_title.md',
            ['--add-toc-title', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_rules.md',
            ['--add-horizontal-rules', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_minimal.md',
            ['--add-toc-title', 'False', '--add-horizontal-rules', 'False'],
        ),
        (
            'proactive_disabled.md',
            'proactive_disabled.md',
            ['--proactive', 'False'],
        ),
        (
            'proactive_disabled.md',
            'proactive_disabled.md',
            ['--proactive', 'False', '--add-horizontal-rules', 'False'],
        ),
    ],
    ids=[
        'heading-default',
        'heading-no-title',
        'heading-no-rules',
        'heading-minimal',
        'extras-default',
        'no-heading-default',
        'placeholder-default',
        'placeholder-no-title',
        'placeholder-no-rules',
        'placeholder-minimal',
        'proactive-off',
        'proactive-off-no-rules',
    ],
)
def test_cli_proactive_option(
        tmp_path: Path,
        before_filename: str,
        after_filename: str,
        cli_args: list[str],
) -> None:
    _assert_cli_result(
        tmp_path=tmp_path,
        base_dir=PROACTIVE_DATA,
        before_filename=before_filename,
        after_filename=after_filename,
        cli_args=cli_args,
    )


@pytest.mark.parametrize(
    ('before_filename', 'after_filename', 'cli_args'),
    [
        (
            'with_placeholder.md',
            'with_placeholder_default.md',
            [],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_title.md',
            ['--add-toc-title', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_rules.md',
            ['--add-horizontal-rules', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_minimal.md',
            ['--add-toc-title', 'False', '--add-horizontal-rules', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_title.md',
            ['--proactive', 'False', '--add-toc-title', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_rules.md',
            ['--proactive', 'False', '--add-horizontal-rules', 'False'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_minimal.md',
            [
                '--proactive',
                'False',
                '--add-toc-title',
                'False',
                '--add-horizontal-rules',
                'False',
            ],
        ),
    ],
    ids=[
        'default',
        'no-title',
        'no-rules',
        'minimal',
        'proactive-off-no-title',
        'proactive-off-no-rules',
        'proactive-off-minimal',
    ],
)
def test_cli_add_toc_title_option(
        tmp_path: Path,
        before_filename: str,
        after_filename: str,
        cli_args: list[str],
) -> None:
    _assert_cli_result(
        tmp_path=tmp_path,
        base_dir=ADD_TOC_TITLE_DATA,
        before_filename=before_filename,
        after_filename=after_filename,
        cli_args=cli_args,
    )


@pytest.mark.parametrize(
    ('before_filename', 'after_filename', 'cli_args'),
    [
        ('with_heading.md', 'with_heading_default.md', []),
        (
            'with_heading.md',
            'with_heading_no_rules.md',
            ['--add-horizontal-rules', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_no_title.md',
            ['--add-toc-title', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_minimal.md',
            ['--add-toc-title', 'False', '--add-horizontal-rules', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_proactive_disabled.md',
            ['--proactive', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_proactive_disabled.md',
            ['--proactive', 'False', '--add-horizontal-rules', 'False'],
        ),
        (
            'with_heading.md',
            'with_heading_proactive_disabled.md',
            ['--proactive', 'False', '--add-toc-title', 'False'],
        ),
    ],
    ids=[
        'default',
        'no-rules',
        'no-title',
        'minimal',
        'proactive-off',
        'proactive-off-no-rules',
        'proactive-off-no-title',
    ],
)
def test_cli_add_horizontal_rules_option(
        tmp_path: Path,
        before_filename: str,
        after_filename: str,
        cli_args: list[str],
) -> None:
    _assert_cli_result(
        tmp_path=tmp_path,
        base_dir=ADD_HORIZONTAL_RULES_DATA,
        before_filename=before_filename,
        after_filename=after_filename,
        cli_args=cli_args,
    )


@pytest.mark.parametrize(
    ('before_filename', 'after_filename', 'cli_args'),
    [
        ('with_placeholder.md', 'with_placeholder_default.md', []),
        (
            'with_placeholder.md',
            'with_placeholder_spanish.md',
            ['--toc-title', 'Tabla de Contenidos'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_emoji.md',
            ['--toc-title', '🍎🍌🍇'],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_title.md',
            [
                '--add-toc-title',
                'False',
                '--toc-title',
                "Doesn't really matter!!",
            ],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_no_rules.md',
            [
                '--toc-title',
                'Tabla de Contenidos',
                '--add-horizontal-rules',
                'False',
            ],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_minimal.md',
            [
                '--toc-title',
                'Tabla de Contenidos',
                '--add-horizontal-rules',
                'False',
                '--add-toc-title',
                'False',
                '--toc-title',
                "Doesn't really matter!!!!!!!!!!!!!!!!",
            ],
        ),
        (
            'with_placeholder.md',
            'with_placeholder_spanish.md',
            ['--toc-title', 'Tabla de Contenidos', '--proactive', 'False'],
        ),
    ],
    ids=[
        'default',
        'custom-spanish',
        'custom-emoji',
        'custom-no-title',
        'custom-no-rules',
        'custom-minimal',
        'custom-proactive-off',
    ],
)
def test_cli_toc_title_option(
        tmp_path: Path,
        before_filename: str,
        after_filename: str,
        cli_args: list[str],
) -> None:
    _assert_cli_result(
        tmp_path=tmp_path,
        base_dir=TOC_TITLE_DATA,
        before_filename=before_filename,
        after_filename=after_filename,
        cli_args=cli_args,
    )


def test_cli_multiple_runs_default_idempotent(tmp_path: Path) -> None:
    """Assert only 1 ToC no matter how many times the tool is run"""
    runner = CliRunner()
    source = PROACTIVE_DATA / 'before' / 'with_heading.md'
    expected = PROACTIVE_DATA / 'after' / 'with_heading_default.md'
    target = tmp_path / 'repeat.md'
    copyfile(source, target)
    for _ in range(100):  # run many times
        result = runner.invoke(main, [str(target)])
        assert result.exit_code == 0

    final_content = target.read_text(encoding='utf-8')
    assert _count_placeholders(final_content) == 2
    assert final_content == expected.read_text(encoding='utf-8')


@pytest.mark.parametrize(
    'style',
    ['github', 'gitlab'],
)
def testCreateTocWithSpecialUnicodeChars(style: str, tmp_path: Path) -> None:
    """
    Test that the tool can handle special Unicode characters like √, ∑, ∫, etc.

    This test ensures that files with mathematical symbols and other special
    Unicode characters can be written correctly with UTF-8 encoding, fixing the
    UnicodeEncodeError that occurred on Windows with cp1252 encoding.
    """
    # Create a test file with special Unicode characters
    test_file = tmp_path / 'test_unicode.md'
    content = """# Test Unicode Special Characters

<!--TOC-->

<!--TOC-->

## Mathematical symbols: √ ∑ ∫ ∞

Some text with square root √25 = 5.

## Greek letters: α β γ δ

Greek alphabet test.

## Special symbols: ™ © ® ±

Trademark and other symbols.

## Emoji and Unicode: 🚀 ✨ ❤️

Emoji test.

## Mixed: √(x²+y²) ≈ 10

Mathematical expression.
"""
    test_file.write_text(content, encoding='utf-8')

    # Run createToc with in_place=True to test writing
    tocLines: list[str] = createToc(
        filename=test_file,
        skip_first_n_lines=1,
        quiet=True,
        in_place=True,
        style=style,
    )

    # Verify the file can be read back with UTF-8 encoding
    result = test_file.read_text(encoding='utf-8')

    # Verify TOC was created and contains Unicode characters
    assert '## Mathematical symbols: √ ∑ ∫ ∞' in result
    assert '## Greek letters: α β γ δ' in result
    assert '## Special symbols: ™ © ® ±' in result
    assert '## Mixed: √(x²+y²) ≈ 10' in result

    # Verify TOC entries were generated correctly
    expected = {
        'github': [
            '- [Mathematical symbols: √ ∑ ∫ ∞](#mathematical-symbols---)',
            '- [Greek letters: α β γ δ](#greek-letters-α-β-γ-δ)',
            '- [Special symbols: ™ © ® ±](#special-symbols---)',
            '- [Emoji and Unicode: 🚀 ✨ ❤️](#emoji-and-unicode--)',
            '- [Mixed: √(x²+y²) ≈ 10](#mixed-x²y²--10)',
        ],
        'gitlab': [
            '- [Mathematical symbols: √ ∑ ∫ ∞](#mathematical-symbols)',
            '- [Greek letters: α β γ δ](#greek-letters-α-β-γ-δ)',
            '- [Special symbols: ™ © ® ±](#special-symbols)',
            '- [Emoji and Unicode: 🚀 ✨ ❤️](#emoji-and-unicode)',
            '- [Mixed: √(x²+y²) ≈ 10](#mixed-x²y²-10)',
        ],
    }
    assert tocLines == expected[style]
