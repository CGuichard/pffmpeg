"""End-to-end package test."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pffmpeg import pffmpeg

VIDEO_PATH = Path(__file__).parent / "data" / "TuxThePenguin.mp4"


def test_video_compression():
    """Run pffmpeg to compress a video."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", prefix="TuxThePenguin") as tf:
        pffmpeg(["-i", VIDEO_PATH, tf.name])


@patch("subprocess.Popen")
def test_abort(mock_popen: MagicMock, capsys: pytest.CaptureFixture):
    """Run pffmpeg and simulate Ctrl+C."""
    mock_popen.side_effect = KeyboardInterrupt

    with tempfile.NamedTemporaryFile(suffix=".mp4", prefix="TuxThePenguin") as tf:
        pffmpeg(["-i", VIDEO_PATH, tf.name])

    captured = capsys.readouterr()
    assert "Abort." in captured.err
