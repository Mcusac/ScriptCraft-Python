# ============================================================
# constants.py — DOMAIN CONFIGURATION (NO LOGIC)
# ============================================================

# ============================================================
# OFF-CAMPUS NORMALIZATION
# ============================================================

OFF_CAMPUS_CANONICAL = "PCCFR  5FE"


# ============================================================
# ASSET FILTERING RULES
# ============================================================

ASSET_DESCRIPTION_PREFIX = "computer"


# ============================================================
# FORM STRUCTURE CONFIG
# ============================================================

DEVICE_SLOT_COUNT = 5


# ============================================================
# FORM WIDE STRUCTURE DEFINITION
# ============================================================

FORM_REPEATED_GROUPS = {
    "device_tag": "Device Tag",
    "location": "Location of Device (ie HP 505 or Off Campus)",
    "status": "How is the device working?",
    "need_device": "Are you still in need of your device?",
    "is_last": "Is this your last device?",
}