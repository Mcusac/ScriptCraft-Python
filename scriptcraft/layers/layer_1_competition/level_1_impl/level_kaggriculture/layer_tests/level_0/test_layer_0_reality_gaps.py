"""
Layer 0 Reality contract tests for Kaggriculture.

These tests verify that layer_0_reality accurately represents the
competition's documented rules and canonical definitions.

The purpose of this suite is not to test implementation details or
future strategy behavior. It establishes a regression boundary around
the competition reality that higher layers are allowed to depend upon.

Coverage includes:

- canonical actions and vocabulary
- immutable crop definitions and crop catalog
- immutable animal definitions and animal catalog
- immutable market definitions and shop catalog
- competition configuration constants
- time rules
- farm geometry and land rules
- shed access
- DIG legality
- weed spawning conditions
- watering/feeding failure thresholds
- animal-to-structure compatibility
- animal care bonus
- animal production timing and yield
- crop production timing and watering/fertilizer behavior
- crop decay
- farm-hand hiring cost
- farm-hand spawn selection
- town shop unlock timing and demand
- market price curves and buy/sell semantics

These tests intentionally do not instantiate an engine, mutate game state,
or test strategy.
"""

from types import MappingProxyType

import pytest

# ============================================================================
# Level 0 definitions
# ============================================================================

from ..layer_0_reality.level_0.definitions.actions import (
    FarmAction,
    MarketAction,
)

from ..layer_0_reality.level_0.definitions.crops import (
    CropDefinition,
    CropType,
    YieldType,
)

from ..layer_0_reality.level_0.definitions.game import (
    ANIMAL_CARE_BONUS_INCREMENT,
    ANIMAL_FERTILIZER_PER_DAY,
    BOARD_SIZE,
    CROP_DECAY_INTERVAL_TURNS,
    DAYS_PER_SEASON,
    EPISODE_STEPS,
    FARM_HAND_COST_MULT,
    FERTILIZER_DURATION_DAYS,
    INITIAL_CONSECUTIVE_UNFED,
    INITIAL_CONSECUTIVE_UNWATERED,
    LAND_QUADRANT_COUNT,
    LAND_QUADRANT_SIZE,
    LAND_PURCHASE_COSTS,
    MAX_CONSECUTIVE_UNFED_DAYS,
    MAX_CONSECUTIVE_UNWATERED_DAYS,
    MAX_TOWN_SHOP_INSTANCES,
    PRICE_FLOOR,
    SHED_CAPACITY,
    STARTING_MONEY,
    TOWN_CENTER_SELL_INTERVAL,
    TOWN_SHOP_SELL_INTERVAL,
    TOWN_SHOP_UNLOCK_INTERVAL,
    TURNS_PER_DAY,
    WEED_SPAWN_CHANCE,
)

from ..layer_0_reality.level_0.definitions.market import (
    MarketDefinition,
    PriceShape,
)

from ..layer_0_reality.level_0.definitions.objects import (
    ObjectType,
)

from ..layer_0_reality.level_0.definitions.shops import (
    TownShopType,
)

# ============================================================================
# Level 1 definitions
# ============================================================================

from ..layer_0_reality.level_1.definitions.animals import (
    AnimalDefinition,
    AnimalType,
    StructureType,
)

from ..layer_0_reality.level_1.definitions.crop_catalog import (
    CROPS,
    crop_definition,
)

from ..layer_0_reality.level_1.definitions.market_catalog import (
    MARKET,
)

from ..layer_0_reality.level_1.definitions.shop_catalog import (
    SHOP_DEMAND,
)

# ============================================================================
# Level 1 rules
# ============================================================================

from ..layer_0_reality.level_1.rules.animal_care import (
    animal_fails_after,
    care_bonus_accrual,
)

from ..layer_0_reality.level_1.rules.animal_initial_state import (
    initial_consecutive_unfed_days,
)

from ..layer_0_reality.level_1.rules.animal_structure import (
    required_structure,
)

from ..layer_0_reality.level_1.rules.crop_initial_state import (
    initial_consecutive_unwatered_days,
)

from ..layer_0_reality.level_1.rules.farm_conditions import (
    can_spawn_weed,
    weed_spawn_chance,
)

from ..layer_0_reality.level_1.rules.farm_geometry import (
    all_land_unlocked,
    initial_unlocked_quadrants,
    is_shed_access_tile,
    is_tile_unlocked,
    next_land_purchase_cost,
    quadrant_bounds,
    quadrant_for_position,
    quadrant_size,
    quadrant_tiles,
    total_board_tiles,
    valid_board_position,
    Quadrant,
)

from ..layer_0_reality.level_1.rules.farm_hands import (
    farm_hand_cost,
    fibonacci,
)

from ..layer_0_reality.level_1.rules.farm_hand_spawning import (
    select_spawn_tile,
    spawn_candidates_in_preference_order,
)

from ..layer_0_reality.level_1.rules.farming import (
    can_dig_empty_structure,
    can_dig_occupied_structure,
    can_dig_plant,
    can_dig_weed,
    shed_access_tiles,
)

from ..layer_0_reality.level_1.rules.time import (
    day_from_step,
    is_end_of_day,
    is_end_of_season,
    season_days,
    turn_in_day,
)

from ..layer_0_reality.level_1.rules.shop import (
    shop_demand,
    shop_unlocks_on_day,
)

# ============================================================================
# Level 2 rules
# ============================================================================

from ..layer_0_reality.level_2.rules.animal_production import (
    animal_production_yield,
    production_count,
    production_yield_with_care,
    produces_on_day,
)

from ..layer_0_reality.level_2.rules.crop_production import (
    bonus_end_day,
    bonus_start_day,
    first_yield_day,
    is_one_time_crop,
    is_ongoing_crop,
    max_yield,
    one_time_bonus_applies,
    one_time_bonus_end_day,
    one_time_bonus_start_day,
    one_time_watering_bonus,
    one_time_yield,
    ongoing_production_count,
    ongoing_production_yield,
    production_interval,
    produces_on_day as crop_produces_on_day,
)

