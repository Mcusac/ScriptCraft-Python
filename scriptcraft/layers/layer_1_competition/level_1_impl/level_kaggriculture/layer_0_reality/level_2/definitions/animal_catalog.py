from types import MappingProxyType

from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_0.definitions.objects import ObjectType
from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_0_reality.level_1.definitions.animals import AnimalDefinition, AnimalType

ANIMALS: MappingProxyType = MappingProxyType({
    AnimalType.GOOSE: AnimalDefinition(
        name="Goose",
        purchase_cost=300,
        product=ObjectType.EGG,
        time_to_first_yield=4,
        production_interval=1,
        max_held=4,
        action_cost=1,
    ),

    AnimalType.COW: AnimalDefinition(
        name="Cow",
        purchase_cost=400,
        product=ObjectType.MILK,
        time_to_first_yield=8,
        production_interval=2,
        max_held=6,
        action_cost=1,
    ),

    AnimalType.SHEEP: AnimalDefinition(
        name="Sheep",
        purchase_cost=500,
        product=ObjectType.WOOL,
        time_to_first_yield=6,
        production_interval=3,
        max_held=6,
        action_cost=1,
    ),
})


def animal_definition(animal: AnimalType) -> AnimalDefinition:
    """Return the immutable definition for an animal."""
    return ANIMALS[animal]