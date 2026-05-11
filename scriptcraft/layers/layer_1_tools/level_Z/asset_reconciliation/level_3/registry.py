# ============================================================
# registry.py — full DAG detector registry (single contract)
# ============================================================

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.detection.off_campus import (
    detect_off_campus,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.detection.duplicates import (
    detect_form_duplicates,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.detection.missing_from_form import (
    detect_missing_from_form,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_1.detection.only_in_form import (
    detect_only_in_form,
)

from scriptcraft.layers.layer_1_tools.level_Z.asset_reconciliation.level_2.change_detector import (
    detect_location_changes,
    detect_custodian_changes,
)


DETECTORS = {
    "duplicates": detect_form_duplicates,
    "missing_from_form": detect_missing_from_form,
    "only_in_form": detect_only_in_form,
    "location_changes": detect_location_changes,
    "custodian_changes": detect_custodian_changes,
    "off_campus": detect_off_campus,
}