from ..layer_0_reality.level_2.rules.crop_decay import (
    becomes_weed,
    decay_reduction,
    decay_start_day,
    decayed_yield,
    is_decaying,
    one_time_decay_start_day,
    ongoing_decay_start_day,
)

from ..layer_0_reality.level_2.rules.market import (
    buy_price,
    can_buy_product,
    can_sell_product,
    market_price,
    price_shape_value,
    sell_price,
)

from ..layer_0_reality.level_2.definitions.market_accessors import (
    initial_market_inventory,
)

# ============================================================================
# Canonical configuration
# ============================================================================


class TestGameConfiguration:
    """Pin the competition's documented default configuration."""

    def test_episode_timing(self):
        assert TURNS_PER_DAY == 24
        assert DAYS_PER_SEASON == 30
        assert EPISODE_STEPS == 720
        assert EPISODE_STEPS == TURNS_PER_DAY * DAYS_PER_SEASON

    def test_board_configuration(self):
        assert BOARD_SIZE == 10
        assert LAND_QUADRANT_COUNT == 4
        assert LAND_QUADRANT_SIZE == 5
        assert LAND_QUADRANT_SIZE * 2 == BOARD_SIZE

    def test_economy_configuration(self):
        assert STARTING_MONEY == 3000
        assert SHED_CAPACITY == 100
        assert initial_market_inventory(ObjectType.WHEAT) == 10_000
        assert PRICE_FLOOR == 1

    def test_land_configuration(self):
        assert LAND_PURCHASE_COSTS == (1000, 2000, 4000)

    def test_failure_configuration(self):
        assert INITIAL_CONSECUTIVE_UNWATERED == 1
        assert INITIAL_CONSECUTIVE_UNFED == 0
        assert MAX_CONSECUTIVE_UNWATERED_DAYS == 2
        assert MAX_CONSECUTIVE_UNFED_DAYS == 2

    def test_fertilizer_configuration(self):
        assert FERTILIZER_DURATION_DAYS == 3
        assert ANIMAL_FERTILIZER_PER_DAY == 1

    def test_decay_configuration(self):
        assert CROP_DECAY_INTERVAL_TURNS == 2

    def test_farm_hand_configuration(self):
        assert FARM_HAND_COST_MULT == 1

    def test_town_configuration(self):
        assert TOWN_SHOP_UNLOCK_INTERVAL == 3
        assert TOWN_SHOP_SELL_INTERVAL == 4
        assert TOWN_CENTER_SELL_INTERVAL == 24
        assert MAX_TOWN_SHOP_INSTANCES == 8

    def test_weed_configuration(self):
        assert WEED_SPAWN_CHANCE == pytest.approx(0.005)

    def test_animal_care_configuration(self):
        assert ANIMAL_CARE_BONUS_INCREMENT == 1


# ============================================================================
# Canonical vocabulary
# ============================================================================


class TestCanonicalVocabulary:
    """Ensure the complete competition vocabulary exists."""

    def test_crop_types(self):
        assert set(CropType) == {
            CropType.WHEAT,
            CropType.CARROT,
            CropType.TOMATO,
            CropType.STRAWBERRY,
            CropType.MELON,
        }

    def test_animal_types(self):
        assert set(AnimalType) == {
            AnimalType.GOOSE,
            AnimalType.COW,
            AnimalType.SHEEP,
        }

    def test_object_types(self):
        assert set(ObjectType) == {
            ObjectType.WHEAT,
            ObjectType.CARROT,
            ObjectType.TOMATO,
            ObjectType.STRAWBERRY,
            ObjectType.MELON,
            ObjectType.EGG,
            ObjectType.MILK,
            ObjectType.WOOL,
            ObjectType.FERTILIZER,
        }

    def test_shop_types(self):
        assert len(tuple(TownShopType)) == 8

    def test_farm_actions_are_defined(self):
        assert FarmAction.NORTH.value == "NORTH"
        assert FarmAction.SOUTH.value == "SOUTH"
        assert FarmAction.EAST.value == "EAST"
        assert FarmAction.WEST.value == "WEST"
        assert FarmAction.PLANT.value == "PLANT"
        assert FarmAction.WATER.value == "WATER"
        assert FarmAction.HARVEST.value == "HARVEST"
        assert FarmAction.FEED.value == "FEED"
        assert FarmAction.CARE.value == "CARE"
        assert FarmAction.DIG.value == "DIG"
        assert FarmAction.PASS.value == "PASS"

    def test_market_actions_are_defined(self):
        assert MarketAction.BUY_SEED.value == "BUY_SEED"
        assert MarketAction.BUY_ANIMAL.value == "BUY_ANIMAL"
        assert MarketAction.BUY_PRODUCT.value == "BUY_PRODUCT"
        assert MarketAction.SELL.value == "SELL"
        assert MarketAction.HIRE.value == "HIRE"
        assert MarketAction.BUY_LAND.value == "BUY_LAND"


# ============================================================================
# Crop definitions
# ============================================================================


