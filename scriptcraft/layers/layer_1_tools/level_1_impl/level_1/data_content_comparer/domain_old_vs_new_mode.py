from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    run_domain_discovery_comparison,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    pipeline_result_to_mode_dict,
)


def domain_old_vs_new_comparison_mode(input_paths, output_dir, domain=None, **kwargs) -> Dict[str, Any]:
    """Domain-based old vs new content comparison."""
    _ = domain, kwargs
    if input_paths:
        raise ValueError(
            "Domain mode does not accept input_paths. It discovers files via domain config."
        )
    result = run_domain_discovery_comparison(
        mode="domain_old_vs_new",
        output_dir=output_dir,
    )
    return pipeline_result_to_mode_dict(mode="domain_old_vs_new", result=result)
