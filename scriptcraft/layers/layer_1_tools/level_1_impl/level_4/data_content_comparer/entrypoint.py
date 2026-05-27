"""CLI/pipeline entrypoint for the data content comparer tool."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import DataContentComparer


def _detect_input_paths_required(argv: list[str]) -> bool:
    release_consistency_mode = "--mode" in argv and ("release_consistency" in argv or "release" in argv)
    return not release_consistency_mode


main = create_entrypoint_main(
    DataContentComparer,
    tool_name="data_content_comparer",
    description="📊 Compares content between datasets and generates detailed reports",
    parser_kind="standard",
    input_paths_required=_detect_input_paths_required(__import__("sys").argv),
)

