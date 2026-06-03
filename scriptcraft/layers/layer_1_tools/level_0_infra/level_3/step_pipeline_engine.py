"""QC step pipeline execution engine."""

import time

from pathlib import Path
from typing import Any, List, Optional

from scriptcraft.layers.layer_0_core.level_0 import PathResolver

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    WorkspacePathResolver,
    log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    dispatch_step,
    PipelineStep,
)


class StepPipelineEngine:
    """
    Execution engine for ordered PipelineStep sequences.

    Path resolution is fully delegated to a PathResolver.
    """

    def __init__(
        self,
        config: Any,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.config = config
        self.name = name or getattr(config, "name", "Unknown Pipeline")
        self.description = description or getattr(config, "description", None)
        self.steps: List[PipelineStep] = []
        self.step_timings: List[tuple] = []

        self._validate_config()
        self.resolver: PathResolver = self._build_resolver(config)

    @staticmethod
    def _build_resolver(config: Any) -> PathResolver:
        if hasattr(config, "get_path_resolver"):
            return config.get_path_resolver()
        return WorkspacePathResolver(Path.cwd())

    def _validate_config(self) -> None:
        if not hasattr(self.config, "domains"):
            raise ValueError("Pipeline config must have 'domains' defined")
        if not isinstance(self.config.domains, list):
            raise ValueError("Pipeline config 'domains' must be a list")

    def add_step(self, step: PipelineStep) -> None:
        self.steps.append(step)

    def insert_step(self, index: int, step: PipelineStep) -> None:
        self.steps.insert(index, step)

    def get_steps(self, tag_filter: Optional[str] = None) -> List[PipelineStep]:
        if tag_filter:
            return [s for s in self.steps if tag_filter in s.tags]
        return list(self.steps)

    def validate(self) -> bool:
        valid = True
        if not self.steps:
            log_and_print(f"⚠️ Pipeline '{self.name}' has no steps.")
            valid = False
        for step in self.steps:
            if not callable(step.qc_func):
                log_and_print(f"❌ Step '{step.name}' has a non-callable qc_func.")
                valid = False
        return valid

    def run(
        self,
        tag_filter: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> None:
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
                dispatch_step(self.resolver, self.config, step, domain)
                duration = time.time() - start
                log_and_print(f"[{idx}/{total}] ✅ {step.name} — {duration:.2f}s")
            except Exception as exc:
                duration = time.time() - start
                log_and_print(
                    f"[{idx}/{total}] ❌ {step.name} failed after {duration:.2f}s: {exc}"
                )
            finally:
                self.step_timings.append((step.name, time.time() - start))

    def print_summary(self) -> None:
        if not self.step_timings:
            return
        log_and_print("\n🧾 Step Timing Summary:")
        total = 0.0
        for name, duration in self.step_timings:
            log_and_print(f"   ⏱️  {name}: {duration:.2f}s")
            total += duration
        log_and_print(f"\n⏱️  Total pipeline duration: {total:.2f}s")
