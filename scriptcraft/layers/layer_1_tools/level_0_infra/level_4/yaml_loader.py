import yaml
from pathlib import Path
from typing import Union

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_2.root_schema import Config
from layers.layer_1_tools.level_0_infra.level_3.legacy_loader import load_legacy_config
from layers.layer_1_tools.level_0_infra.level_3.env_loader import load_from_environment
from layers.layer_1_tools.level_0_infra.level_3.unified_loader import load_unified_config


def load_config_from_yaml(path: Union[str, Path]) -> "Config":
    path = Path(path)

    if not path.exists():
        log_and_print(f"Config file not found: {path}", level="warning")
        return load_from_environment()

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "framework" in data:
        return load_unified_config(data, path)
    else:
        return load_legacy_config(data, path)