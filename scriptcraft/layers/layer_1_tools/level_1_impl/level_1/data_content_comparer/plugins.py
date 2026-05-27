from scriptcraft.layers.layer_0_core.level_1 import ModeRegistry, get_mode as resolve_mode

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    domain_old_vs_new_comparison_mode,
    rhq_comparison_mode,
    run_comparison,
    standard_comparison_mode,
)

MODE_REGISTRY = ModeRegistry()
MODE_REGISTRY.register("rhq", rhq_comparison_mode)
MODE_REGISTRY.register("standard", standard_comparison_mode)
MODE_REGISTRY.register("release_consistency", run_comparison)
MODE_REGISTRY.register("domain_old_vs_new", domain_old_vs_new_comparison_mode)


def get_mode(mode_name: str):
    return resolve_mode(MODE_REGISTRY, mode_name)
