"""Date strings for form fill (stdlib only)."""

from datetime import datetime


def get_current_date_mmddyyyy() -> str:
    return datetime.now().strftime("%m/%d/%Y")
