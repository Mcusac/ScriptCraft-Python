"""
Kaggriculture shop rules.

Defines deterministic shop unlocking, demand access, and town-consumption
behaviour.
"""

from ...level_0.definitions.game import TOWN_SHOP_UNLOCK_INTERVAL
from ...level_0.definitions.shops import TownShopType
from ...level_1.definitions.shop_catalog import SHOP_DEMAND


def shop_unlocks_on_day(day: int) -> bool:
    """
    Return whether a shop unlock event is scheduled on a given in-game day.

    Unlocks occur every `shop_unlock_interval()` days.  Day 0 is the first
    day of the season; the first unlock occurs at day equal to the interval
    (i.e. day % interval == 0 and day > 0).

    This is a pure deterministic calculation.  The random shop selection
    and the 8-instance cap are handled by the engine.
    """
    if day < 0:
        raise ValueError("day must be non-negative")

    return (
        day > 0
        and day % TOWN_SHOP_UNLOCK_INTERVAL == 0
    )


def shop_consumption_multiplier(demand_units: int) -> int:
    """
    Return the units consumed by one shop instance per tick.

    The product-specific demand quantity is already encoded in the demand
    definition; this multiplier is 1:1 (the raw demand value is the
    consumption quantity per instance per tick).
    """
    if demand_units < 0:
        raise ValueError("demand_units must be non-negative")

    return demand_units


def shop_demand(shop_type: TownShopType) -> dict:
    """
    Return the demand for a single shop type as {ObjectType: units}.

    This is the canonical accessor for shop demand.  Callers should use
    this rather than importing SHOP_DEMAND directly.

    Returns a plain dict copy; the caller may modify it freely.

    Important: each shop *instance* consumes independently.  Two instances
    of BAKERY each consume their own egg and wheat quota; they are not
    merged.  The engine is responsible for iterating over instances.
    """
    if shop_type not in SHOP_DEMAND:
        raise ValueError(f"Unknown shop type: {shop_type!r}")

    return dict(SHOP_DEMAND[shop_type])