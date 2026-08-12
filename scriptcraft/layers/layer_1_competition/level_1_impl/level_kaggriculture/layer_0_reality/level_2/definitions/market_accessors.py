from ...level_0.definitions.objects import ObjectType
from ...level_0.definitions.market import MarketDefinition, PriceShape
from ...level_1.definitions.market_catalog import MARKET


def market_definition(product: ObjectType) -> MarketDefinition:
    """Return the immutable market definition for a product."""
    return MARKET[product]


def initial_market_inventory(product: ObjectType) -> int:
    """Return the equilibrium starting inventory for a product."""
    return market_definition(product).initial_inventory


def base_market_price(product: ObjectType) -> int:
    """Return the equilibrium/base market price for a product."""
    return market_definition(product).base_price


def anchor_throughput(product: ObjectType) -> int:
    """Return the calibration throughput for a product."""
    return market_definition(product).anchor_throughput


def price_shape_below(product: ObjectType) -> PriceShape:
    """Return the scarcity-side curve shape."""
    return market_definition(product).below_shape


def price_shape_above(product: ObjectType) -> PriceShape:
    """Return the glut-side curve shape."""
    return market_definition(product).above_shape


def price_target_below(product: ObjectType) -> float:
    """Return the scarcity-side target price movement."""
    return market_definition(product).below_target


def price_target_above(product: ObjectType) -> float:
    """Return the glut-side target price movement."""
    return market_definition(product).above_target