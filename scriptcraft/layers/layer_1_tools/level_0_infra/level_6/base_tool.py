"""
Base Classes Module

Provides a SINGLE, DRY base class for ALL tools.
"""

import logging
import pandas as pd

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable

from layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.environment_resolver import EnvironmentResolver
from layers.layer_1_tools.level_0_infra.level_1.config_accessors import (
    get_tool_config,
    get_pipeline_step,
)
from layers.layer_1_tools.level_0_infra.level_5.config import load_config


class BaseTool(ABC):
    """Universal base class for ALL tools."""

    def __init__(
        self,
        name: str,
        description: str,
        supported_formats: Optional[List[str]] = None,
        tool_name: Optional[str] = None,
        requires_dictionary: bool = False,
    ) -> None:
        self.name = name
        self.description = description
        self.logger = logging.getLogger(name)
        self.supported_formats = supported_formats or ['.csv', '.xlsx', '.xls']
        self.requires_dictionary = requires_dictionary
        self.tool_name = tool_name or name.lower().replace(' ', '_')

        # Lazy config (NO side effects)
        self._config = None

    # ===== CONFIG =====

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

    # ===== LOGGING =====

    def log_message(self, message: str, level: str = "info") -> None:
        log_and_print(message, level=level)

    def log_start(self) -> None:
        self.log_message(f"🚀 Starting {self.name}...")

    def log_completion(self, output_path: Optional[Path] = None) -> None:
        if output_path:
            self.log_message(f"✅ {self.name} completed: {output_path}")
        else:
            self.log_message(f"✅ {self.name} completed")

    def log_error(self, error: Union[str, Exception]) -> None:
        self.log_message(f"❌ {self.name} error: {error}", level="error")

    # ===== ENVIRONMENT =====

    def resolve_input_directory(
        self,
        input_dir: Optional[Union[str, Path]] = None,
    ) -> Path:
        return EnvironmentResolver.resolve_input_directory(input_dir, self.config)

    def resolve_output_directory(
        self,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Path:
        path = EnvironmentResolver.resolve_output_directory(output_dir, self.config)
        ensure_output_dir(path)
        return path

    # ===== FILE VALIDATION =====

    def validate_input_files(
        self,
        input_paths: List[Union[str, Path]],
        required_count: Optional[int] = None,
    ) -> bool:
        if not input_paths:
            self.log_error("No input paths provided")
            return False

        if required_count and len(input_paths) < required_count:
            self.log_error(f"Need {required_count}, got {len(input_paths)}")
            return False

        for path in input_paths:
            path = Path(path)

            if not path.exists():
                self.log_error(f"Missing file: {path}")
                return False

            if path.suffix.lower() not in self.supported_formats:
                self.log_error(f"Unsupported type: {path.suffix}")
                return False

        return True

    # ===== FILE I/O (still here, but now isolated concern) =====

    def load_data_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        file_path = Path(file_path)

        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        self.log_message(f"📂 Loaded {file_path.name}: {df.shape}")
        return df

    def save_data_file(
        self,
        data: pd.DataFrame,
        output_path: Union[str, Path],
        include_index: bool = False,
    ) -> Path:
        output_path = Path(output_path)
        ensure_output_dir(output_path.parent)

        if output_path.suffix.lower() == '.csv':
            data.to_csv(output_path, index=include_index)
        else:
            data.to_excel(output_path, index=include_index)

        self.log_message(f"💾 Saved: {output_path}")
        return output_path

    # ===== UTILITIES =====

    def compare_dataframes(
        self,
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        compare_columns: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        comparison = {
            'shape_difference': df1.shape != df2.shape,
            'df1_shape': df1.shape,
            'df2_shape': df2.shape,
            'column_differences': set(df1.columns) ^ set(df2.columns),
            'common_columns': set(df1.columns) & set(df2.columns),
        }

        if compare_columns:
            comparison['column_differences'] = (
                set(compare_columns) ^ set(df1.columns) ^ set(df2.columns)
            )

        return comparison

    def run_with_error_handling(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        self.log_start()
        try:
            result = func(*args, **kwargs)
            self.log_completion()
            return result
        except Exception as e:
            self.log_error(e)
            raise

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass