"""
Score Totals Checker Tool

This checker validates that calculated totals match expected totals in datasets.
"""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_0_core.level_1 import (
    run_process_domain_over_input_paths,
    build_run_context
)
from scriptcraft.layers.layer_0_core.level_5 import load_tabular as load_data

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import DomainFileToolMixin, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import calculate_totals_and_compare
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool, create_entrypoint_main



class ScoreTotalsChecker(DomainFileToolMixin, BaseTool):
    """
    Checker for validating that calculated totals match expected totals in datasets.
    """

    def __init__(self):
        super().__init__(
            name="Score Totals Checker",
            description="Validates that calculated totals match expected totals in datasets",
            tool_name="score_totals_checker",
        )

    # ---------------------------
    # ORCHESTRATION ENTRY POINT
    # ---------------------------
    def run(self, *args, **kwargs) -> None:
        """Delegates to standardized domain loop runner (outside tool logic)."""
        ctx = build_run_context(*args, **kwargs)
        run_process_domain_over_input_paths(
            self,
            input_paths=ctx.input_paths,
            output_dir=ctx.output_dir or self.default_output_dir,
            domain=ctx.domain or "unknown",
            dictionary_file=ctx.dictionary_file,
            extra_kwargs=ctx.extra_kwargs,
        )

    # ---------------------------
    # MIXIN IMPLEMENTATION
    # ---------------------------
    def _process_domain_impl(
        self,
        domain: str,
        dataset_file: Path,
        dictionary_file: Optional[Path],
        output_path: Path,
        **kwargs,
    ) -> None:
        """
        Core logic: validate totals in dataset.
        """

        log_and_print(f"🔍 Checking totals in {dataset_file.name} for {domain}...")

        try:
            df = load_data(dataset_file)

            results = calculate_totals_and_compare(df, domain)

            if results is not None and not results.empty:
                output_file = output_path / f"{domain}_totals_check.csv"
                results.to_csv(output_file, index=False)
                log_and_print(f"✅ Results saved to: {output_file}")
            else:
                log_and_print(f"⚠️ No total columns found to check in {domain}")

        except Exception as e:
            log_and_print(f"❌ Error checking totals for {domain}: {e}", level="error")
            raise


# ---------------------------
# ENTRYPOINT
# ---------------------------
main = create_entrypoint_main(
    ScoreTotalsChecker,
    tool_name="score_totals_checker",
    description="Validates that calculated totals match expected totals in datasets",
    parser_kind="standard",
)


if __name__ == "__main__":
    main()