"""Utils module - A collection of general-purpose utility functions and classes.

This module provides utility functions and classes for common operations.
These utilities are not specifically related to `pffmpeg` business logic.
"""

import io
import signal
from typing import TypeVar

KEYBOARD_INTERRUPT_RETURN_CODE = signal.SIGINT + 128

T = TypeVar("T")


def index_of(lst: list[T], el: T, /) -> int | None:
    """Index of implementation but with `None` if not found.

    Examples:
        >>> l = ["a"]
        >>> assert index_of(l, "a") == 0
        >>> assert index_of(l, "b") is None
    """
    return lst.index(el) if el in lst else None


def parse_duration(hours: str, minutes: str, seconds: str, centiseconds: str) -> float:
    """Return float representation of time (in seconds) from units of time strings.

    Examples:
        >>> assert parse_duration("02", "20", "20", "02") == 8420.02
    """
    return seconds_of(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(centiseconds) * 10,
    )


def seconds_of(hours: int, minutes: int, seconds: int, milliseconds: int) -> float:
    """Return from multiple units of time a float representation of the time in seconds.

    Examples:
        >>> assert seconds_of(2, 20, 20, 20) == 8420.02
    """
    return ((hours * 60 + minutes) * 60) + seconds + (milliseconds / 1000)


class StringBuffer(io.StringIO):
    """String buffer with clear methods.

    The main problem with `io.StringIO` is that you can easily write
    to the stream, but not clear its value. This class allows you to
    clear the value, and even clear and retrieve the value in a
    single call.

    Examples:
        >>> with StringBuffer() as buff:
        ...     assert not buff.getvalue()
        ...     buff.write("test")
        ...     assert buff.getvalue()
        ...     v = buff.popvalue()
        ...     assert v == "test"
        ...     assert not buff.getvalue()
        4

        The "4" is the output of `write`.
    """

    def __enter__(self) -> "StringBuffer":
        return super().__enter__()

    def clear(self) -> None:
        """Clear the value."""
        self.truncate(0)
        self.seek(0)

    def popvalue(self) -> str:
        """Clear the value and return it."""
        value = self.getvalue()
        self.clear()
        return value
