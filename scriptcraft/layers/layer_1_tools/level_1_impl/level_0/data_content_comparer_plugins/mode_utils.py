"""Shared helpers for data content comparer mode handlers."""

from typing import Any, Dict

from scriptcraft.layers.layer_0_core.level_0 import PipelineResult


def pipeline_result_to_mode_dict(
    *,
    mode: str,
    result: PipelineResult,
) -> Dict[str, Any]:
    """Map a PipelineResult into the dict shape expected by mode dispatch."""
    metadata = dict(result.metadata or {})
    outputs = list(metadata.get("outputs") or [])
    return {
        "mode": mode,
        "status": "success" if result.success else "failed",
        "error": result.error,
        "outputs": outputs,
        **metadata,
    }
