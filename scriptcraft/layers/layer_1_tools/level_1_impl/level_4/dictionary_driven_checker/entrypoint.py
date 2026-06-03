"""CLI entrypoint for the dictionary driven checker (level_3)."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_3 import DictionaryDrivenChecker

main = create_entrypoint_main(
    DictionaryDrivenChecker,
    tool_name="dictionary_driven_checker",
    description="Validates data against a data dictionary using configurable plugins",
    parser_kind="standard",
)
