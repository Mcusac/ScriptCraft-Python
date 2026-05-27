from scriptcraft.layers.layer_0_core.level_1.runtime.mode_execution import (
    ModeRegistry,
    get_mode,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    domain_old_vs_new_comparison_mode,
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    release_consistency_comparison_mode,
    rhq_comparison_mode,
    standard_comparison_mode,
)

MODE_REGISTRY = ModeRegistry()
MODE_REGISTRY.register("rhq", rhq_comparison_mode)
MODE_REGISTRY.register("standard", standard_comparison_mode)
MODE_REGISTRY.register("release", release_consistency_comparison_mode)
MODE_REGISTRY.register("release_consistency", release_consistency_comparison_mode)
MODE_REGISTRY.register("domain_old_vs_new", domain_old_vs_new_comparison_mode)


def get_mode_handler(mode_name: str):
    return get_mode(MODE_REGISTRY, mode_name)


get_mode = get_mode_handler
