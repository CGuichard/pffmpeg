"""Top-level exec environment.

This module serves as the entry point for the pffmpeg command-line interface (CLI)
application. When executed, it imports the pffmpeg function from the cli module,
runs it, and return an exit code.
"""

import sys

from ._cli import pffmpeg

if __name__ == "__main__":
    sys.exit(pffmpeg())
