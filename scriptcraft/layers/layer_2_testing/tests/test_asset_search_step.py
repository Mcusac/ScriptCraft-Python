# tests for asset search step

import unittest
from unittest.mock import MagicMock, patch

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    AssetNotFoundError,
    DATE_OF_TRANSFER_INPUT_SELECTOR,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    is_on_asset_update_page,
    wait_for_asset_update_page,
)

_INFRA_L4 = "scriptcraft.layers.layer_1_tools.level_0_infra.level_4.asset_updater"


class TestIsOnAssetUpdatePage(unittest.TestCase):

    @patch(f"{_INFRA_L4}.asset_search_step.selector_exists")
    def test_true_when_date_field_present(
        self,
        mock_exists: MagicMock,
    ) -> None:
        page = MagicMock()

        def exists(_page, selector: str) -> bool:
            return selector == DATE_OF_TRANSFER_INPUT_SELECTOR

        mock_exists.side_effect = exists
        self.assertTrue(is_on_asset_update_page(page))


class TestWaitForAssetUpdatePage(unittest.TestCase):

    @patch(f"{_INFRA_L4}.asset_search_step.is_on_asset_update_page")
    def test_raises_when_update_page_never_appears(
        self,
        mock_on_update: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_on_update.return_value = False

        with self.assertRaises(AssetNotFoundError):
            wait_for_asset_update_page(page, timeout_ms=500)

        self.assertGreater(page.wait_for_timeout.call_count, 0)


_INFRA_L3 = "scriptcraft.layers.layer_1_tools.level_0_infra.level_3.asset_updater"


class TestPrepareSearchForNextRow(unittest.TestCase):

    @patch(f"{_INFRA_L3}.search_navigation.safe_wait")
    @patch(f"{_INFRA_L3}.search_navigation.clear_field")
    @patch(f"{_INFRA_L3}.search_navigation.dismiss_message_modals")
    def test_clears_tag_and_asset_id(
        self,
        mock_dismiss: MagicMock,
        mock_clear: MagicMock,
        mock_wait: MagicMock,
    ) -> None:
        from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
            prepare_search_for_next_row,
        )

        page = MagicMock()
        prepare_search_for_next_row(page)

        mock_dismiss.assert_called_once_with(page)
        self.assertEqual(mock_clear.call_count, 2)
        mock_wait.assert_called()
