"""Auto-generated package exports."""


from .comparison import (
    ComparisonResult,
    DataFrameComparer,
    compare_dataframes,
    handle_comparison_errors,
)

from .environment_mixin import EnvironmentMixin

from .legacy_api import get_legacy_config

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

from .processing import (
    create_tool_runner,
    merge_dataframes,
    merge_with_key_column,
    process_by_domains,
    setup_tool_files,
    split_dataframe_by_column,
    standardize_tool_execution,
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

from .value_cleaning import (
    is_missing_like,
    normalize_value,
)

__all__ = [
    "BasePipeline",
    "ColumnValidator",
    "ComparisonResult",
    "Config",
    "DataFrameComparer",
    "DataProcessor",
    "EnvironmentMixin",
    "FlaggedValue",
    "PipelineStep",
    "QCLogContext",
    "STATUS_EMOJI",
    "T",
    "auto_resolve_input_files",
    "batch_process_files",
    "build_log_config",
    "clean_sequence_ids",
    "compare_dataframes",
    "compare_entity_changes_over_sequence",
    "create_tool_runner",
    "get_legacy_config",
    "get_status_emoji",
    "handle_comparison_errors",
    "is_missing_like",
    "load_and_process_data",
    "log_fix_summary",
    "merge_dataframes",
    "merge_with_key_column",
    "normalize_value",
    "process_by_domains",
    "qc_log_context",
    "setup_tool_files",
    "split_dataframe_by_column",
    "standardize_tool_execution",
    "validate_and_transform_data",
    "validate_input_paths",
    "validate_required_columns",
    "with_domain_logger",
]
