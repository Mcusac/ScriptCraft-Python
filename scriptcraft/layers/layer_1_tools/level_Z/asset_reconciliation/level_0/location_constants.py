# location_constants.py

STRING_DTYPE = "string"

WHITESPACE_REGEX = r"\s+"
ROOM_REGEX = r"(?i)\broom\b"
BUILDING_REGEX = r"\bHP\b"
SPACING_REGEX = r"([A-Z]+)\s*([0-9]{3,})"

# Set True only during local debugging; False for production runs.
DEBUG_LOCATION_PIPELINE = False