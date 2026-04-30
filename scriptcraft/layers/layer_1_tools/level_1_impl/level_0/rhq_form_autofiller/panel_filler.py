from __future__ import annotations

import time

import pandas as pd

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print

from .constants import FIELD_LABEL_MAPS
from .language import detect_form_language


def fill_panel(driver, panel_idx: int, address_blocks: list, logger=None) -> None:
    try:
        _require_selenium()
        form_language = detect_form_language(driver, logger)

        open_panel(driver, panel_idx)
        panel = get_panel_element(driver, panel_idx)
        ensure_address_blocks(driver, panel, len(address_blocks), form_language)
        remove_extra_address_blocks(driver, panel, len(address_blocks))
        fill_all_blocks(panel, address_blocks, panel_idx, form_language, logger)
    except Exception as e:
        _log(f"⚠️ Could not open/fill panel {panel_idx}: {e}", logger=logger, level="warning")


def open_panel(driver, panel_idx: int) -> None:
    By, _ = _selenium_symbols()
    try:
        panel_header = driver.find_element(By.ID, f"mat-expansion-panel-header-{panel_idx}")
        log_and_print(f"🔍 Opening Panel {panel_idx}...")
        panel_header.click()
        time.sleep(1)
        return
    except Exception:
        pass

    try:
        panel_headers = driver.find_elements(By.CSS_SELECTOR, "mat-expansion-panel-header")
        if panel_idx < len(panel_headers):
            panel_header = panel_headers[panel_idx]
            log_and_print(f"🔍 Opening Panel {panel_idx} (by position)...")
            panel_header.click()
            time.sleep(1)
            return
    except Exception:
        pass

    raise Exception(f"Could not find panel header for panel {panel_idx}")


def get_panel_element(driver, panel_idx: int):
    By, _ = _selenium_symbols()
    try:
        return driver.find_element(By.XPATH, f"//mat-expansion-panel[{panel_idx + 1}]")
    except Exception:
        panels = driver.find_elements(By.TAG_NAME, "mat-expansion-panel")
        if panel_idx < len(panels):
            return panels[panel_idx]
        raise Exception(f"Could not find panel element for panel {panel_idx}")


def remove_extra_address_blocks(driver, panel, required_blocks: int) -> None:
    By, _ = _selenium_symbols()
    panel_content = panel.find_element(By.CSS_SELECTOR, "div.panel-content")
    address_forms = panel_content.find_elements(By.TAG_NAME, "form")
    n_existing = len(address_forms)

    n_to_remove = n_existing - required_blocks
    if n_to_remove <= 0:
        log_and_print("✅ No extra address blocks to remove.")
        return

    log_and_print(f"🗑️ Removing {n_to_remove} extra address block(s).")

    for i in range(n_existing - 1, n_existing - n_to_remove - 1, -1):
        trash_button = address_forms[i].find_element(By.CSS_SELECTOR, ".fas.fa-trash")
        trash_button.click()
        log_and_print(f"🗑️ Removed address block at index {i}.")
        time.sleep(1)

        try:
            confirm_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
            confirm_button.click()
            log_and_print("✅ Confirmed deletion of address block.")
            time.sleep(1)
        except Exception as e:
            log_and_print(f"⚠️ Could not confirm deletion: {e}", level="warning")


def ensure_address_blocks(driver, panel, required_blocks: int, form_language: str = "en") -> None:
    By, _ = _selenium_symbols()
    panel_content = panel.find_element(By.CSS_SELECTOR, "div.panel-content")
    address_forms = panel_content.find_elements(By.TAG_NAME, "form")
    n_existing = len(address_forms)

    log_and_print(f"ℹ️ Address forms detected: {n_existing}")

    n_to_add = required_blocks - n_existing
    for _ in range(n_to_add):
        add_button = _find_add_another_address_button(panel, form_language)
        if not add_button:
            log_and_print("⚠️ Could not find 'Add Another Address' button", level="warning")
            break

        add_button.click()
        log_and_print("➕ Added another address block.")
        time.sleep(1)


def _find_add_another_address_button(panel, form_language: str):
    # 1) language-specific text
    try:
        button_text = FIELD_LABEL_MAPS[form_language].get("Add Another Address")
        if button_text:
            return panel.find_element(By.XPATH, f".//button[.//span[contains(text(), '{button_text}')]]")
    except Exception:
        pass

    # 2) english
    try:
        return panel.find_element(By.XPATH, ".//button[.//span[contains(text(), 'Add Another Address')]]")
    except Exception:
        pass

    # 3) spanish
    try:
        return panel.find_element(By.XPATH, ".//button[.//span[contains(text(), 'Agrega otra dirección')]]")
    except Exception:
        pass

    # 4) icon-based
    try:
        return panel.find_element(By.XPATH, ".//button[.//i[contains(@class, 'fa-address-book')]]")
    except Exception:
        return None


