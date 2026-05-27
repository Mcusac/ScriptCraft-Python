"""Frame introspection (Playwright only; no polling or level_0 barrel)."""

from playwright.sync_api import Frame


def frame_has_selector(frame: Frame, selector: str) -> bool:
    try:
        return frame.query_selector(selector) is not None
    except Exception:
        return False


def is_ptmod_frame(frame: Frame) -> bool:
    return "ptModFrame" in (frame.name or "") or "ptModFrame" in (frame.url or "")


def is_lookup_modal_frame(frame: Frame, *modal_input_selectors: str) -> bool:
    if not is_ptmod_frame(frame):
        return False
    return any(frame_has_selector(frame, sel) for sel in modal_input_selectors)
