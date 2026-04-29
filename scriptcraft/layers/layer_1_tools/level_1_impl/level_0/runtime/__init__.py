"""
Runtime scaffolding helpers for tools.
"""

from .loops import (  # noqa: F401
    run_domains,
    run_process_domain_for_single_pair,
    run_process_domain_over_input_paths,
)
from .normalize import normalize_list  # noqa: F401
from .protocols import DomainLoopTool, ProcessDomainTool  # noqa: F401

