# asset_search_step.py — LEVEL_1

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    poll_until,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    AssetNotFoundError,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    reset_asset_id_field,
)

UPDATE_PAGE_POLL_MS = 200
UPDATE_PAGE_WAIT_MS = 15_000


def is_on_asset_update_page(page: Page) -> bool:
    return ba.selector_exists(
        page,
        c.DATE_OF_TRANSFER_INPUT_SELECTOR,
    ) or ba.selector_exists(page, c.UPDATE_THIS_ASSET_BUTTON_SELECTOR)


def wait_for_asset_update_page(
    page: Page,
    timeout_ms: int = UPDATE_PAGE_WAIT_MS,
) -> None:
    """Wait until search navigates to the asset update form."""
    if poll_until(
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

    ba.fill_input(page, c.TAG_NUMBER_INPUT_SELECTOR, tag_number)
    ba.click(page, c.SEARCH_BUTTON_SELECTOR)

    try:
        page.wait_for_load_state("domcontentloaded", timeout=15_000)
    except Exception:
        pass

    ba.click_ok_if_present(page)

    try:
        wait_for_asset_update_page(page, timeout_ms=UPDATE_PAGE_WAIT_MS)
    except AssetNotFoundError as exc:
        raise AssetNotFoundError(
            f"Tag {tag_number} — search did not open update page"
        ) from exc
