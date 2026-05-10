"""Small types used by the function auditor tool."""

from pathlib import Path
from typing import Any, Dict, List, Union

InputPath = Union[str, Path]
InputPaths = List[InputPath]

AuditResult = Dict[str, Any]
BatchResults = Dict[str, Any]
