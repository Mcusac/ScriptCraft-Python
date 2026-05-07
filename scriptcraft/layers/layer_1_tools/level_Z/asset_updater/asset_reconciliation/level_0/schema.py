# ============================================================
# schema.py — PURE DATAFRAME CONTRACTS (NO LOGIC)
# ============================================================

# ============================================================
# ASSET RAW SCHEMA
# ============================================================

ASSET_RAW = {
    "tag": "tag",
    "emp_id": "emp_id",
    "location": "location",
    "custodian": "custodian",
    "description": "description",
}


# ============================================================
# FORM RAW SCHEMA (post-reshape)
# ============================================================

FORM_RAW = {
    "tag": "tag",
    "emp_id": "emp_id",
    "first_name": "first_name",
    "last_name": "last_name",
    "location": "location",
}


# ============================================================
# FORM NORMALIZED SCHEMA
# ============================================================

FORM_NORMALIZED = {
    "tag": "tag",
    "emp_id": "emp_id",
    "location": "location",
    "employee_name": "employee_name",
}


# ============================================================
# MERGED SCHEMA (FINAL DAG OUTPUT CONTRACT)
# ============================================================

MERGED = {
    "tag": "tag",

    "asset_emp_id": "asset_emp_id",
    "asset_location": "asset_location",
    "asset_custodian": "asset_custodian",
    "asset_description": "asset_description",

    "form_emp_id": "form_emp_id",
    "form_employee_name": "form_employee_name",
    "form_location": "form_location",

    "merge_flag": "merge_flag",
}