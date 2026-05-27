# ============================================================
# constants.py
#
# PURPOSE:
# - Pure constant definitions only
# - No browser logic
# - No transformation logic
# - No orchestration logic
# - No inter-constant dependencies
#
# DESIGN:
# - Stable selectors over raw HTML
# - Explicit semantic naming
# - Playwright/Selenium compatible
# - Centralized DOM references
# - Immutable configuration values
# ============================================================

# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

BUSINESS_UNIT_VALUE = "HS763"

DEFAULT_TIMEOUT_MS = 100_000
DEFAULT_NAVIGATION_TIMEOUT_MS = 30_000

DATE_FORMAT_MM_DD_YYYY = "%m/%d/%Y"


# ============================================================
# ASSET UPDATER URL
# ============================================================

LOGIN_URL = "https://myfs.unt.edu/psp/ps/?cmd=login&languageCd=ENG&"
ASSET_URL = "https://myfs.unt.edu/psp/ps/EMPLOYEE/ERP/c/GBAM_MANAGE_ASSETS.GBAM_CAMPUS_SLFSRV.GBL"

# ============================================================
# SEARCH PAGE SELECTORS
# ============================================================

BUSINESS_UNIT_INPUT_ID = "GBAM_SRCH_VW_BUSINESS_UNIT"
BUSINESS_UNIT_INPUT_SELECTOR = (
    '[id="GBAM_SRCH_VW_BUSINESS_UNIT"]'
)

TAG_NUMBER_INPUT_ID = "GBAM_SRCH_VW_TAG_NUMBER"
TAG_NUMBER_INPUT_SELECTOR = (
    '[id="GBAM_SRCH_VW_TAG_NUMBER"]'
)

ASSET_ID_INPUT_ID = "GBAM_SRCH_VW_ASSET_ID"
ASSET_ID_INPUT_SELECTOR = (
    '[id="GBAM_SRCH_VW_ASSET_ID"]'
)

SEARCH_BUTTON_ID = "PTS_CFG_CL_WRK_PTS_SRCH_BTN"
SEARCH_BUTTON_SELECTOR = (
    '[id="PTS_CFG_CL_WRK_PTS_SRCH_BTN"]'
)


# ============================================================
# ASSET UPDATE PAGE SELECTORS
# ============================================================

DATE_OF_TRANSFER_INPUT_ID = (
    "GBAM_ASSET_REQ_DATE_TRANSFER$0"
)
DATE_OF_TRANSFER_INPUT_SELECTOR = (
    '[id="GBAM_ASSET_REQ_DATE_TRANSFER$0"]'
)

UPDATE_THIS_ASSET_BUTTON_ID = (
    "AM_MY_ASSET_WRK_SUBMIT_PB"
)
UPDATE_THIS_ASSET_BUTTON_SELECTOR = (
    '[id="AM_MY_ASSET_WRK_SUBMIT_PB"]'
)

RETURN_TO_SEARCH_BUTTON_ID = "#ICList"
RETURN_TO_SEARCH_BUTTON_SELECTOR = (
    '[id="#ICList"]'
)

OK_BUTTON_ID = "#ICOK"
OK_BUTTON_SELECTOR = (
    '[id="#ICOK"]'
)

CURRENT_ASSET_LOCATION_CODE_ID = "AM_MY_ASSET_VW_LOCATION$0"
CURRENT_ASSET_LOCATION_CODE_SELECTOR = (
    '[id="AM_MY_ASSET_VW_LOCATION$0"]'
)

CURRENT_ASSET_EMPLOYEE_ID_ID = "AM_MY_ASSET_VW_EMPLID$0"
CURRENT_ASSET_EMPLOYEE_ID_SELECTOR = (
    '[id="AM_MY_ASSET_VW_EMPLID$0"]'
)

OFFSITE_CHECKBOX_SELECTOR = (
    '[id="GBAM_EXTRA_WRK_OFFSITE_SW$0"]'
)

AUTHORIZED_BY_NAME_INPUT_SELECTOR = (
    '[id="GBAM_EXTRA_WRK_NAME1$0"]'
)

