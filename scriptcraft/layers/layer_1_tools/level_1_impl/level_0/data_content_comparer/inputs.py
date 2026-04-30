
from pathlib import Path
from typing import List, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_2.validation import auto_resolve_input_files


def resolve_input_files(
    mode: Optional[str],
    input_dir: Path,
    input_paths: Optional[List[Union[str, Path]]] = None,
) -> Optional[List[Union[str, Path]]]:
    """Resolve input files based on a mode and provided paths."""
    if input_paths:
        return input_paths

    if mode == "rhq_mode":
        base = input_dir.resolve()
        log_and_print(f"🔎 Resolving input files in RHQ mode from: {base.resolve()}")
        return auto_resolve_input_files(base, required_count=2)

    log_and_print(f"🔎 Looking for input files in: {input_dir.resolve()}")
    input_files = sorted(input_dir.glob("*.[cx]sv*"))[-2:]
    if not input_files:
        log_and_print(f"⚠️ No matching files found in directory: {input_dir.resolve()}")
    else:
        log_and_print(f"📂 Found files: {[str(f) for f in input_files]}")

    if len(input_files) != 2:
        log_and_print(f"⚠️ Warning: Expected 2 files in {input_dir}, but found {len(input_files)}. Exiting.")
        return None

    return input_files

