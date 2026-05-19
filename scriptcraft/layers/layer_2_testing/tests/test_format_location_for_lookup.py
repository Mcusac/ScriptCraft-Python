# tests for format_location_for_lookup

import unittest

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.level_0.browser_actions import (
    format_location_for_lookup,
)


class TestFormatLocationForLookup(unittest.TestCase):

    def test_single_space_between_building_and_room(self) -> None:
        self.assertEqual(format_location_for_lookup("PCC 618"), "PCC  618")

    def test_nbsp_between_building_and_room(self) -> None:
        self.assertEqual(format_location_for_lookup("CBH\u00a0220"), "CBH  220")

    def test_already_double_space_unchanged(self) -> None:
        self.assertEqual(format_location_for_lookup("PCC  618"), "PCC  618")

    def test_pcfr_style(self) -> None:
        self.assertEqual(format_location_for_lookup("PCCFR M"), "PCCFR  M")

    def test_single_token_unchanged(self) -> None:
        self.assertEqual(format_location_for_lookup("PCC"), "PCC")

    def test_fifth_floor_room_code(self) -> None:
        self.assertEqual(format_location_for_lookup("PCC 595B"), "PCC  595B")


if __name__ == "__main__":
    unittest.main()
