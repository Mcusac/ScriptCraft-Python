"""
Kaggriculture animal rules.

Defines deterministic animal feeding, care, production, fertilizer, escape,
and structure-compatibility rules.

This module does not mutate animal state or orchestrate actions.
"""

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.game import (
    ANIMAL_CARE_BONUS_INCREMENT,
    MAX_CONSECUTIVE_UNFED_DAYS,
)


def care_bonus_accrual(
    *,
    fed_today: bool,
    cared_today: bool,
) -> int:
    """
    Return the care bonus earned at end of day.

    Care only banks a bonus when the animal was both fed and cared for.
    """
    if not fed_today or not cared_today:
        return 0

    return ANIMAL_CARE_BONUS_INCREMENT


def animal_fails_after(consecutive_unfed_days: int) -> bool:
    """Return whether the animal has reached its escape threshold."""
    return consecutive_unfed_days >= MAX_CONSECUTIVE_UNFED_DAYS