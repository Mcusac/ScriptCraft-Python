from pathlib import Path
from typing import Optional, Union

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


class LoggingMixin:
    """Handles all logging concerns."""

    name: str

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