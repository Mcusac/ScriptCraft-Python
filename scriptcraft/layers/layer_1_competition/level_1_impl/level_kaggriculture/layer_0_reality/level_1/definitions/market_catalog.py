from types import MappingProxyType

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.objects import ObjectType
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.market import MarketDefinition, PriceShape


MARKET: MappingProxyType = MappingProxyType({
    ObjectType.WHEAT: MarketDefinition(
        base_price=25,
        initial_inventory=10_000,
        anchor_throughput=400,
        below_shape=PriceShape.SQRT,
        below_target=0.80,
        above_shape=PriceShape.LOG,
        above_target=0.20,
    ),

    ObjectType.CARROT: MarketDefinition(
        base_price=35,
        initial_inventory=10_000,
        anchor_throughput=450,
        below_shape=PriceShape.LOG,
        below_target=0.20,
        above_shape=PriceShape.SQRT,
        above_target=0.70,
    ),

    ObjectType.TOMATO: MarketDefinition(
        base_price=60,
        initial_inventory=10_000,
        anchor_throughput=200,
        below_shape=PriceShape.LINEAR,
        below_target=0.40,
        above_shape=PriceShape.SQRT,
        above_target=0.60,
    ),

    ObjectType.STRAWBERRY: MarketDefinition(
        base_price=120,
        initial_inventory=10_000,
        anchor_throughput=100,
        below_shape=PriceShape.SQRT,
        below_target=0.70,
        above_shape=PriceShape.LINEAR,
        above_target=1.60,
    ),

    ObjectType.MELON: MarketDefinition(
        base_price=250,
        initial_inventory=10_000,
        anchor_throughput=300,
        below_shape=PriceShape.LOG,
        below_target=0.20,
        above_shape=PriceShape.SQUARE,
        above_target=3.60,
    ),

    ObjectType.EGG: MarketDefinition(
        base_price=50,
        initial_inventory=10_000,
        anchor_throughput=332,
        below_shape=PriceShape.LINEAR,
        below_target=0.40,
        above_shape=PriceShape.LOG,
        above_target=0.20,
    ),

    ObjectType.MILK: MarketDefinition(
        base_price=160,
        initial_inventory=10_000,
        anchor_throughput=122,
        below_shape=PriceShape.SQRT,
        below_target=0.60,
        above_shape=PriceShape.LINEAR,
        above_target=1.60,
    ),

    ObjectType.WOOL: MarketDefinition(
        base_price=200,
        initial_inventory=10_000,
        anchor_throughput=105,
        below_shape=PriceShape.LOG,
        below_target=0.20,
        above_shape=PriceShape.SQUARE,
        above_target=3.20,
    ),

    ObjectType.FERTILIZER: MarketDefinition(
        base_price=100,
        initial_inventory=10_000,
        anchor_throughput=200,
        below_shape=PriceShape.LINEAR,
        below_target=0.40,
        above_shape=PriceShape.LINEAR,
        above_target=0.40,
    ),
})