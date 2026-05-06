# ============================================================
# schema.py — canonical dataframe contracts (clean 3-layer model)
#
# DESIGN RULES:
# 1. RAW schema = direct CSV ingestion fields ONLY
# 2. NORMALIZED schema = transformed / derived fields
# 3. MERGED schema = final system contract
# ============================================================


# ============================================================
# 0. INGESTION MAPPINGS (CSV → RAW schema)
# ============================================================

ASSET_COLUMN_MAP = {
    "Tag Number": "tag",
    "ID": "emp_id",
    "Location": "location",
    "Custodian": "custodian",
    "Descr": "description",
}

FORM_COLUMN_MAP = {
    "Device Tag": "tag",
    "Employee ID": "emp_id",
    "First Name": "first_name",
    "Last Name": "last_name",
    "Location of Device (ie HP 505 or Off Campus)": "location",
}


def standardize_columns(df, column_map: dict):
    """
    Converts raw CSV columns → RAW schema fields.
    Must be run before any normalization logic.
    """
    return df.rename(columns=column_map)


# ============================================================
# 1. RAW SCHEMA (direct ingestion layer ONLY)
# ============================================================

class AssetRawSchema:
    tag = "tag"
    emp_id = "emp_id"
    location = "location"
    custodian = "custodian"
    description = "description"


ASSET_RAW = AssetRawSchema()


class FormRawSchema:
    tag = "tag"
    emp_id = "emp_id"
    first_name = "first_name"
    last_name = "last_name"
    location = "location"


FORM_RAW = FormRawSchema()


# ============================================================
# 2. NORMALIZED SCHEMA (post-transform / derived fields)
# ============================================================

class FormNormalizedSchema:
    tag = "tag"
    emp_id = "emp_id"
    location = "location"
    employee_name = "employee_name"   # derived from first + last


FORM_NORMALIZED = FormNormalizedSchema()


# ============================================================
# 3. MERGED SCHEMA (final system contract)
# ============================================================

class MergedSchema:
    # identity
    tag = "tag"

    # asset side
    asset_emp_id = "asset_emp_id"
    asset_location = "asset_location"
    asset_custodian = "asset_custodian"
    asset_description = "asset_description"

    # form side (normalized only)
    form_emp_id = "form_emp_id"
    form_employee_name = "form_employee_name"
    form_location = "form_location"

    # merge metadata
    merge_flag = "merge_flag"


MERGED = MergedSchema()


# ============================================================
# 4. DOMAIN CONSTANTS
# ============================================================

OFF_CAMPUS_CANONICAL = "PCCFR  5FE"

ASSET_DESCRIPTION_PREFIX = "computer"

DEVICE_SLOTS = ["", "1", "2", "3", "4"]


# ============================================================
# 5. VALIDATION HELPERS
# ============================================================

def require_columns(df, required: list[str], context: str = ""):
    """
    Fail fast if dataframe is missing expected columns.
    """
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(
            f"[SCHEMA ERROR] Missing columns in {context}: {missing}"
        )


def assert_merged_schema(df):
    """
    Validates final merged contract structure.
    """
    require_columns(
        df,
        [
            MERGED.tag,
            MERGED.asset_location,
            MERGED.form_location,
            MERGED.merge_flag,
        ],
        context="MERGED dataframe",
    )