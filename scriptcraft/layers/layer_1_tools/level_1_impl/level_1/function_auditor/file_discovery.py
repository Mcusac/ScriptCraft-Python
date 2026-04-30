"""File-discovery rules for batch function auditing."""

from pathlib import Path
from typing import List, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_tools.level_1_impl.level_0.function_auditor import BatchFunctionAuditor, InputPaths

CURRENT_DIR = "."


def _existing_paths(input_paths: InputPaths) -> List[Path]:
    return [Path(p) for p in input_paths if Path(p).exists()]


def collect_files(
    *,
    input_paths: Optional[InputPaths],
    pattern: Optional[str],
    folder: Optional[str],
    extension: str,
    batch_auditor: BatchFunctionAuditor,
) -> List[Path]:
    """
    Resolve which files the batch audit should process.

    Precedence: explicit ``input_paths`` > ``pattern`` > ``folder`` > extension scan.
    Raises ``ValueError`` if explicit input paths were supplied but none exist.
    """
    if input_paths:
        files = _existing_paths(input_paths)
        if not files:
            raise ValueError("❌ No valid input files found")
        return files

    if pattern:
        files = batch_auditor.get_files_by_pattern(pattern, CURRENT_DIR)
        log_and_print(f"📁 Found {len(files)} files matching pattern: {pattern}")
        return files

    if folder:
        files = batch_auditor.get_files_in_folder(folder)
        log_and_print(f"📁 Found {len(files)} files in folder: {folder}")
        return files

    files = batch_auditor.get_files_by_extension(extension, CURRENT_DIR)
    log_and_print(f"📁 Found {len(files)} files with extension: {extension}")
    return files