class TestCropDefinitions:
    """Verify every crop's canonical definition."""

    def test_all_crop_types_have_definitions(self):
        assert set(CROPS) == set(CropType)

    @pytest.mark.parametrize("crop", list(CropType))
    def test_definition_is_immutable(self, crop):
        definition = crop_definition(crop)

        assert isinstance(definition, CropDefinition)

        with pytest.raises((AttributeError, TypeError)):
            definition.seed_cost = 999  # type: ignore[misc]

    def test_catalog_is_immutable(self):
        assert isinstance(CROPS, MappingProxyType)

        with pytest.raises(TypeError):
            CROPS[CropType.WHEAT] = None  # type: ignore[index]

    @pytest.mark.parametrize(
        "crop,seed_cost,first,max_time,yield_cap",
        [
            (CropType.WHEAT, 10, 2, 4, 6),
            (CropType.CARROT, 20, 2, 3, 4),
            (CropType.TOMATO, 50, 8, 11, 4),
            (CropType.STRAWBERRY, 100, 10, 16, 4),
            (CropType.MELON, 80, 10, 10, 6),
        ],
    )
    def test_crop_values(
        self,
        crop,
        seed_cost,
        first,
        max_time,
        yield_cap,
    ):
        definition = crop_definition(crop)

        assert definition.seed_cost == seed_cost
        assert definition.time_to_first_yield == first
        assert definition.time_to_max_yield == max_time
        assert definition.max_yield == yield_cap
        assert definition.action_cost == 1

    def test_one_time_crop_types(self):
        assert is_one_time_crop(CropType.WHEAT)
        assert is_one_time_crop(CropType.CARROT)
        assert is_one_time_crop(CropType.MELON)

    def test_ongoing_crop_types(self):
        assert is_ongoing_crop(CropType.TOMATO)
        assert is_ongoing_crop(CropType.STRAWBERRY)

    def test_production_intervals(self):
        assert production_interval(CropType.TOMATO) == 1
        assert production_interval(CropType.STRAWBERRY) == 2
        assert production_interval(CropType.WHEAT) == 0
        assert production_interval(CropType.CARROT) == 0
        assert production_interval(CropType.MELON) == 0

    def test_bonus_windows(self):
        assert (
            bonus_start_day(CropType.WHEAT),
            bonus_end_day(CropType.WHEAT),
        ) == (2, 4)

        assert (
            bonus_start_day(CropType.CARROT),
            bonus_end_day(CropType.CARROT),
        ) == (2, 3)

        assert (
            bonus_start_day(CropType.TOMATO),
            bonus_end_day(CropType.TOMATO),
        ) == (8, 11)

        assert (
            bonus_start_day(CropType.STRAWBERRY),
            bonus_end_day(CropType.STRAWBERRY),
        ) == (10, 16)

        assert (
            bonus_start_day(CropType.MELON),
            bonus_end_day(CropType.MELON),
        ) == (6, 12)


# ============================================================================
# Animal definitions
# ============================================================================


class TestAnimalDefinitions:
    def test_all_animals_have_definitions(self):
        from layer_0_reality.level_2.definitions.animal_catalog import ANIMALS

        assert set(ANIMALS) == set(AnimalType)

    @pytest.mark.parametrize("animal", list(AnimalType))
    def test_definition_is_immutable(self, animal):
        from layer_0_reality.level_2.definitions.animal_catalog import animal_definition

        definition = animal_definition(animal)

        assert isinstance(definition, AnimalDefinition)

        with pytest.raises((AttributeError, TypeError)):
            definition.purchase_cost = 999  # type: ignore[misc]

    @pytest.mark.parametrize(
        "animal,cost,product,first,interval,max_held",
        [
            (AnimalType.GOOSE, 300, ObjectType.EGG, 4, 1, 4),
            (AnimalType.COW, 400, ObjectType.MILK, 8, 2, 6),
            (AnimalType.SHEEP, 500, ObjectType.WOOL, 6, 3, 6),
        ],
    )
    def test_animal_values(
        self,
        animal,
        cost,
        product,
        first,
        interval,
        max_held,
    ):
        from layer_0_reality.level_2.definitions.animal_catalog import animal_definition

        definition = animal_definition(animal)

        assert definition.purchase_cost == cost
        assert definition.product is product
        assert definition.time_to_first_yield == first
        assert definition.production_interval == interval
        assert definition.max_held == max_held
        assert definition.action_cost == 1


# ============================================================================
# Market definitions
# ============================================================================


class TestMarketDefinitions:
    def test_market_is_immutable(self):
        assert isinstance(MARKET, MappingProxyType)

        with pytest.raises(TypeError):
            MARKET[ObjectType.WHEAT] = None  # type: ignore[index]

    @pytest.mark.parametrize("product", list(ObjectType))
    def test_every_product_has_market_definition(self, product):
        assert product in MARKET

        definition = MARKET[product]
        assert isinstance(definition, MarketDefinition)

    def test_every_market_definition_is_immutable(self):
        for definition in MARKET.values():
            with pytest.raises((AttributeError, TypeError)):
                definition.base_price = 999  # type: ignore[misc]

    @pytest.mark.parametrize(
        "product,base_price,anchor",
        [
            (ObjectType.WHEAT, 25, 400),
            (ObjectType.CARROT, 35, 450),
            (ObjectType.TOMATO, 60, 200),
            (ObjectType.STRAWBERRY, 120, 100),
            (ObjectType.MELON, 250, 300),
            (ObjectType.EGG, 50, 332),
            (ObjectType.MILK, 160, 122),
            (ObjectType.WOOL, 200, 105),
            (ObjectType.FERTILIZER, 100, 200),
        ],
    )
    def test_market_values(self, product, base_price, anchor):
        definition = MARKET[product]

        assert definition.base_price == base_price
        assert definition.initial_inventory == INITIAL_MARKET_INVENTORY
        assert definition.anchor_throughput == anchor

    def test_all_price_shapes_exist(self):
        assert set(PriceShape) == {
            PriceShape.LINEAR,
            PriceShape.SQUARE,
            PriceShape.SQRT,
            PriceShape.LOG,
            PriceShape.LOG10,
        }


# ============================================================================
# Shop catalog
# ============================================================================


