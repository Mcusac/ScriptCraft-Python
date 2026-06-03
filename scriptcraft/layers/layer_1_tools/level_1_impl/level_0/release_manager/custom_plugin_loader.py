"""Release-manager workflow plugins (delegates to infra file plugin loader)."""

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    PluginWorkflowRegistryProtocol,
    log_and_print,
    load_plugins,
)

MODE_ATTR = "MODE"
WORKFLOW_ATTR = "WORKFLOW"
INFO_ATTR = "INFO"


def load_custom_plugins(
    registry: PluginWorkflowRegistryProtocol,
    plugins_dir: Path,
    pattern: str = "custom_*.py",
) -> int:
    """
    Load release workflow plugins from ``plugins_dir``.

    Per-file failures are logged and skipped; returns count of successfully loaded plugins.
    """

    def _emit(message: str) -> None:
        prefix = ""
        if message.startswith("Plugin directory not found"):
            prefix = "⚠️ "
        elif message.startswith("Skipping duplicate"):
            prefix = "⚠️ "
        elif message.startswith("Failed to load"):
            prefix = "❌ "
        elif message.startswith("Loaded plugin"):
            prefix = "✅ "
            message = message.replace("Loaded plugin", "Loaded custom plugin", 1)
        log_and_print(f"{prefix}{message}" if prefix else message)

    return load_plugins(
        registry,
        plugins_dir,
        pattern=pattern,
        mode_attr=MODE_ATTR,
        workflow_attr=WORKFLOW_ATTR,
        info_attr=INFO_ATTR,
        on_message=_emit,
    )