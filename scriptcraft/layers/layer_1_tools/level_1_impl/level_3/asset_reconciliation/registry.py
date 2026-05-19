# ============================================================
# registry.py — full DAG detector registry (single contract)
# ============================================================

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    detect_off_campus,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    detect_location_changes,
    detect_custodian_changes,
)


DETECTORS = {
    "location_changes": detect_location_changes,
    "custodian_changes": detect_custodian_changes,
    "off_campus": detect_off_campus,
}