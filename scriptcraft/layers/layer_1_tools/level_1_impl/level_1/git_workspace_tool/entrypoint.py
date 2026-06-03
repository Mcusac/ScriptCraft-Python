"""CLI entrypoint for Git workspace tool."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    GitWorkspaceTool,
)

main = create_entrypoint_main(
    GitWorkspaceTool,
    tool_name="git_workspace_tool",
    description="Handles Git workspace operations (push, pull, status, commit, tag)",
    parser_kind="standard",
)
