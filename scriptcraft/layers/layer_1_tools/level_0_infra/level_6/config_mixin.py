from typing import Any, Dict

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
    get_pipeline_step,
    get_tool_config,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_5 import load_config


class ConfigMixin:
    """Handles config loading + access."""

    _config = None
    tool_name: str

    @property
    def config(self):
        if self._config is None:
            try:
                self._config = load_config("config.yaml")
                self.log_message("📋 Configuration loaded")
            except Exception as e:
                self.log_message(f"⚠️ Config load failed: {e}", level="warning")
                self._config = None
        return self._config

    def get_tool_config(self) -> Dict[str, Any]:
        if self.config:
            try:
                return get_tool_config(self.config, self.tool_name)
            except Exception:
                pass
        return {}

    def get_pipeline_step(self, step_name: str) -> Dict[str, Any]:
        if self.config:
            try:
                return get_pipeline_step(self.config, step_name)
            except Exception:
                pass
        return {}