class TestShopCatalog:
    def test_shop_catalog_is_immutable(self):
        assert isinstance(SHOP_DEMAND, MappingProxyType)

        with pytest.raises(TypeError):
            SHOP_DEMAND[TownShopType.BAKERY] = {}  # type: ignore[index]

    def test_inner_shop_demands_are_immutable(self):
        for demand in SHOP_DEMAND.values():
            assert isinstance(demand, MappingProxyType)

    def test_all_shop_types_have_demand(self):
        assert set(SHOP_DEMAND) == set(TownShopType)

    @pytest.mark.parametrize(
        "shop,expected",
        [
            (
                TownShopType.BAKERY,
                {ObjectType.EGG: 1, ObjectType.WHEAT: 1},
            ),
            (
                TownShopType.PIZZA_SHOP,
                {
                    ObjectType.MILK: 1,
                    ObjectType.TOMATO: 1,
                    ObjectType.WHEAT: 1,
                },
            ),
            (
                TownShopType.BRUNCH_SPOT,
                {
                    ObjectType.EGG: 1,
                    ObjectType.WHEAT: 1,
                    ObjectType.STRAWBERRY: 1,
                },
            ),
            (
                TownShopType.YARN_STORE,
                {ObjectType.WOOL: 2},
            ),
            (
                TownShopType.ICE_CREAM_SHOP,
                {
                    ObjectType.STRAWBERRY: 1,
                    ObjectType.MILK: 1,
                    ObjectType.WHEAT: 1,
                },
            ),
            (
                TownShopType.PET_CAFE,
                {ObjectType.CARROT: 2},
            ),
            (
                TownShopType.SMOOTHIE_SHOP,
                {
                    ObjectType.STRAWBERRY: 1,
                    ObjectType.MILK: 1,
                },
            ),
            (
                TownShopType.FARMERS_MARKET,
                {
                    ObjectType.WHEAT: 1,
                    ObjectType.CARROT: 1,
                    ObjectType.TOMATO: 1,
                    ObjectType.STRAWBERRY: 1,
                },
            ),
        ],
    )
    def test_shop_demand_catalog(self, shop, expected):
        assert dict(SHOP_DEMAND[shop]) == expected


# ============================================================================
# Time rules
# ============================================================================


class TestTimeRules:
    def test_day_from_step(self):
        assert day_from_step(0) == 0
        assert day_from_step(23) == 0
        assert day_from_step(24) == 1
        assert day_from_step(47) == 1
        assert day_from_step(719) == 29

    def test_turn_in_day(self):
        assert turn_in_day(0) == 0
        assert turn_in_day(23) == 23
        assert turn_in_day(24) == 0
        assert turn_in_day(719) == 23

    def test_end_of_day(self):
        assert is_end_of_day(22) is False
        assert is_end_of_day(23) is True
        assert is_end_of_day(24) is False
        assert is_end_of_day(47) is True

    def test_end_of_season(self):
        assert is_end_of_season(718) is False
        assert is_end_of_season(719) is True

    def test_season_days(self):
        assert season_days() == 30

    @pytest.mark.parametrize("function", [
        day_from_step,
        turn_in_day,
        is_end_of_day,
    ])
    def test_time_rules_reject_negative_steps(self, function):
        with pytest.raises(ValueError):
            function(-1)

    def test_rejects_invalid_turn_configuration(self):
        with pytest.raises(ValueError):
            day_from_step(0, 0)

        with pytest.raises(ValueError):
            turn_in_day(0, 0)

        with pytest.raises(ValueError):
            is_end_of_day(0, 0)

    def test_rejects_invalid_episode_configuration(self):
        with pytest.raises(ValueError):
            is_end_of_season(0, 0)


# ============================================================================
# Farm geometry and land
# ============================================================================


class TestFarmGeometry:
    def test_quadrant_size(self):
        assert quadrant_size() == 5
        assert quadrant_size(8) == 4
        assert quadrant_size(12) == 6

    @pytest.mark.parametrize("size", [0, -1, 9, 11])
    def test_invalid_quadrant_size(self, size):
        with pytest.raises(ValueError):
            quadrant_size(size)

    def test_total_board_tiles(self):
        assert total_board_tiles() == 100
        assert total_board_tiles(8) == 64

    @pytest.mark.parametrize("size", [0, -1])
    def test_invalid_total_board_size(self, size):
        with pytest.raises(ValueError):
            total_board_tiles(size)

    def test_quadrant_tiles(self):
        assert quadrant_tiles() == 25
        assert quadrant_tiles(8) == 16

    def test_quadrant_bounds(self):
        assert quadrant_bounds(Quadrant.NW) == (0, 0, 5, 5)
        assert quadrant_bounds(Quadrant.NE) == (5, 0, 10, 5)
        assert quadrant_bounds(Quadrant.SW) == (0, 5, 5, 10)
        assert quadrant_bounds(Quadrant.SE) == (5, 5, 10, 10)

    @pytest.mark.parametrize(
        "position,quadrant",
        [
            ((0, 0), Quadrant.NW),
            ((4, 4), Quadrant.NW),
            ((5, 0), Quadrant.NE),
            ((9, 4), Quadrant.NE),
            ((0, 5), Quadrant.SW),
            ((4, 9), Quadrant.SW),
            ((5, 5), Quadrant.SE),
            ((9, 9), Quadrant.SE),
        ],
    )
    def test_quadrant_for_position(self, position, quadrant):
        assert quadrant_for_position(*position) is quadrant

    @pytest.mark.parametrize(
        "position",
        [
            (-1, 0),
            (0, -1),
            (10, 0),
            (0, 10),
        ],
    )
    def test_invalid_positions(self, position):
        assert valid_board_position(*position) is False

        with pytest.raises(ValueError):
            quadrant_for_position(*position)

    def test_initial_land(self):
        assert initial_unlocked_quadrants() == frozenset({Quadrant.NW})

    def test_tile_unlock_state(self):
        assert is_tile_unlocked(0, 0, {Quadrant.NW})
        assert not is_tile_unlocked(5, 0, {Quadrant.NW})

    def test_land_purchase_costs(self):
        assert next_land_purchase_cost(1) == 1000
        assert next_land_purchase_cost(2) == 2000
        assert next_land_purchase_cost(3) == 4000
        assert next_land_purchase_cost(4) is None

    def test_land_purchase_requires_one_unlocked_quadrant(self):
        with pytest.raises(ValueError):
            next_land_purchase_cost(0)

    def test_all_land_unlocked(self):
        assert not all_land_unlocked(3)
        assert all_land_unlocked(4)
        assert all_land_unlocked(5)


# ============================================================================
# Shed
# ============================================================================


class TestShedGeometry:
    def test_shed_access_tiles(self):
        assert shed_access_tiles() == (
            (4, 4),
            (5, 4),
            (4, 5),
            (5, 5),
        )

    def test_shed_access_order_is_nwse(self):
        tiles = shed_access_tiles()

        assert tiles[0] == (4, 4)
        assert tiles[1] == (5, 4)
        assert tiles[2] == (4, 5)
        assert tiles[3] == (5, 5)

    def test_shed_access_tiles_scale_with_board(self):
        assert shed_access_tiles(8) == (
            (3, 3),
            (4, 3),
            (3, 4),
            (4, 4),
        )

    def test_is_shed_access_tile(self):
        assert is_shed_access_tile(4, 4)
        assert is_shed_access_tile(5, 4)
        assert not is_shed_access_tile(0, 0)


