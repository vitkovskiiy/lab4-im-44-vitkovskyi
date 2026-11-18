from unittest.mock import create_autospec

from tetris.app import TetrisApp
from tetris.io_adapters import ConsoleWriter, FileReader


def make_app(text: str = "", error: Exception | None = None):
    """TetrisApp wired to autospec mocks of the real reader and writer."""
    reader = create_autospec(FileReader, instance=True)
    if error is not None:
        reader.read.side_effect = error
    else:
        reader.read.return_value = text
    writer = create_autospec(ConsoleWriter, instance=True)
    return TetrisApp(reader=reader, writer=writer), reader, writer


def test_run_asks_reader_for_file_at_given_path_once():
    app, reader, _ = make_app(text="1 1\np\n")

    app.run("input.txt")

    reader.read.assert_called_once_with("input.txt")


def test_run_writes_dropped_field_to_writer_exactly_once():
    app, _, writer = make_app(text="3 2\np.\n..\n.#\n")

    app.run("input.txt")

    writer.write.assert_called_once_with("..\n..\np#\n")


def test_run_writes_only_generic_error_message_when_input_is_invalid():
    app, _, writer = make_app(text="2 2\n.x\n..\n")

    app.run("input.txt")

    writer.write.assert_called_once_with("Error: invalid input\n")


def test_run_writes_same_error_message_when_file_cannot_be_read():
    app, _, writer = make_app(error=FileNotFoundError("missing.txt"))

    app.run("missing.txt")

    writer.write.assert_called_once_with("Error: invalid input\n")


def test_run_with_all_steps_writes_every_step_of_the_fall_once():
    app, _, writer = make_app(text="3 1\np\n.\n#\n")

    app.run("input.txt", all_steps=True)

    writer.write.assert_called_once_with("STEP 0\np\n.\n#\nSTEP 1\n.\np\n#\n")
