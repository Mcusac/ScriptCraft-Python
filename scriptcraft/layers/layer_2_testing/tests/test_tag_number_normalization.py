# tests for normalize_tag_number / tag_number_from_row

import unittest

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    normalize_tag_number,
    tag_number_from_row,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.asset_updater.constants import (
    TAG_NUMBER_ROW_KEYS,
    TAG_PAD_WIDTH,
)


def _tag_from_row(row: dict) -> str:
    return tag_number_from_row(row, TAG_NUMBER_ROW_KEYS, pad_width=TAG_PAD_WIDTH)


class TestNormalizeTagNumber(unittest.TestCase):

    def test_six_digit_tag_starting_with_three_unchanged(self) -> None:
        self.assertEqual(normalize_tag_number("302382"), "302382")

    def test_eight_digit_tag_with_leading_zeros_unchanged(self) -> None:
        self.assertEqual(normalize_tag_number("00041159"), "00041159")

    def test_short_legacy_tag_pads_to_eight(self) -> None:
        self.assertEqual(normalize_tag_number("47072"), "00047072")

    def test_five_digit_non_three_prefix_pads(self) -> None:
        self.assertEqual(normalize_tag_number("41159"), "00041159")


class TestTagNumberFromRow(unittest.TestCase):

    def test_row_six_digit_tag(self) -> None:
        row = {"tag": "302382"}
        self.assertEqual(_tag_from_row(row), "302382")

    def test_row_float_string_tag(self) -> None:
        row = {"tag": "302382.0"}
        self.assertEqual(_tag_from_row(row), "302382")

    def test_row_eight_digit_tag(self) -> None:
        row = {"tag": "00041159"}
        self.assertEqual(_tag_from_row(row), "00041159")

    def test_row_short_tag(self) -> None:
        row = {"tag": "47072"}
        self.assertEqual(_tag_from_row(row), "00047072")


if __name__ == "__main__":
    unittest.main()
