#!/usr/bin/env python3
"""Watch changes at given path and execute given command."""

import argparse
import fnmatch
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

console = Console()


def timestamp() -> float:
    return time.time()


class FileChangeHandler(FileSystemEventHandler):
    def __init__(
        self, commands: str, clear: bool, wait_time: float, glob_filter: str | None
    ) -> None:
        super().__init__()
        self._commands = commands.split(";")
        self._clear = clear
        self._wait_time = wait_time
        self._glob = glob_filter if glob_filter else "*"
        self._executed_at: float = timestamp() - wait_time

    def on_modified(self, event: FileSystemEvent) -> None:
        src_path = (
            event.src_path
            if isinstance(event.src_path, str)
            else event.src_path.decode()
        )
        if (
            fnmatch.fnmatch(src_path, self._glob)
            and not event.is_directory
            and timestamp() > self._executed_at + self._wait_time
        ):
            if self._clear:
                console.clear()

            console.print(f"Changes detected {src_path}")
            for cmd in self._commands:
                _cmd = cmd.strip()
                console.print(f"[bold]$ {_cmd}")
                subprocess.run(_cmd.split(" "), check=False)  # noqa: S603

            self._executed_at = timestamp()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("PATH", help="Path to watch.")
    parser.add_argument("COMMANDS", help="Commands separated by comma.")
    parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="Clear console before each execution.",
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        type=float,
        default=0.1,
        help="Time in seconds waited for before running the command again.",
    )
    parser.add_argument("-f", "--filter", help="File glob filter.")
    args = parser.parse_args(argv)

    path = Path(args.PATH).resolve()
    commands = args.COMMANDS
    clear = args.clear
    wait_time = args.wait_time
    glob_filter = args.filter

    if clear:
        console.clear()

    console.print(
        f"Watching {path}{f' ({glob_filter})' if glob_filter else ''} "
        f"wait: [bold cyan]{wait_time}s"
    )

    event_handler = FileChangeHandler(
        commands=commands,
        clear=clear,
        wait_time=wait_time,
        glob_filter=glob_filter,
    )
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        console.print("\nStopping watch", end="")
    finally:
        observer.stop()
        observer.join()

    return 0


if __name__ == "__main__":
    sys.exit(main())
