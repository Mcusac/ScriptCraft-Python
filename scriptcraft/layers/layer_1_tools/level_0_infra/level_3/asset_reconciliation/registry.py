# ============================================================
# registry.py — detector dispatch contracts
# ============================================================

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    detect_off_campus,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    detect_custodian_changes,
    detect_location_changes,
)

# Detectors invoked via ``run_nodes(merged, MERGED_DETECTORS)``.
MERGED_DETECTORS = {
    "location_changes": detect_location_changes,
    "custodian_changes": detect_custodian_changes,
    "off_campus": detect_off_campus,
}
