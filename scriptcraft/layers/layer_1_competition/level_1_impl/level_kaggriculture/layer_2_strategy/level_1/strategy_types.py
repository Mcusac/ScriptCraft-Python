"""
Kaggriculture strategy type catalog.

This module defines the available strategy families/types and their
Layer 2 implementations.

Strategy types describe HOW a strategy operates, not WHAT resource
the strategy focuses on.
"""

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_0.basic.buy_once import (
    BuyOnceStrategy,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_0.basic.one_tile_one_crop import (
    OneTileOneCropStrategy,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_0.maxxer.melon_maxxer import (
    MelonMaxxerStrategy,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_0.meta.meta_milk import (
    MetaMilkStrategy,
)
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_2_strategy.level_0.meta.meta_wool import (
    MetaWoolStrategy,
)


# Strategy types/families that require no resource parameter.
STRATEGIES = {
    "buy_once": BuyOnceStrategy,
    "melon_maxxer": MelonMaxxerStrategy,
    "meta_milk": MetaMilkStrategy,
    "meta_wool": MetaWoolStrategy,
}


# Strategy types/families that accept a resource parameter.
PARAMETERIZED_STRATEGIES = {
    "one_tile_one_crop": OneTileOneCropStrategy,
}