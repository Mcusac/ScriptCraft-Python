"""Reusable page wait primitives for asset-updater orchestration."""

from collections.abc import Callable
from playwright.sync_api import Page

from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline

DEFAULT_POLL_MS = 200


def wait_until_page_condition(
    page: Page,
    condition: Callable[[], bool],
    *,
    timeout_ms: int,
    poll_ms: int = DEFAULT_POLL_MS,
) -> bool:
    """Poll until a page condition is true or the timeout expires."""
    return poll_until_deadline(
        condition,
        timeout_ms=timeout_ms,
        poll_ms=poll_ms,
        on_poll=page.wait_for_timeout,
    )
