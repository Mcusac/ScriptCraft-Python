"""
Kaggriculture action definitions.

This module contains only the actions that exist in the competition.
It does not determine whether an action is currently legal or useful.
"""

from enum import Enum


class FarmAction(Enum):
    """Actions available to the farmer or farm hands."""

    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

    PICKUP = "PICKUP"
    DROP = "DROP"
    PLACE = "PLACE"

    PLANT = "PLANT"
    WATER = "WATER"
    HARVEST = "HARVEST"
    FERTILIZE = "FERTILIZE"

    FEED = "FEED"
    COLLECT_FERTILIZER = "COLLECT_FERTILIZER"
    CARE = "CARE"

    BUILD_COOP = "BUILD_COOP"
    BUILD_PASTURE = "BUILD_PASTURE"
    DIG = "DIG"

    PASS = "PASS"


class MarketAction(Enum):
    """Actions available through the market channel."""

    BUY_SEED = "BUY_SEED"
    BUY_ANIMAL = "BUY_ANIMAL"
    BUY_PRODUCT = "BUY_PRODUCT"
    SELL = "SELL"
    HIRE = "HIRE"
    BUY_LAND = "BUY_LAND"