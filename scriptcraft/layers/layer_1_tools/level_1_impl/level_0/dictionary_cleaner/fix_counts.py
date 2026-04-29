
from dataclasses import dataclass
from typing import Dict


DEFAULT_FIX_COUNTS: Dict[str, int] = {
    "Switched numerical representations of categorical variables to integers": 0,
    "Normalized = or : to comma": 0,
    "Ensure space after comma in '{}' pairs": 0,
    "Inserted missing comma between key and label": 0,
    "Curly brace spacing fixed": 0,
    "Multiple spaces replaced with ' | '": 0,
    "Leading zero added inside '{}'": 0,
    "Missing space between number and word fixed": 0,
    "Removed spaces before and after '/' for consistency": 0,
    "Replaced incorrect ']' inside '{}'": 0,
    "Ensured `[` remains for labels": 0,
    "Replaced incorrect '(' with '{'": 0,
    "Removed extra spaces after '{'": 0,
    "Fixed incorrect `}` in numeric ranges": 0,
    "Removed space before a comma": 0,
    "Remove commas between `{}` pairs": 0,
    "Ensured exactly one space between '{}' pairs": 0,
    "Removed unnecessary trailing spaces": 0,
    "Add space before and after '='": 0,
    "Removed trailing spaces inside '{}'": 0,
    "Removed spaces around '-' between numbers inside '{}'": 0,
    "Added spaces around '-' between words and numbers inside '{}'": 0,
    "Removed random trailing ' - '": 0,
    "Fixed incorrect 'Don't' capitalization": 0,
    "Added space before '{' following '-'": 0,
    "Collapsed multiple spaces to single space": 0,
}


@dataclass
class FixCounter:
    counts: Dict[str, int]

    @classmethod
    def fresh(cls) -> "FixCounter":
        return cls(counts={key: 0 for key in DEFAULT_FIX_COUNTS})

    def inc(self, key: str, amount: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + amount

    def reset(self) -> None:
        for key in list(self.counts.keys()):
            self.counts[key] = 0

