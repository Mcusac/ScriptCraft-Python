
import re

from layers.layer_1_tools.level_1_impl.level_0.dictionary_cleaner.fix_counts import FixCounter
from layers.layer_1_tools.level_1_impl.level_1.dictionary_cleaner.numeric_keys import convert_numeric_keys_to_ints


def fix_language_blocks(text: str, counter: FixCounter) -> str:
    """Fix bilingual value blocks like [Spanish = {...} {...}] [English = {...} {...}]"""

    def fix_block(match: re.Match) -> str:
        content = match.group(1)
        fixed_content = re.sub(
            r"\{(\d+(?:\.\d+)?)\s*[:=]?\s*([^\{\}]+?)\}",
            r"{\1, \2}",
            content,
        )
        fixed_content = convert_numeric_keys_to_ints(fixed_content, counter=counter)
        return f"[{fixed_content}]"

    pattern = r"\[([^\[\]]*?=\s*(?:\{.*?\}\s*)+)\]"
    return re.sub(pattern, fix_block, text)

