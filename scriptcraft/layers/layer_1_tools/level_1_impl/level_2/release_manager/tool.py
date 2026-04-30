
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.release_manager_plugins.registry import ReleaseWorkflowRegistry
from layers.layer_1_tools.level_1_impl.level_1.release_manager_plugins import (
    load_builtin_plugins,
)

class ReleaseManager(BaseTool):
    """Tool for automated release management with plugin-based workflows."""

    def __init__(self) -> None:
        super().__init__(
            name="Release Manager",
            description="🚀 Automated release management for Python packages with plugin-based workflows",
            tool_name="release_manager",
        )

        self.workflow_registry = ReleaseWorkflowRegistry()
        self._load_plugins()

    def _load_plugins(self) -> None:
        """Load available release plugins."""
        try:
            load_builtin_plugins(self.workflow_registry)
            self._load_custom_plugins()
        except Exception as e:
            log_and_print(f"⚠️ Could not load plugins: {e}", level="warning")

    def _load_custom_plugins(self) -> None:
        """Load custom plugins from plugins directory."""
        plugins_dir = Path(__file__).parent / "plugins"
        if plugins_dir.exists():
            for plugin_file in plugins_dir.glob("*.py"):
                if plugin_file.name.startswith("custom_") and plugin_file.name != "__init__.py":
                    try:
                        plugin_name = plugin_file.stem.replace("custom_", "")
                        log_and_print(f"🔌 Loading custom plugin: {plugin_name}")
                    except Exception as e:
                        log_and_print(
                            f"⚠️ Failed to load custom plugin {plugin_file.name}: {e}",
                            level="warning",
                        )

    def run(
        self,
        mode: Optional[str] = None,
        input_paths: Optional[List[Union[str, Path]]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        domain: Optional[str] = None,
        output_filename: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Run the release management process.

        Args:
            mode: Release mode (e.g., 'python_package', 'workspace', 'custom')
            input_paths: List containing paths to files/directories to release
            output_dir: Directory to save release artifacts
            domain: Optional domain context
            output_filename: Optional custom output filename
            **kwargs: Plugin-specific args (version_type, auto_push, force, custom_message, skip_pypi, etc.)
        """
        self.log_start()
        try:
            if not mode:
                mode = "python_package"

            plugin_func = self.workflow_registry.get_workflow(mode)
            if not plugin_func:
                available_modes = self.workflow_registry.list_workflows()
                raise ValueError(f"❌ Unknown mode '{mode}'. Available modes: {available_modes}")

            log_and_print(f"🔧 Running {mode} release mode...")
            plugin_func(
                input_paths=input_paths or [],
                output_dir=output_dir or self.default_output_dir,
                domain=domain,
                **kwargs,
            )

            self.log_completion()
        except Exception as e:
            self.log_error(f"Release failed: {e}")
            raise

    def list_available_modes(self) -> List[str]:
        """List all available release modes."""
        return self.workflow_registry.list_workflows()

    def get_plugin_info(self, mode: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific plugin."""
        return self.workflow_registry.get_workflow_info(mode)

