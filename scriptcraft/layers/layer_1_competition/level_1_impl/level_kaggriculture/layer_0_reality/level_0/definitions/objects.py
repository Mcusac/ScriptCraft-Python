"""
Kaggriculture product definitions.

ObjectType is the canonical vocabulary for goods that can appear in the
market, shed, inventory, or production systems.

Prices are intentionally not defined here. Market prices belong to the
market definitions because the market is the authority for product pricing.
"""

from enum import Enum


class ObjectType(Enum):
    WHEAT = "WHEAT"
    CARROT = "CARROT"
    TOMATO = "TOMATO"
    STRAWBERRY = "STRAWBERRY"
    MELON = "MELON"

    EGG = "EGG"
    MILK = "MILK"
    WOOL = "WOOL"

    FERTILIZER = "FERTILIZER"