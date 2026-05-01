"""
level_2/log_config.py

Logging configuration classes: LogConfig and StructuredFormatter.
No dependency on root_schema.Config — safe to live at level_2.
"""

import json
import logging
from pathlib import Path
from typing import Union

from layers.layer_1_tools.level_0_infra.level_1.paths import LOG_LEVEL


class StructuredFormatter(logging.Formatter):
    """Formatter for structured JSON logging."""

    def __init__(self, use_timestamps: bool = True) -> None:
        super().__init__()
        self.use_timestamps = use_timestamps

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if self.use_timestamps:
            log_data["timestamp"] = self.formatTime(record)
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        return json.dumps(log_data)


class LogConfig:
    """
    Centralized logging configuration management.

    Controls timestamp formatting, log levels, structured logging,
    verbose console output, and default log file locations.

    Example:
        config.set_log_level("DEBUG")
        config.set_structured_logging(True)
    """

    def __init__(self) -> None:
        self.use_timestamps: bool = True
        self.log_level: int = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
        self.verbose_mode: bool = False
        self.use_structured_logging: bool = False
        self.default_log_dir: Path = Path("logs")
        self.formatter: logging.Formatter = logging.Formatter()
        self._update_formatter()

    # ── Formatter ────────────────────────────────────────────────────────────

    def _update_formatter(self) -> None:
        """Rebuild the formatter from current settings."""
        if self.use_structured_logging:
            self.formatter = StructuredFormatter(use_timestamps=self.use_timestamps)
        else:
            fmt = (
                "%(asctime)s — %(levelname)s — %(message)s"
                if self.use_timestamps
                else "%(levelname)s — %(message)s"
            )
            datefmt = "%Y-%m-%d %H:%M:%S" if self.use_timestamps else None
            self.formatter = logging.Formatter(fmt, datefmt)

    def _refresh_handlers(self) -> None:
        """Apply the current formatter to all root-logger handlers."""
        for handler in logging.getLogger().handlers:
            handler.setFormatter(self.formatter)

    # ── Public setters ───────────────────────────────────────────────────────

    def set_timestamps(self, enabled: bool) -> None:
        self.use_timestamps = enabled
        self._update_formatter()
        self._refresh_handlers()

    def set_log_level(self, level: Union[str, int]) -> None:
        self.log_level = (
            getattr(logging, level.upper(), logging.INFO)
            if isinstance(level, str)
            else level
        )
        logging.getLogger().setLevel(self.log_level)

    def set_structured_logging(self, enabled: bool) -> None:
        self.use_structured_logging = enabled
        self._update_formatter()
        self._refresh_handlers()

    def set_verbose_mode(self, enabled: bool) -> None:
        self.verbose_mode = enabled

    def set_default_log_dir(self, path: Union[str, Path]) -> None:
        self.default_log_dir = Path(path)
        self.default_log_dir.mkdir(parents=True, exist_ok=True)


# ── Global singleton ──────────────────────────────────────────────────────────

def _load_global_config() -> LogConfig:
    """Build the module-level LogConfig, optionally seeded from config.yaml."""
    import yaml
    from layers.layer_1_tools.level_0_infra.level_1.paths import get_project_root

    cfg = LogConfig()
    config_path = get_project_root() / "config.yaml"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8", errors="replace") as f:
                yaml_data = yaml.safe_load(f) or {}
            cfg.set_verbose_mode(bool(yaml_data.get("verbose_mode", False)))
        except Exception as exc:
            logging.warning(f"Failed to load verbose_mode from config.yaml: {exc}")
    return cfg


config: LogConfig = _load_global_config()