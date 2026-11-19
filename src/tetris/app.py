from typing import Protocol

from .codec import parse_field, render_field, render_steps
from .field import drop, fall_steps

ERROR_MESSAGE = "Error: invalid input\n"


class Reader(Protocol):
    def read(self, path: str) -> str: ...


class Writer(Protocol):
    def write(self, text: str) -> None: ...


class TetrisApp:
    """Connects the game logic with input/output; both are injected."""

    def __init__(self, reader: Reader, writer: Writer):
        self._reader = reader
        self._writer = writer

    def run(self, path: str, all_steps: bool = False) -> None:
        try:
            field = parse_field(self._reader.read(path))
        except (OSError, ValueError):
            self._writer.write(ERROR_MESSAGE)
            return
        if all_steps:
            self._writer.write(render_steps(fall_steps(field)))
        else:
            self._writer.write(render_field(drop(field)))
