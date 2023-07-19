import re
from collections import defaultdict
from typing import List, Set

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

    def render(self) -> str:
        text = self.removePoundChar(self.displayText)
        return self.indent + f'- [{text}]({self.anchorLinkText})'

    def _calcAnchorLinkText(self) -> str:
        text = self.removePoundChar(self.displayText)

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

    @classmethod
    def removePoundChar(cls, string: str) -> str:
        # remove '#' characters from the start of the header
        return re.sub(r'^#+\s', '', string)


def deduplicateAnchorLinkText(tocEntries: List[TocEntry]) -> None:
    allAnchorLinkTexts: List[str] = [_.anchorLinkText for _ in tocEntries]

    seen: Set[str] = set()
    duplicated: Set[str] = set()

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
