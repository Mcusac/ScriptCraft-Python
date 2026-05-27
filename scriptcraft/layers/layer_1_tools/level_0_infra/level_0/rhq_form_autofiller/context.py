from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class RHQContext:
  input_file: Path
  output_dir: Path
  log_dir: Path
  data: Dict[str, Any]
  driver: Optional[Any] = None
  logger: Optional[Any] = None

