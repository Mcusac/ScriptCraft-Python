"""CLI/pipeline entrypoint for the automated labeler tool."""

from layers.layer_1_pypi.level_1_impl.level_0.main_common import create_entrypoint_main

from layers.layer_1_pypi.level_1_impl.level_2.automated_labeler.tool import AutomatedLabeler


main = create_entrypoint_main(
    AutomatedLabeler,
    tool_name="automated_labeler",
    description="🏷️ Automatically generates labels and fills document templates with data",
    parser_kind="standard",
)

