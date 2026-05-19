# tests for offsite workflow

import unittest
from unittest.mock import MagicMock, patch

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0 import (
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1.offsite_workflow import (
    apply_offsite_and_authorization,
    is_offsite_location,
)


class TestIsOffsiteLocation(unittest.TestCase):

    def test_pccfr_5fe_double_space(self) -> None:
        self.assertTrue(is_offsite_location("PCCFR  5FE"))

    def test_pccfr_5fe_single_space(self) -> None:
        self.assertTrue(is_offsite_location("PCCFR 5FE"))

    def test_on_campus_locations_false(self) -> None:
        self.assertFalse(is_offsite_location("PCC  618"))
        self.assertFalse(is_offsite_location("CBH  220"))


class TestApplyOffsiteAndAuthorization(unittest.TestCase):

    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.load_authorizer_name"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.ba.fill_input"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.ba.set_checkbox_checked"
    )
    def test_offsite_checked_for_pccfr_5fe(
        self,
        mock_checkbox: MagicMock,
        mock_fill: MagicMock,
        mock_name: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_name.return_value = "Jane Doe"

        apply_offsite_and_authorization(page, "PCCFR  5FE")

        mock_checkbox.assert_called_once_with(
            page,
            c.OFFSITE_CHECKBOX_SELECTOR,
            True,
        )
        mock_fill.assert_called_once_with(
            page,
            c.AUTHORIZED_BY_NAME_INPUT_SELECTOR,
            "Jane Doe",
        )

    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.load_authorizer_name"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.ba.fill_input"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.ba.set_checkbox_checked"
    )
    def test_offsite_unchecked_for_on_campus(
        self,
        mock_checkbox: MagicMock,
        mock_fill: MagicMock,
        mock_name: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_name.return_value = "Jane Doe"

        apply_offsite_and_authorization(page, "PCC  618")

        mock_checkbox.assert_called_once_with(
            page,
            c.OFFSITE_CHECKBOX_SELECTOR,
            False,
        )

    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.load_authorizer_name"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.ba.fill_input"
    )
    @patch(
        "scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_1."
        "offsite_workflow.ba.set_checkbox_checked"
    )
    def test_skips_name_fill_when_not_configured(
        self,
        mock_checkbox: MagicMock,
        mock_fill: MagicMock,
        mock_name: MagicMock,
    ) -> None:
        page = MagicMock()
        mock_name.return_value = None

        apply_offsite_and_authorization(page, "PCC  618")

        mock_fill.assert_not_called()
        mock_checkbox.assert_called_once()


if __name__ == "__main__":
    unittest.main()
