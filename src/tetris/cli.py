import sys

from .app import ERROR_MESSAGE, TetrisApp
from .io_adapters import ConsoleWriter, FileReader

ALL_STEPS_FLAG = "--all-steps"


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    all_steps = ALL_STEPS_FLAG in args
    paths = [arg for arg in args if arg != ALL_STEPS_FLAG]
    writer = ConsoleWriter()
    if len(paths) != 1:
        writer.write(ERROR_MESSAGE)
        return
    TetrisApp(reader=FileReader(), writer=writer).run(paths[0], all_steps=all_steps)
