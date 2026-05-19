# ============================================================
# loop_runner.py — LEVEL_4
# ============================================================

from typing import Any
from typing import Dict
from typing import List

from playwright.sync_api import Page

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    set_business_unit,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_3.asset_updater import (
    classify_update_row,
    execute_asset_update_row,
    tag_number_from_row,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_4 import (
    recover_to_asset_search,
)



def run_asset_update_loop(
    page: Page,
    dataset: List[Dict[str, Any]],
) -> None:
    """
    Controls dataset iteration and failure isolation.
    """

    set_business_unit(page)

    total_rows = len(dataset)

    print(
        f"\nStarting asset update loop "
        f"({total_rows} rows)..."
    )

    for idx, row in enumerate(dataset, start=1):

        try:
            tag_number = tag_number_from_row(row)
        except KeyError:
            tag_number = "UNKNOWN"

        try:
            update_kind = classify_update_row(row)
        except Exception:
            update_kind = "unknown"

        print(
            f"\n[{idx}/{total_rows}] "
            f"Processing tag: {tag_number} ({update_kind})"
        )

        try:

            execute_asset_update_row(
                page,
                row,
                clear_asset_id=(idx > 1),
            )

            print(
                f"[SUCCESS] "
                f"Tag {tag_number}"
            )

        except Exception as e:

            print(
                f"[ERROR] Row failed "
                f"(Tag={tag_number}): {e}"
            )

            try:
                if recover_to_asset_search(page):
                    set_business_unit(page)
                    print(
                        f"[RECOVERED] Ready for next tag "
                        f"after failure on {tag_number}"
                    )
                else:
                    print(
                        f"[WARN] Recovery incomplete; "
                        f"next row may fail"
                    )
            except Exception as recovery_error:
                print(
                    f"[WARN] Recovery failed: {recovery_error}"
                )

            continue