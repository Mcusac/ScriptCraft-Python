"""
Config resolution layer.

Single responsibility:
- Fetch tool configs safely
"""

from typing import Any, Dict, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.root_schema import get_config


def _root() -> Dict[str, Any]:
    return get_config().tool_configs.get("data_content_comparer", {})


def get_domain_config(domain: str) -> Optional[Dict[str, Any]]:
    try:
        return _root().get("domains", {}).get(domain)
    except Exception as e:
        log_and_print(f"⚠️ Domain config error {domain}: {e}", level="warning")
        return None


def get_release_config() -> Dict[str, Any]:
    try:
        return _root().get("release_consistency", {})
    except Exception as e:
        log_and_print(f"⚠️ Release config error: {e}", level="warning")
        return {
            "base_path": "data/domains",
            "release_file_pattern": "HD Release *.csv",
            "release_number_regex": r"HD Release (\d+)",
            "fallback_patterns": ["RP_HD*.xlsx", "HD Release *.xlsx"],
        }