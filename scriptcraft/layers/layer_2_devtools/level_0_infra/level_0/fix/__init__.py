"""Auto-generated package exports."""


from .import_fix_models import (
    EditOperation,
    FileEditResult,
    FixRunSummary,
)

from .import_fix_strategies import (
    FixOptions,
    build_edit_operations_for_tree,
    iter_python_files,
)

from .import_rewrite_engine import apply_edit_operations

from .layer_core_import_rewrite import (
    LEVEL_RE,
    file_info,
    process,
    rewrite_line,
    run_layer_core_import_rewrite,
)

from .move_import_rewriter import (
    MoveImportRewrite,
    build_move_import_rewrite_ops,
)

from .text_span_rewrite_engine import (
    SpanEditOperation,
    SpanEditResult,
    SpanFixRunSummary,
    apply_span_edit_operations,
)

from .unused_import_cleanup import (
    UnusedImportRemover,
    load_health_report,
    run_unused_import_cleanup,
)

from .violation_fix_bundle import run_violation_fix_bundle

__all__ = [
    "EditOperation",
    "FileEditResult",
    "FixOptions",
    "FixRunSummary",
    "LEVEL_RE",
    "MoveImportRewrite",
    "SpanEditOperation",
    "SpanEditResult",
    "SpanFixRunSummary",
    "UnusedImportRemover",
    "apply_edit_operations",
    "apply_span_edit_operations",
    "build_edit_operations_for_tree",
    "build_move_import_rewrite_ops",
    "file_info",
    "iter_python_files",
    "load_health_report",
    "process",
    "rewrite_line",
    "run_layer_core_import_rewrite",
    "run_unused_import_cleanup",
    "run_violation_fix_bundle",
]
