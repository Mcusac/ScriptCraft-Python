"""CLI entrypoint for MedVisit integrity validator."""

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import create_entrypoint_main

from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import (
    MedVisitIntegrityValidator,
)

main = create_entrypoint_main(
    MedVisitIntegrityValidator,
    tool_name="medvisit_integrity_validator",
    description="Validates Med_ID and Visit_ID integrity between old and new datasets",
    parser_kind="standard",
)