# ============================================================================
# Farm conditions
# ============================================================================


class TestFarmConditions:
    def test_weed_spawn_chance(self):
        assert weed_spawn_chance() == pytest.approx(0.005)

    @pytest.mark.parametrize(
        "empty,unlocked,expected",
        [
            (True, True, True),
            (True, False, False),
            (False, True, False),
            (False, False, False),
        ],
    )
    def test_can_spawn_weed(self, empty, unlocked, expected):
        assert can_spawn_weed(
            tile_is_empty=empty,
            tile_is_unlocked=unlocked,
        ) is expected


# ============================================================================
# Initial crop and animal state
# ============================================================================


class TestInitialConditions:
    def test_new_crop_starts_one_day_unwatered(self):
        assert initial_consecutive_unwatered_days() == 1

    def test_new_animal_starts_fully_fed_condition(self):
        assert initial_consecutive_unfed_days() == 0


# ============================================================================
# DIG rules
# ============================================================================


class TestDIGRules:
    def test_plant_can_be_dug(self):
        assert can_dig_plant() is True

    def test_weed_can_be_dug(self):
        assert can_dig_weed() is True

    def test_empty_structure_can_be_dug(self):
        assert can_dig_empty_structure() is True

    def test_occupied_structure_cannot_be_dug(self):
        assert can_dig_occupied_structure() is False


# ============================================================================
# Animal structure compatibility
# ============================================================================


class TestAnimalStructures:
    def test_goose_requires_coop(self):
        assert required_structure(AnimalType.GOOSE) is StructureType.COOP

    def test_cow_requires_pasture(self):
        assert required_structure(AnimalType.COW) is StructureType.PASTURE

    def test_sheep_requires_pasture(self):
        assert required_structure(AnimalType.SHEEP) is StructureType.PASTURE

    @pytest.mark.parametrize("animal", list(AnimalType))
    def test_every_animal_has_structure(self, animal):
        assert isinstance(required_structure(animal), StructureType)


# ============================================================================
# Animal care and failure
# ============================================================================


class TestAnimalCare:
    @pytest.mark.parametrize(
        "fed,cared,expected",
        [
            (False, False, 0),
            (False, True, 0),
            (True, False, 0),
            (True, True, 1),
        ],
    )
    def test_care_bonus_accrual(self, fed, cared, expected):
        assert care_bonus_accrual(
            fed_today=fed,
            cared_today=cared,
        ) == expected

    @pytest.mark.parametrize(
        "consecutive_unfed,expected",
        [
            (0, False),
            (1, False),
            (2, True),
            (3, True),
        ],
    )
    def test_animal_failure_threshold(self, consecutive_unfed, expected):
        assert (
            animal_fails_after(consecutive_unfed)
            is expected
        )


# ============================================================================
# Animal production
# ============================================================================


class TestAnimalProduction:
    @pytest.mark.parametrize(
        "animal,first,interval",
        [
            (AnimalType.GOOSE, 4, 1),
            (AnimalType.COW, 8, 2),
            (AnimalType.SHEEP, 6, 3),
        ],
    )
    def test_first_production_day(self, animal, first, interval):
        assert produces_on_day(animal, first - 1) is False
        assert produces_on_day(animal, first) is True

    def test_goose_produces_daily_after_first_yield(self):
        assert produces_on_day(AnimalType.GOOSE, 4)
        assert produces_on_day(AnimalType.GOOSE, 5)
        assert produces_on_day(AnimalType.GOOSE, 6)

    def test_cow_produces_every_two_days(self):
        assert produces_on_day(AnimalType.COW, 8)
        assert not produces_on_day(AnimalType.COW, 9)
        assert produces_on_day(AnimalType.COW, 10)
        assert not produces_on_day(AnimalType.COW, 11)

    def test_sheep_produces_every_three_days(self):
        assert produces_on_day(AnimalType.SHEEP, 6)
        assert not produces_on_day(AnimalType.SHEEP, 7)
        assert not produces_on_day(AnimalType.SHEEP, 8)
        assert produces_on_day(AnimalType.SHEEP, 9)

    def test_negative_age_never_produces(self):
        assert produces_on_day(AnimalType.GOOSE, -1) is False

    def test_production_count(self):
        assert production_count(AnimalType.GOOSE, 3) == 0
        assert production_count(AnimalType.GOOSE, 4) == 1
        assert production_count(AnimalType.GOOSE, 6) == 3

        assert production_count(AnimalType.COW, 7) == 0
        assert production_count(AnimalType.COW, 8) == 1
        assert production_count(AnimalType.COW, 12) == 3

    def test_production_yield_base(self):
        assert production_yield_with_care(
            fed_today=False,
            pending_care_bonus=5,
        ) == 1

    def test_production_yield_with_care(self):
        assert production_yield_with_care(
            fed_today=True,
            pending_care_bonus=0,
        ) == 1

        assert production_yield_with_care(
            fed_today=True,
            pending_care_bonus=2,
        ) == 3

    def test_negative_care_bonus_rejected(self):
        with pytest.raises(ValueError):
            production_yield_with_care(
                fed_today=True,
                pending_care_bonus=-1,
            )

    def test_actual_production_respects_held_cap(self):
        assert animal_production_yield(
            AnimalType.GOOSE,
            4,
            fed_today=True,
            pending_care_bonus=2,
            current_held_yield=3,
        ) == 1

        assert animal_production_yield(
            AnimalType.GOOSE,
            4,
            fed_today=True,
            pending_care_bonus=2,
            current_held_yield=4,
        ) == 0

    def test_actual_production_zero_on_non_production_day(self):
        assert animal_production_yield(
            AnimalType.COW,
            9,
            fed_today=True,
            pending_care_bonus=2,
        ) == 0

    def test_actual_production_rejects_negative_held_yield(self):
        with pytest.raises(ValueError):
            animal_production_yield(
                AnimalType.GOOSE,
                4,
                fed_today=True,
                pending_care_bonus=0,
                current_held_yield=-1,
            )


