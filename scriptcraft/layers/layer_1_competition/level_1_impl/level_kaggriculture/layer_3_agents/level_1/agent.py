"""
Generic Kaggriculture Layer 3 agent adapter.

This module provides the Kaggle-compatible agent entry point and delegates
decision-making to a strategy selected from the Layer 3 strategy registry.
"""

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
    create_default_strategy,
    create_strategy,
)


strategy = create_default_strategy()


def agent(obs: dict) -> dict:
    """Kaggriculture entry point using the configured strategy."""
    return strategy.decide(obs)


def make_agent(strategy_name: str):
    """
    Create a Kaggriculture agent backed by a named strategy.

    This is primarily useful for local testing and strategy comparison.
    """

    selected_strategy = create_strategy(strategy_name)

    def configured_agent(obs: dict) -> dict:
        return selected_strategy.decide(obs)

    return configured_agent