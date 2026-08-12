from ...level_1.definitions.animals import (
    AnimalType,
    StructureType,
)

def required_structure(animal: AnimalType) -> StructureType:
    """
    Return the structure type required to house an animal.

    Canonical mapping from the specification:
        GOOSE → COOP
        COW   → PASTURE
        SHEEP → PASTURE
    """
    if animal is AnimalType.GOOSE:
        return StructureType.COOP

    if animal in (AnimalType.COW, AnimalType.SHEEP):
        return StructureType.PASTURE

    raise ValueError(f"Unrecognised animal type: {animal!r}")
