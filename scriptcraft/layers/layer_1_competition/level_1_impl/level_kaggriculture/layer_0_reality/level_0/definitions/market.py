"""
Kaggriculture market definitions.

The market is the single source of truth for product base prices and
dynamic-price calibration parameters.

Static crop/animal definitions intentionally do not duplicate market prices.
"""

from dataclasses import dataclass
from enum import Enum


class PriceShape(Enum):
    """Supported market price curve shapes.

    Note: README.md documents all five shapes (linear, sq, sqrt, log, log10).
    AGENTS.md omits log10 but AGENTS.md is an abbreviated guide, not the
    authoritative specification.  log10 is retained.
    """

    LINEAR = "linear"
    SQUARE = "sq"
    SQRT = "sqrt"
    LOG = "log"
    LOG10 = "log10"


@dataclass(frozen=True)
class MarketDefinition:
    """
    Static parameters for one product's dynamic market price.

    `initial_inventory` is the equilibrium inventory.

    `anchor_throughput` is the inventory displacement used to calibrate
    the curve amplitude.

    The actual curve amplitude is derived by the market rules rather than
    stored as another tuning value.
    """

    base_price: int
    initial_inventory: int
    anchor_throughput: int

    below_shape: PriceShape
    below_target: float

    above_shape: PriceShape
    above_target: float