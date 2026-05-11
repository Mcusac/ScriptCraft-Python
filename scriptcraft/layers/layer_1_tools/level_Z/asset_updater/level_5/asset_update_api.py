# asset_update_api.py — LEVEL_5

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.session_manager import (
    open_asset_updater,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_4.loop_runner import (
    run_asset_update_loop,
)


def run_asset_update(page: Page, url: str, dataset) -> None:
    """
    Single entrypoint for Level_2 system.
    """

    open_asset_updater(page, url)
    run_asset_update_loop(page, dataset)