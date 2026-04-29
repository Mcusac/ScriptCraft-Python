import pandas as pd

from pathlib import Path
from typing import Any, Dict, Union


from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


def generate_report(
    comparison_results: Dict[str, Any],
    report_path: Union[str, Path],
    *,
    format: str = "excel",
) -> None:
    """Generate and save a comparison report."""
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(comparison_results)

    if format.lower() == "excel":
        results_df.to_excel(report_path, index=False)
    else:
        results_df.to_csv(report_path, index=False)

    log_and_print(f"📄 Report saved to: {report_path.resolve()}")

