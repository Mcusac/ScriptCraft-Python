"""Auto-generated package exports."""


from .cleaning import (
    clean_brace_formatting,
    clean_dataframe,
    clean_supplement_data,
    create_standardized_supplement_row,
    fix_numeric_dash_inside_braces,
    fix_word_number_dash_inside_braces,
    get_clean_numeric_series,
    is_missing_like,
    normalize_value,
    parse_missing_unit,
    prevent_pipe_inside_braces,
    standardize_columns,
    standardize_supplement_columns,
)

from .comparison import (
    ComparisonResult,
    DataFrameComparer,
    compare_dataframes,
    handle_comparison_errors,
)

from .log_config import (
    LogConfig,
    StructuredFormatter,
    config,
)

from .logging_bootstrap import build_log_config

from .logging_context import (
    QCLogContext,
    T,
    log_fix_summary,
    qc_log_context,
    with_domain_logger,
)

from .pipeline_base import (
    BasePipeline,
    PipelineStep,
)

from .processor import (
    DataProcessor,
    batch_process_files,
    load_and_process_data,
    validate_and_transform_data,
)

from .root_schema import Config

from .timepoint import (
    clean_sequence_ids,
    compare_entity_changes_over_sequence,
)

from .validation import (
    ColumnValidator,
    FlaggedValue,
    STATUS_EMOJI,
    auto_resolve_input_files,
    get_status_emoji,
    validate_input_paths,
    validate_required_columns,
)

__all__ = [
    "BasePipeline",
    "ColumnValidator",
    "ComparisonResult",
    "Config",
    "DataFrameComparer",
    "DataProcessor",
    "FlaggedValue",
    "LogConfig",
    "PipelineStep",
    "QCLogContext",
    "STATUS_EMOJI",
    "StructuredFormatter",
    "T",
    "auto_resolve_input_files",
    "batch_process_files",
    "build_log_config",
    "clean_brace_formatting",
    "clean_dataframe",
    "clean_sequence_ids",
    "clean_supplement_data",
    "compare_dataframes",
    "compare_entity_changes_over_sequence",
    "config",
    "create_standardized_supplement_row",
    "fix_numeric_dash_inside_braces",
    "fix_word_number_dash_inside_braces",
    "get_clean_numeric_series",
    "get_status_emoji",
    "handle_comparison_errors",
    "is_missing_like",
    "load_and_process_data",
    "log_fix_summary",
    "normalize_value",
    "parse_missing_unit",
    "prevent_pipe_inside_braces",
    "qc_log_context",
    "standardize_columns",
    "standardize_supplement_columns",
    "validate_and_transform_data",
    "validate_input_paths",
    "validate_required_columns",
    "with_domain_logger",
]
