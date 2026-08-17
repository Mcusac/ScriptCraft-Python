from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.game import (
    MAX_CONSECUTIVE_UNFED_DAYS,
    MAX_CONSECUTIVE_UNWATERED_DAYS,
    WEED_SPAWN_CHANCE,
)


def weed_spawn_chance() -> float:
    """Return the per-tile probability of spontaneous weed spawning."""
    return WEED_SPAWN_CHANCE


def can_spawn_weed(
    *,
    tile_is_empty: bool,
    tile_is_unlocked: bool,
) -> bool:
    """
    Return whether a tile qualifies for weed spawning.

    The probability itself is exposed separately by `weed_spawn_chance()`.
    """
    return tile_is_empty and tile_is_unlocked


def plant_requires_daily_watering() -> bool:
    """Return whether plants require daily watering."""
    return True


def animal_requires_daily_feeding() -> bool:
    """Return whether animals require daily feeding."""
    return True


def plant_failure_after_unwatered_days() -> int:
    """Return the consecutive-unwatered threshold for plant failure."""
    return MAX_CONSECUTIVE_UNWATERED_DAYS


def animal_failure_after_unfed_days() -> int:
    """Return the consecutive-unfed threshold for animal escape."""
    return MAX_CONSECUTIVE_UNFED_DAYS


def plant_fails_after(consecutive_unwatered_days: int) -> bool:
    """Return whether a plant has reached its watering failure threshold."""
    return consecutive_unwatered_days >= plant_failure_after_unwatered_days()


def animal_fails_after(consecutive_unfed_days: int) -> bool:
    """Return whether an animal has reached its feeding failure threshold."""
    return consecutive_unfed_days >= animal_failure_after_unfed_days()

# ---------------------------------------------------------------------------
# DIG rules
# ---------------------------------------------------------------------------

def can_dig_plant() -> bool:
    """
    Return whether DIG may remove a plant tile.

    The specification lists plants as a valid DIG target.
    """
    return True


def can_dig_weed() -> bool:
    """
    Return whether DIG may remove a weed tile.

    The specification lists weeds as a valid DIG target.
    """
    return True


def can_dig_empty_structure() -> bool:
    """
    Return whether DIG may remove an empty coop or pasture.

    The specification explicitly permits DIG on empty structures.
    """
    return True


def can_dig_occupied_structure() -> bool:
    """
    Return whether DIG may remove a structure that contains an animal.

    The specification states: "A coop or pasture with an animal on it
    cannot be dug; the DIG is a no-op."
    """
    return False