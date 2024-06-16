"""Args module - Parsing and other utilities to process ffmpeg CLI args.

Contains the `parse_args` function used to parse the ffmpeg command-line.
"""

import sys

from pffmpeg._utils import index_of

FFMPEG_VERBOSITY_OPTIONS = {
    "quiet": -8,
    "panic": 0,
    "fatal": 8,
    "error": 16,
    "warning": 24,
    "info": 32,
    "verbose": 40,
    "debug": 48,
    "trace": 56,
}


def parse_args(args: list[str], /) -> list[str]:
    """Parse the given `args`, remove incompatible args and flags.

    Examples:
        >>> args = ["-nostats", "-v", "0", "-i", "input.mp4", "output.mp4"]
        >>> assert parse_args(args) == ["-i", "input.mp4", "output.mp4"]
    """
    parsed_args = list(args)

    min_verbosity = FFMPEG_VERBOSITY_OPTIONS["info"]
    remove_flags(parsed_args, ["-nostats"])
    remove_loglevel(parsed_args, "-v", min_verbosity)
    remove_loglevel(parsed_args, "-loglevel", min_verbosity)

    return parsed_args


def remove_flags(args: list[str], /, flags: list[str]) -> None:
    """Remove `flags` from list of `args`.

    Examples:
        >>> args = ["-codecs"]
        >>> remove_flags(args, ["-test"])
        >>> assert args
        >>> remove_flags(args, ["-codecs"])
        >>> assert not args
    """
    for flag in flags:
        if (i := index_of(args, flag)) is not None:
            args.pop(i)
            print(f"Incompatible flag removed: {flag}", file=sys.stderr)


def remove_loglevel(
    args: list[str],
    /,
    loglevel_arg: str,
    min_verbosity: int,
) -> None:
    """Remove `loglevel_arg` from list of `args` if value is less than `min_verbosity`.

    Examples:
        >>> args = ["-v", "20"]
        >>> remove_loglevel(args, "-v", 20)
        >>> assert args
        >>> remove_loglevel(args, "-loglevel", 21)
        >>> assert args
        >>> remove_loglevel(args, "-v", 21)
        >>> assert not args
    """
    if (loglevel_index := index_of(args, loglevel_arg)) is not None:
        loglevel = args[loglevel_index + 1]
        loglevel_val = (
            int(loglevel)
            if loglevel.isdigit()
            else FFMPEG_VERBOSITY_OPTIONS.get(loglevel)
        )
        if loglevel_val is not None and loglevel_val < min_verbosity:
            args.pop(loglevel_index + 1)
            args.pop(loglevel_index)
            print(
                f"Incompatible loglevel removed: {loglevel} "
                f"(min verbosity = {min_verbosity})",
                file=sys.stderr,
            )
