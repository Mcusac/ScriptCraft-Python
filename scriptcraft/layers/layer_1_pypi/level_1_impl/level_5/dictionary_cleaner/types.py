"""Small types used by the dictionary cleaner tool."""

from pathlib import Path
from typing import List, Optional, Union

InputPath = Union[str, Path]
InputPaths = List[InputPath]

OptionalStr = Optional[str]
