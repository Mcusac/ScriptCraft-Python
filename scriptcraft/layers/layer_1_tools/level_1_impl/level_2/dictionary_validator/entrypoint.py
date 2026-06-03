"""CLI entrypoint for dictionary validator."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_3.dictionary_validator.tool import (
    DictionaryValidator,
    create_dictionary_validator_parser,
)

main = create_entrypoint_main(
    DictionaryValidator,
    tool_name="dictionary_validator",
    description="Validates consistency between dataset columns and dictionary columns",
    parser_kind="custom",
    create_parser_func=create_dictionary_validator_parser,
    run_style="kwargs",
)
