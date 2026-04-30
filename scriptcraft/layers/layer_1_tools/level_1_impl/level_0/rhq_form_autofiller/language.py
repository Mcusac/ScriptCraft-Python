from __future__ import annotations

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print


def detect_form_language(driver, logger=None) -> str:
    """
    Detect the form language by looking at the main header.

    Returns:
        'en' or 'es' (defaults to 'en' if detection fails).
    """
    try:
        from selenium.webdriver.common.by import By
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "selenium is required for form language detection. Install it (e.g. `pip install selenium`)."
        ) from e

    try:
        try:
            headers = driver.find_elements(By.TAG_NAME, "h3")
            for header in headers:
                header_text = header.text.strip()
                if "Historia Residencial" in header_text:
                    _log("🌍 Detected form language: es", logger=logger)
                    return "es"
                if "Residential History" in header_text:
                    _log("🌍 Detected form language: en", logger=logger)
                    return "en"
        except Exception:
            pass

        page_text = driver.page_source
        if "Historia Residencial" in page_text:
            _log("🌍 Detected form language: es (from page source)", logger=logger)
            return "es"
        if "Residential History" in page_text:
            _log("🌍 Detected form language: en (from page source)", logger=logger)
            return "en"

        _log("⚠️ Could not detect form language, defaulting to English", logger=logger, level="warning")
        return "en"
    except Exception as e:
        _log(f"⚠️ Error detecting form language: {e}, defaulting to English", logger=logger, level="warning")
        return "en"


def _log(message: str, logger=None, level: str | None = None) -> None:
    if logger:
        if level == "warning":
            logger.warning(message)
        else:
            logger.info(message)
        return

    if level:
        log_and_print(message, level=level)
    else:
        log_and_print(message)

