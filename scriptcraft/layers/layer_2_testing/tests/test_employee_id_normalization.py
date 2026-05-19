# tests for normalize_employee_id

import unittest

from scriptcraft.layers.layer_1_tools.level_1_impl.level_3.asset_updater import (
    employee_id_from_row,
    load_updater_dataset,
    normalize_employee_id,
    optional_employee_id_from_row,
)


class TestNormalizeEmployeeId(unittest.TestCase):

    def test_strips_float_suffix(self) -> None:
        self.assertEqual(normalize_employee_id("11991079.0"), "11991079")

    def test_plain_digits_unchanged(self) -> None:
        self.assertEqual(normalize_employee_id("11991079"), "11991079")

    def test_float_str_conversion(self) -> None:
        self.assertEqual(normalize_employee_id(str(11991079.0)), "11991079")

    def test_row_with_float_like_string(self) -> None:
        row = {"tag": "00041076", "new_custodian_id": "11991079.0"}
        self.assertEqual(optional_employee_id_from_row(row), "11991079")
        self.assertEqual(employee_id_from_row(row), "11991079")


class TestLoadUpdaterDatasetEmployeeIds(unittest.TestCase):

    def test_custodian_ids_loaded_without_float_suffix(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[9]
        records = load_updater_dataset(
            root / "workspace/input/location_changes.csv",
            root / "workspace/input/custodian_changes.csv",
            log_summary=False,
        )
        row = next(r for r in records if r.get("tag") == "00041076")
        emp = optional_employee_id_from_row(row)
        self.assertEqual(emp, "11991079")
        self.assertNotIn(".0", emp or "")


if __name__ == "__main__":
    unittest.main()
