"""Runner module - Implementation of ffmpeg runner wrapper.

This module provides the runner wrapping the execution of `ffmpeg`.
The command `ffmpeg` is run with the arguments given to `pffmpeg`,
and the command output is patched to include a progress bar.
"""

import re
import subprocess
import sys
from abc import ABCMeta, abstractmethod
from typing import IO, cast

from rich.progress import (
    Progress,
    SpinnerColumn,
    TimeElapsedColumn,
)

from pffmpeg._args import parse_args
from pffmpeg._utils import KEYBOARD_INTERRUPT_RETURN_CODE, StringBuffer, parse_duration

FFMPEG_DURATION_REGEX = re.compile(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})")
FFMPEG_STATUS_REGEX = re.compile(r"frame=.*time=(\d{2}):(\d{2}):(\d{2})\.(\d{2}).*")

FFMPEG_CONFIRM_TEXT = "[y/N] "


class FfmpegRunnerWithProgressBar:
    """Execute `ffmpeg` and patch output with progress bar.

    This runner implements the state design pattern to handle the parsing of the
    execution output.
    """

    def __init__(self) -> None:
        self.state: FfmpegState = NullState(runner=self)
        self.total_duration: float | None = None
        self.progress = Progress(
            SpinnerColumn(finished_text=":heavy_check_mark:"),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
        )
        self.task = self.progress.add_task("Progress")

    def exec(self, args: list[str], /) -> int:
        """Execute `ffmpeg` command with `args`, patch output with progress bar."""
        self.set_total_duration(None)
        self.set_progress(None)
        self.stop_progress()
        self.change_state(PrintBeforeDurationState)
        try:
            cmd = ["ffmpeg", *parse_args(args)]
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)  # noqa: S603
            output = cast(IO[str], process.stderr)
            with StringBuffer() as buffer:
                while process.poll() is None:
                    self._process_output(output, buffer=buffer)
            returncode = process.returncode
            return process.returncode if isinstance(returncode, int) else -1
        except KeyboardInterrupt:
            self.stop_progress()
            self.print_line("Abort.")
            return KEYBOARD_INTERRUPT_RETURN_CODE

    def _process_output(self, output: IO[str], /, buffer: StringBuffer) -> None:
        # Handle confirmation inputs
        if buffer.getvalue().endswith(FFMPEG_CONFIRM_TEXT):
            self.print_line(buffer.popvalue(), newline=False, force=True)

        # Handle output parsing and processing
        char = output.read(1)
        if char == "\n":
            self.state.handle_line(line=buffer.popvalue())
        else:
            buffer.write(char)

    def change_state(self, state_cls: type["FfmpegState"], /) -> None:
        """Change current state of the runner."""
        self.state = state_cls(runner=self)

    def set_total_duration(self, duration: float | None, /) -> None:
        """Set progress bar total, save value for `complete_progress`."""
        self.total_duration = duration
        self.progress.update(self.task, total=duration)

    def set_progress(self, duration: float | None, /) -> None:
        """Set progress bar progress, start if is not started."""
        self.progress.update(self.task, completed=duration)
        if duration and not self.progress.live.is_started:
            self.progress.start()

    def stop_progress(self) -> None:
        """Stop the progress bar."""
        self.progress.stop()

    def complete_progress(self) -> None:
        """Complete the progress bar, stop it, and print duration."""
        self.set_progress(self.total_duration)
        self.stop_progress()
        progress_duration = (
            self.progress.tasks[0].finished_time
            if self.progress.tasks[0].finished_time
            else 0.0
        )
        self.print_line(
            f"Finished in {progress_duration:.3f} seconds",
        )

    @staticmethod
    def print_line(line: str, newline: bool = True, force: bool = False) -> None:
        """Print line to stderr (like `ffmpeg`)."""
        print(line, end="\n" if newline else "", file=sys.stderr, flush=force)


class FfmpegState(metaclass=ABCMeta):
    """Abstract class for FFmpeg output parser state."""

    runner: FfmpegRunnerWithProgressBar

    def __init__(self, runner: FfmpegRunnerWithProgressBar) -> None:
        self.runner = runner

    @abstractmethod
    def handle_line(self, line: str) -> None:
        """Should implement actions by parsing a line from the output."""
        raise NotImplementedError


class NullState(FfmpegState):
    """NullState, a Null object for FfmpegState."""

    def handle_line(self, line: str) -> None:  # noqa: ARG002
        """Always raise RuntimeError."""
        msg = "State must use a proper implementation class."
        raise RuntimeError(msg)


class PrintBeforeDurationState(FfmpegState):
    """Initial state, before duration display."""

    def handle_line(self, line: str) -> None:
        """Print line before duration parsed.

        Print line, and if duration is found in the line, set the total duration
        of the runner and change its state to PrintBeforeProgressState.
        """
        self.runner.print_line(line)
        if m := FFMPEG_DURATION_REGEX.search(line):
            duration = parse_duration(*m.groups())
            self.runner.set_total_duration(duration)
            self.runner.change_state(PrintBeforeProgressState)


class PrintBeforeProgressState(FfmpegState):
    """State before the display of the progress bar and after duration parsing."""

    def handle_line(self, line: str) -> None:
        """Print before progress bar.

        Print line, and if operation status is found in the line, change the runner
        state to DisplayProgressBarState.
        """
        if FFMPEG_STATUS_REGEX.search(line):
            self.runner.change_state(DisplayProgressBarState)
        else:
            self.runner.print_line(line)


class DisplayProgressBarState(FfmpegState):
    """State that displays / update the progress bar."""

    def handle_line(self, line: str) -> None:
        """Display progress bar.

        Parse the line to evaluate current progress, and update the progress bar.
        If the line don'' match the progress status, complete the progress and
        change the state to PrintAfterProgressState.
        """
        if m := FFMPEG_STATUS_REGEX.search(line):
            duration = parse_duration(*m.groups())
            self.runner.set_progress(duration)
        else:
            self.runner.complete_progress()
            self.runner.change_state(PrintAfterProgressState)


class PrintAfterProgressState(FfmpegState):
    """State that display line after the progress bar."""

    def handle_line(self, line: str) -> None:
        """Print line after progress.

        Print line, unless it match a progress status. This is due the fact that in
        this state `ffmpeg` print a line for the "completed" progress status, but we
        already displayed our completion information, so we avoid to print this line.
        """
        self.runner.print_line(line)
