"""Batch mode for the function auditor tool."""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_0_core.level_0 import InputPaths

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import save_batch_audit
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import BatchFunctionAuditor
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import collect_files


def run_batch_mode(
    *,
    input_paths: Optional[InputPaths],
    output_path: Path,
    language: str,
    extension: str,
    pattern: Optional[str],
    folder: Optional[str],
    summary_only: bool,
    unused_only: bool,
    detailed_unused: bool,
) -> None:
    """Run a batch audit and persist the aggregated results."""
    log_and_print(
        f"🔍 Starting batch audit (language: {language}, extension: {extension})"
    )

    batch_auditor = BatchFunctionAuditor()

    files = collect_files(
        input_paths=input_paths,
        pattern=pattern,
        folder=folder,
        extension=extension,
        batch_auditor=batch_auditor,
    )

    if not files:
        log_and_print("❌ No files found to audit")
        return

    results = batch_auditor.audit_files(
        files,
        show_details=not summary_only,
        unused_only=unused_only,
        verbose=True,
    )

    batch_auditor.generate_batch_report(results, verbose=True)

    if detailed_unused:
        batch_auditor.generate_unused_functions_report(results, verbose=True)

    save_batch_audit(results, output_path, language)
