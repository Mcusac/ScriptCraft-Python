"""
Kaggriculture market rules.

Defines deterministic dynamic-market behaviour.

Market definitions live one dependency level below this module, so the
pricing algorithm remains separate from its static tuning parameters.
"""

import math

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.game import (
    MAX_MARKET_ORDERS_PER_TURN,
    PRICE_FLOOR,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.objects import ObjectType
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.market import PriceShape
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_2.definitions.market_accessors import market_definition


BUYABLE_PRODUCTS = frozenset({
    ObjectType.WHEAT,
    ObjectType.FERTILIZER,
})


def max_market_orders_per_turn() -> int:
    """Return the maximum number of market orders processed per turn."""
    return MAX_MARKET_ORDERS_PER_TURN


def price_floor() -> int:
    """Return the minimum possible market price."""
    return PRICE_FLOOR


def can_buy_product(product: ObjectType) -> bool:
    """Return whether a product may be purchased with BUY_PRODUCT."""
    return product in BUYABLE_PRODUCTS


def can_sell_product(product: ObjectType) -> bool:
    """Return whether a defined product may be sold to the market."""
    return True


def price_shape_value(shape: PriceShape, distance: float) -> float:
    """Evaluate a market price curve at a non-negative inventory distance."""
    if distance < 0:
        raise ValueError("distance must be non-negative")

    if shape is PriceShape.LINEAR:
        return distance

    if shape is PriceShape.SQUARE:
        return distance * distance

    if shape is PriceShape.SQRT:
        return math.sqrt(distance)

    if shape is PriceShape.LOG:
        return math.log1p(distance)

    if shape is PriceShape.LOG10:
        return math.log10(1 + distance)

    raise ValueError(f"Unsupported price shape: {shape!r}")


def market_price(
    base_price: int,
    initial_inventory: int,
    inventory: int,
    anchor_throughput: int,
    shape: PriceShape,
    target: float,
) -> int:
    """
    Calculate the dynamic market price for one side of the price curve.

    The curve is calibrated so that `target` describes the relative price
    movement at `anchor_throughput` units of displacement from equilibrium.

    Below equilibrium inventory the price rises; above it falls.
    The result is floored at PRICE_FLOOR.
    """
    if base_price < 0:
        raise ValueError("base_price must be non-negative")

    if anchor_throughput <= 0:
        raise ValueError("anchor_throughput must be positive")

    if target < 0:
        raise ValueError("target must be non-negative")

    if inventory == initial_inventory:
        return max(PRICE_FLOOR, base_price)

    distance = abs(inventory - initial_inventory)

    anchor_value = price_shape_value(shape, anchor_throughput)

    if anchor_value == 0:
        raise ValueError(
            "price shape must produce a non-zero anchor value"
        )

    amplitude = target * base_price / anchor_value
    movement = amplitude * price_shape_value(shape, distance)

    if inventory < initial_inventory:
        raw_price = base_price + movement
    else:
        raw_price = base_price - movement

    return max(PRICE_FLOOR, round(raw_price))


def _price_for_inventory(product: ObjectType, inventory: int) -> int:
    """
    Internal helper: compute price given an inventory level.

    Selects below- or above-equilibrium curve parameters automatically.
    """
    defn = market_definition(product)

    if inventory < defn.initial_inventory:
        shape = defn.below_shape
        target = defn.below_target
    else:
        shape = defn.above_shape
        target = defn.above_target

    return market_price(
        base_price=defn.base_price,
        initial_inventory=defn.initial_inventory,
        inventory=inventory,
        anchor_throughput=defn.anchor_throughput,
        shape=shape,
        target=target,
    )


def sell_price(product: ObjectType, market_inventory: int) -> int:
    """
    Return the sell price for one unit of a product.

    **Quote semantics**: sell price is quoted at the *pre-sell* inventory.
    Pass the current market inventory *before* the unit is removed.

    The price rises when inventory is below I0 (scarcity) and falls when
    above (glut), using the product's configured curve shape and target.
    """
    return _price_for_inventory(product, market_inventory)


def buy_price(product: ObjectType, market_inventory: int) -> int:
    """
    Return the buy price for one unit of a product.

    **Quote semantics**: buy price is quoted at the *post-buy* inventory.
    Pass the market inventory *after* the unit has been removed.

    An immediate buy followed by a sell of the same item against an
    otherwise-unchanged market nets exactly zero.
    """
    return _price_for_inventory(product, market_inventory)