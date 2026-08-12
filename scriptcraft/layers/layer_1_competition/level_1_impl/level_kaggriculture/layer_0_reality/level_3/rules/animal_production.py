from ...level_1.definitions.animals import (
    AnimalType,
)
from ...level_2.definitions.animal_catalog import animal_definition


def produces_on_day(animal: AnimalType, age: int) -> bool:
    """
    Return whether the animal has a scheduled production event at this age.

    Production continues indefinitely on schedule; the held-yield cap is
    handled separately when calculating actual production.
    """
    if age < 0:
        return False

    definition = animal_definition(animal)

    if age < definition.time_to_first_yield:
        return False

    return (
        (age - definition.time_to_first_yield)
        % definition.production_interval
        == 0
    )


def production_count(animal: AnimalType, age: int) -> int:
    """Return the number of scheduled production events reached by this age."""
    if age < 0:
        return 0

    definition = animal_definition(animal)

    if age < definition.time_to_first_yield:
        return 0

    return (
        (age - definition.time_to_first_yield)
        // definition.production_interval
    ) + 1

    
def production_yield_with_care(
    *,
    fed_today: bool,
    pending_care_bonus: int,
) -> int:
    """
    Return production on a scheduled production day before held-yield capping.

    The base unit is always produced.  The banked care bonus is added only
    when the animal is fed on the production day.  If it is unfed the bonus
    is forfeited and the bank resets to 0.
    """
    if pending_care_bonus < 0:
        raise ValueError("pending_care_bonus must be non-negative")

    base = 1

    if not fed_today:
        return base

    return base + pending_care_bonus


def animal_production_yield(
    animal: AnimalType,
    age: int,
    *,
    fed_today: bool,
    pending_care_bonus: int,
    current_held_yield: int = 0,
) -> int:
    """
    Return the actual yield added by today's scheduled animal production.

    Animals are not affected by crop watering or fertilizer.
    The production is capped by the animal's maximum held yield.
    """
    if not produces_on_day(animal, age):
        return 0

    if current_held_yield < 0:
        raise ValueError("current_held_yield must be non-negative")

    maximum = animal_definition(animal).max_held

    if current_held_yield >= maximum:
        return 0

    production = production_yield_with_care(
        fed_today=fed_today,
        pending_care_bonus=pending_care_bonus,
    )
    return min(production, maximum - current_held_yield)