from types import MappingProxyType

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.crops import CropDefinition, CropType, YieldType


CROPS: MappingProxyType = MappingProxyType({
    CropType.WHEAT: CropDefinition(
        name="Wheat",
        seed_cost=10,
        time_to_first_yield=2,
        time_to_max_yield=4,
        max_yield=6,
        action_cost=1,
        yield_type=YieldType.ONE_TIME,
        bonus_start_day=2,
        bonus_end_day=4,
    ),

    CropType.CARROT: CropDefinition(
        name="Carrot",
        seed_cost=20,
        time_to_first_yield=2,
        time_to_max_yield=3,
        max_yield=4,
        action_cost=1,
        yield_type=YieldType.ONE_TIME,
        bonus_start_day=2,
        bonus_end_day=3,
    ),

    CropType.TOMATO: CropDefinition(
        name="Tomato",
        seed_cost=50,
        time_to_first_yield=8,
        time_to_max_yield=11,
        max_yield=4,
        action_cost=1,
        yield_type=YieldType.ONGOING,
        bonus_start_day=8,
        bonus_end_day=11,
        production_interval=1,
    ),

    CropType.STRAWBERRY: CropDefinition(
        name="Strawberry",
        seed_cost=100,
        time_to_first_yield=10,
        time_to_max_yield=16,
        max_yield=4,
        action_cost=1,
        yield_type=YieldType.ONGOING,
        bonus_start_day=10,
        bonus_end_day=16,
        production_interval=2,
    ),

    CropType.MELON: CropDefinition(
        name="Melon",
        seed_cost=80,
        time_to_first_yield=10,
        time_to_max_yield=10,
        max_yield=6,
        action_cost=1,
        yield_type=YieldType.ONE_TIME,
        bonus_start_day=6,
        bonus_end_day=12,
    ),
})


def crop_definition(crop: CropType) -> CropDefinition:
    """Return the immutable definition for a crop."""
    return CROPS[crop]