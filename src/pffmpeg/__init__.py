"""PFFmpeg package.

PFFmpeg enhances the user experience of running FFmpeg commands by providing
a [`rich`](https://rich.readthedocs.io/en/latest/progress.html) progress bar.
This allows users to execute their usual `ffmpeg` commands while benefiting
from a visually appealing and informative progress display.

To use PFFmpeg, replace the `ffmpeg` command with `pffmpeg` in your terminal.

Example:
    ```bash
    pffmeg -i input.mp4 output.mp4
    ```

    The command above runs `ffmpeg -i input.mp4 output.mp4`.

Dependencies:
    - `ffmpeg`: Not included if you install `pffmeg`, follow the proper
                installation procedure of `ffmpeg` for your system.
    - `rich`: Used for displaying the progress bar.
"""

from importlib.metadata import PackageNotFoundError, version

from ._cli import pffmpeg

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    __version__ = "undefined"

__all__ = ["pffmpeg"]
