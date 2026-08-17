"""
Kaggriculture single-game test primitive.

Runs one strategy against one opponent and returns the resulting
Kaggle environment. Higher-level test runners can use this primitive
to perform local games, batches, comparisons, or regression tests.
"""

import json

from pathlib import Path
from typing import Any

from kaggle_environments import make

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
    DEFAULT_STRATEGY,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_1.agent import (
    make_agent,
)


EPISODE_STEPS = 720


def run_game(
    strategy_name: str = DEFAULT_STRATEGY,
    opponent: str = "self",
    episode_steps: int = EPISODE_STEPS,
) -> Any:
    """
    Run one Kaggriculture game.

    Args:
        strategy_name: Registered strategy to run.
        opponent: Kaggriculture opponent agent.
        episode_steps: Number of steps in the episode.

    Returns:
        The completed Kaggle environment.
    """


    agent = make_agent(strategy_name)

    if opponent == "self":
        opponent_agent = make_agent(strategy_name)
    else:
        opponent_agent = opponent

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": episode_steps},
        debug=False,
    )

    env.run([agent, opponent_agent])

    return env


def save_replay(env: Any, path: str | Path) -> None:
    """Save a completed game as a Kaggle replay JSON file."""

    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(env.toJSON(), file)


def print_results(env: Any) -> None:
    """Print the final results of a completed game."""

    final = env.steps[-1]

    for i, state in enumerate(final):
        print(
            f"Player {i}: "
            f"reward={state.reward}, "
            f"status={state.status}",
        )


def render_game(
    env: Any,
    width: int = 1200,
    height: int = 800,
) -> None:
    """Render a completed game."""

    env.render(
        mode="ipython",
        width=width,
        height=height,
    )