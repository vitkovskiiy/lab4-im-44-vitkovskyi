from dataclasses import dataclass
from typing import NamedTuple


class Point(NamedTuple):
    row: int
    col: int


@dataclass(frozen=True)
class Field:
    height: int
    width: int
    piece: frozenset[Point]
    landscape: frozenset[Point]


def step_down(field: Field) -> Field:
    moved = frozenset(Point(p.row + 1, p.col) for p in field.piece)
    if any(p.row >= field.height or p in field.landscape for p in moved):
        return field
    return Field(field.height, field.width, moved, field.landscape)


def drop(field: Field) -> Field:
    while (moved := step_down(field)) != field:
        field = moved
    return field


def fall_steps(field: Field) -> list[Field]:
    steps = [field]
    while (moved := step_down(steps[-1])) != steps[-1]:
        steps.append(moved)
    return steps
