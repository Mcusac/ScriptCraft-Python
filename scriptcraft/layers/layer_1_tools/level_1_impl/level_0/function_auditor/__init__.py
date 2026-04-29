"""
Function auditor (level_0).

Public surface:
- FunctionAuditor: audit a single file for unused functions
- BatchFunctionAuditor: audit many files and generate reports
"""

from .auditor import FunctionAuditor
from .batch import BatchFunctionAuditor

__all__ = ["FunctionAuditor", "BatchFunctionAuditor"]

