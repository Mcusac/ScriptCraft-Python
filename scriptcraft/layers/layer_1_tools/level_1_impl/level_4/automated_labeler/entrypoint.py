"""CLI entrypoint for the automated labeler (level_4)."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import AutomatedLabeler

main = create_entrypoint_main(
    AutomatedLabeler,
    tool_name="automated_labeler",
    description="Automatically generates labels and fills document templates with data",
    parser_kind="standard",
)
