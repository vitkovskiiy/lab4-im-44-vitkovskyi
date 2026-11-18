from .field import Field, Point


def parse_field(text: str) -> Field:
    lines = text.rstrip("\r\n").splitlines()
    if not lines:
        raise ValueError("empty input")
    height, width = (int(n) for n in lines[0].split())
    if height < 1 or width < 1:
        raise ValueError("field size must be positive")
    rows = lines[1:]
    if len(rows) != height:
        raise ValueError("row count does not match height")
    piece = set()
    landscape = set()
    for row, line in enumerate(rows):
        if len(line) != width:
            raise ValueError("row length does not match width")
        for col, char in enumerate(line):
            if char == "p":
                piece.add(Point(row, col))
            elif char == "#":
                landscape.add(Point(row, col))
            elif char != ".":
                raise ValueError(f"unknown pixel {char!r}")
    if not piece:
        raise ValueError("field has no piece")
    return Field(height, width, frozenset(piece), frozenset(landscape))


def render_field(field: Field) -> str:
    lines = []
    for row in range(field.height):
        line = ""
        for col in range(field.width):
            point = Point(row, col)
            if point in field.piece:
                line += "p"
            elif point in field.landscape:
                line += "#"
            else:
                line += "."
        lines.append(line + "\n")
    return "".join(lines)


def render_steps(fields: list[Field]) -> str:
    return "".join(f"STEP {number}\n{render_field(field)}" for number, field in enumerate(fields))
