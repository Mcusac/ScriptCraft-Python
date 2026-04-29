
from collections.abc import Iterable

from layers.layer_1_pypi.level_1_impl.level_0.compare_columns import compute_case_mismatches, CompareColumnsResult


def compare_columns(dataset_cols: Iterable[str], dictionary_cols: Iterable[str]) -> CompareColumnsResult:
    """Compare dataset vs dictionary column sets and return a detailed result."""
    dataset_set = set(dataset_cols)
    dictionary_set = set(dictionary_cols)

    in_both = dataset_set & dictionary_set
    only_in_dataset = dataset_set - dictionary_set
    only_in_dictionary = dictionary_set - dataset_set

    return CompareColumnsResult(
        in_both=in_both,
        only_in_dataset=only_in_dataset,
        only_in_dictionary=only_in_dictionary,
        case_mismatches=compute_case_mismatches(dataset_set, dictionary_set),
    )