# ============================================================================
# Crop production
# ============================================================================


class TestCropProduction:
    def test_one_time_and_ongoing_categories(self):
        assert is_one_time_crop(CropType.WHEAT)
        assert is_one_time_crop(CropType.CARROT)
        assert is_one_time_crop(CropType.MELON)

        assert is_ongoing_crop(CropType.TOMATO)
        assert is_ongoing_crop(CropType.STRAWBERRY)

    def test_first_yield_days(self):
        assert first_yield_day(CropType.WHEAT) == 2
        assert first_yield_day(CropType.CARROT) == 2
        assert first_yield_day(CropType.TOMATO) == 8
        assert first_yield_day(CropType.STRAWBERRY) == 10
        assert first_yield_day(CropType.MELON) == 10

    def test_one_time_bonus_windows(self):
        assert one_time_bonus_start_day(CropType.WHEAT) == 2
        assert one_time_bonus_end_day(CropType.WHEAT) == 4

        assert one_time_bonus_start_day(CropType.CARROT) == 2
        assert one_time_bonus_end_day(CropType.CARROT) == 3

        assert one_time_bonus_start_day(CropType.MELON) == 6
        assert one_time_bonus_end_day(CropType.MELON) == 12

    def test_ongoing_crop_bonus_accessors_return_negative_one(self):
        assert one_time_bonus_start_day(CropType.TOMATO) == -1
        assert one_time_bonus_end_day(CropType.TOMATO) == -1
        assert one_time_bonus_start_day(CropType.STRAWBERRY) == -1
        assert one_time_bonus_end_day(CropType.STRAWBERRY) == -1

    def test_one_time_bonus_window_is_inclusive(self):
        assert one_time_bonus_applies(CropType.WHEAT, 2)
        assert one_time_bonus_applies(CropType.WHEAT, 4)
        assert not one_time_bonus_applies(CropType.WHEAT, 1)
        assert not one_time_bonus_applies(CropType.WHEAT, 5)

    def test_ongoing_crop_does_not_use_one_time_bonus(self):
        assert not one_time_bonus_applies(CropType.TOMATO, 8)

    def test_one_time_watering_bonus(self):
        assert one_time_watering_bonus(
            CropType.WHEAT,
            2,
            watered=False,
            fertilizer_active=False,
        ) == 0

        assert one_time_watering_bonus(
            CropType.WHEAT,
            2,
            watered=True,
            fertilizer_active=False,
        ) == 1

        assert one_time_watering_bonus(
            CropType.WHEAT,
            2,
            watered=True,
            fertilizer_active=True,
        ) == 2

    def test_one_time_yield_without_fertilizer(self):
        assert one_time_yield(
            CropType.WHEAT,
            watered_days=0,
        ) == 1

        assert one_time_yield(
            CropType.WHEAT,
            watered_days=4,
        ) == 5

    def test_one_time_yield_with_fertilized_watering(self):
        assert one_time_yield(
            CropType.WHEAT,
            watered_days=4,
            fertilized_watered_days=2,
        ) == 6

    def test_one_time_yield_is_capped(self):
        assert one_time_yield(
            CropType.WHEAT,
            watered_days=100,
            fertilized_watered_days=100,
        ) == 6

    def test_one_time_yield_rejects_invalid_counts(self):
        with pytest.raises(ValueError):
            one_time_yield(
                CropType.WHEAT,
                watered_days=-1,
            )

        with pytest.raises(ValueError):
            one_time_yield(
                CropType.WHEAT,
                watered_days=1,
                fertilized_watered_days=2,
            )

    def test_one_time_yield_is_not_defined_for_ongoing_crop(self):
        assert one_time_yield(
            CropType.TOMATO,
            watered_days=10,
        ) == 0

    def test_tomato_production_schedule(self):
        assert crop_produces_on_day(CropType.TOMATO, 7) is False
        assert crop_produces_on_day(CropType.TOMATO, 8) is True
        assert crop_produces_on_day(CropType.TOMATO, 9) is True
        assert crop_produces_on_day(CropType.TOMATO, 11) is True
        assert crop_produces_on_day(CropType.TOMATO, 12) is False

    def test_strawberry_production_schedule(self):
        assert crop_produces_on_day(CropType.STRAWBERRY, 9) is False
        assert crop_produces_on_day(CropType.STRAWBERRY, 10) is True
        assert crop_produces_on_day(CropType.STRAWBERRY, 11) is False
        assert crop_produces_on_day(CropType.STRAWBERRY, 12) is True
        assert crop_produces_on_day(CropType.STRAWBERRY, 14) is True
        assert crop_produces_on_day(CropType.STRAWBERRY, 16) is True
        assert crop_produces_on_day(CropType.STRAWBERRY, 18) is False

    def test_ongoing_production_count(self):
        assert ongoing_production_count(CropType.TOMATO, 7) == 0
        assert ongoing_production_count(CropType.TOMATO, 8) == 1
        assert ongoing_production_count(CropType.TOMATO, 11) == 4
        assert ongoing_production_count(CropType.TOMATO, 12) == 4

        assert ongoing_production_count(CropType.STRAWBERRY, 10) == 1
        assert ongoing_production_count(CropType.STRAWBERRY, 16) == 4
        assert ongoing_production_count(CropType.STRAWBERRY, 18) == 4

    def test_ongoing_production_yield(self):
        assert ongoing_production_yield(
            CropType.TOMATO,
            8,
            watered=False,
            fertilizer_active=False,
        ) == 1

        assert ongoing_production_yield(
            CropType.TOMATO,
            8,
            watered=True,
            fertilizer_active=True,
        ) == 2

    def test_ongoing_yield_respects_held_cap(self):
        assert ongoing_production_yield(
            CropType.TOMATO,
            8,
            watered=True,
            fertilizer_active=True,
            current_held_yield=3,
        ) == 1

        assert ongoing_production_yield(
            CropType.TOMATO,
            8,
            watered=True,
            fertilizer_active=True,
            current_held_yield=4,
        ) == 0


