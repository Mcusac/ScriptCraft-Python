from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
  run_keyed_cell_comparison,
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
  return {
    "mode": "rhq",
    "status": "success" if result.success else "failed",
    "error": result.error,
    "outputs": result.metadata.get("outputs", []),
    **dict(result.metadata or {}),
  }
