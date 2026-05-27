"""Wait for selectors across page/iframe contexts."""

import time

from playwright.sync_api import Page

from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    get_context_for_selector,
)


def selector_exists(page: Page, selector: str) -> bool:
    return get_context_for_selector(page, selector) is not None


def wait_for_selector(
    page: Page,
    selector: str,
    timeout_ms: int = 100_000,
) -> None:
    deadline = time.monotonic() + (timeout_ms / 1000)

    def _wait_for_ctx() -> bool:
        ctx = get_context_for_selector(page, selector)
        if ctx is None:
            return False

        remaining_ms = int((deadline - time.monotonic()) * 1000)
        ctx.wait_for_selector(
            selector,
            timeout=max(remaining_ms, 500),
        )
        return True

    if poll_until_deadline(
        _wait_for_ctx,
        timeout_ms=timeout_ms,
        poll_ms=200,
        on_poll=page.wait_for_timeout,
    ):
        return

    raise TimeoutError(f"Timeout waiting for selector: {selector}")
