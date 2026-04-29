"""CLI/pipeline entrypoint for the data content comparer tool."""

from layers.layer_1_pypi.level_1_impl.level_0.main_common import create_entrypoint_main
from layers.layer_1_pypi.level_1_impl.level_1.data_content_comparer.tool import DataContentComparer


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

