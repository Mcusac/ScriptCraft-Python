"""
level_2/pipeline_base.py

Core pipeline classes and data structures.

Provides:
- PipelineStep: Validated dataclass for a single pipeline step
- BasePipeline:  Execution engine that delegates path resolution to PathResolver
                 and logging to level_2 context managers.
"""

import time
import traceback

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_0.path_resolver import (
    PathResolver,
    create_path_resolver,
)
from layers.layer_1_tools.level_0_infra.level_2.logging_context import (
    qc_log_context,
    with_domain_logger,
)


# ── Constants ─────────────────────────────────────────────────────────────────

_DOMAIN_SCOPED_INPUTS = frozenset({"raw_data", "merged_data", "processed_data", "old_data"})
_GLOBAL_INPUTS        = frozenset({"rhq_inputs", "global_data"})


# ── Data structures ───────────────────────────────────────────────────────────

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

    name:            str
    log_filename:    str
    qc_func:         Callable
    input_key:       str
    output_filename: Optional[str]       = None
    check_exists:    bool                = False
    run_mode:        str                 = "domain"
    tags:            List[str]           = field(default_factory=list)

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


# ── Pipeline engine ───────────────────────────────────────────────────────────

class BasePipeline:
    """
    Execution engine for ordered PipelineStep sequences.

    Path resolution is fully delegated to a PathResolver.  If the supplied
    config provides get_path_resolver(), that resolver is used; otherwise a
    WorkspacePathResolver rooted at Path.cwd() is constructed automatically.
    Either way, self.resolver is always a valid PathResolver — no None checks.
    """

    def __init__(
        self,
        config: Any,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.config      = config
        self.name        = name        or getattr(config, "name",        "Unknown Pipeline")
        self.description = description or getattr(config, "description", None)
        self.steps:        List[PipelineStep]  = []
        self.step_timings: List[tuple]         = []

        self._validate_config()
        self.resolver: PathResolver = self._build_resolver(config)

    # ── Construction helpers ──────────────────────────────────────────────────

    @staticmethod
    def _build_resolver(config: Any) -> PathResolver:
        """Return config's resolver, or a cwd-rooted fallback — never None."""
        if hasattr(config, "get_path_resolver"):
            return config.get_path_resolver()
        return create_path_resolver(Path.cwd())

    def _validate_config(self) -> None:
        if not hasattr(self.config, "domains"):
            raise ValueError("Pipeline config must have 'domains' defined")
        if not isinstance(self.config.domains, list):
            raise ValueError("Pipeline config 'domains' must be a list")

    # ── Step management ───────────────────────────────────────────────────────

    def add_step(self, step: PipelineStep) -> None:
        """Append a step."""
        self.steps.append(step)

    def insert_step(self, index: int, step: PipelineStep) -> None:
        """Insert a step at *index*."""
        self.steps.insert(index, step)

    def get_steps(self, tag_filter: Optional[str] = None) -> List[PipelineStep]:
        """Return all steps, or only those tagged with *tag_filter*."""
        if tag_filter:
            return [s for s in self.steps if tag_filter in s.tags]
        return list(self.steps)

    # ── Validation ────────────────────────────────────────────────────────────

    def validate(self) -> bool:
        """Return True only if the pipeline is runnable."""
        valid = True
        if not self.steps:
            log_and_print(f"⚠️ Pipeline '{self.name}' has no steps.")
            valid = False
        for step in self.steps:
            if not callable(step.qc_func):
                log_and_print(f"❌ Step '{step.name}' has a non-callable qc_func.")
                valid = False
        return valid

    # ── Step runners ──────────────────────────────────────────────────────────

    def _run_domain_step(self, step: PipelineStep, domain: str) -> None:
        """Execute *step* for a single *domain*."""
        domain_paths = self.resolver.get_domain_paths(domain)
        if not domain_paths:
            log_and_print(f"❌ Domain '{domain}' not found.")
            return

        input_path  = self.resolver.resolve_input_path(step.input_key, domain)
        output_path = self.resolver.resolve_output_path(step.output_filename, domain)
        log_path    = (
            self.resolver.get_logs_dir()
            / f"{step.log_filename.replace('.log', '')}_{domain}.log"
        )

        if step.check_exists and (not input_path or not input_path.exists()):
            log_and_print(f"⚠️ Input path not found, skipping: {input_path}")
            return

        log_path.parent.mkdir(parents=True, exist_ok=True)

        with with_domain_logger(
            log_path,
            lambda: step.qc_func(
                domain=domain,
                input_path=input_path,
                output_path=output_path,
                paths=domain_paths,
            ),
        ):
            pass  # timing / success logging is handled inside the context manager

    def _run_global_step(self, step: PipelineStep) -> None:
        """Execute a workspace-global *step*."""
        log_path    = self.resolver.get_logs_dir() / step.log_filename
        input_path  = self.resolver.resolve_input_path(step.input_key)
        output_path = self.resolver.resolve_output_path(step.output_filename)

        log_path.parent.mkdir(parents=True, exist_ok=True)

        with qc_log_context(log_path, operation=step.name):
            self._execute_global_step(step, input_path, output_path)

    def _execute_global_step(
        self,
        step: PipelineStep,
        input_path: Optional[Path],
        output_path: Path,
    ) -> None:
        """Build kwargs and invoke *step.qc_func* for a global step."""
        try:
            kwargs: Dict[str, Any] = {
                "input_paths":     [input_path] if input_path and input_path.is_file() else None,
                "output_dir":      output_path,
                "config":          self.config,
                "input_key":       step.input_key,
                "output_filename": step.output_filename,
                "check_exists":    step.check_exists,
                "log_dir":         self.resolver.get_logs_dir(),
                "input_dir":       self.resolver.get_input_dir(),
            }
            step.qc_func(**kwargs)
        except Exception as exc:
            log_and_print(f"❌ Error in global step '{step.name}': {exc}")
            log_and_print(traceback.format_exc(), level="debug")

    # ── Orchestration ─────────────────────────────────────────────────────────

    def run(
        self,
        tag_filter: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> None:
        """
        Execute all (optionally filtered) steps.

        Args:
            tag_filter: Run only steps carrying this tag.
            domain:     Required for single_domain mode.
        """
        log_and_print(
            f"🔍 Pipeline '{self.name}' starting — {len(self.steps)} total steps"
        )
        if not self.validate():
            log_and_print("❌ Validation failed. Aborting.")
            return

        filtered = self.get_steps(tag_filter)
        log_and_print(f"🔍 Running {len(filtered)} steps after filtering")

        self.step_timings = []
        total = len(filtered)

        for idx, step in enumerate(filtered, 1):
            log_and_print(f"\n[{idx}/{total}] 🚀 {step.name}")
            start = time.time()
            try:
                self._dispatch_step(step, domain)
                duration = time.time() - start
                log_and_print(f"[{idx}/{total}] ✅ {step.name} — {duration:.2f}s")
            except Exception as exc:
                duration = time.time() - start
                log_and_print(
                    f"[{idx}/{total}] ❌ {step.name} failed after {duration:.2f}s: {exc}"
                )
            finally:
                self.step_timings.append((step.name, time.time() - start))

    def _dispatch_step(self, step: PipelineStep, domain: Optional[str]) -> None:
        """Route *step* to the correct runner based on its run_mode."""
        if step.run_mode == "global":
            self._run_global_step(step)

        elif step.run_mode == "single_domain":
            if not domain:
                log_and_print(f"❌ '{step.name}' requires a domain argument.")
                return
            self._run_domain_step(step, domain)

        elif step.run_mode == "custom":
            step.qc_func()

        else:  # "domain" — run across every discovered domain
            for domain_name in self.resolver.get_all_domain_paths():
                self._run_domain_step(step, domain_name)

    # ── Reporting ─────────────────────────────────────────────────────────────

    def print_summary(self) -> None:
        """Print a timing table for all completed steps."""
        if not self.step_timings:
            return
        log_and_print("\n🧾 Step Timing Summary:")
        total = 0.0
        for name, duration in self.step_timings:
            log_and_print(f"   ⏱️  {name}: {duration:.2f}s")
            total += duration
        log_and_print(f"\n⏱️  Total pipeline duration: {total:.2f}s")