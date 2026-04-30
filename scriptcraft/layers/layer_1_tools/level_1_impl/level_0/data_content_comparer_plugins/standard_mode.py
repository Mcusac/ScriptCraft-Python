
from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_comparison_datasets
from layers.layer_1_tools.level_0_infra.level_1.comparison import compare_dataframes


def run_mode(input_paths, output_dir, domain=None, **kwargs) -> None:
    """Standard row-wise content comparison without special logic."""
    if not input_paths:
        raise ValueError("Standard mode requires two input files provided via --input.")

    log_and_print(f"📌 Running Standard Comparison{' for domain: ' + domain if domain else ''}...")

    df1, df2, dataset_name = load_comparison_datasets(input_paths)

    # Run the generic comparison from shared utils
    compare_dataframes(df1, df2, dataset_name, output_dir)

    log_and_print(f"📁 Results saved to: {output_dir.resolve()}")

