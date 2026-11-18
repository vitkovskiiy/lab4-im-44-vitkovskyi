from tetris.field import Field, Point, drop, fall_steps, step_down


def test_step_down_moves_piece_one_row_down_when_space_below_is_free():
    field = Field(
        height=3,
        width=3,
        piece=frozenset({Point(0, 1)}),
        landscape=frozenset(),
    )

    assert step_down(field) == Field(
        height=3,
        width=3,
        piece=frozenset({Point(1, 1)}),
        landscape=frozenset(),
    )


def test_step_down_leaves_field_unchanged_when_piece_is_on_bottom_row():
    field = Field(
        height=2,
        width=3,
        piece=frozenset({Point(1, 0), Point(1, 1)}),
        landscape=frozenset(),
    )

    assert step_down(field) == field


def test_step_down_leaves_field_unchanged_when_landscape_is_directly_below_piece():
    field = Field(
        height=4,
        width=3,
        piece=frozenset({Point(0, 1), Point(1, 1)}),
        landscape=frozenset({Point(2, 1), Point(3, 0), Point(3, 1)}),
    )

    assert step_down(field) == field


def test_drop_moves_piece_down_until_it_rests_on_landscape():
    field = Field(
        height=5,
        width=2,
        piece=frozenset({Point(0, 0), Point(0, 1)}),
        landscape=frozenset({Point(4, 1)}),
    )

    assert drop(field) == Field(
        height=5,
        width=2,
        piece=frozenset({Point(3, 0), Point(3, 1)}),
        landscape=frozenset({Point(4, 1)}),
    )


def test_drop_moves_piece_to_bottom_row_when_there_is_no_landscape():
    field = Field(
        height=4,
        width=2,
        piece=frozenset({Point(0, 0), Point(0, 1)}),
        landscape=frozenset(),
    )

    assert drop(field).piece == frozenset({Point(3, 0), Point(3, 1)})


def test_drop_leaves_field_unchanged_when_piece_already_rests_on_landscape():
    field = Field(
        height=3,
        width=1,
        piece=frozenset({Point(1, 0)}),
        landscape=frozenset({Point(2, 0)}),
    )

    assert drop(field) == field


def test_drop_stops_when_upper_pixel_of_piece_hits_landscape_first():
    # The lowest piece pixel (column 1) still has free space below it,
    # but the pixel in column 0 lands on the landscape one step earlier.
    field = Field(
        height=4,
        width=2,
        piece=frozenset({Point(0, 0), Point(0, 1), Point(1, 1)}),
        landscape=frozenset({Point(2, 0)}),
    )

    assert drop(field).piece == frozenset({Point(1, 0), Point(1, 1), Point(2, 1)})


def test_drop_never_changes_size_or_landscape():
    landscape = frozenset({Point(3, 0), Point(3, 2), Point(2, 2)})
    field = Field(
        height=4,
        width=3,
        piece=frozenset({Point(0, 1)}),
        landscape=landscape,
    )

    dropped = drop(field)

    assert (dropped.height, dropped.width, dropped.landscape) == (4, 3, landscape)


def test_fall_steps_returns_only_initial_field_when_piece_cannot_move():
    field = Field(
        height=2,
        width=1,
        piece=frozenset({Point(0, 0)}),
        landscape=frozenset({Point(1, 0)}),
    )

    assert fall_steps(field) == [field]
