"""Runner test package, validate `pffmpeg._runner`."""

from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from pffmpeg._runner import (
    DisplayProgressBarState,
    FfmpegRunnerWithProgressBar,
    NullState,
    PrintAfterProgressState,
    PrintBeforeDurationState,
    PrintBeforeProgressState,
)


def test_initial_state_is_null_state():
    """Initial runner state is NullState."""
    runner = FfmpegRunnerWithProgressBar()
    assert isinstance(runner.state, NullState)


def test_change_state():
    """Method change_state should instantiate given state class for runner."""
    runner = FfmpegRunnerWithProgressBar()

    assert not isinstance(runner.state, PrintBeforeDurationState)
    runner.change_state(PrintBeforeDurationState)
    assert isinstance(runner.state, PrintBeforeDurationState)


@patch("rich.progress.Progress.update")
def test_set_total_duration(mock_progress_update: MagicMock):
    """Method set_total_duration check.

    The method `set_total_duration` should set total_duration
    and call progress.update with total.
    """
    runner = FfmpegRunnerWithProgressBar()
    total_duration = 60.0

    runner.set_total_duration(total_duration)

    assert runner.total_duration == total_duration
    mock_progress_update.assert_called_once_with(runner.task, total=total_duration)


@patch("rich.progress.Progress.update")
@patch("rich.progress.Progress.start")
def test_set_progress(mock_progress_start: MagicMock, mock_progress_update: MagicMock):
    """Method set_progress should call progress.update and progress.start."""
    runner = FfmpegRunnerWithProgressBar()

    runner.set_progress(30.0)

    mock_progress_update.assert_called_once_with(runner.task, completed=30.0)
    mock_progress_start.assert_called_once()


@patch("rich.progress.Progress.update")
@patch("rich.progress.Progress.start")
def test_set_progress_none(
    mock_progress_start: MagicMock, mock_progress_update: MagicMock
):
    """Method set_progress should not trigger progress start if given None."""
    runner = FfmpegRunnerWithProgressBar()

    runner.set_progress(None)

    mock_progress_update.assert_called_once_with(runner.task, completed=None)
    mock_progress_start.assert_not_called()


@patch("rich.progress.Progress.stop")
def test_runner_stop_progress(mock_progress_stop: MagicMock):
    """Method stop_progress should call progress.stop()."""
    runner = FfmpegRunnerWithProgressBar()

    runner.stop_progress()

    mock_progress_stop.assert_called_once()


@patch.object(FfmpegRunnerWithProgressBar, "set_progress")
@patch.object(FfmpegRunnerWithProgressBar, "stop_progress")
@patch.object(FfmpegRunnerWithProgressBar, "print_line")
def test_runner_complete_progress(
    mock_print_line: MagicMock,
    mock_stop_progress: MagicMock,
    mock_set_progress: MagicMock,
):
    """Method complete_progress call set_progress, stop_progress and print_line."""
    runner = FfmpegRunnerWithProgressBar()

    runner.complete_progress()

    mock_set_progress.assert_called_once()
    mock_stop_progress.assert_called_once()
    mock_print_line.assert_called_once()


@patch("sys.stderr", new_callable=StringIO)
def test_print_line(mock_stderr: StringIO):
    """Method print_line should print to sys.stderr."""
    runner = FfmpegRunnerWithProgressBar()

    runner.print_line("My test line")

    assert mock_stderr.getvalue() == "My test line\n"


@patch("sys.stderr", new_callable=StringIO)
def test_print_line_with_no_new_line(mock_stderr: StringIO):
    r"""Method print_line with newline should print to sys.stderr without `\n`."""
    runner = FfmpegRunnerWithProgressBar()

    runner.print_line("My test line", newline=False)

    assert mock_stderr.getvalue() == "My test line"


def test_null_state_raise_runtime_error():
    """NullState should raise a RuntimeError."""
    runner = FfmpegRunnerWithProgressBar()

    runner.change_state(NullState)

    with pytest.raises(RuntimeError):
        runner.state.handle_line("test")


@patch.object(FfmpegRunnerWithProgressBar, "print_line")
def test_print_before_duration_state_prints_line(mock_print_line: MagicMock):
    """PrintBeforeDurationState should print any line."""
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(PrintBeforeDurationState)

    runner.state.handle_line("test")

    mock_print_line.assert_called_once_with("test")


@patch.object(FfmpegRunnerWithProgressBar, "set_total_duration")
def test_print_before_duration_state_set_duration(mock_set_total_duration: MagicMock):
    """PrintBeforeDurationState should print any line."""
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(PrintBeforeDurationState)

    runner.state.handle_line("Duration: 00:00:10.00")

    mock_set_total_duration.assert_called_once_with(10.0)
    assert isinstance(
        runner.state, PrintBeforeProgressState
    ), "State should change if line contains the duration"


@patch.object(FfmpegRunnerWithProgressBar, "print_line")
def test_print_before_progress_state(
    mock_print_line: MagicMock,
):
    """DisplayProgressBarState should set progress completed value if status line."""
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(PrintBeforeProgressState)

    runner.state.handle_line("Some output")

    mock_print_line.assert_called_once_with("Some output")
    assert isinstance(
        runner.state, PrintBeforeProgressState
    ), "State should not change if line is not a status line"


@patch.object(FfmpegRunnerWithProgressBar, "print_line")
def test_print_before_progress_state_when_status_line(
    mock_print_line: MagicMock,
):
    """DisplayProgressBarState should set progress completed value if status line."""
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(PrintBeforeProgressState)

    runner.state.handle_line("frame=999 time=00:00:05.00")

    mock_print_line.assert_not_called()
    assert isinstance(
        runner.state, DisplayProgressBarState
    ), "State should change if line is a status line"


@patch.object(FfmpegRunnerWithProgressBar, "complete_progress")
@patch.object(FfmpegRunnerWithProgressBar, "set_progress")
def test_display_progress_bar_state_handles_progress_not_completed(
    mock_set_progress: MagicMock,
    mock_complete_progress: MagicMock,
):
    """DisplayProgressBarState should set progress completed value if status line."""
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(DisplayProgressBarState)

    runner.state.handle_line("frame=999 time=00:00:05.00")

    mock_complete_progress.assert_not_called()
    mock_set_progress.assert_called_once_with(5.0)  # 5 seconds
    assert isinstance(
        runner.state, DisplayProgressBarState
    ), "State should not change because progress is not completed"


@patch.object(FfmpegRunnerWithProgressBar, "complete_progress")
def test_display_progress_bar_state_handles_progress_completed(
    mock_complete_progress: MagicMock,
):
    """DisplayProgressBarState completion.

    DisplayProgressBarState should call runner.complete_progress and change state
    to PrintAfterProgressState when line given is not a status line.
    """
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(DisplayProgressBarState)

    runner.state.handle_line("Not status line")

    mock_complete_progress.assert_called_once()
    assert isinstance(
        runner.state, PrintAfterProgressState
    ), "State should change if line is not a status line"


@patch.object(FfmpegRunnerWithProgressBar, "print_line")
def test_print_after_progress_state(mock_print_line: MagicMock):
    """PrintAfterProgressState should print lines."""
    runner = FfmpegRunnerWithProgressBar()
    runner.change_state(PrintAfterProgressState)

    runner.state.handle_line("Some log after progress")

    mock_print_line.assert_called_once_with("Some log after progress")
