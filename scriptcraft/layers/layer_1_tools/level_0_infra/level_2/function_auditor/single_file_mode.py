"""Single-file mode for the function auditor tool."""

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    log_and_print,
    InputPath,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    save_single_audit,
    FunctionAuditor,
)


def run_single_file_mode(*, file_path: InputPath, output_path: Path) -> None:
    """Run an audit against a single file and persist the results."""
    target = Path(file_path)
    if not target.exists():
        raise ValueError(f"❌ File not found: {target}")

    log_and_print(f"🔍 Auditing single file: {target}")

    auditor = FunctionAuditor(str(target))
    result = auditor.audit_functions(verbose=True)
    auditor.generate_report(result, verbose=True)

    save_single_audit(result, output_path, target.stem)
