"""Error-handling helpers for comparison workflows."""

from typing import Any, Callable

from scriptcraft.layers.layer_0_core.level_0 import swallow_errors

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    log_and_print,
)


def _comparison_error_handler(exc: Exception, func_name: str) -> None:
    log_and_print(
        f"❌ Error in {func_name}: "
        f"{type(exc).__name__}: {exc}"
    )


def handle_comparison_errors(
    func: Callable[..., Any],
) -> Callable[..., Any]:
    return swallow_errors(func, on_error=_comparison_error_handler)
