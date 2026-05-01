"""Auto-generated package exports."""


from .architecture_score import (
    ScoreComponent,
    ScoreConfig,
    ScoreResult,
    compute_architecture_score,
    compute_health_score,
    compute_manifest_score,
    load_score_config_optional,
)

from .architecture_scorecard_markdown import (
    ScorecardOptions,
    build_health_markdown_scorecard,
    build_manifest_markdown_scorecard,
    load_health_report,
    load_manifest,
)

from .audit_machine_emit_templates import (
    build_audit_markdown,
    build_inventory_markdown,
)

from .base_health_reporter import BaseReporter

from .console_format_helpers import FormattingHelpers

from .file_level_suggestions_markdown import build_file_level_suggestions_markdown

from .health_report_views import (
    DEFAULT_COMPLEXITY_TARGET_NAMES,
    extract_duplicate_blocks,
    lines_complexity_targets,
    lines_duplication_summary,
    lines_health_compare,
    lines_oversized_modules,
    lines_srp_summary,
    remap_duplicate_loc,
)

from .import_organizer import (
    ImportOrganizerItem,
    ImportOrganizerResult,
    ImportOrganizerSpanResult,
    build_import_organizer_span_edit,
    organize_imports_text,
)

from .inventory_bootstrap_markdown import bootstrap_markdown

from .move_plan_from_scan import build_move_plan_markdown

from .promotion_demotion_suggestions_markdown import build_promotion_demotion_suggestions_markdown

from .scan_violation_summary import format_scan_violation_summary_lines

__all__ = [
    "BaseReporter",
    "DEFAULT_COMPLEXITY_TARGET_NAMES",
    "FormattingHelpers",
    "ImportOrganizerItem",
    "ImportOrganizerResult",
    "ImportOrganizerSpanResult",
    "ScoreComponent",
    "ScoreConfig",
    "ScoreResult",
    "ScorecardOptions",
    "bootstrap_markdown",
    "build_audit_markdown",
    "build_file_level_suggestions_markdown",
    "build_health_markdown_scorecard",
    "build_import_organizer_span_edit",
    "build_inventory_markdown",
    "build_manifest_markdown_scorecard",
    "build_move_plan_markdown",
    "build_promotion_demotion_suggestions_markdown",
    "compute_architecture_score",
    "compute_health_score",
    "compute_manifest_score",
    "extract_duplicate_blocks",
    "format_scan_violation_summary_lines",
    "lines_complexity_targets",
    "lines_duplication_summary",
    "lines_health_compare",
    "lines_oversized_modules",
    "lines_srp_summary",
    "load_health_report",
    "load_manifest",
    "load_score_config_optional",
    "organize_imports_text",
    "remap_duplicate_loc",
]
