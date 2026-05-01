# ✅ CLEANED PSEUDO-CODE (STRUCTURED + LOOP-DEFINED)
# 🔹 PHASE 0 — DATA PREPARATION (RUN ONCE)
# Load user_changed.csv
    # columns: Tag Number, user_norm_forms

# Load location_changed.csv
    # columns: Tag Number, location_norm_forms

# Normalize Tag Number in BOTH datasets
    # ensure all Tag Numbers are strings
    # pad left with zeros to length 12 (or required system length)
    # example: "12345" → "000000012345"

# Merge datasets on Tag Number (inner join preferred)
    # result contains:
        # Tag Number
        # user_norm_forms (employee id)
        # location_norm_forms (formatted location string)

# Drop duplicates based on Tag Number (keep first or last, define rule explicitly)

# Convert merged dataset into iterable list of records:
    # records = [
    #     {
    #         tag_number,
    #         employee_id,
    #         location_code
    #     },
    #     ...
    # ]


# 🔹 PHASE 1 — OPEN BROWSER + INITIAL NAVIGATION (RUN ONCE)
# Open browser
# Navigate to Asset Updater page

# If first login of the day:
    # complete login flow
    # complete Duo Mobile authentication if prompted

# Wait until Asset Updater page fully loads

# 🔹 PHASE 2 — STATIC FIELD SETUP (RUN ONCE)
# Set Business Unit (DO NOT CHANGE DURING LOOP)
    # find input GBAM_SRCH_VW_BUSINESS_UNIT
    # enter "HS763"


# 🔹 PHASE 3 — MAIN LOOP (CORE LOGIC)
# FOR each record IN records:

    # ------------------------------------------------------------
    # 🔸 STEP A — RESET SEARCH STATE
    # ------------------------------------------------------------

    # Clear Asset ID field (IMPORTANT: prevents carryover)
        # find GBAM_SRCH_VW_ASSET_ID
        # set value = ""

    # ------------------------------------------------------------
    # 🔸 STEP B — SEARCH BY TAG NUMBER
    # ------------------------------------------------------------

    # Enter Tag Number
        # find GBAM_SRCH_VW_TAG_NUMBER
        # enter record.tag_number

    # Click Search
        # click PTS_CFG_CL_WRK_PTS_SRCH_BTN

    # Wait for results page load

    # ------------------------------------------------------------
    # 🔸 STEP C — OPEN ASSET RECORD
    # ------------------------------------------------------------

    # Click result row matching Tag Number (if needed)
    # Wait for asset detail page to load

    # ------------------------------------------------------------
    # 🔸 STEP D — SET TRANSFER DATE
    # ------------------------------------------------------------

    # Click Date of Transfer field
    # Enter current date (MM/DD/YYYY)

    # ------------------------------------------------------------
    # 🔸 STEP E — SET LOCATION (SPYGLASS FLOW)
    # ------------------------------------------------------------

    # Click Location spyglass
    # Wait for modal

    # Enter Location Code
        # find LOCATION_VW_LOCATION
        # enter record.location_code

    # Click Look Up
    # Wait for results

    # Click matching result row
    # Wait for modal close

    # ------------------------------------------------------------
    # 🔸 STEP F — SET CUSTODIAN (SPYGLASS FLOW)
    # ------------------------------------------------------------

    # Click Custodian spyglass
    # Wait for modal

    # Enter Employee ID
        # find employee lookup input
        # enter record.employee_id

    # Click Look Up
    # Wait for results

    # Click matching Employee ID row
    # Wait for modal close

    # ------------------------------------------------------------
    # 🔸 STEP G — SUBMIT UPDATE
    # ------------------------------------------------------------

    # Click "Update this Asset"
    # Wait for confirmation modal

    # Click OK

    # ------------------------------------------------------------
    # 🔸 STEP H — RETURN TO SEARCH (LOOP RESET POINT)
    # ------------------------------------------------------------

    # Click "Return to Search"
    # Wait for page reload

    # ------------------------------------------------------------
    # 🔸 LOOP END
    # ------------------------------------------------------------

# END FOR