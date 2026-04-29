
from typing import TypedDict


class CompareColumnsResult(TypedDict):
    in_both: set[str]
    only_in_dataset: set[str]
    only_in_dictionary: set[str]
    case_mismatches: list[str]

