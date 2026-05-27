from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
    run_pairwise_comparison,
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
    return {
        "mode": "standard",
        "status": "success" if result.success else "failed",
        "error": result.error,
        "outputs": result.metadata.get("outputs", []),
        **dict(result.metadata or {}),
    }
