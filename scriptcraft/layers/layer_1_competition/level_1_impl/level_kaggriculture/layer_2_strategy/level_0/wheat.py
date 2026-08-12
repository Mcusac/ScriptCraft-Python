"""
Basic wheat farming strategy.

This strategy performs a simple wheat production cycle:

    buy seed
    -> plant wheat
    -> water wheat
    -> harvest mature wheat
    -> sell wheat
    -> repeat
"""


class WheatStrategy:
    """Simple single-crop wheat farming strategy."""

    def decide(self, obs: dict) -> dict:
        """Return the actions for the current observation."""

        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]

        fx, fy = me["farmer"]
        tile = me["tiles"][fy][fx]

        market = []

        # Buy a wheat seed if we have none and have enough money.
        if (
            private["seeds"].get("WHEAT", 0) == 0
            and me["money"] >= 10
        ):
            market.append(["BUY_SEED", "WHEAT", 1])

        # Sell any wheat currently stored in the shed.
        wheat_in_shed = private["shed"].get("WHEAT", 0)

        if wheat_in_shed > 0:
            market.append(["SELL", "WHEAT", wheat_in_shed])

        # If standing on an empty tile and we have wheat seed,
        # plant wheat.
        if (
            tile is None
            and private["seeds"].get("WHEAT", 0) > 0
        ):
            return {
                "farmer": ["PLANT", "WHEAT"],
                "hands": [],
                "market": market,
            }

        # If standing on a plant, manage watering and harvesting.
        if isinstance(tile, dict) and tile.get("kind") == "PLANT":
            crop_age = obs["day"] - tile["planted_day"]

            # Wheat first yield day.
            if crop_age >= 2:
                return {
                    "farmer": ["HARVEST"],
                    "hands": [],
                    "market": market,
                }

            # Water the crop if it has not been watered today.
            if not tile["watered_today"]:
                return {
                    "farmer": ["WATER"],
                    "hands": [],
                    "market": market,
                }

        # Nothing else to do this turn.
        return {
            "farmer": ["PASS"],
            "hands": [],
            "market": market,
        }