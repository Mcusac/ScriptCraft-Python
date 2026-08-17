import argparse

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
    DEFAULT_STRATEGY,
    available_strategies,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_tests.level_0.single_game import (
    print_results,
    render_game,
    run_game,
    save_replay,
)


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
        default=720,
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


def main() -> None:
    """Run the local single-game test."""

    args = parse_args()

    if args.list_strategies:
        print("Available strategies:")
        for name in available_strategies():
            print(f"  - {name}")
        return

    if args.strategy not in available_strategies():
        print(f"Unknown strategy: {args.strategy}")
        print()
        print("Available strategies:")
        for name in available_strategies():
            print(f"  - {name}")
        raise SystemExit(2)

    print(f"Strategy: {args.strategy}")
    print(f"Opponent: {args.opponent}")
    print(f"Episode steps: {args.steps}")
    print()

    env = run_game(
        strategy_name=args.strategy,
        opponent=args.opponent,
        episode_steps=args.steps,
    )

    print("Final results:")
    print_results(env)

    render_game(env)
    save_replay(env, args.replay)

    print()
    print(f"Replay written to: {args.replay}")


if __name__ == "__main__":
    main()