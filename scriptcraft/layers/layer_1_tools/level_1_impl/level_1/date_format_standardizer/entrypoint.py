"""CLI/pipeline entrypoint for the date format standardizer tool."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import DateFormatStandardizer

main = create_entrypoint_main(
    DateFormatStandardizer,
    tool_name="date_format_standardizer",
    description="📅 Standardizes date formats in datasets to ensure consistency",
    parser_kind="standard",
)

