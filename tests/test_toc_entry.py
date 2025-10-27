from __future__ import annotations

import pytest

from markdown_toc_creator.toc_entry import (
    TocEntry,
    _buildListOfCharGroups,
    _CharGroup,
)


@pytest.mark.parametrize(
    ('string', 'expected'),
    [
        (
            'something',
            [
                _CharGroup(
                    chars=['s', 'o', 'm', 'e', 't', 'h', 'i', 'n', 'g'],
                    insideBacktickPairs=False,
                )
            ],
        ),
        (
            'ab`cd`?!^',
            [
                _CharGroup(
                    chars=['a', 'b'],
                    insideBacktickPairs=False,
                ),
                _CharGroup(
                    chars=['c', 'd'],
                    insideBacktickPairs=True,
                ),
                _CharGroup(
                    chars=['?', '!', '^'],
                    insideBacktickPairs=False,
                ),
            ],
        ),
        (
            'ab`cd`',
            [
                _CharGroup(
                    chars=['a', 'b'],
                    insideBacktickPairs=False,
                ),
                _CharGroup(
                    chars=['c', 'd'],
                    insideBacktickPairs=True,
                ),
            ],
        ),
        (
            'ab`cd',
            [
                _CharGroup(
                    chars=['a', 'b'],
                    insideBacktickPairs=False,
                ),
                _CharGroup(
                    chars=['c', 'd'],
                    insideBacktickPairs=True,
                ),
            ],
        ),
        (
            '`abcd`',
            [
                _CharGroup(
                    chars=['a', 'b', 'c', 'd'],
                    insideBacktickPairs=True,
                ),
            ],
        ),
        (
            '`abcd',
            [
                _CharGroup(
                    chars=['a', 'b', 'c', 'd'],
                    insideBacktickPairs=True,
                ),
            ],
        ),
        (
            'abcd`',
            [
                _CharGroup(
                    chars=['a', 'b', 'c', 'd'],
                    insideBacktickPairs=False,
                ),
            ],
        ),
        (
            "shouldn't",
            [
                _CharGroup(
                    chars=['s', 'h', 'o', 'u', 'l', 'd', 'n', "'", 't'],
                    insideBacktickPairs=False,
                ),
            ],
        ),
    ],
)
def testBuildListOfCharGroups(string: str, expected: list[_CharGroup]) -> None:
    result = _buildListOfCharGroups(string)
    assert result == expected


def test_link_removal() -> None:
    entry = TocEntry('hello world [somelink](https://foo.bar)', '', 'github')
    assert entry.render() == '- [hello world somelink](#hello-world-somelink)'


def test_emoji_at_beginning() -> None:
    entry = TocEntry('🐧 hello world', '', 'github')
    assert entry.anchorLinkText == '#-hello-world'
    assert entry.render() == '- [🐧 hello world](#-hello-world)'


@pytest.mark.parametrize(
    ('heading', 'style', 'expected_anchor'),
    [
        (
            "3.3. `--exclude` (default: '.git|.tox|.pytest_cache')",
            'github',
            '#33---exclude-default-gittoxpytest_cache',
        ),
        (
            "3.3. `--exclude` (default: '.git|.tox|.pytest_cache')",
            'gitlab',
            '#33-exclude-default-gittoxpytest_cache',
        ),
        (
            'Heading literal pytest_cache',
            'github',
            '#heading-literal-pytest_cache',
        ),
        (
            'Heading literal pytest_cache',
            'gitlab',
            '#heading-literal-pytest_cache',
        ),
        (
            'Use __init__ for __repr__',
            'github',
            '#use-init-for-repr',
        ),
        (
            'Use __init__ for __repr__',
            'gitlab',
            '#use-init-for-repr',
        ),
        (
            'Mix `code_block` and literal cache_name',
            'github',
            '#mix-code_block-and-literal-cache_name',
        ),
        (
            'Mix `code_block` and literal cache_name',
            'gitlab',
            '#mix-code_block-and-literal-cache_name',
        ),
    ],
)
def test_anchor_generation_with_underscores(
        heading: str, style: str, expected_anchor: str
) -> None:
    entry = TocEntry(heading, '', style)
    assert entry.anchorLinkText == expected_anchor


@pytest.mark.parametrize(
    ('heading', 'expected_github', 'expected_gitlab'),
    [
        ('Hello _world_', '#hello-world', '#hello-world'),
        ('Hello __world__', '#hello-world', '#hello-world'),
        ('_Hello_ world', '#hello-world', '#hello-world'),
        (
            'Hello _world_ literal pytest_cache',
            '#hello-world-literal-pytest_cache',
            '#hello-world-literal-pytest_cache',
        ),
        (
            '__Hello__ _world_ literal_underscore',
            '#hello-world-literal_underscore',
            '#hello-world-literal_underscore',
        ),
    ],
)
def test_markdown_emphasis_underscores(
        heading: str,
        expected_github: str,
        expected_gitlab: str,
) -> None:
    github_entry = TocEntry(heading, '', 'github')
    gitlab_entry = TocEntry(heading, '', 'gitlab')

    assert github_entry.anchorLinkText == expected_github
    assert gitlab_entry.anchorLinkText == expected_gitlab


@pytest.mark.parametrize(
    ('oldChars', 'expectedChars'),
    [
        ('', ''),
        ('    ', ' '),
        ('\t\n \t\n \n', '\n'),
        (':? 2. best', ' 2. best'),
        (': Good', ' Good'),
        ('🐧: Good', '🐧: Good'),
        (':;!你好', '!你好'),
    ],
)
def testReduceToOnlyOneLeadingNonAlphaNumericChars(
        oldChars: list[str],
        expectedChars: list[str],
) -> None:
    charGroup = _CharGroup(chars=oldChars, insideBacktickPairs=False)
    charGroup.reduceToOnlyOneLeadingNonAlphaNumericChars()
    assert ''.join(charGroup.chars) == expectedChars
