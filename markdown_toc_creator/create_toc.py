from __future__ import annotations

from pathlib import Path

from markdown_toc_creator.exceptions import HeaderLevelNotContinuousError
from markdown_toc_creator.toc_entry import TocEntry, deduplicateAnchorLinkText

TOC_TAG = '<!--TOC-->'

DEFAULT_HORIZONTAL_RULE_STYLE: str = 'mdformat'
HORIZONTAL_RULE_STYLES: dict[str, str] = {
    # 70 underscores, which is the default style of mdformat:
    # https://mdformat.readthedocs.io/en/stable/users/style.html#thematic-breaks
    'mdformat': '_' * 70,
    # Matches Prettier's default thematic break:
    'prettier': '---',
}


def createToc(  # noqa: C901
        filename: Path,
        skip_first_n_lines: int = 1,
        quiet: bool = False,
        in_place: bool = True,
        proactive: bool = True,
        add_toc_title: bool = True,
        add_horizontal_rules: bool = True,
        toc_title: str = 'Table of Contents',
        style: str = 'github',
        horizontal_rule_style: str = DEFAULT_HORIZONTAL_RULE_STYLE,
) -> list[str]:
    """Create table of content"""
    if not quiet:
        print('----------------------')
        print(filename)
        print()

    with Path(filename).open(encoding='utf-8') as fp:
        lines = fp.readlines()

    lines = [_[:-1] for _ in lines]  # remove '\n' at the end of each line

    hasInsertionPoint = hasTocInsertionPoint(lines)
    if not hasInsertionPoint and not proactive:
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
                raise HeaderLevelNotContinuousError(f'"{line}"')

            if thisLevel - prevLevel > 1:
                print(thisLevel)
                print(prevLevel)
                raise HeaderLevelNotContinuousError(f'"{line}"')

            absoluteLevelDiff: int = thisLevel - initialLevel
            indent = absoluteLevelDiff * '  '

            tocEntries.append(TocEntry(line.strip(), indent, style=style))

            prevLevel = thisLevel

    if proactive and (not hasInsertionPoint) and not tocEntries:
        # Proactive mode should not create ToCs without headings beyond the
        # skipped lines
        return []

    deduplicateAnchorLinkText(tocEntries=tocEntries)

    tocLines: list[str] = [_.render() for _ in tocEntries]

    if not quiet:
        for entry in tocEntries:
            print(entry.render())

    if in_place:
        horizontal_rule: str = _resolve_horizontal_rule(horizontal_rule_style)
        if hasInsertionPoint:
            start, end = findTocInsertionPoint(lines)
            innerContent = _buildInnerTocContent(
                tocLines=tocLines,
                add_toc_title=add_toc_title,
                add_horizontal_rules=add_horizontal_rules,
                toc_title=toc_title,
                horizontal_rule=horizontal_rule,
            )
            prefix = lines[:start]
            suffix = lines[end + 1 :]
            final = prefix + [TOC_TAG] + innerContent + [TOC_TAG] + suffix
        else:
            final = _insertTocWithoutPlaceholder(
                lines=lines,
                tocLines=tocLines,
                add_toc_title=add_toc_title,
                add_horizontal_rules=add_horizontal_rules,
                toc_title=toc_title,
                horizontal_rule=horizontal_rule,
            )

        with Path(filename).open('w', encoding='utf-8') as fp:
            fp.writelines([_ + '\n' for _ in final])

    return tocLines


def hasTocInsertionPoint(textLines: list[str]) -> bool:
    """Detect whether the lines have ToC insertion point"""
    tagCounter = 0
    for line in textLines:
        if line == TOC_TAG:
            tagCounter += 1

    return tagCounter >= 2


def findTocInsertionPoint(textLine: list[str]) -> tuple[int, int]:
    """Find the indices of the first pair of ToC placeholders"""
    first: int | None = None
    second: int | None = None
    for i, line in enumerate(textLine):
        if line == TOC_TAG:
            if first is None:
                first = i
            elif second is None:
                second = i
                break

    if first is None or second is None:
        raise ValueError('Could not locate two ToC placeholders')

    return first, second


def _countNumOfPoundSigns(string: str) -> int:
    numOfPoundSigns: int = 0
    for char in string:
        if char == '#':
            numOfPoundSigns += 1
        else:
            break

    return numOfPoundSigns


def _findFirstNonEmptyLine(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        if line.strip():
            return index

    return None


def _buildInnerTocContent(
        tocLines: list[str],
        add_toc_title: bool,
        add_horizontal_rules: bool,
        toc_title: str,
        horizontal_rule: str,
) -> list[str]:
    content: list[str] = ['']

    if add_horizontal_rules:
        content.append(horizontal_rule)
        content.append('')

    if add_toc_title:
        content.append(f'**{toc_title}**')
        content.append('')

    if tocLines:
        content.extend(tocLines)
        content.append('')
    else:
        content.append('')

    if add_horizontal_rules:
        content.append(horizontal_rule)
        content.append('')

    return content


def _buildProactiveBlock(
        tocLines: list[str],
        add_toc_title: bool,
        add_horizontal_rules: bool,
        toc_title: str,
        horizontal_rule: str,
) -> list[str]:
    innerContent = _buildInnerTocContent(
        tocLines=tocLines,
        add_toc_title=add_toc_title,
        add_horizontal_rules=add_horizontal_rules,
        toc_title=toc_title,
        horizontal_rule=horizontal_rule,
    )
    return [TOC_TAG] + innerContent + [TOC_TAG]


def _insertTocWithoutPlaceholder(
        lines: list[str],
        tocLines: list[str],
        add_toc_title: bool,
        add_horizontal_rules: bool,
        toc_title: str,
        horizontal_rule: str,
) -> list[str]:
    tocSection = _buildProactiveBlock(
        tocLines=tocLines,
        add_toc_title=add_toc_title,
        add_horizontal_rules=add_horizontal_rules,
        toc_title=toc_title,
        horizontal_rule=horizontal_rule,
    )
    blockWithSpacing = [''] + tocSection

    firstNonEmptyIndex = _findFirstNonEmptyLine(lines)
    if firstNonEmptyIndex is None:
        return blockWithSpacing

    firstLine = lines[firstNonEmptyIndex]
    if firstLine.lstrip().startswith('#'):
        insertPos = firstNonEmptyIndex + 1
        return lines[:insertPos] + blockWithSpacing + lines[insertPos:]

    return blockWithSpacing + lines


def _resolve_horizontal_rule(style: str) -> str:
    try:
        return HORIZONTAL_RULE_STYLES[style]
    except KeyError as exc:
        raise ValueError(
            '"--horizontal-rule-style" must be one of'
            f' {sorted(HORIZONTAL_RULE_STYLES)}'
        ) from exc
