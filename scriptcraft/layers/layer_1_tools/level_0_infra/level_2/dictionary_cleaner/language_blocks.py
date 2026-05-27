
import re

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import FixCounter
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import convert_numeric_keys_to_ints


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

