"""
Kaggriculture resource-focused strategy definitions.

This module defines how parameterized strategy types map to their
canonical Layer 0 resource vocabularies and Layer 2 constructors.

Layer 0 remains the single source of truth for resource definitions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.crops import (
    CropType,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_0.basic.one_tile_one_crop import (
    OneTileOneCropStrategy,
)


@dataclass(frozen=True)
class ResourceFocusedStrategyDefinition:
    """Definition of a strategy type parameterized by a resource."""

    resource_type: type[Enum]
    constructor: Callable[[Any], Any]


RESOURCE_FOCUSED_STRATEGIES = {
    "one_tile_one_crop": ResourceFocusedStrategyDefinition(
        resource_type=CropType,
        constructor=OneTileOneCropStrategy,
    ),
}


def available_resource_focused_strategies() -> tuple[str, ...]:
    """Return all concrete resource-focused strategy names."""

    names: list[str] = []

    for strategy_type, definition in RESOURCE_FOCUSED_STRATEGIES.items():
        names.extend(
            f"{strategy_type}:{resource.name}"
            for resource in definition.resource_type
        )

    return tuple(names)


def create_resource_focused_strategy(name: str):
    """Create a resource-focused strategy from its public name."""

    strategy_type, resource_name = name.split(":", 1)

    try:
        definition = RESOURCE_FOCUSED_STRATEGIES[strategy_type]
    except KeyError as exc:
        available = ", ".join(
            RESOURCE_FOCUSED_STRATEGIES
        )
        raise KeyError(
            f"Unknown resource-focused strategy type "
            f"'{strategy_type}'. Available types: {available}"
        ) from exc

    try:
        resource = definition.resource_type[resource_name]
    except KeyError as exc:
        available = ", ".join(
            item.name for item in definition.resource_type
        )
        raise KeyError(
            f"Unknown resource '{resource_name}' for "
            f"'{strategy_type}'. Available resources: {available}"
        ) from exc

    return definition.constructor(resource)