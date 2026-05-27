from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ASSET_RAW,
    FORM_NORMALIZED,
    FORM_RAW,
    MERGED,
)

# ----------------------------
# REQUIRED INPUT CONTRACTS
# ----------------------------

ASSET_REQUIRED_COLUMNS = [
    ASSET_RAW.tag,
    ASSET_RAW.emp_id,
    ASSET_RAW.location,
    ASSET_RAW.custodian,
    ASSET_RAW.description,
]

FORM_REQUIRED_COLUMNS = [
    FORM_RAW.tag,
    FORM_RAW.emp_id,
    FORM_RAW.location,
    FORM_NORMALIZED.employee_name,
]


# ----------------------------
# RENAME MAPS (DRY FIX)
# ----------------------------

ASSET_TO_MERGED_MAP = {
    ASSET_RAW.emp_id: MERGED.asset_emp_id,
    ASSET_RAW.location: MERGED.asset_location,
    ASSET_RAW.custodian: MERGED.asset_custodian,
    ASSET_RAW.description: MERGED.asset_description,
}

FORM_TO_MERGED_MAP = {
    FORM_RAW.emp_id: MERGED.form_emp_id,
    FORM_RAW.location: MERGED.form_location,
    FORM_NORMALIZED.employee_name: MERGED.form_employee_name,
}