def fill_all_blocks(panel, address_blocks: list, panel_idx: int, form_language: str, logger=None) -> None:
    By, _ = _selenium_symbols()
    panel_content = panel.find_element(By.CSS_SELECTOR, "div.panel-content")
    address_forms = panel_content.find_elements(By.TAG_NAME, "form")

    for idx, (form, block_data) in enumerate(zip(address_forms, address_blocks)):
        _log(f"📝 Filling address block {idx + 1} in panel {panel_idx}...", logger=logger)
        fill_single_block(form, block_data, form_language, logger)


def fill_single_block(form, block_data: dict, form_language: str, logger=None) -> None:
    for col, val in block_data.items():
        if pd.isna(val) or not str(val).strip() or str(val).strip().upper() == "MISSING":
            _log(f"⚠️ Skipping empty/missing field: {col}", logger=logger)
            continue

        try:
            if col == "Questionable Validity":
                fill_checkbox(form, val, form_language, logger)
                continue

            if col in ["StreetNumber", "Zip Code"] and isinstance(val, (int, float)):
                val = str(int(val))

            fill_input_field(form, col, val, form_language, logger)
        except Exception as e:
            _log(f"⚠️ Could not enter {col}: {e}", logger=logger, level="warning")


def fill_checkbox(panel, val: str, form_language: str, logger=None) -> None:
    By, _ = _selenium_symbols()
    if str(val).strip() != "1":
        return

    checkbox_label = FIELD_LABEL_MAPS[form_language].get("Questionable Validity", "Questionable Validity")

    # Prefer "last checkbox" heuristic first.
    try:
        checkboxes = panel.find_elements(By.CSS_SELECTOR, "mat-checkbox")
        if checkboxes:
            checkbox = checkboxes[-1]
            input_checkbox = checkbox.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            if not input_checkbox.is_selected():
                checkbox.click()
                _log(f"✅ {checkbox_label}: Checked (1)", logger=logger)
            return
    except Exception:
        pass

    # Fallback: label-based match.
    try:
        checkbox = panel.find_element(By.XPATH, f".//mat-checkbox[.//span[contains(text(), '{checkbox_label}')]]")
        input_checkbox = checkbox.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        if not input_checkbox.is_selected():
            checkbox.click()
            _log(f"✅ {checkbox_label}: Checked (1)", logger=logger)
    except Exception as e:
        _log(f"⚠️ Could not find/check {checkbox_label} checkbox: {e}", logger=logger, level="warning")


def fill_input_field(panel, label: str, value: str, form_language: str, logger=None) -> None:
    By, Keys = _selenium_symbols()
    real_label = FIELD_LABEL_MAPS[form_language].get(label, label)

    form_field = _find_form_field(panel, label=label, real_label=real_label, form_language=form_language)
    if form_field is None:
        _log(f"⚠️ Could not find field for {label} (expected label: {real_label})", logger=logger, level="warning")
        return

    try:
        input_element = form_field.find_element(By.CSS_SELECTOR, "input, textarea")
        input_element.send_keys(Keys.CONTROL + "a")
        input_element.send_keys(Keys.BACKSPACE)

        if value and str(value).strip():
            input_element.send_keys(str(value).strip())
            _log(f"✅ {label}: {value}", logger=logger)
    except Exception as e:
        _log(f"⚠️ Could not enter {label}: {e}", logger=logger, level="warning")


def _find_form_field(panel, label: str, real_label: str, form_language: str):
    By, _ = _selenium_symbols()
    # 1) exact match
    try:
        return panel.find_element(
            By.XPATH,
            f".//mat-form-field[.//mat-label[normalize-space(text())='{real_label}']]",
        )
    except Exception:
        pass

    # 2) case-insensitive match
    try:
        return panel.find_element(
            By.XPATH,
            ".//mat-form-field[.//mat-label["
            "translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')="
            f"translate('{real_label}', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"
            "]]",
        )
    except Exception:
        pass

    # 3) contains match
    try:
        return panel.find_element(
            By.XPATH,
            f".//mat-form-field[.//mat-label[contains(normalize-space(text()), '{real_label}')]]",
        )
    except Exception:
        pass

    # 4) if mapped and non-English, fallback to English label
    if form_language != "en" and label in FIELD_LABEL_MAPS.get(form_language, {}):
        try:
            english_label = FIELD_LABEL_MAPS["en"].get(label, label)
            return panel.find_element(
                By.XPATH,
                f".//mat-form-field[.//mat-label[normalize-space(text())='{english_label}']]",
            )
        except Exception:
            pass

    return None


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


def _require_selenium() -> None:
    _selenium_symbols()


def _selenium_symbols():
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "selenium is required for RHQ form filling. Install it (e.g. `pip install selenium`)."
        ) from e
    return By, Keys

