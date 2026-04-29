"""Automated labeler domain utilities (cohesive, DRY modules)."""

from .labeling import apply_labeling_rules
from .persistence import save_labeled_data
from .docx_template import fill_full_page


__all__ = [
    "fill_full_page",
    "apply_labeling_rules",
    "save_labeled_data",
]