# ============================================================================
# Crop decay
# ============================================================================


class TestCropDecay:
    def test_one_time_decay_start(self):
        assert one_time_decay_start_day(CropType.WHEAT) == 5
        assert one_time_decay_start_day(CropType.CARROT) == 4
        assert one_time_decay_start_day(CropType.MELON) == 11

    def test_ongoing_decay_start(self):
        # Tomato: production at 8,9,10,11; decay starts at 12.
        assert ongoing_decay_start_day(CropType.TOMATO) == 12

        # Strawberry: production at 10,12,14,16; decay starts at 17.
        assert ongoing_decay_start_day(CropType.STRAWBERRY) == 17

    def test_decay_start_type_selection(self):
        assert decay_start_day(CropType.WHEAT) == 5
        assert decay_start_day(CropType.TOMATO) == 12

    def test_is_decaying(self):
        assert not is_decaying(CropType.WHEAT, 4)
        assert is_decaying(CropType.WHEAT, 5)

        assert not is_decaying(CropType.TOMATO, 11)
        assert is_decaying(CropType.TOMATO, 12)

    @pytest.mark.parametrize(
        "turns,lost",
        [
            (0, 0),
            (1, 0),
            (2, 1),
            (3, 1),
            (4, 2),
            (5, 2),
            (6, 3),
        ],
    )
    def test_decay_reduction(self, turns, lost):
        assert decay_reduction(
            turns_since_decay_start=turns,
        ) == lost

    def test_negative_decay_elapsed_time_has_no_reduction(self):
        assert decay_reduction(
            turns_since_decay_start=-1,
        ) == 0

    def test_decayed_yield_cannot_be_negative(self):
        assert decayed_yield(
            2,
            turns_since_decay_start=100,
        ) == 0

        assert decayed_yield(
            5,
            turns_since_decay_start=4,
        ) == 3

    def test_becomes_weed_at_zero_yield(self):
        assert becomes_weed(0)
        assert becomes_weed(-1)
        assert not becomes_weed(1)


# ============================================================================
# Farm-hand hiring and spawning
# ============================================================================


class TestFarmHands:
    def test_fibonacci_sequence(self):
        assert [
            fibonacci(n)
            for n in range(1, 9)
        ] == [1, 1, 2, 3, 5, 8, 13, 21]

    def test_fibonacci_rejects_zero_and_negative(self):
        with pytest.raises(ValueError):
            fibonacci(0)

        with pytest.raises(ValueError):
            fibonacci(-1)

    def test_farm_hand_cost_sequence(self):
        assert [
            farm_hand_cost(hires_today=n)
            for n in range(6)
        ] == [1, 1, 2, 3, 5, 8]

    def test_farm_hand_cost_respects_multiplier(self):
        assert farm_hand_cost(
            hires_today=0,
            farm_hand_cost_mult=3,
        ) == 3

        assert farm_hand_cost(
            hires_today=4,
            farm_hand_cost_mult=3,
        ) == 15

    def test_farm_hand_cost_rejects_negative_hires(self):
        with pytest.raises(ValueError):
            farm_hand_cost(hires_today=-1)

    def test_farm_hand_cost_rejects_negative_multiplier(self):
        with pytest.raises(ValueError):
            farm_hand_cost(
                hires_today=0,
                farm_hand_cost_mult=-1,
            )

    def test_spawn_candidates_are_nwse(self):
        assert spawn_candidates_in_preference_order(10) == (
            (4, 4),
            (5, 4),
            (4, 5),
            (5, 5),
        )

    def test_spawn_candidates_scale_with_board(self):
        assert spawn_candidates_in_preference_order(8) == (
            (3, 3),
            (4, 3),
            (3, 4),
            (4, 4),
        )

    def test_first_free_spawn_tile_wins(self):
        candidates = (
            (4, 4),
            (5, 4),
            (4, 5),
            (5, 5),
        )

        occupancy = {
            (4, 4): 1,
            (5, 4): 1,
            (4, 5): 0,
            (5, 5): 0,
        }

        assert select_spawn_tile(candidates, occupancy) == (4, 5)

    def test_least_occupied_tile_wins_when_all_are_occupied(self):
        candidates = (
            (4, 4),
            (5, 4),
            (4, 5),
            (5, 5),
        )

        occupancy = {
            (4, 4): 3,
            (5, 4): 1,
            (4, 5): 2,
            (5, 5): 1,
        }

        assert select_spawn_tile(candidates, occupancy) == (5, 4)

    def test_spawn_ties_preserve_nwse_order(self):
        candidates = (
            (4, 4),
            (5, 4),
            (4, 5),
            (5, 5),
        )

        occupancy = {
            (4, 4): 2,
            (5, 4): 1,
            (4, 5): 3,
            (5, 5): 1,
        }

        assert select_spawn_tile(candidates, occupancy) == (5, 4)

    def test_missing_occupancy_is_zero(self):
        candidates = (
            (4, 4),
            (5, 4),
            (4, 5),
            (5, 5),
        )

        assert select_spawn_tile(
            candidates,
            {(4, 4): 2},
        ) == (5, 4)

    def test_empty_candidates_rejected(self):
        with pytest.raises(ValueError):
            select_spawn_tile((), {})


# ============================================================================
# Town rules
# ============================================================================


