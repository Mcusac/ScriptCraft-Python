
import re
from typing import List

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_1_impl.level_0.dictionary_cleaner.fix_counts import FixCounter


def convert_numeric_keys_to_ints(text: str, *, counter: FixCounter) -> str:
    """Convert numeric keys like 1.0 or 2.00 to integers inside {key, value} pairs, skipping ranges like {0-1}."""
    count = 0
    malformed: List[str] = []

    def replace(match: re.Match) -> str:
        nonlocal count, malformed
        content = match.group(1).strip()

        if re.match(r"^\d+(\.\d+)?\s*-\s*\d+(\.\d+)?$", content):
            return f"{{{content}}}"

        if "," not in content:
            malformed.append(content)
            return f"{{{content}}}"

        key, label = content.split(",", 1)
        key = key.strip()
        label = label.strip()

        try:
            key_val = float(key)
            new_key = str(int(key_val)) if key_val.is_integer() else str(key_val)
            if new_key != key:
                count += 1
                key = new_key
        except ValueError:
            pass

        return f"{{{key}, {label}}}"

    new_text = re.sub(r"\{([^{}]+?)\}", replace, text)

    if count > 0:
        counter.inc("Switched numerical representations of categorical variables to integers", count)

    if malformed:
        log_and_print(f"⚠️ Malformed pairs in: {text}")
        for item in malformed:
            log_and_print(f"   - {{{item}}}")

    return new_text

