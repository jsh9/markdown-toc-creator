from pathlib import Path

import pytest

from markdown_toc_creator.main import createToc

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'data'


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
            '  - [This header has a :thumbsup: in it](#this-header-has-a-thumbsup-in-it)',
            '- [This header has Unicode in it: 中文](#this-header-has-unicode-in-it-中文)',
            '  - [This header has spaces in it](#this-header-has-spaces-in-it-1)',
            '    - [This header has spaces in it](#this-header-has-spaces-in-it-2)',
            '  - [This header has 3.5 in it (and parentheses)](#this-header-has-35-in-it-and-parentheses)',
            "    - [What day is today? I don't know.](#what-day-is-today-i-dont-know)",
            '  - [This header has     consecutive spaces in it](#this-header-has-----consecutive-spaces-in-it)',
            '    - [Hello _world_](#hello-world)',
            '    - [Hello *world*](#hello-world-1)',
            '    - [Hello __world__](#hello-world-2)',
            '    - [Hello **world**](#hello-world-3)',
            '    - [Hello _**world**_](#hello-world-4)',
            '    - [Hello *__world__*](#hello-world-5)',
            '  - [Here is `hello_?and!_world`](#here-is-hello_and_world)',
            '  - [🌻 This is a sunflower](#-this-is-a-sunflower)',
            '  - [This is a link to pypi](#this-is-a-link-to-pypi)',
            "  - [5. `ABC`,:! There shouldn't be two consecutive dashes here](#5-abc-there-shouldnt-be-two-consecutive-dashes-here)",
            '  - [7. ABC: This is great](#7-abc-this-is-great)',
            '  - [8. DEF:: This is better](#8-def-this-is-better)',
        ],
        'gitlab': [
            '- [This header has spaces in it](#this-header-has-spaces-in-it)',
            '  - [This header has a :thumbsup: in it](#this-header-has-a-in-it)',
            '- [This header has Unicode in it: 中文](#this-header-has-unicode-in-it-中文)',
            '  - [This header has spaces in it](#this-header-has-spaces-in-it-1)',
            '    - [This header has spaces in it](#this-header-has-spaces-in-it-2)',
            '  - [This header has 3.5 in it (and parentheses)](#this-header-has-35-in-it-and-parentheses)',
            "    - [What day is today? I don't know.](#what-day-is-today-i-dont-know)",
            '  - [This header has     consecutive spaces in it](#this-header-has-consecutive-spaces-in-it)',
            '    - [Hello _world_](#hello-world)',
            '    - [Hello *world*](#hello-world-1)',
            '    - [Hello __world__](#hello-world-2)',
            '    - [Hello **world**](#hello-world-3)',
            '    - [Hello _**world**_](#hello-world-4)',
            '    - [Hello *__world__*](#hello-world-5)',
            '  - [Here is `hello_?and!_world`](#here-is-hello_and_world)',
            '  - [🌻 This is a sunflower](#-this-is-a-sunflower)',
            '  - [This is a link to pypi](#this-is-a-link-to-pypi)',
            "  - [5. `ABC`,:! There shouldn't be two consecutive dashes here](#5-abc-there-shouldnt-be-two-consecutive-dashes-here)",
            '  - [7. ABC: This is great](#7-abc-this-is-great)',
            '  - [8. DEF:: This is better](#8-def-this-is-better)',
        ],
    }
    assert tocLines == expected[style]


@pytest.mark.parametrize(
    'style',
    ['github', 'gitlab'],
)
def testCreateTocWithSpecialUnicodeChars(style: str, tmp_path: Path) -> None:
    """Test that the tool can handle special Unicode characters like √, ∑, ∫, etc.

    This test ensures that files with mathematical symbols and other special
    Unicode characters can be written correctly with UTF-8 encoding, fixing
    the UnicodeEncodeError that occurred on Windows with cp1252 encoding.
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
