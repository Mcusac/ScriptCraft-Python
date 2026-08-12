"""
Kaggriculture farming rules.

Defines deterministic rules for farm geometry, land, shed access,
watering/feeding failure, weeds, DIG legality, and board capacity.

No farm state is stored or mutated here.
"""


from ...level_0.definitions.game import (
    LAND_PURCHASE_COSTS,
    SHED_CAPACITY,
    INITIAL_CONSECUTIVE_UNWATERED,
)
from ...level_1.rules.farm_geomety import QUADRANTS


def initial_consecutive_unwatered_days() -> int:
    """
    Return the initial consecutive_unwatered value for a newly planted crop.

    The specification states: "A new seed starts with
    consecutive_unwatered = 1 — the planting day itself counts as the
    first missed day."
    """
    return INITIAL_CONSECUTIVE_UNWATERED


def next_land_purchase_cost(
    unlocked_quadrant_count: int,
) -> int | None:
    """
    Return the cost of the next land purchase, or None if fully unlocked.

    With one starting quadrant:
        1 unlocked → $1 000
        2 unlocked → $2 000
        3 unlocked → $4 000
        4 unlocked → None (no further purchase possible)
    """
    if unlocked_quadrant_count < 1:
        raise ValueError("A farm must have at least one unlocked quadrant")

    purchase_index = unlocked_quadrant_count - 1

    if purchase_index >= len(LAND_PURCHASE_COSTS):
        return None

    return LAND_PURCHASE_COSTS[purchase_index]


def land_purchase_cost(unlocked_quadrant_count: int) -> int | None:
    """Return the cost of the next land purchase."""
    return next_land_purchase_cost(unlocked_quadrant_count)


def all_land_unlocked(unlocked_quadrant_count: int) -> bool:
    """Return whether all four quadrants are unlocked."""
    return unlocked_quadrant_count >= len(QUADRANTS)


def shed_capacity() -> int:
    """Return the maximum number of non-seed items held by the shed."""
    return SHED_CAPACITY