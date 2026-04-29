"""CLI/pipeline entrypoint for the date format standardizer tool."""

from layers.layer_1_pypi.level_1_impl.level_0.main_common import create_entrypoint_main

from layers.layer_1_pypi.level_1_impl.level_0.date_format_standardizer.tool import DateFormatStandardizer

main = create_entrypoint_main(
    DateFormatStandardizer,
    tool_name="date_format_standardizer",
    description="📅 Standardizes date formats in datasets to ensure consistency",
    parser_kind="standard",
)

