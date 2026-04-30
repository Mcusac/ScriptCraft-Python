"""DataContentComparer tool implementation (level_1)."""

from pathlib import Path
from typing import Any, Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.data_content_comparer_plugins import get_plugin, list_plugins
from layers.layer_1_tools.level_1_impl.level_0.data_content_comparer.logging_setup import resolve_log_dir, setup_file_logging


class DataContentComparer(BaseTool):
    """Tool for comparing content between datasets."""

    def __init__(self) -> None:
        super().__init__(
            name="Data Content Comparer",
            description="📊 Compares content between datasets and generates detailed reports",
            tool_name="data_content_comparer",
        )

        setup_file_logging(log_dir=resolve_log_dir(self.config))

    def run(
        self,
        mode: Optional[str] = None,
        input_paths: Optional[list[Union[str, Path]]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        domain: Optional[str] = None,
        output_filename: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        _ = output_filename  # reserved; handled by mode plugins today

        self.log_start()

        try:
            output_path = self.resolve_output_directory(output_dir or self.default_output_dir)

            resolved_mode = mode or "standard"

            plugin_func = get_plugin(resolved_mode)
            if not plugin_func:
                raise ValueError(
                    f"❌ Unknown mode '{resolved_mode}'. Available modes: {list_plugins()}"
                )

            if resolved_mode in ["release_consistency", "release"]:
                if input_paths and len(input_paths) >= 2:
                    log_and_print(f"📁 Manual file comparison mode with {len(input_paths)} files")
                elif domain:
                    log_and_print(f"📊 Domain-based comparison for: {domain}")
                else:
                    log_and_print("📊 Processing all available domains")
            else:
                if not self.validate_input_files(input_paths or [], required_count=2):
                    raise ValueError("❌ Need at least two input files to compare")

            log_and_print(f"🔧 Running {resolved_mode} mode...")
            plugin_func(
                input_paths=input_paths or [],
                output_dir=output_path,
                domain=domain,
                **kwargs,
            )

            self.log_completion(output_path)
        except Exception as e:
            self.log_error(f"Comparison failed: {e}")
            raise

