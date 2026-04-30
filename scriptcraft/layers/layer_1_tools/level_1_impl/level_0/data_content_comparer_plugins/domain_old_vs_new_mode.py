
from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.paths import get_project_root
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_comparison_datasets
from layers.layer_1_tools.level_0_infra.level_1.comparison import compare_dataframes
from layers.layer_1_tools.level_0_infra.level_2.validation import get_domain_paths


def run_mode(input_paths, output_dir, domain=None, **kwargs) -> None:
    """Domain-based old vs new content comparison."""
    domain_paths = get_domain_paths(get_project_root())

    for domain, paths in domain_paths.items():
        log_and_print(f"📌 Comparing domain: {domain}")
        old_file = paths["old_data"] / "your_old_file.xlsx"
        new_file = paths["processed_data"] / "your_new_file.xlsx"

        try:
            df1, df2, dataset_name = load_comparison_datasets([old_file, new_file])
            compare_dataframes(df1, df2, dataset_name, output_dir)
        except Exception as e:
            log_and_print(f"❌ Failed comparison for {domain}: {e}")

    log_and_print(f"📁 All domain comparisons completed. Results saved to: {output_dir.resolve()}")

