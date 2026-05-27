# asset_search_step.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    click,
    fill_input,
    selector_exists,
    AssetNotFoundError,
    DATE_OF_TRANSFER_INPUT_SELECTOR,
    UPDATE_THIS_ASSET_BUTTON_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    TAG_NUMBER_INPUT_SELECTOR,
    wait_until_page_condition,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    reset_asset_id_field,
    click_ok_if_present,
)


UPDATE_PAGE_POLL_MS = 200
UPDATE_PAGE_WAIT_MS = 15_000


def is_on_asset_update_page(page: Page) -> bool:
    return selector_exists(
        page,
        DATE_OF_TRANSFER_INPUT_SELECTOR,
    ) or selector_exists(page, UPDATE_THIS_ASSET_BUTTON_SELECTOR)


def wait_for_asset_update_page(
    page: Page,
    timeout_ms: int = UPDATE_PAGE_WAIT_MS,
) -> None:
    """Wait until search navigates to the asset update form."""
    if wait_until_page_condition(
        page,
        lambda: is_on_asset_update_page(page),
        timeout_ms=timeout_ms,
        poll_ms=UPDATE_PAGE_POLL_MS,
    ):
        return

    raise AssetNotFoundError(
        "Search did not open the asset update page "
        f"(timeout {timeout_ms}ms)"
    )


def execute_asset_search_step(
    page: Page,
    tag_number: str,
    *,
    clear_asset_id: bool = False,
) -> None:
    """
    Executes ONLY asset search step.
    When clear_asset_id is True, blanks GBAM_SRCH_VW_ASSET_ID before tag search.
    """
    if clear_asset_id:
        reset_asset_id_field(page)

    fill_input(page, TAG_NUMBER_INPUT_SELECTOR, tag_number)
    click(page, SEARCH_BUTTON_SELECTOR)

    try:
        page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception:
        pass

    click_ok_if_present(page)

    try:
        wait_for_asset_update_page(page, timeout_ms=UPDATE_PAGE_WAIT_MS)
    except AssetNotFoundError as exc:
        raise AssetNotFoundError(
            f"Tag {tag_number} — search did not open update page"
        ) from exc
