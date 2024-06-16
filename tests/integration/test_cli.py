"""CLI test package, validate `pffmpeg._cli.pffmpeg`."""

import sys
from unittest.mock import MagicMock, patch

from pffmpeg._cli import pffmpeg


@patch("pffmpeg._runner.FfmpegRunnerWithProgressBar.exec")
def test_cli_call_runner_exec(mock_runner_exec: MagicMock):
    """CLI should call `FfmpegRunnerWithProgressBar.exec`."""
    pffmpeg()
    mock_runner_exec.assert_called_once()


@patch("pffmpeg._runner.FfmpegRunnerWithProgressBar.exec")
def test_cli_pass_args(mock_runner_exec: MagicMock):
    """CLI should pass args to `FfmpegRunnerWithProgressBar.exec`."""
    args = ["-i", "input.mp4", "output.mp4"]
    pffmpeg(args=args)
    mock_runner_exec.assert_called_once_with(args)


@patch("pffmpeg._runner.FfmpegRunnerWithProgressBar.exec")
def test_cli_use_sys_arv_if_no_args_given(mock_runner_exec: MagicMock):
    """CLI should use sys.argv[1:] to resolve args if None is given."""
    args = ["-i", "input.mp4", "output.mp4"]
    with patch.object(sys, "argv", ["pffmpeg", *args]):
        pffmpeg(args=None)
    mock_runner_exec.assert_called_once_with(args)


@patch("pffmpeg._runner.FfmpegRunnerWithProgressBar.exec")
def test_cli_return_runner_exec_code(mock_runner_exec: MagicMock):
    """CLI should return FfmpegRunnerWithProgressBar.exec return code."""
    mock_runner_exec.return_value = 0
    assert pffmpeg() == 0
    mock_runner_exec.return_value = 1
    assert pffmpeg() == 1
