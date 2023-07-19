from __future__ import annotations

import re
from pathlib import Path

import click

from markdown_toc_creator import __version__
from markdown_toc_creator.create_toc import createToc

# Due to a potential bug in Windows + pre-commit, non-ASCII
# characters cannot be rendered correctly as stdout in the terminal.
# Therefore, we set all CLI output as stderr.
# (More details in https://github.com/jsh9/pydoclint/issues/20)
echoAsError = True


def validateStyleValue(
        context: click.Context,
        param: click.Parameter,
        value: str | None,
) -> str | None:
    """Validate the value of the 'style' option"""
    if value not in {'github', 'gitlab'}:
        raise click.BadParameter('"--style" must be "github" or "gitlab"')

    return value


@click.command(
    context_settings={'help_option_names': ['-h', '--help']},
    help='Create table of contents for markdown files',
)
@click.option(
    '--exclude',
    type=str,
    show_default=True,
    default=r'\.git|\.tox|\.pytest_cache',
    help=(
        'Regex pattern to exclude files/folders. Please add quotes (both'
        ' double and single quotes are fine) around the regex in the'
        ' command line.'
    ),
)
@click.option(
    '--style',
    type=str,
    show_default=True,
    default='github',
    callback=validateStyleValue,
    help='',
)
@click.option(
    '--in-place',
    type=bool,
    show_default=True,
    default=True,
    help='If True, change the markdown file in place',
)
@click.option(
    '--skip-first-n-lines',
    type=int,
    show_default=True,
    default=1,
    help='How many lines from the top of the markdown to skip',
)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    default=False,
    help='If True, do not print results to the terminal.',
)
@click.option(
    '-s',
    '--src',
    type=str,
    help='The source file to check',
)
@click.argument(
    'paths',
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        allow_dash=True,
    ),
    is_eager=True,
)
@click.version_option(__version__)
@click.pass_context
def main(
        ctx: click.Context,
        exclude: str,
        skip_first_n_lines: int,
        quiet: bool,
        in_place: bool,
        src: str | None,
        paths: tuple[str, ...],
        style: str,
):
    """Command-line entry point"""
    ctx.ensure_object(dict)

    if paths and src is not None:
        click.echo(
            main.get_usage(ctx)
            + "\n\n'paths' and 'src' cannot be passed simultaneously.",
            err=echoAsError,
        )
        ctx.exit(1)

    if not paths and src is None:
        click.echo(
            main.get_usage(ctx) + "\n\nOne of 'paths' or 'src' is required.",
            err=echoAsError,
        )
        ctx.exit(1)

    _checkPaths(
        paths,
        exclude=exclude,
        skip_first_n_lines=skip_first_n_lines,
        quiet=quiet,
        in_place=in_place,
        style=style,
    )


def _checkPaths(
        paths: tuple[str, ...],
        exclude: str = '',
        skip_first_n_lines: int = 1,
        quiet: bool = False,
        in_place: bool = True,
        style: str = 'github',
) -> None:
    filenames: list[Path] = []

    if not quiet:
        skipMsg = f'Skipping files that match this pattern: {exclude}'
        click.echo(
            click.style(skipMsg, fg='yellow', bold=True), err=echoAsError
        )

    excludePattern = re.compile(exclude)

    for path_ in paths:
        path = Path(path_)
        if path.is_file():
            filenames.append(path)
        elif path.is_dir():
            filenames.extend(sorted(path.rglob('*.md')))

    for filename in filenames:
        if excludePattern.search(filename.as_posix()):
            continue

        createToc(
            filename,
            skip_first_n_lines=skip_first_n_lines,
            quiet=quiet,
            in_place=in_place,
            style=style,
        )


if __name__ == '__main__':
    main()
