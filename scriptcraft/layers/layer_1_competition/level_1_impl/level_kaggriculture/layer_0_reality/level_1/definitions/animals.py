"""
Kaggriculture animal definitions.

This module contains immutable characteristics of the supported animals
and the canonical animal-to-structure compatibility mapping.

Animal behaviour belongs in level_1/rules/animals.py.
"""

from dataclasses import dataclass
from enum import Enum

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.objects import ObjectType


class AnimalType(Enum):
    """Supported Kaggriculture animals."""

    GOOSE = "GOOSE"
    COW = "COW"
    SHEEP = "SHEEP"


class StructureType(Enum):
    """Farm structures that can be built on tiles to house animals."""

    COOP = "COOP"
    PASTURE = "PASTURE"


@dataclass(frozen=True)
class AnimalDefinition:
    """
    Immutable static characteristics of an animal.

    `time_to_first_yield` is the age at which the first scheduled
    production event occurs.

    `production_interval` is the number of days between scheduled
    production events.

    `max_held` is the maximum unharvested product that may accumulate on
    the animal structure tile.
    """

    name: str
    purchase_cost: int

    product: ObjectType

    time_to_first_yield: int
    production_interval: int
    max_held: int

    action_cost: int