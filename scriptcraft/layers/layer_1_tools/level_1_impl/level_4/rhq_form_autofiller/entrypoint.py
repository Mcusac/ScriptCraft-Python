"""CLI entrypoint for RHQ form autofiller."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import (
    RHQFormAutofiller,
)

main = create_entrypoint_main(
    RHQFormAutofiller,
    tool_name="rhq_form_autofiller",
    description="Automates RHQ form filling",
    parser_kind="standard",
)
