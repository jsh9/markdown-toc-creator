from __future__ import annotations

import re
import unicodedata
import warnings
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

import bs4


class TocEntry:
    def __init__(
            self,
            displayText: str,
            indent: str,
            style: str,
    ) -> None:
        self.displayText = displayText
        self.indent = indent
        self.style = style
        self.anchorLinkText: str = self._calcAnchorLinkText()

    def render(self) -> str:
        text = self.removePoundChar(self.displayText)
        text = self.mdLinkToText(text)
        return self.indent + f'- [{text}]({self.anchorLinkText})'

    def _calcAnchorLinkText(self) -> str:
        text = self.removePoundChar(self.displayText)

        # remove HTML tags
        with warnings.catch_warnings():
            warnings.filterwarnings(
                action='ignore', category=bs4.MarkupResemblesLocatorWarning
            )
            soup = bs4.BeautifulSoup(text, 'html.parser')
            text = soup.get_text()

        return self.convertToAnchorLink(text=text, style=self.style)

    @classmethod
    def removePoundChar(cls, string: str) -> str:
        # remove '#' characters from the start of the header
        return re.sub(r'^#+\s', '', string)

    @classmethod
    def mdLinkToText(cls, string: str) -> str:
        # Replace markdown links with their display text
        # E.g., [my site](mysite.com) -> my site
        return re.sub(r'\[(.*?)]\(.*?\)', '\\1', string)

    @classmethod
    def convertToAnchorLink(
            cls,
            text: str,
            style: Literal['gitlab', 'github'],
    ) -> str:
        if style == 'gitlab':
            # remove emojis represented as :emoji_name:
            text = re.sub(r':[\w\d_]+:', '', text)

        text = text.lower()
        text = cls.mdLinkToText(text)

        listOfCharGroups: list[_CharGroup] = _buildListOfCharGroups(text)
        anchorLink: str = _constructAnchorLink(listOfCharGroups)

        if style == 'gitlab':
            anchorLink = re.sub(r'-+', '-', anchorLink)

        # check last character
        anchorLink = anchorLink[:-1] if anchorLink[-1] == '-' else anchorLink

        # prepend '#' to create a URL anchor
        return '#' + anchorLink


def deduplicateAnchorLinkText(tocEntries: list[TocEntry]) -> None:
    allAnchorLinkTexts: list[str] = [_.anchorLinkText for _ in tocEntries]

    seen: set[str] = set()
    duplicated: set[str] = set()

    for text in allAnchorLinkTexts:
        if text not in seen:
            seen.add(text)
        else:
            duplicated.add(text)

    if len(duplicated) == 0:
        return

    counter = defaultdict(int)

    for entry in tocEntries:
        if entry.anchorLinkText in duplicated:
            counter[entry.anchorLinkText] += 1
            count: int = counter[entry.anchorLinkText]
            if count >= 2:  # we only modify anchor link from the 2nd occurrence
                entry.anchorLinkText += f'-{count - 1}'


@dataclass
class _CharGroup:
    chars: list[str]
    insideBacktickPairs: bool

    def __eq__(self, other: '_CharGroup') -> bool:
        return (
            self.chars == other.chars
            and self.insideBacktickPairs == other.insideBacktickPairs
        )

    def reduceToOnlyOneLeadingNonAlphaNumericChars(self) -> None:
        """Reduce to only 1 leading non-alphanumeric characters"""
        flag: bool = False
        leadingNonAlphaNumericChars: list[str] = []
        otherChars: list[str] = []

        for i, char in enumerate(self.chars):
            if flag:
                break

            if _isWordChar(char):
                flag = True
                otherChars.extend(self.chars[i:])
                continue

            leadingNonAlphaNumericChars.append(char)

        self.chars = leadingNonAlphaNumericChars[-1:] + otherChars


def _isWordChar(char: str) -> bool:
    """
    Check if a char is a word character (alphanumeric, emoji, characters of
    other languages).
    """
    if char.isalnum():
        return True

    if unicodedata.category(char) == 'So':  # "Symbol, other", i.e., emoji
        return True

    if unicodedata.category(char).startswith('L'):  # letters of any script
        return True

    return False


def _buildListOfCharGroups(string: str) -> list[_CharGroup]:
    result: list[_CharGroup]
    isWithinBacktickPair: bool

    if string[0] == '`':
        result = [_CharGroup(chars=[], insideBacktickPairs=True)]
    else:
        result = [_CharGroup(chars=[string[0]], insideBacktickPairs=False)]

    isWithinBacktickPair: bool = False
    for char in string[1:]:
        if char == '`':
            isWithinBacktickPair = not isWithinBacktickPair
            result.append(
                _CharGroup(chars=[], insideBacktickPairs=isWithinBacktickPair)
            )
        else:
            result[-1].chars.append(char)

    if result[-1].chars == []:
        return result[:-1]

    return result


def _constructAnchorLink(listOfCharGroups: list[_CharGroup]) -> str:
    temp: list[str] = []
    for charGroup in listOfCharGroups:
        if not charGroup.insideBacktickPairs:
            # This is fine for both GitHub and Gitlab styles
            charGroup.reduceToOnlyOneLeadingNonAlphaNumericChars()

            # We put `strip()` before replacing " " to "-" to prevent
            # double dashes
            temp.append(
                ''.join(charGroup.chars)
                .strip()
                .replace(' ', '-')
                .replace('_', '')
            )
        else:
            temp.append(''.join(charGroup.chars).strip().replace(' ', '-'))

    return re.sub(
        r'[^\w\s-]+',
        '',
        '-'.join(temp),
    )
