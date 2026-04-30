"""JSON persistence helpers for the function auditor tool."""

import json
from pathlib import Path
from typing import Any

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.function_auditor.types import AuditResult, BatchResults

SUMMARY_SUFFIX = "_summary.json"
DETAILED_SUFFIX = "_detailed.json"
SINGLE_BASE_SUFFIX = "_audit"
BATCH_FILENAME_TEMPLATE = "batch_audit_{language}_results.json"


def write_json(path: Path, payload: Any) -> None:
    """Write ``payload`` as indented JSON, falling back to ``str()`` for unknown types."""
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, default=str)


def _compute_audit_summary(result: AuditResult) -> AuditResult:
    used = len(result["used"])
    unused = len(result["unused"])
    total = used + unused
    unused_percentage = (unused / total) * 100 if total > 0 else 0
    return {
        "total_functions": total,
        "used_functions": used,
        "unused_functions": unused,
        "unused_percentage": unused_percentage,
    }


def save_single_audit(result: AuditResult, output_path: Path, file_stem: str) -> None:
    """Persist single-file audit summary + detailed results next to one another."""
    base_name = f"{file_stem}{SINGLE_BASE_SUFFIX}"
    summary_file = output_path / f"{base_name}{SUMMARY_SUFFIX}"
    results_file = output_path / f"{base_name}{DETAILED_SUFFIX}"

    write_json(summary_file, _compute_audit_summary(result))
    write_json(results_file, result)

    log_and_print(f"📊 Results saved to: {summary_file} and {results_file}")


def save_batch_audit(results: BatchResults, output_path: Path, language: str) -> None:
    """Persist batch audit results, named by language."""
    results_file = output_path / BATCH_FILENAME_TEMPLATE.format(language=language)
    write_json(results_file, results)
    log_and_print(f"📊 Batch results saved to: {results_file}")
