"""Generic retry helper built on deadline polling."""

import time

from collections.abc import Callable
from typing import TypeVar

from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline

T = TypeVar("T")


def retry_until_success(
    operation: Callable[[], T],
    *,
    timeout_ms: int,
    poll_ms: int = 100,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T | None:
    """
    Retry operation until it succeeds without raising, or timeout elapses.

    Returns the last successful result, or None if timed out.
    """
    result: T | None = None
    last_error: BaseException | None = None

    def _condition() -> bool:
        nonlocal result, last_error
        try:
            result = operation()
            last_error = None
            return True
        except BaseException as exc:
            last_error = exc
            return False

    if poll_until_deadline(
        _condition,
        timeout_ms=timeout_ms,
        poll_ms=poll_ms,
        on_poll=lambda ms: sleep_fn(ms / 1000),
    ):
        return result

    if last_error is not None:
        raise last_error
    return None
