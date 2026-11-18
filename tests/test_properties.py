"""Property-based tests with Hypothesis.

The `fields` strategy builds random valid fields; each test checks one
property of `drop` on many of them. On failure Hypothesis shrinks the field
to a minimal example and prints it.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from tetris.field import Field, Point, drop, fall_steps

# derandomize: the same examples on every run, so CI results are reproducible.
PROPERTY_SETTINGS = settings(max_examples=500, derandomize=True, deadline=None)


@st.composite
def fields(draw) -> Field:
    """Random size, random landscape at the bottom, one piece above it."""
    height = draw(st.integers(min_value=2, max_value=10))
    width = draw(st.integers(min_value=1, max_value=10))
    piece_rows = draw(st.integers(min_value=1, max_value=max(1, height // 2)))
    bottom = [Point(row, col) for row in range(piece_rows, height) for col in range(width)]
    top = [Point(row, col) for row in range(piece_rows) for col in range(width)]
    landscape = draw(st.frozensets(st.sampled_from(bottom)))
    piece = draw(st.frozensets(st.sampled_from(top), min_size=1, max_size=4))
    return Field(height, width, piece, landscape)


@PROPERTY_SETTINGS
@given(fields())
def test_generated_fields_are_valid(field):
    assert field.piece
    assert not field.piece & field.landscape


@PROPERTY_SETTINGS
@given(fields())
def test_drop_keeps_field_size(field):
    final = drop(field)
    assert (final.height, final.width) == (field.height, field.width)


@PROPERTY_SETTINGS
@given(fields())
def test_drop_keeps_landscape(field):
    assert drop(field).landscape == field.landscape


@PROPERTY_SETTINGS
@given(fields())
def test_drop_keeps_piece_pixel_count(field):
    assert len(drop(field).piece) == len(field.piece)


@PROPERTY_SETTINGS
@given(fields())
def test_drop_keeps_piece_shape_and_only_moves_it_down(field):
    final = drop(field)
    shift = min(p.row for p in final.piece) - min(p.row for p in field.piece)
    assert shift >= 0
    assert final.piece == frozenset(Point(p.row + shift, p.col) for p in field.piece)


@PROPERTY_SETTINGS
@given(fields())
def test_dropped_piece_is_inside_field_and_off_landscape(field):
    final = drop(field)
    for p in final.piece:
        assert 0 <= p.row < final.height and 0 <= p.col < final.width
        assert p not in final.landscape


@PROPERTY_SETTINGS
@given(fields())
def test_dropped_field_is_stable(field):
    final = drop(field)
    assert drop(final) == final


@PROPERTY_SETTINGS
@given(fields())
def test_fall_steps_start_with_initial_field_and_end_with_dropped_field(field):
    steps = fall_steps(field)
    assert steps[0] == field
    assert steps[-1] == drop(field)


@PROPERTY_SETTINGS
@given(fields())
def test_each_fall_step_moves_piece_exactly_one_row_down(field):
    steps = fall_steps(field)
    for before, after in zip(steps, steps[1:]):
        assert after.piece == frozenset(Point(p.row + 1, p.col) for p in before.piece)
        assert after.landscape == before.landscape
