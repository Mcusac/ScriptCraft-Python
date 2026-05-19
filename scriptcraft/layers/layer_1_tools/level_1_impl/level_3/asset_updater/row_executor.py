# ============================================================
# row_executor.py — LEVEL_3
# ============================================================

from typing import Any
from typing import Dict
from typing import Iterable
from typing import Literal

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.asset_updater_row_values import (
    is_present,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    constants as c,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    execute_asset_post_update_step,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    execute_asset_search_step,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    execute_asset_update_step,
)

UpdateKind = Literal["both", "location_only", "custodian_only"]


def _optional_value_from_row(
    row: Dict[str, Any],
    keys: Iterable[str],
) -> str | None:

    for key in keys:

        value = row.get(key)

        if is_present(value):
            return str(value).strip()

    return None


def _value_from_row(
    row: Dict[str, Any],
    keys: Iterable[str],
    label: str,
) -> str:

    value = _optional_value_from_row(row, keys)

    if value is not None:
        return value

    raise KeyError(
        f"Row missing {label}. "
        f"Expected one of: {tuple(keys)}"
    )


def normalize_tag_number(digits: str) -> str:
    """
    Format tag digits for PeopleSoft search.
    Six-digit tags starting with 3 stay as-is; shorter tags pad to TAG_PAD_WIDTH.
    """
    if len(digits) == 6 and digits[0] == "3":
        return digits

    if len(digits) >= c.TAG_PAD_WIDTH:
        return digits

    return digits.zfill(c.TAG_PAD_WIDTH)


def tag_number_from_row(row: Dict[str, Any]) -> str:
    """
    Resolve tag from row and pad to PeopleSoft width.
    """

    raw = _value_from_row(
        row,
        c.TAG_NUMBER_ROW_KEYS,
        "tag identifier",
    )

    if raw.endswith(".0"):
        raw = raw[:-2]

    digits = "".join(ch for ch in raw if ch.isdigit())

    if digits:
        return normalize_tag_number(digits)

    return raw.zfill(c.TAG_PAD_WIDTH)


def normalize_employee_id(raw: str) -> str:
    """
    Strip pandas float artifacts and non-digits from employee IDs.
    """
    text = str(raw).strip()

    if text.endswith(".0"):
        text = text[:-2]

    digits = "".join(ch for ch in text if ch.isdigit())

    return digits if digits else text


def optional_location_code_from_row(row: Dict[str, Any]) -> str | None:
    """
    new_location from CSV, or None if this row is custodian-only.
    """

    return _optional_value_from_row(row, c.LOCATION_CODE_ROW_KEYS)


def optional_employee_id_from_row(row: Dict[str, Any]) -> str | None:
    """
    new_custodian_id from CSV, or None if this row is location-only.
    """

    raw = _optional_value_from_row(row, c.EMPLOYEE_ID_ROW_KEYS)

    if raw is None:
        return None

    return normalize_employee_id(raw)


def location_code_from_row(row: Dict[str, Any]) -> str:
    """
    Location code for PeopleSoft lookup (reconciliation: new_location).
    """

    return _value_from_row(
        row,
        c.LOCATION_CODE_ROW_KEYS,
        "location code",
    )


def employee_id_from_row(row: Dict[str, Any]) -> str:
    """
    Employee ID for custodian lookup (reconciliation: new_custodian_id).
    """

    raw = _value_from_row(
        row,
        c.EMPLOYEE_ID_ROW_KEYS,
        "employee id",
    )

    return normalize_employee_id(raw)


def classify_update_row(row: Dict[str, Any]) -> UpdateKind:
    """
    both | location_only | custodian_only
    """

    has_location = optional_location_code_from_row(row) is not None
    has_custodian = optional_employee_id_from_row(row) is not None

    if has_location and has_custodian:
        return "both"

    if has_location:
        return "location_only"

    return "custodian_only"


def execute_asset_update_row(
    page: Page,
    row: Dict[str, Any],
    *,
    clear_asset_id: bool = False,
) -> None:
    """
    DAG-style row execution:
    SEARCH → UPDATE → SUBMIT
    """

    tag_number = tag_number_from_row(row)

    execute_asset_search_step(
        page,
        tag_number,
        clear_asset_id=clear_asset_id,
    )

    execute_asset_update_step(
        page,
        location_code=optional_location_code_from_row(row),
        employee_id=optional_employee_id_from_row(row),
    )

    execute_asset_post_update_step(page)
