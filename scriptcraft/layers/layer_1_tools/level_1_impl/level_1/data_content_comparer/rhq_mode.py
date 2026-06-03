from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    run_keyed_cell_comparison,
)

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    pipeline_result_to_mode_dict,
)

_RHQ_KEYS = [
    "Med_ID",
    "AgePeriod (this is the decade of life starting at 0)",
]


def rhq_comparison_mode(input_paths, output_dir, domain=None, **kwargs) -> Dict[str, Any]:
    """RHQ-specific keyed comparison."""
    _ = kwargs
    result = run_keyed_cell_comparison(
        mode="rhq",
        input_paths=input_paths,
        output_dir=output_dir,
        keys=_RHQ_KEYS,
        domain=domain,
    )
    return pipeline_result_to_mode_dict(mode="rhq", result=result)
