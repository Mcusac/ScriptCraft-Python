"""Dictionary file auto-discovery for a dataset file."""

from pathlib import Path
from typing import Optional, Union


def find_dictionary_file(input_path: Union[str, Path], domain: Optional[str]) -> Path:
    """Find the appropriate dictionary file for the given input and domain."""

    input_path = Path(input_path)

    if domain:
        candidates = [
            input_path.parent / f"{domain}_dictionary.csv",
            input_path.parent / f"{domain}_dictionary.xlsx",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate

    for name in [
        "dictionary.csv",
        "dictionary.xlsx",
        "data_dictionary.csv",
        "data_dictionary.xlsx",
    ]:
        candidate = input_path.parent / name
        if candidate.exists():
            return candidate

    raise FileNotFoundError(f"No dictionary file found for {input_path}")