OFFSITE_LOCATION_BUILDING = "PCCFR"
OFFSITE_LOCATION_ROOM = "5FE"


# ============================================================
# LOCATION LOOKUP MODAL SELECTORS
# ============================================================

LOCATION_SPYGLASS_BUTTON_ID = (
    "LOCATION_VW_DESCR$prompt$img$0"
)
LOCATION_SPYGLASS_BUTTON_SELECTOR = (
    '[id="LOCATION_VW_DESCR$prompt$img$0"]'
)

LOCATION_CODE_INPUT_ID = "LOCATION_VW_LOCATION"
LOCATION_CODE_INPUT_SELECTOR = (
    '[id="LOCATION_VW_LOCATION"]'
)

LOCATION_LOOKUP_BUTTON_ID = "#ICSearch"

# Scoped modal lookup selector recommended over generic ID.
LOCATION_LOOKUP_BUTTON_SELECTOR = (
    '[id="#ICSearch"]'
)

LOCATION_SEARCH_RESULT_SELECTOR = 'a[name^="RESULT1$"]'

LOOKUP_MODAL_CANCEL_SELECTOR = '[id="#ICCancel"]'


# ============================================================
# CUSTODIAN LOOKUP MODAL SELECTORS
# ============================================================

CUSTODIAN_SPYGLASS_BUTTON_ID = (
    "PERSONAL_DATA_NAME$prompt$img$0"
)
CUSTODIAN_SPYGLASS_BUTTON_SELECTOR = (
    '[id="PERSONAL_DATA_NAME$prompt$img$0"]'
)

EMPLOYEE_ID_INPUT_ID = "PERSONAL_DATA_EMPLID"
EMPLOYEE_ID_INPUT_SELECTOR = (
    '[id="PERSONAL_DATA_EMPLID"]'
)

CUSTODIAN_LOOKUP_BUTTON_ID = "#ICSearch"

# NOTE:
# PeopleSoft reuses #ICSearch across modals.
# Scope usage to active modal during implementation.
CUSTODIAN_LOOKUP_BUTTON_SELECTOR = (
    '[id="#ICSearch"]'
)

EMPLOYEE_SEARCH_RESULT_SELECTOR = (
    'a[name^="RESULT0$"]'
)


# ============================================================
# GENERIC PEOPLE SOFT MODAL SELECTORS
# ============================================================

LOOKUP_MODAL_SELECTOR = '[id="ptModFrame_0"]'

MODAL_CONTENT_FRAME_SELECTOR = (
    'iframe[id^="ptModFrame_"]'
)

MODAL_WAIT_SELECTOR = (
    '.PSMODAL'
)


# ============================================================
# PAGE LOAD / STATE SELECTORS
# ============================================================

PEOPLESOFT_PROCESSING_INDICATOR_SELECTOR = (
    '[id="processing"]'
)

PEOPLESOFT_BODY_SELECTOR = "body"

PEOPLESOFT_MAIN_FORM_SELECTOR = 'form[name="win0"]'


# ============================================================
# OPTIONAL RAW HTML REFERENCES
#
# PURPOSE:
# - Debugging only
# - Human reference only
# - NEVER use as runtime selectors
# ============================================================

BUSINESS_UNIT_INPUT_HTML_REFERENCE = """
<input
    type="text"
    name="GBAM_SRCH_VW_BUSINESS_UNIT"
    id="GBAM_SRCH_VW_BUSINESS_UNIT"
/>
"""

TAG_NUMBER_INPUT_HTML_REFERENCE = """
<input
    type="text"
    name="GBAM_SRCH_VW_TAG_NUMBER"
    id="GBAM_SRCH_VW_TAG_NUMBER"
/>
"""

DATE_OF_TRANSFER_INPUT_HTML_REFERENCE = """
<input
    type="text"
    name="GBAM_ASSET_REQ_DATE_TRANSFER$0"
    id="GBAM_ASSET_REQ_DATE_TRANSFER$0"
/>
"""

