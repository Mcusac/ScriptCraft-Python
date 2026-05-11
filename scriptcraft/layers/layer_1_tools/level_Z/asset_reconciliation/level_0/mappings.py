# ============================================================
# mappings.py — EXTERNAL CSV → RAW SCHEMA TRANSFORMATION
# ============================================================

# ============================================================
# ASSET CSV MAPPING
# ============================================================

ASSET_COLUMN_MAP = {
    "Tag Number": "tag",
    "ID": "emp_id",
    "Location": "location",
    "Custodian": "custodian",
    "Descr": "description",
}


# ============================================================
# FORM CSV BASE MAPPING (IMPORTANT: WIDE STRUCTURE HANDLED LATER)
# ============================================================

FORM_BASE_COLUMN_MAP = {
    "Employee ID": "emp_id",
    "First Name": "first_name",
    "Last Name": "last_name",
}