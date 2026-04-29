
from collections.abc import Iterable, Mapping


def compute_case_mismatches(dataset_cols: Iterable[str], dictionary_cols: Iterable[str]) -> list[str]:
    """
    Return dataset column names whose lowercase exists in the dictionary columns,
    but the actual casing differs.
    """
    dataset_set = set(dataset_cols)
    dictionary_set = set(dictionary_cols)

    lower_dataset: Mapping[str, str] = {col.lower(): col for col in dataset_set}
    lower_dict: Mapping[str, str] = {col.lower(): col for col in dictionary_set}

    shared_lower = set(lower_dataset) & set(lower_dict)
    return [lower_dataset[name] for name in shared_lower if lower_dataset[name] != lower_dict[name]]

