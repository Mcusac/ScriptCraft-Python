
from typing import Literal, TypeVar

TTool = TypeVar("TTool")

ParserKind = Literal["standard", "dictionary_workflow", "tool", "custom"]
RunStyle = Literal["kwargs", "namespace"]

