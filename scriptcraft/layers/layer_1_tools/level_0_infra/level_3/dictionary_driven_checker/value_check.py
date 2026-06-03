"""Per-value date format validation (tools emoji wrapper)."""

from typing import Any, Optional

from scriptcraft.layers.layer_0_core.level_0 import matches_date_format

from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import get_status_emoji


def date_format_error_message(value: Any, expected_format: str) -> Optional[str]:
    """Return an error message when a single value fails format compliance."""
    if value is None or (isinstance(value, float) and str(value) == "nan"):
        return None
    if matches_date_format(value, expected_format):
        return None
    return (
        f"{get_status_emoji('invalid')} Invalid date format "
        f"(expected: {expected_format})"
    )
