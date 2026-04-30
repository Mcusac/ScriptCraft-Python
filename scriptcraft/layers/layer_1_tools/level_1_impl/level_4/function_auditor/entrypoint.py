"""CLI/pipeline entrypoint for the function auditor tool."""

from layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main

from layers.layer_1_tools.level_1_impl.level_3.function_auditor.tool import FunctionAuditorTool


main = create_entrypoint_main(
    FunctionAuditorTool,
    tool_name="function_auditor",
    description=(
        "🔍 Audits unused functions in codebases and provides cleanup recommendations"
    ),
    parser_kind="standard",
)