class TestTownRules:
    @pytest.mark.parametrize(
        "day,expected",
        [
            (0, False),
            (1, False),
            (2, False),
            (3, True),
            (4, False),
            (5, False),
            (6, True),
            (9, True),
            (24, True),
            (27, True),
        ],
    )
    def test_shop_unlock_schedule(self, day, expected):
        assert shop_unlocks_on_day(day) is expected

    def test_negative_shop_day_rejected(self):
        with pytest.raises(ValueError):
            shop_unlocks_on_day(-1)

    def test_shop_demand_accessor_returns_copy(self):
        demand = shop_demand(TownShopType.BAKERY)

        demand[ObjectType.WHEAT] = 999

        assert shop_demand(
            TownShopType.BAKERY
        )[ObjectType.WHEAT] == 1

    @pytest.mark.parametrize("shop", list(TownShopType))
    def test_every_shop_has_nonempty_demand(self, shop):
        demand = shop_demand(shop)

        assert demand
        assert all(
            isinstance(product, ObjectType)
            for product in demand
        )
        assert all(
            isinstance(quantity, int) and quantity > 0
            for quantity in demand.values()
        )

    def test_unknown_shop_is_rejected(self):
        with pytest.raises(ValueError):
            shop_demand("NOT_A_SHOP")  # type: ignore[arg-type]


# ============================================================================
# Market rules
# ============================================================================


class TestMarketRules:
    def test_price_shape_values(self):
        assert price_shape_value(PriceShape.LINEAR, 10) == 10
        assert price_shape_value(PriceShape.SQUARE, 10) == 100
        assert price_shape_value(PriceShape.SQRT, 9) == pytest.approx(3)
        assert price_shape_value(PriceShape.LOG, 0) == pytest.approx(0)
        assert price_shape_value(PriceShape.LOG10, 0) == pytest.approx(0)

    def test_price_shape_value_rejects_negative_distance(self):
        with pytest.raises(ValueError):
            price_shape_value(PriceShape.LINEAR, -1)

    @pytest.mark.parametrize(
        "product,expected",
        [
            (ObjectType.WHEAT, 25),
            (ObjectType.CARROT, 35),
            (ObjectType.TOMATO, 60),
            (ObjectType.STRAWBERRY, 120),
            (ObjectType.MELON, 250),
            (ObjectType.EGG, 50),
            (ObjectType.MILK, 160),
            (ObjectType.WOOL, 200),
            (ObjectType.FERTILIZER, 100),
        ],
    )
    def test_equilibrium_price_equals_base_price(self, product, expected):
        assert sell_price(product, 10_000) == expected

    def test_wheat_scarcity_curve(self):
        assert sell_price(ObjectType.WHEAT, 9_600) == 45

    def test_wheat_glut_curve(self):
        assert sell_price(ObjectType.WHEAT, 10_400) == 20

    def test_wheat_far_glut_respects_floor(self):
        assert sell_price(ObjectType.WHEAT, 10_800) == 19

    def test_carrot_scarcity_curve(self):
        assert sell_price(ObjectType.CARROT, 9_550) == 42

    def test_carrot_glut_curve(self):
        assert sell_price(ObjectType.CARROT, 10_450) == 10

    def test_carrot_far_glut_respects_floor(self):
        assert sell_price(ObjectType.CARROT, 10_900) == 1

    def test_market_price_floor(self):
        assert market_price(
            base_price=10,
            initial_inventory=100,
            inventory=1000,
            anchor_throughput=10,
            shape=PriceShape.LINEAR,
            target=1.0,
        ) == PRICE_FLOOR

    def test_market_price_rejects_invalid_base_price(self):
        with pytest.raises(ValueError):
            market_price(
                base_price=-1,
                initial_inventory=100,
                inventory=100,
                anchor_throughput=10,
                shape=PriceShape.LINEAR,
                target=1.0,
            )

    def test_market_price_rejects_invalid_anchor(self):
        with pytest.raises(ValueError):
            market_price(
                base_price=10,
                initial_inventory=100,
                inventory=90,
                anchor_throughput=0,
                shape=PriceShape.LINEAR,
                target=1.0,
            )

    def test_market_price_rejects_negative_target(self):
        with pytest.raises(ValueError):
            market_price(
                base_price=10,
                initial_inventory=100,
                inventory=90,
                anchor_throughput=10,
                shape=PriceShape.LINEAR,
                target=-1,
            )

    def test_buyable_products_match_competition(self):
        assert can_buy_product(ObjectType.WHEAT)
        assert can_buy_product(ObjectType.FERTILIZER)

        for product in ObjectType:
            if product not in {
                ObjectType.WHEAT,
                ObjectType.FERTILIZER,
            }:
                assert not can_buy_product(product)

    @pytest.mark.parametrize("product", list(ObjectType))
    def test_all_products_can_be_sold(self, product):
        assert can_sell_product(product)

    def test_buy_price_uses_post_buy_inventory(self):
        inventory_before_buy = 9_999

        assert buy_price(
            ObjectType.WHEAT,
            inventory_before_buy,
        ) == sell_price(
            ObjectType.WHEAT,
            inventory_before_buy,
        )

    def test_sell_price_uses_pre_sell_inventory(self):
        inventory_before_sell = 10_001

        assert sell_price(
            ObjectType.WHEAT,
            inventory_before_sell,
        ) == market_price(
            base_price=25,
            initial_inventory=10_000,
            inventory=10_001,
            anchor_throughput=400,
            shape=PriceShape.LOG,
            target=0.20,
        )


# ============================================================================
# Cross-definition consistency
# ============================================================================


class TestCrossDefinitionConsistency:
    """
    These tests catch drift between separate canonical vocabularies.

    They are especially important because layer_0_reality intentionally
    separates vocabulary from catalogs and rules.
    """

    def test_every_crop_is_a_market_product(self):
        for crop in CropType:
            product = ObjectType[crop.name]
            assert product in MARKET

    def test_every_animal_product_is_a_market_product(self):
        from layer_0_reality.level_2.definitions.animal_catalog import (
            animal_definition,
        )

        for animal in AnimalType:
            assert animal_definition(animal).product in MARKET

    def test_shop_demand_only_references_market_products(self):
        for demand in SHOP_DEMAND.values():
            for product in demand:
                assert product in MARKET

    def test_crop_catalog_and_crop_vocabulary_have_same_members(self):
        assert set(CROPS) == set(CropType)

    def test_animal_catalog_and_animal_vocabulary_have_same_members(self):
        from layer_0_reality.level_2.definitions.animal_catalog import ANIMALS

        assert set(ANIMALS) == set(AnimalType)

    def test_market_catalog_covers_every_object(self):
        assert set(MARKET) == set(ObjectType)