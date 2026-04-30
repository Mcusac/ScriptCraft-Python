"""Single-file mode for the function auditor tool."""

from pathlib import Path

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_1_impl.level_0.function_auditor import FunctionAuditor

from layers.layer_1_tools.level_1_impl.level_0.function_auditor.types import InputPath
from layers.layer_1_tools.level_1_impl.level_1.function_auditor.persistence import save_single_audit


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
