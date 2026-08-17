"""
Kaggriculture farm-hand hiring rules.

Defines deterministic rules for farm-hand cost calculation, spawn-position
selection, and daily lifecycle.

No actual spawning, inventory mutation, entity creation, or day orchestration
is performed here.
"""

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.game import FARM_HAND_COST_MULT


def fibonacci(n: int) -> int:
    """
    Return the n-th Fibonacci number (1-indexed).

    Sequence: 1, 1, 2, 3, 5, 8, 13, 21, ...

    fibonacci(1) = 1, fibonacci(2) = 1, fibonacci(3) = 2, ...
    """
    if n <= 0:
        raise ValueError("fibonacci index must be positive")

    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b

    return a if n == 1 else b


def farm_hand_cost(
    hires_today: int,
    farm_hand_cost_mult: int = FARM_HAND_COST_MULT,
) -> int:
    """
    Return the coin cost to hire the next farm hand today.

    The specification defines:

        cost = farmHandCostMult × fib(n)

    where n = hires_today + 1 (the 1-based index of the next hire).

    With the default farmHandCostMult = 1:
        hires_today=0 → fib(1) = 1
        hires_today=1 → fib(2) = 1
        hires_today=2 → fib(3) = 2
        hires_today=3 → fib(4) = 3
        hires_today=4 → fib(5) = 5
        ...

    Hire count resets at the start of each day.
    """
    if hires_today < 0:
        raise ValueError("hires_today must be non-negative")

    if farm_hand_cost_mult < 0:
        raise ValueError("farm_hand_cost_mult must be non-negative")

    return farm_hand_cost_mult * fibonacci(hires_today + 1)


def hires_reset_each_day() -> bool:
    """Return whether farm-hand hire count resets at the start of each day."""
    return True


def hired_hands_are_daily() -> bool:
    """
    Return whether hired hands disappear at the end of each day.

    Hands must be re-hired at the start of each subsequent day.
    """
    return True

