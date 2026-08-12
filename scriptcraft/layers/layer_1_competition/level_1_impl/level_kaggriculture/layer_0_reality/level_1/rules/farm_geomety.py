from enum import Enum

from ...level_0.definitions.game import (
    BOARD_SIZE,
)

class Quadrant(Enum):
    """The four quadrants of the standard square farm."""

    NW = "NW"
    NE = "NE"
    SW = "SW"
    SE = "SE"


QUADRANTS = (
    Quadrant.NW,
    Quadrant.NE,
    Quadrant.SW,
    Quadrant.SE,
)

INITIAL_UNLOCKED_QUADRANTS = frozenset({Quadrant.NW})


def quadrant_size(board_size: int = BOARD_SIZE) -> int:
    """
    Return the width/height of one quadrant.

    Requires a positive even board_size.  The competition default is 10,
    producing four 5×5 quadrants.  An odd board_size cannot be divided
    into four equal quadrants and is therefore rejected.
    """
    if board_size <= 0:
        raise ValueError("board_size must be positive")

    if board_size % 2 != 0:
        raise ValueError(
            "board_size must be even to produce four equal quadrants"
        )

    return board_size // 2


def total_board_tiles(board_size: int = BOARD_SIZE) -> int:
    """Return the total number of board positions."""
    if board_size <= 0:
        raise ValueError("board_size must be positive")

    return board_size * board_size


def quadrant_tiles(board_size: int = BOARD_SIZE) -> int:
    """Return the number of positions represented by one quadrant."""
    size = quadrant_size(board_size)
    return size * size


def quadrant_bounds(
    quadrant: Quadrant,
    board_size: int = BOARD_SIZE,
) -> tuple[int, int, int, int]:
    """
    Return the bounds for a quadrant as (x_start, y_start, x_end, y_end).

    x_start and y_start are inclusive; x_end and y_end are exclusive.
    """
    half = quadrant_size(board_size)

    if quadrant is Quadrant.NW:
        return 0, 0, half, half

    if quadrant is Quadrant.NE:
        return half, 0, board_size, half

    if quadrant is Quadrant.SW:
        return 0, half, half, board_size

    if quadrant is Quadrant.SE:
        return half, half, board_size, board_size

    raise ValueError(f"Unsupported quadrant: {quadrant!r}")


def quadrant_for_position(
    x: int,
    y: int,
    board_size: int = BOARD_SIZE,
) -> Quadrant:
    """Return the quadrant containing a board position."""
    if not valid_board_position(x, y, board_size):
        raise ValueError(f"position out of bounds: ({x}, {y})")

    half = quadrant_size(board_size)

    if x < half and y < half:
        return Quadrant.NW

    if x >= half and y < half:
        return Quadrant.NE

    if x < half and y >= half:
        return Quadrant.SW

    return Quadrant.SE


def valid_board_position(
    x: int,
    y: int,
    board_size: int = BOARD_SIZE,
) -> bool:
    """Return whether a coordinate is inside the board."""
    return 0 <= x < board_size and 0 <= y < board_size


def is_tile_unlocked(
    x: int,
    y: int,
    unlocked_quadrants: set[Quadrant] | frozenset[Quadrant],
    board_size: int = BOARD_SIZE,
) -> bool:
    """Return whether a board position belongs to unlocked land."""
    quadrant = quadrant_for_position(x, y, board_size)
    return quadrant in unlocked_quadrants


def initial_unlocked_quadrants() -> frozenset[Quadrant]:
    """Return the quadrants unlocked at episode start."""
    return INITIAL_UNLOCKED_QUADRANTS



def shed_access_tiles(
    board_size: int = BOARD_SIZE,
) -> tuple[tuple[int, int], ...]:
    """
    Return the four board positions surrounding the centered shed in
    NW, NE, SW, SE order.

    The shed itself is not a tile.  These are the standing positions from
    which shed actions (PICKUP, DROP, PLACE into shed) are accessible.

    For board_size = 10: (4,4), (5,4), (4,5), (5,5).
    """
    half = quadrant_size(board_size)   # validates board_size

    return (
        (half - 1, half - 1),   # NW
        (half,     half - 1),   # NE
        (half - 1, half    ),   # SW
        (half,     half    ),   # SE
    )


def is_shed_access_tile(
    x: int,
    y: int,
    board_size: int = BOARD_SIZE,
) -> bool:
    """Return whether a position is one of the shed access positions."""
    return (x, y) in shed_access_tiles(board_size)