from scriptcraft.layers.layer_0_core.level_1.runtime.mode_execution import (
    ModeCallable,
    ModeRegistry,
    get_mode as resolve_registered_mode,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    domain_old_vs_new_comparison_mode,
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


def get_mode(mode_name: str) -> ModeCallable:
    return resolve_registered_mode(MODE_REGISTRY, mode_name)
