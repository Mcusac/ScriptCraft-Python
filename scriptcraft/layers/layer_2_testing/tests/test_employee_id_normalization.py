# tests for normalize_employee_id

import unittest

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import normalize_employee_id
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    employee_id_from_row as _employee_id_from_row,
    optional_employee_id_from_row as _optional_employee_id_from_row,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    EMPLOYEE_ID_ROW_KEYS,
)


def employee_id_from_row(row: dict) -> str:
    return _employee_id_from_row(row, EMPLOYEE_ID_ROW_KEYS)


def optional_employee_id_from_row(row: dict) -> str | None:
    return _optional_employee_id_from_row(row, EMPLOYEE_ID_ROW_KEYS)


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

    @unittest.skipUnless(
        __import__("pathlib").Path(__file__).resolve().parents[5]
        .joinpath("workspace", "input", "location_changes.csv").is_file(),
        "workspace/input CSV fixtures required for integration test",
    )
    def test_custodian_ids_loaded_without_float_suffix(self) -> None:
        from pathlib import Path

        from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
            load_updater_dataset,
        )

        root = Path(__file__).resolve().parents[5]
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
