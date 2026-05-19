# tests for asset search step

import unittest
from unittest.mock import MagicMock, patch

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.asset_search_step import (
    is_on_asset_update_page,
    wait_for_asset_update_page,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.errors import (
    AssetNotFoundError,
)


class TestIsOnAssetUpdatePage(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "asset_search_step.ba.selector_exists"
    )
    def test_true_when_date_field_present(
        self,
        mock_exists: MagicMock,
    ) -> None:
        page = MagicMock()

        def exists(_page, selector: str) -> bool:
            return selector == c.DATE_OF_TRANSFER_INPUT_SELECTOR

        mock_exists.side_effect = exists
        self.assertTrue(is_on_asset_update_page(page))


class TestWaitForAssetUpdatePage(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "asset_search_step.is_on_asset_update_page"
    )
    def test_raises_when_update_page_never_appears(
        self,
        mock_on_update: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_on_update.return_value = False

        with self.assertRaises(AssetNotFoundError):
            wait_for_asset_update_page(page, timeout_ms=500)

        self.assertGreater(page.wait_for_timeout.call_count, 0)


class TestPrepareSearchForNextRow(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "asset_update_page_workflow.ba.safe_wait"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "asset_update_page_workflow.ba.clear_field"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "asset_update_page_workflow.ba.dismiss_message_modals"
    )
    def test_clears_tag_and_asset_id(
        self,
        mock_dismiss: MagicMock,
        mock_clear: MagicMock,
        _mock_wait: MagicMock,
    ) -> None:
        from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.asset_update_page_workflow import (
            prepare_search_for_next_row,
        )

        page = MagicMock()
        prepare_search_for_next_row(page)

        mock_dismiss.assert_called_once_with(page)
        cleared = {call.args[1] for call in mock_clear.call_args_list}
        self.assertIn(c.TAG_NUMBER_INPUT_SELECTOR, cleared)
        self.assertIn(c.ASSET_ID_INPUT_SELECTOR, cleared)


if __name__ == "__main__":
    unittest.main()
