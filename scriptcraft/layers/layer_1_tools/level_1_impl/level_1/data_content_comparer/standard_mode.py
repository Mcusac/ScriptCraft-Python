from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    run_pairwise_comparison,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    pipeline_result_to_mode_dict,
)


def standard_comparison_mode(input_paths, output_dir, domain=None, **kwargs) -> Dict[str, Any]:
    """Standard row-wise content comparison (two input files)."""
    _ = kwargs
    result = run_pairwise_comparison(
        mode="standard",
        input_paths=input_paths,
        output_dir=output_dir,
        domain=domain,
    )
    return pipeline_result_to_mode_dict(mode="standard", result=result)
