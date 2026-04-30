"""CLI/pipeline entrypoint for the dictionary cleaner tool."""

from layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main

from .tool import DictionaryCleaner


main = create_entrypoint_main(
    DictionaryCleaner,
    tool_name="dictionary_cleaner",
    description=(
        "🧹 Cleans and standardizes data dictionary entries including value types "
        "and expected values"
    ),
    parser_kind="standard",
)
