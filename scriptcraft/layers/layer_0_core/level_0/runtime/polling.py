"""Framework-agnostic deadline polling primitive."""

import time
from collections.abc import Callable


def poll_until_deadline(
    condition: Callable[[], bool],
    *,
    timeout_ms: int,
    poll_ms: int,
    on_poll: Callable[[int], None] | None = None,
) -> bool:
    """Poll condition until it returns True or timeout elapses."""
    deadline = time.monotonic() + (timeout_ms / 1000)

    while time.monotonic() < deadline:
        if condition():
            return True
        if on_poll is not None:
            on_poll(poll_ms)

    return False
