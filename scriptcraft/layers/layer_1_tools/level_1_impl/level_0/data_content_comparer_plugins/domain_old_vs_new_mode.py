from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
  run_domain_discovery_comparison,
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
  return {
    "mode": "domain_old_vs_new",
    "status": "success" if result.success else "failed",
    "error": result.error,
    "outputs": result.metadata.get("outputs", []),
    **dict(result.metadata or {}),
  }
