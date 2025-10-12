from __future__ import annotations

from pathlib import Path

from markdown_toc_creator.exceptions import HeaderLevelNotContinuousException
from markdown_toc_creator.toc_entry import TocEntry, deduplicateAnchorLinkText

TOC_TAG = '<!--TOC-->'


def createToc(  # noqa: C901
        filename: Path,
        skip_first_n_lines: int = 1,
        quiet: bool = False,
        in_place: bool = True,
        style: str = 'github',
) -> list[str]:
    """Create table of content"""
    if not quiet:
        print('----------------------')
        print(filename)
        print('')

    with open(filename, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    lines = [_[:-1] for _ in lines]  # remove '\n' at the end of each line

    if not hasTocInsertionPoint(lines):
        return []

    prevLevel = -1  # just a placeholder
    initialLevel = -1  # just a placeholder

    isInitialHeader: bool = True
    tocEntries: list[TocEntry] = []
    inCodeBlock: bool = False

    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            inCodeBlock = not inCodeBlock

        if i + 1 <= skip_first_n_lines:
            continue

        if line.strip().startswith('#') and not inCodeBlock:
            thisLevel: int = _countNumOfPoundSigns(line)
            if isInitialHeader:
                isInitialHeader = False
                initialLevel = thisLevel
                prevLevel = thisLevel

            if thisLevel < initialLevel:
                raise HeaderLevelNotContinuousException(f'"{line}"')

            if thisLevel - prevLevel > 1:
                print(thisLevel)
                print(prevLevel)
                raise HeaderLevelNotContinuousException(f'"{line}"')

            absoluteLevelDiff: int = thisLevel - initialLevel
            indent = absoluteLevelDiff * '  '

            tocEntries.append(TocEntry(line.strip(), indent, style=style))

            prevLevel = thisLevel

    deduplicateAnchorLinkText(tocEntries=tocEntries)

    tocLines: list[str] = [_.render() for _ in tocEntries]

    if not quiet:
        for entry in tocEntries:
            print(entry.render())

    if in_place:
        start, end = findTocInsertionPoint(lines)
        final = lines[: start + 1] + [''] + tocLines + [''] + lines[end + 1 :]
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.writelines([_ + '\n' for _ in final])

    return tocLines


def hasTocInsertionPoint(textLines: list[str]) -> bool:
    tagCounter = 0
    for line in textLines:
        if line == TOC_TAG:
            tagCounter += 1

    return tagCounter == 2


def findTocInsertionPoint(textLine: list[str]) -> tuple[int, int]:
    """Assuming this markdown has ToC insertion point, find it"""
    counter = 0
    result = []
    for i, line in enumerate(textLine):
        if line == TOC_TAG:
            counter += 1
            if counter == 1:
                result.append(i)
            elif counter == 2:
                result.append(i - 1)
            else:
                raise ValueError('Internal error', counter)

    return tuple(result)


def _countNumOfPoundSigns(string: str) -> int:
    numOfPoundSigns: int = 0
    for char in string:
        if char == '#':
            numOfPoundSigns += 1
        else:
            break

    return numOfPoundSigns
