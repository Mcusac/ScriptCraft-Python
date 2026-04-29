from dataclasses import dataclass
from typing import Optional


@dataclass
class LogConfig:
    level: str = "INFO"
    verbose_mode: bool = True
    structured_logging: bool = True
    log_dir: str = "logs"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None