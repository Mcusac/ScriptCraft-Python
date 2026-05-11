# ============================================================
# dag_runner.py — pure DAG execution engine
# ============================================================

import pandas as pd


def run_nodes(
    merged: pd.DataFrame,
    detectors: dict[str, callable],
) -> dict[str, pd.DataFrame]:
    """
    Executes all detector nodes.

    PURE orchestration only:
        - no business logic
        - no schema knowledge
        - no special cases
    """

    return {
        name: node(merged)
        for name, node in detectors.items()
    }