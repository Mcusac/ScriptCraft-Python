
def spawn_candidates_in_preference_order(
    board_size: int,
) -> tuple[tuple[int, int], ...]:
    """
    Return shed-adjacent spawn candidates in NWSE preference order.

    The specification requires NWSE preference: a hand appears on the
    first qualifying tile in this sequence.  These are exactly the four
    shed-access positions; the naming reflects their quadrant membership.

    For board_size = 10 (half = 5):
        NW: (4, 4)
        NE: (5, 4)
        SW: (4, 5)
        SE: (5, 5)
    """
    half = board_size // 2
    return (
        (half - 1, half - 1),   # NW
        (half,     half - 1),   # NE
        (half - 1, half    ),   # SW
        (half,     half    ),   # SE
    )


def select_spawn_tile(
    candidates: tuple[tuple[int, int], ...],
    occupancy: dict[tuple[int, int], int],
) -> tuple[int, int]:
    """
    Return the spawn tile for a hired hand given current tile occupancy.

    Selection rules (applied in order):
    1. First candidate with occupancy == 0 wins (free-tile preference).
    2. If no free tile exists, choose the candidate with the lowest
       occupancy count.
    3. Ties in occupancy are broken by position in the candidates tuple
       (preserving NWSE order).

    Candidates must be ordered in NWSE preference.
    Locked tiles are valid spawn positions; locking is not checked here.

    `occupancy` maps (x, y) → current number of units on the tile.
    Missing keys are treated as 0 occupancy.
    """
    if not candidates:
        raise ValueError("candidates must be non-empty")

    best = candidates[0]
    best_count = occupancy.get(best, 0)

    for tile in candidates[1:]:
        count = occupancy.get(tile, 0)
        if count == 0:
            return tile          # free tile: take it immediately
        if count < best_count:
            best = tile
            best_count = count

    # Return best free tile if we found one during iteration, or best overall.
    if occupancy.get(best, 0) == 0:
        return best

    return best


def spawn_may_land_on_locked_tile() -> bool:
    """
    Return whether a hired hand may spawn on a locked-quadrant tile.

    The specification notes that the NE shed-access tile starts locked
    and a spawn may occur there anyway; hands can move off locked land
    but may not perform tile actions on it.
    """
    return True