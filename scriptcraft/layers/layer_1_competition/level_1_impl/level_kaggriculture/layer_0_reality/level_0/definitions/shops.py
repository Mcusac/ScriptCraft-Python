"""
Kaggriculture town definitions.

Contains the static demand composition of each town shop.
"""

from enum import Enum


class TownShopType(Enum):
    BAKERY = "BAKERY"
    PIZZA_SHOP = "PIZZA_SHOP"
    BRUNCH_SPOT = "BRUNCH_SPOT"
    YARN_STORE = "YARN_STORE"
    ICE_CREAM_SHOP = "ICE_CREAM_SHOP"
    PET_CAFE = "PET_CAFE"
    SMOOTHIE_SHOP = "SMOOTHIE_SHOP"
    FARMERS_MARKET = "FARMERS_MARKET"
