"""
Melon maximizer strategy.

Plants melons repeatedly and sells them when the market price is above
a threshold. No hiring, no land expansion, no fertilizer — intentionally
pure to establish a baseline.

Based on Notebook 2 tutorial (boatlee/kaggriculture-tutorial).
"""


class MelonMaxxerStrategy:
    """Grow melons and sell when price is favorable."""

    MELON_SEED_COST = 80
    MELON_FIRST_YIELD_DAY = 10
    MELON_MAX_YIELD_DAY = 10
    SELL_THRESHOLD = 200  # Only sell if price >= $200

    def __init__(self):
        pass

    def _step_toward(self, fx: int, fy: int, tx: int, ty: int) -> str:
        """Return the direction to move from (fx, fy) toward (tx, ty)."""
        if fx > tx:
            return "WEST"
        if fx < tx:
            return "EAST"
        if fy > ty:
            return "NORTH"
        if fy < ty:
            return "SOUTH"
        return "PASS"

    def _find_target_tile(self, farm: dict, board_size: int, have_seed: bool) -> tuple:
        """
        Find the next tile to act on (plant, water, or harvest melon).

        Returns (x, y, action) or None.
        Priority: harvest > water > plant (sorted by distance).
        """
        fx, fy = farm["farmer"]
        candidates = []

        for y in range(board_size):
            for x in range(board_size):
                tile = farm["tiles"][y][x]

                # Existing melon plant: water or harvest
                if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile["crop"] == "MELON":
                    if tile["yield_units"] > 0:
                        candidates.append((x, y, "harvest"))
                    elif not tile["watered_today"]:
                        candidates.append((x, y, "water"))

                # Empty tile: plant if we have seed
                elif tile is None and have_seed:
                    candidates.append((x, y, "plant"))

        if not candidates:
            return None

        # Priority: harvest > water > plant; then by distance
        priority = {"harvest": 0, "water": 1, "plant": 2}
        candidates.sort(
            key=lambda c: (
                priority[c[2]],
                abs(c[0] - fx) + abs(c[1] - fy),
            )
        )
        return candidates[0]

    def decide(self, obs: dict) -> dict:
        """Return actions for this turn."""

        farms = obs.get("farms", [])
        player = obs.get("player", 0)
        private = obs.get("private") or {}

        if not farms or player >= len(farms):
            return {"farmer": ["PASS"], "hands": [], "market": []}

        farm = farms[player]
        board_size = len(farm["tiles"])
        fx, fy = farm["farmer"]
        tile = farm["tiles"][fy][fx]
        day = obs.get("day", 0)

        seeds = private.get("seeds", {})
        shed = private.get("shed", {})
        market_prices = (obs.get("market") or {}).get("prices", {})
        melon_price = market_prices.get("MELON", 0)

        market = []

        # Sell melons only when price is above threshold
        melons_in_shed = shed.get("MELON", 0)
        if melons_in_shed > 0 and melon_price >= self.SELL_THRESHOLD:
            market.append(["SELL", "MELON", melons_in_shed])

        # Buy melon seed if we're out
        if seeds.get("MELON", 0) == 0 and farm["money"] >= self.MELON_SEED_COST:
            market.append(["BUY_SEED", "MELON", 1])

        # Decide farmer action
        farmer = ["PASS"]

        # If standing on a melon plant
        if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile["crop"] == "MELON":
            age = day - tile["planted_day"]
            # Harvest if mature and has yield
            if age >= self.MELON_MAX_YIELD_DAY and tile["yield_units"] > 0:
                farmer = ["HARVEST"]
            # Water if not watered today
            elif not tile["watered_today"]:
                farmer = ["WATER"]
            # Otherwise move to next target
            else:
                target = self._find_target_tile(farm, board_size, seeds.get("MELON", 0) > 0)
                if target:
                    step = self._step_toward(fx, fy, target[0], target[1])
                    if step != "PASS":
                        farmer = [step]

        # If standing on empty tile and have seed, plant
        elif tile is None and seeds.get("MELON", 0) > 0:
            farmer = ["PLANT", "MELON"]

        # Otherwise move toward target
        else:
            target = self._find_target_tile(farm, board_size, seeds.get("MELON", 0) > 0)
            if target:
                step = self._step_toward(fx, fy, target[0], target[1])
                if step != "PASS":
                    farmer = [step]

        return {"farmer": farmer, "hands": [], "market": market}