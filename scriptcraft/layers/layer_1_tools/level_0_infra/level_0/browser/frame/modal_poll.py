"""Lookup modal frame resolution using poll_until_deadline + frame probes."""

from playwright.sync_api import Frame, Page

from scriptcraft.layers.layer_0_core.level_0 import poll_until_deadline

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.browser.frame.probe import (
    frame_has_selector,
    is_ptmod_frame,
)


def get_lookup_modal_frame(
    page: Page,
    anchor_selector: str,
    timeout_ms: int = 30_000,
) -> Frame:
    found_frame: list[Frame | None] = [None]

    def _find_frame() -> bool:
        modal_matches: list[Frame] = []
        other_matches: list[Frame] = []

        for frame in page.frames:
            if not frame_has_selector(frame, anchor_selector):
                continue
            if is_ptmod_frame(frame):
                modal_matches.append(frame)
            else:
                other_matches.append(frame)

        if modal_matches:
            found_frame[0] = modal_matches[0]
            return True
        if other_matches:
            found_frame[0] = other_matches[0]
            return True
        return False

    if poll_until_deadline(
        _find_frame,
        timeout_ms=timeout_ms,
        poll_ms=200,
        on_poll=page.wait_for_timeout,
    ):
        return found_frame[0]  # type: ignore[return-value]

    raise RuntimeError(
        f"Lookup modal frame not found (anchor: {anchor_selector})"
    )


def wait_for_lookup_modal_closed(
    page: Page,
    anchor_selector: str,
    timeout_ms: int = 15_000,
) -> None:
    def _modal_closed() -> bool:
        for frame in page.frames:
            if is_ptmod_frame(frame) and frame_has_selector(frame, anchor_selector):
                return False
        return True

    if poll_until_deadline(
        _modal_closed,
        timeout_ms=timeout_ms,
        poll_ms=200,
        on_poll=page.wait_for_timeout,
    ):
        return

    raise RuntimeError(
        f"Lookup modal did not close within {timeout_ms}ms "
        f"(anchor: {anchor_selector})"
    )
