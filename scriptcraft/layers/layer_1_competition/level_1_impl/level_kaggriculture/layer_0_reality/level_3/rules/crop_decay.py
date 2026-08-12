from ...level_0.definitions.game import (
    CROP_DECAY_INTERVAL_TURNS,
)
from ...level_0.definitions.crops import (
    CropType,
)
from ...level_1.definitions.crop_catalog import crop_definition
from ...level_2.rules.crop_production import is_one_time_crop, is_ongoing_crop


def one_time_decay_start_day(crop: CropType) -> int:
    """
    Return the first age at which a one-time crop begins decay.

    One day after time_to_max_yield.  Returns -1 for ongoing crops.
    """
    if not is_one_time_crop(crop):
        return -1

    return crop_definition(crop).time_to_max_yield + 1


def ongoing_decay_start_day(crop: CropType) -> int:
    """
    Return the first age at which an ongoing crop begins decay.

    One day after the final scheduled production event.
    Returns -1 for one-time crops.
    """
    if not is_ongoing_crop(crop):
        return -1

    definition = crop_definition(crop)
    interval = definition.production_interval

    if interval is None:
        return -1

    final_production_day = (
        definition.time_to_first_yield
        + (definition.max_yield - 1) * interval
    )
    return final_production_day + 1


def decay_start_day(crop: CropType) -> int:
    """Return the first crop age at which decay begins."""
    if is_one_time_crop(crop):
        return one_time_decay_start_day(crop)

    return ongoing_decay_start_day(crop)


def is_decaying(crop: CropType, age: int) -> bool:
    """Return whether the crop has reached its decay period."""
    start_day = decay_start_day(crop)
    return start_day >= 0 and age >= start_day


def decay_reduction(*, turns_since_decay_start: int) -> int:
    """
    Return cumulative yield lost to decay.

    Yield decreases by 1 every 2 turns:
        0–1 turns → 0 lost
        2–3 turns → 1 lost
        4–5 turns → 2 lost
        ...
    """
    if turns_since_decay_start < 0:
        return 0

    return turns_since_decay_start // CROP_DECAY_INTERVAL_TURNS


def decayed_yield(current_yield: int, *, turns_since_decay_start: int) -> int:
    """Return the remaining yield after elapsed decay."""
    if current_yield <= 0:
        return 0

    reduction = decay_reduction(turns_since_decay_start=turns_since_decay_start)
    return max(0, current_yield - reduction)


def becomes_weed(current_yield: int) -> bool:
    """Return whether a crop has exhausted all remaining held yield."""
    return current_yield <= 0