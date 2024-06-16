"""CLI module - Command-line interface.

This module provides the command-line interface (CLI) wrapping `ffmpeg`.
The command `ffmpeg` is run with the arguments given to `pffmpeg`, and the command
output is modified to include a progress bar.
"""

import sys

from pffmpeg._runner import FfmpegRunnerWithProgressBar


def pffmpeg(args: list[str] | None = None) -> int:
    """PFFmpeg CLI, run ffmpeg with progress bar.

    Parameters:
        args: List of `ffmpeg` arguments, resolve as `sys.argv[1:]` if None given.
    """
    if args is None:
        args = sys.argv[1:]
    return FfmpegRunnerWithProgressBar().exec(args)
