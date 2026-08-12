"""
Kaggriculture time rules.

Defines the relationship between simulation steps, days, turns, and the
season.

These functions intentionally operate on explicit step/configuration values
rather than storing any mutable clock state.
"""

from ...level_0.definitions.game import (
    DAYS_PER_SEASON,
    EPISODE_STEPS,
    TURNS_PER_DAY,
)


def day_from_step(
    step: int,
    turns_per_day: int = TURNS_PER_DAY,
) -> int:
    """Return the zero-indexed in-game day containing a step."""
    if step < 0:
        raise ValueError("step must be non-negative")

    if turns_per_day <= 0:
        raise ValueError("turns_per_day must be positive")

    return step // turns_per_day


def turn_in_day(
    step: int,
    turns_per_day: int = TURNS_PER_DAY,
) -> int:
    """Return the zero-indexed turn within the current day."""
    if step < 0:
        raise ValueError("step must be non-negative")

    if turns_per_day <= 0:
        raise ValueError("turns_per_day must be positive")

    return step % turns_per_day


def is_end_of_day(
    step: int,
    turns_per_day: int = TURNS_PER_DAY,
) -> bool:
    """Return whether the step is the final turn of its day."""
    if step < 0:
        raise ValueError("step must be non-negative")

    if turns_per_day <= 0:
        raise ValueError("turns_per_day must be positive")

    return (step + 1) % turns_per_day == 0


def is_end_of_season(
    step: int,
    episode_steps: int = EPISODE_STEPS,
) -> bool:
    """Return whether the step is the final configured episode step."""
    if step < 0:
        raise ValueError("step must be non-negative")

    if episode_steps <= 0:
        raise ValueError("episode_steps must be positive")

    return step == episode_steps - 1


def season_days() -> int:
    """Return the competition's configured season length in days."""
    return DAYS_PER_SEASON