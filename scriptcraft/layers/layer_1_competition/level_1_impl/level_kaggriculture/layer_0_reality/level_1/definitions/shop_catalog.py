"""
Kaggriculture town definitions.

Contains the static demand composition of each town shop.
"""

from types import MappingProxyType

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.objects import ObjectType
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.shops import TownShopType

SHOP_DEMAND: MappingProxyType = MappingProxyType({
    TownShopType.BAKERY: MappingProxyType({
        ObjectType.EGG: 1,
        ObjectType.WHEAT: 1,
    }),

    TownShopType.PIZZA_SHOP: MappingProxyType({
        ObjectType.MILK: 1,
        ObjectType.TOMATO: 1,
        ObjectType.WHEAT: 1,
    }),

    TownShopType.BRUNCH_SPOT: MappingProxyType({
        ObjectType.EGG: 1,
        ObjectType.WHEAT: 1,
        ObjectType.STRAWBERRY: 1,
    }),

    TownShopType.YARN_STORE: MappingProxyType({
        ObjectType.WOOL: 2,
    }),

    TownShopType.ICE_CREAM_SHOP: MappingProxyType({
        ObjectType.STRAWBERRY: 1,
        ObjectType.MILK: 1,
        ObjectType.WHEAT: 1,
    }),

    TownShopType.PET_CAFE: MappingProxyType({
        ObjectType.CARROT: 2,
    }),

    TownShopType.SMOOTHIE_SHOP: MappingProxyType({
        ObjectType.STRAWBERRY: 1,
        ObjectType.MILK: 1,
    }),

    TownShopType.FARMERS_MARKET: MappingProxyType({
        ObjectType.WHEAT: 1,
        ObjectType.CARROT: 1,
        ObjectType.TOMATO: 1,
        ObjectType.STRAWBERRY: 1,
    }),
})