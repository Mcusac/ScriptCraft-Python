import pandas as pd

from pathlib import Path
from typing import Union


from layers.layer_1_tools.level_0_infra.level_1.timepoint import (
    clean_sequence_ids,
    compare_entity_changes_over_sequence,
)


def run_between_visit_changes(df: pd.DataFrame, feature: str, output_dir: Union[str, Path]) -> None:
    """Run between-visit changes analysis."""
    df = df[["Med_ID", "Visit_ID", feature]]
    df = clean_sequence_ids(df)
    compare_entity_changes_over_sequence(
        df,
        dataset_name="BetweenVisitChanges",
        chosen_feature=feature,
        output_folder=output_dir,
    )

