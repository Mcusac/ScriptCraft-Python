"""
Kaggriculture strategy registry.

This module provides the canonical Layer 3 interface for resolving
public strategy names into Layer 2 strategy instances.

Layer 2 owns strategy implementations and strategy-family/resource
definitions. Layer 3 exposes those strategies to the agent system.
"""

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_1.strategy_types import (
    STRATEGIES,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_1.resource_focus import (
    available_resource_focused_strategies,
    create_resource_focused_strategy,
)


DEFAULT_STRATEGY = "one_tile_one_crop:WHEAT"


def available_strategies() -> tuple[str, ...]:
    """
    Return the names of all registered strategies.
    """

    return (
        tuple(STRATEGIES.keys())
        + available_resource_focused_strategies()
    )


def create_strategy(name: str):
    """
    Create a strategy instance by registered name.

    Supports:

        Simple:
            "buy_once"

        Resource-focused:
            "one_tile_one_crop:WHEAT"
    """

    if ":" in name:
        return create_resource_focused_strategy(name)

    try:
        strategy_class = STRATEGIES[name]
    except KeyError as exc:
        available = ", ".join(available_strategies())
        raise KeyError(
            f"Unknown Kaggriculture strategy '{name}'. "
            f"Available strategies: {available}"
        ) from exc

    return strategy_class()


def create_default_strategy():
    """Create the currently configured default strategy."""

    return create_strategy(DEFAULT_STRATEGY)