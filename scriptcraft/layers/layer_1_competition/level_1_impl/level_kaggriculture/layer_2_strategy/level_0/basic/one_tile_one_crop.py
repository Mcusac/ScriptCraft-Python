"""
One tile one crop farming strategy for a specific crop.

This strategy performs a simple crop production cycle:
    buy seed
    -> plant crop
    -> water crop
    -> harvest mature crop
    -> sell crop
    -> repeat

Uses layer_0_reality for crop definitions and production rules.
Parameterized by crop type at initialization.
"""

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.crops import CropType
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_1.definitions.crop_catalog import crop_definition
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_2.rules.crop_production import (
    is_one_time_crop,
    is_ongoing_crop,
    produces_on_day as crop_produces_on_day,
)


class OneTileOneCropStrategy:
    """One tile one crop farming strategy focused on one crop type."""

    def __init__(self, crop_type: CropType):
        """
        Initialize strategy for a specific crop.

        Args:
            crop_type: CropType enum value (e.g., CropType.WHEAT)
        """
        if not isinstance(crop_type, CropType):
            raise TypeError(f"crop_type must be CropType, got {type(crop_type)}")

        self.crop_type = crop_type
        self.crop_name = crop_type.value
        self.definition = crop_definition(crop_type)

    def decide(self, obs: dict) -> dict:
        """Return the actions for the current observation."""

        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        current_day = obs["day"]

        fx, fy = me["farmer"]
        tile = me["tiles"][fy][fx]

        market = []

        # Buy seed if we have none and can afford it
        if (
            private["seeds"].get(self.crop_name, 0) == 0
            and me["money"] >= self.definition.seed_cost
        ):
            market.append(["BUY_SEED", self.crop_name, 1])

        # Sell any harvested crop in the shed
        crop_in_shed = private["shed"].get(self.crop_name, 0)
        if crop_in_shed > 0:
            market.append(["SELL", self.crop_name, crop_in_shed])

        # If standing on an empty tile and we have a seed, plant it
        if tile is None:
            if private["seeds"].get(self.crop_name, 0) > 0:
                return {
                    "farmer": ["PLANT", self.crop_name],
                    "hands": [],
                    "market": market,
                }

        # If standing on our crop, manage watering and harvesting
        if isinstance(tile, dict) and tile.get("kind") == "PLANT":
            if tile["crop"] != self.crop_name:
                # Different crop on this tile; pass
                return {
                    "farmer": ["PASS"],
                    "hands": [],
                    "market": market,
                }

            crop_age = current_day - tile["planted_day"]

            # Determine harvest eligibility based on crop type
            is_harvestable = False

            if is_one_time_crop(self.crop_type):
                # One-time crops ready when they reach first yield day
                is_harvestable = crop_age >= self.definition.time_to_first_yield

            elif is_ongoing_crop(self.crop_type):
                # Ongoing crops only produce on scheduled days
                is_harvestable = crop_produces_on_day(self.crop_type, crop_age)

            # Harvest if eligible and we have yield
            if is_harvestable and tile["yield_units"] > 0:
                return {
                    "farmer": ["HARVEST"],
                    "hands": [],
                    "market": market,
                }

            # Water the crop if it has not been watered today
            if not tile["watered_today"]:
                return {
                    "farmer": ["WATER"],
                    "hands": [],
                    "market": market,
                }

        # Nothing else to do this turn
        return {
            "farmer": ["PASS"],
            "hands": [],
            "market": market,
        }