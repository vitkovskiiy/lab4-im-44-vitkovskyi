import pytest

from tetris.codec import parse_field, render_field, render_steps
from tetris.field import Field, Point


def test_parse_field_reads_size_and_splits_pixels_into_piece_and_landscape():
    text = "3 4\n.pp.\n....\n#..#\n"

    assert parse_field(text) == Field(
        height=3,
        width=4,
        piece=frozenset({Point(0, 1), Point(0, 2)}),
        landscape=frozenset({Point(2, 0), Point(2, 3)}),
    )


def test_render_field_draws_rows_with_dots_piece_and_landscape_pixels():
    field = Field(
        height=2,
        width=3,
        piece=frozenset({Point(0, 1)}),
        landscape=frozenset({Point(1, 0), Point(1, 2)}),
    )

    assert render_field(field) == ".p.\n#.#\n"


def test_parse_field_rejects_unknown_pixel_character():
    with pytest.raises(ValueError):
        parse_field("2 3\n.p.\n#x#\n")


@pytest.mark.parametrize(
    "text",
    [
        "",
        "2\n.p\n..\n",
        "2 2 2\n.p\n..\n",
        "a 2\n.p\n..\n",
        "0 2\n",
        "2 0\n\n\n",
        "-1 2\n.p\n",
    ],
    ids=[
        "empty file",
        "one number",
        "three numbers",
        "not a number",
        "zero height",
        "zero width",
        "negative height",
    ],
)
def test_parse_field_rejects_invalid_size_line(text):
    with pytest.raises(ValueError):
        parse_field(text)


@pytest.mark.parametrize(
    "text",
    ["3 2\n.p\n..\n", "1 2\n.p\n..\n"],
    ids=["fewer rows than height", "more rows than height"],
)
def test_parse_field_rejects_row_count_different_from_height(text):
    with pytest.raises(ValueError):
        parse_field(text)


def test_parse_field_ignores_empty_lines_at_end_of_file():
    assert parse_field("2 2\n.p\n#.\n\n\n") == Field(
        height=2,
        width=2,
        piece=frozenset({Point(0, 1)}),
        landscape=frozenset({Point(1, 0)}),
    )


def test_parse_field_accepts_windows_line_endings_with_trailing_empty_line():
    assert parse_field("2 2\r\n.p\r\n#.\r\n\r\n") == Field(
        height=2,
        width=2,
        piece=frozenset({Point(0, 1)}),
        landscape=frozenset({Point(1, 0)}),
    )


@pytest.mark.parametrize(
    "text",
    ["2 3\n.p.\n#.\n", "2 3\n.p.\n#..#\n"],
    ids=["row shorter than width", "row longer than width"],
)
def test_parse_field_rejects_row_length_different_from_width(text):
    with pytest.raises(ValueError):
        parse_field(text)


def test_parse_field_rejects_field_without_piece():
    with pytest.raises(ValueError):
        parse_field("2 2\n..\n##\n")


def test_render_steps_prints_numbered_step_header_before_each_field():
    first = Field(height=2, width=2, piece=frozenset({Point(0, 1)}), landscape=frozenset({Point(1, 0)}))
    second = Field(height=2, width=2, piece=frozenset({Point(1, 1)}), landscape=frozenset({Point(1, 0)}))

    assert render_steps([first, second]) == "STEP 0\n.p\n#.\nSTEP 1\n..\n#p\n"
