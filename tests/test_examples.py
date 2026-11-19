import pytest

from tetris.codec import parse_field, render_field, render_steps
from tetris.field import drop, fall_steps

# Input/output pairs copied from the assignment PDF.
PDF_EXAMPLES = [
    (
        "7 8\n"
        "..p.....\n"
        ".ppp....\n"
        "..p.....\n"
        "........\n"
        "...#....\n"
        "...#...#\n"
        "#..#####\n",
        "........\n"
        "........\n"
        "..p.....\n"
        ".ppp....\n"
        "..p#....\n"
        "...#...#\n"
        "#..#####\n",
    ),
    (
        "5 6\n"
        "..p...\n"
        "##p.##\n"
        "##pp##\n"
        "##..##\n"
        "##..##\n",
        "......\n"
        "##..##\n"
        "##p.##\n"
        "##p.##\n"
        "##pp##\n",
    ),
]


@pytest.mark.parametrize(
    "input_text, expected_output",
    PDF_EXAMPLES,
    ids=["cross stops on landscape", "piece falls into well"],
)
def test_dropped_field_matches_pdf_example(input_text, expected_output):
    assert render_field(drop(parse_field(input_text))) == expected_output



# "Print all steps" example from the Lab 4 PDF (same input as the first example).
PDF_ALL_STEPS_OUTPUT = (
    "STEP 0\n"
    "..p.....\n"
    ".ppp....\n"
    "..p.....\n"
    "........\n"
    "...#....\n"
    "...#...#\n"
    "#..#####\n"
    "STEP 1\n"
    "........\n"
    "..p.....\n"
    ".ppp....\n"
    "..p.....\n"
    "...#....\n"
    "...#...#\n"
    "#..#####\n"
    "STEP 2\n"
    "........\n"
    "........\n"
    "..p.....\n"
    ".ppp....\n"
    "..p#....\n"
    "...#...#\n"
    "#..#####\n"
)


def test_all_steps_output_matches_pdf_example():
    input_text = PDF_EXAMPLES[0][0]

    assert render_steps(fall_steps(parse_field(input_text))) == PDF_ALL_STEPS_OUTPUT
