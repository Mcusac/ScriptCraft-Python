from pathlib import Path
from typing import Dict, Any

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_comparison_datasets
from layers.layer_1_tools.level_0_infra.level_2.comparison import compare_dataframes


def run_mode(input_paths, output_dir, domain=None, **kwargs) -> Dict[str, Any]:
    """
    Standard row-wise content comparison without special logic.
    Expects exactly two input files.
    """

    if not input_paths or len(input_paths) != 2:
        raise ValueError("Standard mode requires exactly two input files.")

    suffix = f" for domain: {domain}" if domain else ""
    log_and_print(f"📌 Running Standard Comparison{suffix}...")

    try:
        df1, df2, dataset_name = load_comparison_datasets(input_paths)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        compare_dataframes(df1, df2, dataset_name, output_dir)

        log_and_print(f"📁 Results saved to: {output_dir.resolve()}")

        return {
            "mode": "standard",
            "dataset": dataset_name,
            "outputs": [],  # compare_dataframes currently handles file writing internally
            "status": "success",
        }

    except Exception as e:
        log_and_print(f"❌ Standard comparison failed: {e}")

        return {
            "mode": "standard",
            "dataset": None,
            "outputs": [],
            "status": "failed",
            "error": str(e),
        }