"""
Kaggriculture game constants.

The values in the first section are the competition's default environment
configuration.  An episode may override configurable values when the
environment is created.

The second section contains intrinsic gameplay rules that are not agent
strategy and are not expected to vary between episodes.
"""

# ---------------------------------------------------------------------------
# Configurable / default environment values
# ---------------------------------------------------------------------------

EPISODE_STEPS = 720
TURNS_PER_DAY = 24
DAYS_PER_SEASON = 30

BOARD_SIZE = 10
STARTING_MONEY = 3_000

MAX_MARKET_ORDERS_PER_TURN = 10

SHED_CAPACITY = 100

WEED_SPAWN_CHANCE = 0.005

TOWN_SHOP_UNLOCK_INTERVAL = 3
TOWN_SHOP_SELL_INTERVAL = 4
TOWN_CENTER_SELL_INTERVAL = 24

MAX_TOWN_SHOP_INSTANCES = 8

FARM_HAND_COST_MULT = 1


# ---------------------------------------------------------------------------
# Intrinsic game rules
# ---------------------------------------------------------------------------

LAND_QUADRANT_COUNT = 4
LAND_QUADRANT_SIZE = 5

LAND_PURCHASE_COSTS = (1_000, 2_000, 4_000)

PRICE_FLOOR = 1

MAX_CONSECUTIVE_UNWATERED_DAYS = 2
MAX_CONSECUTIVE_UNFED_DAYS = 2

# Initial per-entity state as documented in the specification.
# "A new seed starts with consecutive_unwatered = 1"
INITIAL_CONSECUTIVE_UNWATERED = 1
# "A newly placed animal starts with consecutive_unfed = 0"
INITIAL_CONSECUTIVE_UNFED = 0

ANIMAL_CARE_BONUS_INCREMENT = 1

ANIMAL_FERTILIZER_PER_DAY = 1

CROP_DECAY_INTERVAL_TURNS = 2

FERTILIZER_DURATION_DAYS = 3