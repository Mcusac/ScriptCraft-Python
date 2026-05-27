"""Generic callable-map execution helpers."""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def run_nodes(
    data: T,
    nodes: dict[str, Callable[[T], Any]],
) -> dict[str, Any]:
    """Execute named callables against shared input data."""
    return {name: node(data) for name, node in nodes.items()}
