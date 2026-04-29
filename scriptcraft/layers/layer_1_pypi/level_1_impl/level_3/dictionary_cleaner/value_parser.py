
import re
from typing import Union

import pandas as pd

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_1.cleaning import (
    fix_numeric_dash_inside_braces,
    fix_word_number_dash_inside_braces,
    parse_missing_unit,
    prevent_pipe_inside_braces,
)

from layers.layer_1_pypi.level_1_impl.level_0.dictionary_cleaner.fix_counts import FixCounter
from layers.layer_1_pypi.level_1_impl.level_1.dictionary_cleaner.numeric_keys import convert_numeric_keys_to_ints
from layers.layer_1_pypi.level_1_impl.level_2.dictionary_cleaner.language_blocks import fix_language_blocks


def parse_values(value: Union[str, float, None], *, filename: str, counter: FixCounter) -> Union[str, float, None]:
    if pd.isna(value) or value in ["Numeric", "Text", "Mm/YYYY"]:
        return value

    original_value = value

    fixed_braces = re.sub(r"\}\s*\{", "} {", value)
    if original_value != fixed_braces:
        counter.inc("Curly brace spacing fixed")

    if "biomarkers" in filename.lower():
        fixed_spaces = re.sub(r"(?<!\{)\s{2,}(?!\})", " | ", fixed_braces)
        if fixed_braces != fixed_spaces:
            counter.inc("Multiple spaces replaced with ' | '")
        fixed_pipe_separation = prevent_pipe_inside_braces(fixed_spaces)
    else:
        fixed_pipe_separation = fixed_braces

    fixed = fixed_pipe_separation
    fixed = fix_language_blocks(fixed, counter)

    fixed = re.sub(r"\{([^{}]*?),\s*(\d+\s*[:=])", r"{\1} {\2", fixed)
    fixed = re.sub(r"(?<!\{)(\d+(?:\.\d+)?)[\s]*[:=][\s]*([^\{\}]+)(?!\})", r"{\1, \2}", fixed)

    steps = [
        (r"\{([^{}]*?)(?:\s*[=:]\s*)([^{}]*?)\}", r"{\1, \2}", "Normalized = or : to comma"),
        (r"(\{[^,]+),\s*([^\}]+)", r"\1, \2", "Ensure space after comma in '{}' pairs"),
        (r"\{(\d+(?:\.\d+)?)\s+([^\{\}]+?)\}", r"{\1, \2}", "Inserted missing comma between key and label"),
        (r"\{(\.)", r"{0.", "Leading zero added inside '{}'"),
        (r"(\d)([A-Za-z])", r"\1 \2", "Missing space between number and word fixed"),
        (r"\s*/\s*", "/", "Removed spaces before and after '/' for consistency"),
        (r"(\{[^}]+)\]", r"\1}", "Replaced incorrect ']' inside '{}'"),
        (r"(?<=\w)\[", "[", "Ensured `[` remains for labels"),
        (r"\((\d+\.\d+, [^\}]+?)\}", r"{\1}", "Replaced incorrect '(' with '{'"),
        (r"\{\s+", "{", "Removed extra spaces after '{'"),
        (r"(\[\d+-\d+)}", r"\1]", "Fixed incorrect `}` in numeric ranges"),
        (r"(\d)\s+,", r"\1,", "Removed space before a comma"),
        (r"\}\s*,\s*\{", "} {", "Remove commas between `{}` pairs"),
        (r"\} {", "} {", "Ensured exactly one space between '{}' pairs"),
        (r"\s*=\s*", " = ", "Add space before and after '='"),
        (r"\{\s*([^}]*\S)\s*\}", r"{\1}", "Removed trailing spaces inside '{}'"),
        (r"\s+-\s*$", "", "Removed random trailing ' - '"),
        (r"[''`´ʹ]", "'", None),
        (r"\b[Dd]on[''`]?[Tt]+\b", "Don't", "Fixed incorrect 'Don't' capitalization"),
        (r"-(\{)", r" - \1", "Added space before '{' following '-'"),
        (r" {2,}", " ", "Collapsed multiple spaces to single space"),
    ]

    for pattern, repl, desc in steps:
        updated = re.sub(pattern, repl, fixed)
        if updated != fixed and desc:
            counter.inc(desc)
        fixed = updated

    dash_fixed = fix_numeric_dash_inside_braces(fixed)
    if fixed != dash_fixed:
        counter.inc("Removed spaces around '-' between numbers inside '{}'")

    word_dash_fixed = fix_word_number_dash_inside_braces(dash_fixed)

    if fixed.count("{") > fixed.count("}"):
        log_and_print(f"⚠️ Detected unclosed brace in: {fixed}")

    try:
        converted = convert_numeric_keys_to_ints(word_dash_fixed, counter=counter)
    except Exception as e:
        log_and_print(f"❌ Failed to convert numeric keys for value: {word_dash_fixed} → {e}")
        converted = word_dash_fixed

    return converted


def parse_missing_or_unit(value: Union[str, float, None]) -> Union[str, float, None]:
    return parse_missing_unit(value)

