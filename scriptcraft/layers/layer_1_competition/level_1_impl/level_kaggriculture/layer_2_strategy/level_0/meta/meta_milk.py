"""
Milk maximizer strategy via cows.

Buys cow animals, builds pastures, feeds them with wheat, harvests milk,
and sells milk when price is favorable. Grows minimal wheat (only for feed).
No sheep, no other crops — pure animal focus on cows.
"""


class MetaMilkStrategy:
    """Grow cows for milk production."""

    WHEAT_SEED_COST = 10
    COW_COST = 400
    PASTURE_BUILD_COST = 1  # action cost to build pasture
    MILK_SELL_THRESHOLD = 120  # Only sell if price >= $120

    TARGET_COWS = 5  # Target number of cows to build toward
    TARGET_WHEAT_TILES = 2  # Target wheat tiles for cow feed

    def __init__(self):
        pass

    def _step_toward(self, fx: int, fy: int, tx: int, ty: int) -> str:
        """Return direction to move from (fx, fy) toward (tx, ty)."""
        if fx > tx:
            return "WEST"
        if fx < tx:
            return "EAST"
        if fy > ty:
            return "NORTH"
        if fy < ty:
            return "SOUTH"
        return "PASS"

    def _count_structures(self, farm: dict, structure_type: str) -> int:
        """Count existing pastures or coops on the farm."""
        count = 0
        for row in farm["tiles"]:
            for tile in row:
                if isinstance(tile, dict) and tile.get("kind") == structure_type:
                    count += 1
        return count

    def _count_occupied_structures(self, farm: dict, structure_type: str) -> int:
        """Count occupied pastures/coops (with an animal)."""
        count = 0
        for row in farm["tiles"]:
            for tile in row:
                if (
                    isinstance(tile, dict)
                    and tile.get("kind") == structure_type
                    and tile.get("animal") is not None
                ):
                    count += 1
        return count

    def _count_crops(self, farm: dict, crop: str) -> int:
        """Count existing planted crops."""
        count = 0
        for row in farm["tiles"]:
            for tile in row:
                if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") == crop:
                    count += 1
        return count

    def _find_target_tile(self, farm: dict, board_size: int, task: str) -> tuple:
        """
        Find next tile to act on.
        Tasks: "water_wheat", "harvest_wheat", "feed_cow", "harvest_milk", "build_pasture", "place_cow", "plant_wheat"

        Returns (x, y, task) or None.
        """
        fx, fy = farm["farmer"]
        candidates = []

        for y in range(board_size):
            for x in range(board_size):
                tile = farm["tiles"][y][x]

                # Wheat plant: water or harvest
                if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") == "WHEAT":
                    age = tile.get("planted_day", 0)
                    if tile["yield_units"] > 0 and age >= 2:  # Wheat ready at day 2+
                        candidates.append((x, y, "harvest_wheat"))
                    elif not tile["watered_today"]:
                        candidates.append((x, y, "water_wheat"))

                # Pasture with cow: feed or harvest milk
                elif isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                    if tile.get("animal") == "COW":
                        if not tile["fed_today"]:
                            candidates.append((x, y, "feed_cow"))
                        if tile["yield_units"] > 0:
                            candidates.append((x, y, "harvest_milk"))

                # Empty pasture: place cow if we have one
                elif isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") is None:
                    candidates.append((x, y, "place_cow"))

                # Empty tile: build pasture or plant wheat
                elif tile is None:
                    candidates.append((x, y, "build_pasture"))
                    candidates.append((x, y, "plant_wheat"))

        if not candidates:
            return None

        # Priority by task
        priority = {
            "feed_cow": 0,
            "harvest_milk": 1,
            "harvest_wheat": 2,
            "water_wheat": 3,
            "place_cow": 4,
            "build_pasture": 5,
            "plant_wheat": 6,
        }

        # Filter to the requested task
        candidates = [c for c in candidates if c[2] == task]
        if not candidates:
            return None

        # Sort by distance
        candidates.sort(key=lambda c: abs(c[0] - fx) + abs(c[1] - fy))
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
        milk_price = market_prices.get("MILK", 0)
        wheat_price = market_prices.get("WHEAT", 0)

        market = []

        # Sell milk when price is favorable
        milk_in_shed = shed.get("MILK", 0)
        if milk_in_shed > 0 and milk_price >= self.MILK_SELL_THRESHOLD:
            market.append(["SELL", "MILK", milk_in_shed])

        # Buy wheat seed if we're running low (need it for feed)
        if seeds.get("WHEAT", 0) < 5 and farm["money"] >= self.WHEAT_SEED_COST * 5:
            market.append(["BUY_SEED", "WHEAT", 5])

        # Buy cows if we have money and haven't reached target
        occupied_pastures = self._count_occupied_structures(farm, "PASTURE")
        if occupied_pastures < self.TARGET_COWS and farm["money"] >= self.COW_COST:
            market.append(["BUY_ANIMAL", "COW", 1])

        # Sell wheat if we have excess (more than we need for feed)
        wheat_in_shed = shed.get("WHEAT", 0)
        if wheat_in_shed > occupied_pastures + 3:  # Keep at least (cows + 3) for buffer
            market.append(["SELL", "WHEAT", wheat_in_shed - (occupied_pastures + 3)])

        # Decide farmer action
        farmer = ["PASS"]

        # Priority 1: Feed cows (critical)
        target = self._find_target_tile(farm, board_size, "feed_cow")
        if target:
            step = self._step_toward(fx, fy, target[0], target[1])
            if step != "PASS":
                farmer = [step]
            elif (fx, fy) == (target[0], target[1]):
                farmer = ["FEED"]
                return {"farmer": farmer, "hands": [], "market": market}

        # Priority 2: Harvest milk
        target = self._find_target_tile(farm, board_size, "harvest_milk")
        if target:
            step = self._step_toward(fx, fy, target[0], target[1])
            if step != "PASS":
                farmer = [step]
            elif (fx, fy) == (target[0], target[1]):
                farmer = ["HARVEST"]
                return {"farmer": farmer, "hands": [], "market": market}

        # Priority 3: Place cows in empty pastures
        target = self._find_target_tile(farm, board_size, "place_cow")
        if target and shed.get("COW", 0) > 0:
            step = self._step_toward(fx, fy, target[0], target[1])
            if step != "PASS":
                farmer = [step]
            elif (fx, fy) == (target[0], target[1]):
                farmer = ["PLACE", "COW"]
                return {"farmer": farmer, "hands": [], "market": market}

        # Priority 4: Build pastures (if not at target)
        if occupied_pastures < self.TARGET_COWS:
            target = self._find_target_tile(farm, board_size, "build_pasture")
            if target:
                step = self._step_toward(fx, fy, target[0], target[1])
                if step != "PASS":
                    farmer = [step]
                elif (fx, fy) == (target[0], target[1]):
                    farmer = ["BUILD_PASTURE"]
                    return {"farmer": farmer, "hands": [], "market": market}

        # Priority 5: Harvest wheat
        target = self._find_target_tile(farm, board_size, "harvest_wheat")
        if target:
            step = self._step_toward(fx, fy, target[0], target[1])
            if step != "PASS":
                farmer = [step]
            elif (fx, fy) == (target[0], target[1]):
                farmer = ["HARVEST"]
                return {"farmer": farmer, "hands": [], "market": market}

        # Priority 6: Water wheat
        target = self._find_target_tile(farm, board_size, "water_wheat")
        if target:
            step = self._step_toward(fx, fy, target[0], target[1])
            if step != "PASS":
                farmer = [step]
            elif (fx, fy) == (target[0], target[1]):
                farmer = ["WATER"]
                return {"farmer": farmer, "hands": [], "market": market}

        # Priority 7: Plant wheat
        if seeds.get("WHEAT", 0) > 0:
            target = self._find_target_tile(farm, board_size, "plant_wheat")
            if target:
                step = self._step_toward(fx, fy, target[0], target[1])
                if step != "PASS":
                    farmer = [step]
                elif (fx, fy) == (target[0], target[1]):
                    farmer = ["PLANT", "WHEAT"]
                    return {"farmer": farmer, "hands": [], "market": market}

        return {"farmer": farmer, "hands": [], "market": market}