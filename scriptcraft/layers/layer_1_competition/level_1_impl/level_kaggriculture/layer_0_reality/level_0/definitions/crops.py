"""
Kaggriculture crop definitions.

This module defines the canonical crop vocabulary and the immutable
characteristics of each supported crop.
"""

from dataclasses import dataclass
from enum import Enum


class YieldType(Enum):
    """Production model used by a crop."""

    ONE_TIME = "one_time"
    ONGOING = "ongoing"


class CropType(Enum):
    """Supported Kaggriculture crops."""

    WHEAT = "WHEAT"
    CARROT = "CARROT"
    TOMATO = "TOMATO"
    STRAWBERRY = "STRAWBERRY"
    MELON = "MELON"


@dataclass(frozen=True)
class CropDefinition:
    """
    Immutable characteristics of a crop.

    `time_to_first_yield` is the age at which the first harvestable
    yield or scheduled production occurs.

    `time_to_max_yield` is the competition's documented Time to Max Yield.
    For one-time crops, this describes the age at which normal watering
    reaches the ordinary yield cap.

    `bonus_start_day` and `bonus_end_day` define the explicit watering
    bonus window.  These values are independent from `time_to_max_yield`.

    For ongoing crops, `production_interval` is the number of days
    between scheduled production events.  It must be defined for ongoing
    crops and omitted for one-time crops.
    """

    name: str
    seed_cost: int

    time_to_first_yield: int
    time_to_max_yield: int
    max_yield: int

    action_cost: int

    yield_type: YieldType

    bonus_start_day: int
    bonus_end_day: int

    production_interval: int | None = None

    def __post_init__(self) -> None:
        if self.seed_cost < 0:
            raise ValueError("seed_cost must be non-negative")

        if self.time_to_first_yield < 0:
            raise ValueError("time_to_first_yield must be non-negative")

        if self.time_to_max_yield < 0:
            raise ValueError("time_to_max_yield must be non-negative")

        if self.time_to_max_yield < self.time_to_first_yield:
            raise ValueError(
                "time_to_max_yield must not precede time_to_first_yield"
            )

        if self.max_yield < 0:
            raise ValueError("max_yield must be non-negative")

        if self.action_cost < 0:
            raise ValueError("action_cost must be non-negative")

        if self.bonus_start_day < 0:
            raise ValueError("bonus_start_day must be non-negative")

        if self.bonus_end_day < self.bonus_start_day:
            raise ValueError("bonus_end_day must not precede bonus_start_day")

        if self.yield_type is YieldType.ONGOING:
            if self.production_interval is None:
                raise ValueError(
                    "ongoing crops must define production_interval"
                )
            if self.production_interval <= 0:
                raise ValueError("production_interval must be positive")

        elif self.production_interval is not None:
            raise ValueError(
                "one-time crops must not define production_interval"
            )