from typing import List

import pytest

from markdown_toc_creator.toc_entry import _buildListOfCharGroups, _CharGroup


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
    ],
)
def testBuildListOfCharGroups(string: str, expected: List[_CharGroup]) -> None:
    result = _buildListOfCharGroups(string)
    assert result == expected
