from typing import Callable, Dict

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.data_content_comparer_plugins.rhq_mode import run_mode as rhq_mode
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.data_content_comparer_plugins.standard_mode import run_mode as standard_mode
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.data_content_comparer_plugins.release_consistency_mode import run_mode as release_consistency_mode
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.data_content_comparer_plugins.domain_old_vs_new_mode import run_mode as domain_old_vs_new_mode


MODE_REGISTRY: Dict[str, Callable] = {
    "rhq": rhq_mode,
    "standard": standard_mode,
    "release_consistency": release_consistency_mode,
    "domain_old_vs_new": domain_old_vs_new_mode,
}


def get_mode(mode_name: str) -> Callable:
    """Return a mode execution function."""
    try:
        return MODE_REGISTRY[mode_name]
    except KeyError:
        raise ValueError(f"Unknown mode: {mode_name}. Available: {list(MODE_REGISTRY.keys())}")