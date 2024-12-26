from typing import List

import pytest

from markdown_toc_creator.toc_entry import (
    TocEntry,
    _buildListOfCharGroups,
    _CharGroup,
)


@pytest.mark.parametrize(
    'string, expected',
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
def testBuildListOfCharGroups(string: str, expected: List[_CharGroup]) -> None:
    result = _buildListOfCharGroups(string)
    assert result == expected


def test_link_removal():
    entry = TocEntry('hello world [somelink](https://foo.bar)', '', 'github')
    assert entry.render() == '- [hello world somelink](#hello-world-somelink)'


def test_emoji_at_beginning():
    entry = TocEntry('🐧 hello world', '', 'github')
    assert entry.anchorLinkText == '#-hello-world'
    assert entry.render() == '- [🐧 hello world](#-hello-world)'
