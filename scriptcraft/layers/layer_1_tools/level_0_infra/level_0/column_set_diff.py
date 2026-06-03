"""Column-set comparison helpers for dictionary vs dataset alignment."""

from dataclasses import dataclass
from typing import Set, Tuple


@dataclass(frozen=True)
class CompareColumnsResult:
    in_both: Set[str]
    only_in_dataset: Set[str]
    only_in_dictionary: Set[str]
    case_mismatches: Tuple[Tuple[str, str], ...]
