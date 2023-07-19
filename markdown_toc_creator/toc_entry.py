from __future__ import annotations

import re
from collections import defaultdict

from bs4 import BeautifulSoup


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

    def _calcAnchorLinkText(self) -> str:
        # remove '#' characters from the start of the header
        text = re.sub(r'^#+\s', '', self.displayText)

        # remove HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()

        if self.style == 'gitlab':
            # remove emojis represented as :emoji_name:
            text = re.sub(r':[\w\d_]+:', '', text)

        # convert to lower case, replace spaces with hyphens, remove special characters
        anchorLink = re.sub(r'[^\w\s-]+', '', text.lower().replace(' ', '-'))

        if self.style == 'gitlab':
            anchorLink = re.sub(r'-+', '-', anchorLink)

        # check last character
        anchorLink = anchorLink[:-1] if anchorLink[-1] == '-' else anchorLink

        # prepend '#' to create a URL anchor
        return '#' + anchorLink

    def render(self) -> str:
        return self.indent + f'- [{self.displayText}]({self.anchorLinkText})'


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