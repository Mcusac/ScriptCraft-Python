from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.crops import (
    CropType,
    YieldType,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_1.definitions.crop_catalog import crop_definition


def is_one_time_crop(crop: CropType) -> bool:
    """Return whether a crop produces one harvest rather than recurring yields."""
    return crop_definition(crop).yield_type is YieldType.ONE_TIME


def is_ongoing_crop(crop: CropType) -> bool:
    """Return whether a crop produces on a recurring schedule."""
    return crop_definition(crop).yield_type is YieldType.ONGOING


def first_yield_day(crop: CropType) -> int:
    """Return the age of the crop's first yield or production event."""
    return crop_definition(crop).time_to_first_yield


def max_yield(crop: CropType) -> int:
    """Return the crop's maximum scheduled/harvestable yield."""
    return crop_definition(crop).max_yield


def bonus_start_day(crop: CropType) -> int:
    """Return the first age in the crop's watering bonus window."""
    return crop_definition(crop).bonus_start_day


def bonus_end_day(crop: CropType) -> int:
    """Return the final age in the crop's watering bonus window."""
    return crop_definition(crop).bonus_end_day


def one_time_bonus_start_day(crop: CropType) -> int:
    """
    Return the first age at which watering can increase a one-time crop's
    yield.  Returns -1 for ongoing crops.
    """
    if not is_one_time_crop(crop):
        return -1

    return bonus_start_day(crop)


def one_time_bonus_end_day(crop: CropType) -> int:
    """
    Return the final age at which watering can increase a one-time crop's
    yield.  Returns -1 for ongoing crops.
    """
    if not is_one_time_crop(crop):
        return -1

    return bonus_end_day(crop)


def one_time_bonus_applies(crop: CropType, age: int) -> bool:
    """Return whether a one-time crop is inside its explicit bonus window."""
    if not is_one_time_crop(crop):
        return False

    definition = crop_definition(crop)
    return definition.bonus_start_day <= age <= definition.bonus_end_day


def fertilizer_active_on_day(
    current_day: int,
    fertilized_until_day: int,
) -> bool:
    """
    Return whether fertilizer is active on a given in-game day.

    The observation stores the actual final active day in
    `fertilized_until_day`.  `-1` means no fertilizer is active.
    """
    return (
        fertilized_until_day >= 0
        and current_day <= fertilized_until_day
    )


def one_time_watering_bonus(
    crop: CropType,
    age: int,
    *,
    watered: bool,
    fertilizer_active: bool,
) -> int:
    """
    Return the yield bonus from watering a one-time crop on one age.

    Outside the explicit bonus window, watering contributes nothing.

    Inside the window:
      - ordinary watering adds 1
      - watering while fertilizer is active adds 2
    """
    if not watered:
        return 0

    if not one_time_bonus_applies(crop, age):
        return 0

    return 2 if fertilizer_active else 1


def one_time_yield(
    crop: CropType,
    *,
    watered_days: int,
    fertilized_watered_days: int = 0,
) -> int:
    """
    Calculate total harvestable yield for a one-time crop.

    `watered_days`
        Number of days the crop was watered inside its bonus window.

    `fertilized_watered_days`
        Number of those watering days on which fertilizer was active.

    Yield = 1 + watered_days + fertilized_watered_days, capped at max_yield.
    """
    if not is_one_time_crop(crop):
        return 0

    if watered_days < 0:
        raise ValueError("watered_days must be non-negative")

    if fertilized_watered_days < 0:
        raise ValueError("fertilized_watered_days must be non-negative")

    if fertilized_watered_days > watered_days:
        raise ValueError(
            "fertilized_watered_days cannot exceed watered_days"
        )

    definition = crop_definition(crop)
    yield_units = 1 + watered_days + fertilized_watered_days
    return min(yield_units, definition.max_yield)


def production_interval(crop: CropType) -> int:
    """
    Return the recurring production interval for an ongoing crop.

    Returns 0 for one-time crops.
    """
    definition = crop_definition(crop)

    if not is_ongoing_crop(crop):
        return 0

    return definition.production_interval or 0


def produces_on_day(crop: CropType, age: int) -> bool:
    """
    Return whether an ongoing crop has a scheduled production event at age.

    Events occur at first_yield_day + n × production_interval until the
    crop has reached its maximum number of scheduled productions.
    """
    if not is_ongoing_crop(crop):
        return False

    definition = crop_definition(crop)
    interval = definition.production_interval

    if interval is None:
        return False

    if age < definition.time_to_first_yield:
        return False

    production_number = (age - definition.time_to_first_yield) // interval
    return production_number < definition.max_yield


def ongoing_production_count(crop: CropType, age: int) -> int:
    """
    Return the number of scheduled production events reached by this age.

    This counts scheduled events, not successfully harvested units.
    Decay begins after the scheduled count reaches the cap regardless
    of whether produce has been collected.
    """
    if not is_ongoing_crop(crop):
        return 0

    definition = crop_definition(crop)
    interval = definition.production_interval

    if interval is None:
        return 0

    if age < definition.time_to_first_yield:
        return 0

    count = (age - definition.time_to_first_yield) // interval + 1
    return min(count, definition.max_yield)


def ongoing_production_yield(
    crop: CropType,
    age: int,
    *,
    watered: bool,
    fertilizer_active: bool,
    current_held_yield: int = 0,
) -> int:
    """
    Return the yield added by today's ongoing production event.

    - 1 unit normally
    - 2 units when both watered AND fertilizer is active

    Result is capped by the crop's maximum held yield.
    """
    if not produces_on_day(crop, age):
        return 0

    if current_held_yield < 0:
        raise ValueError("current_held_yield must be non-negative")

    definition = crop_definition(crop)

    if current_held_yield >= definition.max_yield:
        return 0

    production = 2 if watered and fertilizer_active else 1
    return min(production, definition.max_yield - current_held_yield)