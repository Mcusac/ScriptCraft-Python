"""CLI entrypoint for dictionary cleaner (level_4)."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import DictionaryCleaner

main = create_entrypoint_main(
    DictionaryCleaner,
    tool_name="dictionary_cleaner",
    description=(
        "Cleans and standardizes data dictionary entries including value types "
        "and expected values"
    ),
    parser_kind="standard",
)
