from pathlib import Path
from typing import Dict, Any, List

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_1.paths import get_project_root
from layers.layer_1_tools.level_1.data_loading import load_comparison_datasets
from layers.layer_1_tools.level_2.comparison import compare_dataframes
from layers.layer_1_tools.level_2.validation import get_domain_paths


def run_mode(input_paths, output_dir, domain=None, **kwargs) -> Dict[str, Any]:
    """
    Domain-based old vs new content comparison across all configured domains.
    """

    log_and_print("📌 Running Domain Old vs New Comparison...")

    try:
        project_root = get_project_root()
        domain_paths = get_domain_paths(project_root)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results: List[str] = []
        failures: List[str] = []

        # Allow override mode (optional but important for consistency)
        if input_paths:
            raise ValueError(
                "Domain mode does not accept input_paths. It discovers files via domain config."
            )

        # ----------------------------
        # Iterate domains safely
        # ----------------------------
        for domain_name, paths in domain_paths.items():
            log_and_print(f"📌 Comparing domain: {domain_name}")

            try:
                # Replace hardcoded placeholders with real patterns or config-driven logic
                old_candidates = list(paths["old_data"].glob("*.xlsx"))
                new_candidates = list(paths["processed_data"].glob("*.xlsx"))

                if not old_candidates or not new_candidates:
                    raise FileNotFoundError(
                        f"No files found for domain {domain_name}"
                    )

                # Deterministic selection (highest priority: latest file)
                old_file = sorted(old_candidates)[-1]
                new_file = sorted(new_candidates)[-1]

                df1, df2, dataset_name = load_comparison_datasets(
                    [old_file, new_file]
                )

                compare_dataframes(df1, df2, dataset_name, output_dir)

                results.append(domain_name)

            except Exception as e:
                log_and_print(f"❌ Failed comparison for {domain_name}: {e}")
                failures.append(f"{domain_name}: {str(e)}")

        log_and_print(
            f"📁 All domain comparisons completed. Results saved to: {output_dir.resolve()}"
        )

        return {
            "mode": "domain_old_vs_new",
            "processed_domains": results,
            "failed_domains": failures,
            "status": "success" if not failures else "partial_failure",
            "outputs": [],  # compare_dataframes writes internally
        }

    except Exception as e:
        log_and_print(f"❌ Domain comparison system failure: {e}")

        return {
            "mode": "domain_old_vs_new",
            "status": "failed",
            "error": str(e),
            "outputs": [],
        }