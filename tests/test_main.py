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
        ],
    }
    assert tocLines == expected[style]
