"""
Kaggriculture local strategy test runner.

Examples:

    python test_agent.py
    python test_agent.py wheat
    python test_agent.py melon_maxxer
    python test_agent.py --list
    python test_agent.py meta_milk --opponent random
"""

import argparse
import json

from kaggle_environments import make

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
    DEFAULT_STRATEGY,
    available_strategies,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_1.agent import (
    make_agent,
)


EPISODE_STEPS = 720


def parse_args() -> argparse.Namespace:
    """Parse local test runner arguments."""

    parser = argparse.ArgumentParser(
        description="Run a Kaggriculture strategy locally.",
    )

    parser.add_argument(
        "strategy",
        nargs="?",
        default=DEFAULT_STRATEGY,
        help="Strategy to test.",
    )

    parser.add_argument(
        "--opponent",
        default="random",
        help="Opponent agent to run against.",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=EPISODE_STEPS,
        help="Number of episode steps.",
    )

    parser.add_argument(
        "--replay",
        default="replay.json",
        help="Path for the generated replay JSON.",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_strategies",
        help="List registered strategies and exit.",
    )

    return parser.parse_args()


def print_strategies() -> None:
    """Print all registered strategy names."""

    print("Available strategies:")

    for name in available_strategies():
        print(f"  - {name}")


def run_agent(
    strategy_name: str,
    opponent: str,
    episode_steps: int,
    replay_path: str,
) -> None:
    """Run a selected strategy against the selected opponent."""

    agent = make_agent(strategy_name)

    print(f"Strategy: {strategy_name}")
    print(f"Opponent: {opponent}")
    print(f"Episode steps: {episode_steps}")
    print()

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": episode_steps},
        debug=False,
    )

    env.run([agent, opponent])

    final = env.steps[-1]

    print("Final results:")

    for i, state in enumerate(final):
        print(
            f"  Player {i}: "
            f"reward={state.reward}, "
            f"status={state.status}",
        )

    env.render(
        mode="ipython",
        width=1200,
        height=800,
    )

    with open(replay_path, "w", encoding="utf-8") as f:
        json.dump(env.toJSON(), f)

    print()
    print(f"Replay written to: {replay_path}")


def main() -> None:
    """Run the local strategy test."""

    args = parse_args()

    if args.list_strategies:
        print_strategies()
        return

    available = set(available_strategies())

    if args.strategy not in available:
        print(f"Unknown strategy: {args.strategy}")
        print()
        print_strategies()
        raise SystemExit(2)

    run_agent(
        strategy_name=args.strategy,
        opponent=args.opponent,
        episode_steps=args.steps,
        replay_path=args.replay,
    )


if __name__ == "__main__":
    main()