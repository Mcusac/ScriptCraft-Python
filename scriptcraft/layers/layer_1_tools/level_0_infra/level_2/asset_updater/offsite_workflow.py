# offsite_workflow.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    fill_input,
    format_location_for_lookup,
    normalize_lookup_text,
    set_checkbox_checked,
    OFFSITE_LOCATION_BUILDING,
    OFFSITE_LOCATION_ROOM,
    OFFSITE_CHECKBOX_SELECTOR,
    AUTHORIZED_BY_NAME_INPUT_SELECTOR,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    load_authorizer_name,
)


def is_offsite_location(location_code: str) -> bool:
    """
    True when location is PCCFR 5FE (off-campus storage).
    """
    formatted = format_location_for_lookup(location_code)
    normalized = normalize_lookup_text(formatted)
    building, _, room = normalized.partition(" ")

    return (
        building.upper() == OFFSITE_LOCATION_BUILDING.upper()
        and room.upper() == OFFSITE_LOCATION_ROOM.upper()
    )


def apply_offsite_and_authorization(
    page: Page,
    location_code: str,
) -> None:
    """
    Set offsite checkbox from resolved location; fill Authorized By when configured.
    Run after location/custodian lookups, before Update this Asset.
    """
    offsite = is_offsite_location(location_code)
    set_checkbox_checked(page, OFFSITE_CHECKBOX_SELECTOR, offsite)

    authorizer_name = load_authorizer_name()

    if authorizer_name:
        fill_input(page, AUTHORIZED_BY_NAME_INPUT_SELECTOR, authorizer_name)
    else:
        print(
            "[WARN] AUTHORIZED_BY_NAME not set in credentials.py "
            "— skipping Authorized By fill"
        )