LOCATION_SPYGLASS_BUTTON_HTML_REFERENCE = """
<img
    id="LOCATION_VW_DESCR$prompt$img$0"
/>
"""

LOCATION_CODE_INPUT_HTML_REFERENCE = """
<input
    type="text"
    name="LOCATION_VW_LOCATION"
    id="LOCATION_VW_LOCATION"
/>
"""

CUSTODIAN_SPYGLASS_BUTTON_HTML_REFERENCE = """
<img
    id="PERSONAL_DATA_NAME$prompt$img$0"
/>
"""

UPDATE_THIS_ASSET_BUTTON_HTML_REFERENCE = """
<input
    type="button"
    id="AM_MY_ASSET_WRK_SUBMIT_PB"
/>
"""

OK_BUTTON_HTML_REFERENCE = """
<input
    type="button"
    id="#ICOK"
/>
"""

RETURN_TO_SEARCH_BUTTON_HTML_REFERENCE = """
<input
    type="button"
    id="#ICList"
/>
"""

ASSET_ID_INPUT_HTML_REFERENCE = """
<input
    type="text"
    name="GBAM_SRCH_VW_ASSET_ID"
    id="GBAM_SRCH_VW_ASSET_ID"
/>
"""

SEARCH_BUTTON_HTML_REFERENCE = """
<input
    type="button"
    name="PTS_CFG_CL_WRK_PTS_SRCH_BTN"
    id="PTS_CFG_CL_WRK_PTS_SRCH_BTN"
/>
"""


# ============================================================
# AUTHENTICATION STATE DETECTION
# ============================================================

LOGIN_FORM_USERID_SELECTOR = (
    'input[name="userid"]'
)

LOGIN_FORM_PASSWORD_SELECTOR = (
    'input[name="pwd"]'
)

TERMS_ACCEPT_BUTTON_SELECTOR = (
    "#modal-cookie-accept-btn"
)

LOGIN_SUBMIT_BUTTON_SELECTOR = (
    "button.login100-form-btn"
)

TERMS_MODAL_APPEAR_DELAY_MS = 1_500

MFA_DUO_IFRAME_SELECTOR = (
    'iframe[src*="duo"]'
)

MFA_DUO_SECURITY_TEXT_SELECTOR = (
    'text="Duo Security"'
)

# ============================================================
# AUTHENTICATION STATES
# ============================================================

STATE_LOGIN_PAGE = "LOGIN_PAGE"

STATE_MFA_PAGE = "MFA_PAGE"

STATE_AUTHENTICATED = "AUTHENTICATED"

STATE_UNKNOWN = "UNKNOWN"

# ============================================================
# SESSION WAIT CONFIGURATION
# ============================================================

POST_AUTH_TIMEOUT_MS = 120_000

STATE_CHECK_INTERVAL_MS = 2_000

# ============================================================
# MFA PROVIDER DETECTION
# ============================================================

DUO_URL_KEYWORD = "duosecurity.com"

# ============================================================
# DIAGNOSTICS
# ============================================================

DIAGNOSTIC_ALL_TEXT_INPUTS = (
    "input[type='text'], input[type='password']"
)

# ============================================================
# RECONCILIATION OUTPUT (INPUT TO UPDATER)
# ============================================================

LOCATION_CHANGES_CSV = "location_changes.csv"

CUSTODIAN_CHANGES_CSV = "custodian_changes.csv"

ASSET_RECONCILIATION_OUTPUT_DIR = (
    "workspace/output/asset_compare_2026"
)

MERGE_ON_COLUMN = "tag"

# 6-digit tags starting with 3 are used as-is; shorter legacy tags zfill to 8.
TAG_PAD_WIDTH = 8

TAG_NUMBER_ROW_KEYS = (
    "tag",
    "Tag Number",
)

LOCATION_CODE_ROW_KEYS = (
    "new_location",
    "location_norm_forms",
)

EMPLOYEE_ID_ROW_KEYS = (
    "new_custodian_id",
    "user_norm_forms",
)