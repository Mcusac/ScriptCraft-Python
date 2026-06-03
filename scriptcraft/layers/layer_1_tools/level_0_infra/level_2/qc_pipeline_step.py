"""Pipeline step schema and run-mode validation."""

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print

_DOMAIN_SCOPED_INPUTS = frozenset(
    {"raw_data", "merged_data", "processed_data", "old_data"}
)
_GLOBAL_INPUTS = frozenset({"rhq_inputs", "global_data"})


@dataclass
class PipelineStep:
    """
    A single step in a pipeline.

    Attributes:
        name:            Human-readable step label.
        log_filename:    Base name for the step's log file.
        qc_func:         Callable executed by the step.
        input_key:       Key used to resolve the input path from the PathResolver.
        output_filename: Optional output file name (None → directory is used).
        check_exists:    Abort the step if the resolved input path is missing.
        run_mode:        One of "domain", "single_domain", "global", "custom".
        tags:            Optional list of filter tags.
    """

    name: str
    log_filename: str
    qc_func: Callable
    input_key: str
    output_filename: Optional[str] = None
    check_exists: bool = False
    run_mode: str = "domain"
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_run_mode()

    def _validate_run_mode(self) -> None:
        """Warn on likely input_key / run_mode mismatches."""
        if self.run_mode == "domain" and self.input_key in _GLOBAL_INPUTS:
            log_and_print(
                f"⚠️ Step '{self.name}': domain mode with global input_key '{self.input_key}'."
            )
        elif self.run_mode == "single_domain" and self.input_key not in _DOMAIN_SCOPED_INPUTS:
            log_and_print(
                f"⚠️ Step '{self.name}': single_domain mode with non-domain input_key '{self.input_key}'."
            )
        elif self.run_mode == "global" and self.input_key in _DOMAIN_SCOPED_INPUTS:
            log_and_print(
                f"⚠️ Step '{self.name}': global mode with domain-scoped input_key '{self.input_key}'."
            )
        elif self.run_mode == "custom":
            log_and_print(
                f"ℹ️ Step '{self.name}': custom mode — qc_func must handle all path resolution."
            )
