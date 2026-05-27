from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import ASSET_ID_INPUT_SELECTOR
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import clear_field


def reset_asset_id_field(page: Page) -> None:
    clear_field(page, ASSET_ID_INPUT_SELECTOR)

