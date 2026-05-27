"""CLI/pipeline entrypoint for the automated labeler tool."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import AutomatedLabeler


main = create_entrypoint_main(
    AutomatedLabeler,
    tool_name="automated_labeler",
    description="🏷️ Automatically generates labels and fills document templates with data",
    parser_kind="standard",
)

