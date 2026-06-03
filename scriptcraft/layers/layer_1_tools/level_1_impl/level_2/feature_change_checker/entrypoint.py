"""CLI entrypoint for feature change checker."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    FeatureChangeChecker,
)

main = create_entrypoint_main(
    FeatureChangeChecker,
    tool_name="feature_change_checker",
    description="Tracks and categorizes changes in feature values between visits",
    parser_kind="standard",
)
