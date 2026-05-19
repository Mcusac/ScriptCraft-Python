# offsite_workflow.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    load_authorizer_name,
)


def is_offsite_location(location_code: str) -> bool:
    """
    True when location is PCCFR 5FE (off-campus storage).
    """
    formatted = ba.format_location_for_lookup(location_code)
    normalized = ba.normalize_lookup_text(formatted)
    building, _, room = normalized.partition(" ")

    return (
        building.upper() == c.OFFSITE_LOCATION_BUILDING.upper()
        and room.upper() == c.OFFSITE_LOCATION_ROOM.upper()
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
    ba.set_checkbox_checked(page, c.OFFSITE_CHECKBOX_SELECTOR, offsite)

    authorizer_name = load_authorizer_name()

    if authorizer_name:
        ba.fill_input(page, c.AUTHORIZED_BY_NAME_INPUT_SELECTOR, authorizer_name)
    else:
        print(
            "[WARN] AUTHORIZED_BY_NAME not set in credentials.py "
            "— skipping Authorized By fill"
        )
