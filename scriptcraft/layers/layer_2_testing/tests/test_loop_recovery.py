# tests for loop recovery helpers

import unittest
from unittest.mock import MagicMock, patch

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    browser_actions as ba,
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1.asset_updater.loop_recovery_workflow import (
    is_on_asset_search_page,
    recover_to_asset_search,
    wait_for_asset_search_page,
)


class TestFrameHelpers(unittest.TestCase):

    def test_ptmod_frame_detection(self) -> None:
        frame = MagicMock()
        frame.name = "ptModFrame_0"
        frame.url = ""
        self.assertTrue(ba._is_ptmod_frame(frame))

        frame.name = ""
        frame.url = "https://example.com/ptModFrame/iscript"
        self.assertTrue(ba._is_ptmod_frame(frame))

        frame.name = "main"
        frame.url = "https://example.com/"
        self.assertFalse(ba._is_ptmod_frame(frame))

    def test_open_lookup_modal_requires_ptmod_and_anchor(self) -> None:
        frame = MagicMock()
        frame.name = "ptModFrame_0"
        frame.url = ""
        frame.query_selector.return_value = MagicMock()
        self.assertTrue(
            ba.is_open_lookup_modal_frame(frame),
        )

        frame.name = "main"
        self.assertFalse(ba.is_open_lookup_modal_frame(frame))


class TestIsOnAssetSearchPage(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.selector_exists"
    )
    def test_false_when_update_submit_visible(
        self,
        mock_exists: MagicMock,
    ) -> None:
        page = MagicMock()

        def exists(_page, selector: str) -> bool:
            return selector == c.UPDATE_THIS_ASSET_BUTTON_SELECTOR

        mock_exists.side_effect = exists
        self.assertFalse(is_on_asset_search_page(page))

    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.selector_exists"
    )
    def test_true_when_search_fields_present(
        self,
        mock_exists: MagicMock,
    ) -> None:
        page = MagicMock()
        search_selectors = {
            c.TAG_NUMBER_INPUT_SELECTOR,
            c.BUSINESS_UNIT_INPUT_SELECTOR,
            c.SEARCH_BUTTON_SELECTOR,
        }

        def exists(_page, selector: str) -> bool:
            return selector in search_selectors

        mock_exists.side_effect = exists
        self.assertTrue(is_on_asset_search_page(page))


class TestWaitForAssetSearchPage(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.is_on_asset_search_page"
    )
    def test_polls_until_ready(
        self,
        mock_on_search: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_on_search.side_effect = [False, False, True]

        self.assertTrue(wait_for_asset_search_page(page, timeout_ms=5_000))

        self.assertEqual(mock_on_search.call_count, 3)
        self.assertEqual(page.wait_for_timeout.call_count, 2)


class TestRecoverToAssetSearch(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.prepare_search_for_next_row"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.wait_for_asset_search_page"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.click_ok_if_present"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.selector_exists"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow._dismiss_lookup_modals"
    )
    def test_returns_true_without_goto_when_poll_succeeds(
        self,
        _mock_dismiss: MagicMock,
        mock_exists: MagicMock,
        _mock_ok: MagicMock,
        mock_wait: MagicMock,
        mock_prepare: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_exists.return_value = True
        mock_wait.return_value = True

        self.assertTrue(recover_to_asset_search(page))

        mock_prepare.assert_called_once_with(page)
        page.goto.assert_not_called()

    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow._try_goto_asset_search"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.wait_for_asset_search_page"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.return_to_search_after_failure"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.click_ok_if_present"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.selector_exists"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow._dismiss_lookup_modals"
    )
    def test_no_goto_when_return_button_still_visible(
        self,
        _mock_dismiss: MagicMock,
        mock_exists: MagicMock,
        _mock_ok: MagicMock,
        mock_return: MagicMock,
        mock_wait: MagicMock,
        mock_goto: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_exists.return_value = True
        mock_wait.return_value = False

        self.assertFalse(recover_to_asset_search(page))

        mock_return.assert_called_once_with(page)
        mock_goto.assert_not_called()
        page.goto.assert_not_called()

    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.prepare_search_for_next_row"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.wait_for_asset_search_page"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.return_to_search_after_failure"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.click_ok_if_present"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow.ba.selector_exists"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1."
        "asset_updater.loop_recovery_workflow._dismiss_lookup_modals"
    )
    def test_uses_fast_return_to_search_path(
        self,
        _mock_dismiss: MagicMock,
        mock_exists: MagicMock,
        _mock_ok: MagicMock,
        mock_return: MagicMock,
        mock_wait: MagicMock,
        mock_prepare: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_exists.return_value = True
        mock_wait.return_value = True

        recover_to_asset_search(page)

        mock_return.assert_called_once_with(page)
        mock_prepare.assert_called_once_with(page)


if __name__ == "__main__":
    unittest.main()
