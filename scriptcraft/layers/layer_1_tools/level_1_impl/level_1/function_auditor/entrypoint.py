"""CLI/pipeline entrypoint for the function auditor tool."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import FunctionAuditorTool


main = create_entrypoint_main(
    FunctionAuditorTool,
    tool_name="function_auditor",
    description=(
        "🔍 Audits unused functions in codebases and provides cleanup recommendations"
    ),
    parser_kind="standard",
)
