"""Domain and global pipeline step runners."""

import traceback
from pathlib import Path
from typing import Any, Dict, Optional

from scriptcraft.layers.layer_0_core.level_0.paths import PathResolver
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.logging_context import (
    qc_log_context,
    with_domain_logger,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.qc_pipeline_step import (
    PipelineStep,
)


def run_domain_step(
    resolver: PathResolver,
    step: PipelineStep,
    domain: str,
) -> None:
    """Execute *step* for a single *domain*."""
    domain_paths = resolver.get_domain_paths(domain)
    if not domain_paths:
        log_and_print(f"❌ Domain '{domain}' not found.")
        return

    input_path = resolver.resolve_input_path(step.input_key, domain)
    output_path = resolver.resolve_output_path(step.output_filename, domain)
    log_path = (
        resolver.get_logs_dir()
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
        pass


def run_global_step(
    resolver: PathResolver,
    config: Any,
    step: PipelineStep,
) -> None:
    """Execute a workspace-global *step*."""
    log_path = resolver.get_logs_dir() / step.log_filename
    input_path = resolver.resolve_input_path(step.input_key)
    output_path = resolver.resolve_output_path(step.output_filename)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    with qc_log_context(log_path, operation=step.name):
        execute_global_step(resolver, config, step, input_path, output_path)


def execute_global_step(
    resolver: PathResolver,
    config: Any,
    step: PipelineStep,
    input_path: Optional[Path],
    output_path: Path,
) -> None:
    """Build kwargs and invoke *step.qc_func* for a global step."""
    try:
        kwargs: Dict[str, Any] = {
            "input_paths": [input_path] if input_path and input_path.is_file() else None,
            "output_dir": output_path,
            "config": config,
            "input_key": step.input_key,
            "output_filename": step.output_filename,
            "check_exists": step.check_exists,
            "log_dir": resolver.get_logs_dir(),
            "input_dir": resolver.get_input_dir(),
        }
        step.qc_func(**kwargs)
    except Exception as exc:
        log_and_print(f"❌ Error in global step '{step.name}': {exc}")
        log_and_print(traceback.format_exc(), level="debug")


def dispatch_step(
    resolver: PathResolver,
    config: Any,
    step: PipelineStep,
    domain: Optional[str],
) -> None:
    """Route *step* to the correct runner based on its run_mode."""
    if step.run_mode == "global":
        run_global_step(resolver, config, step)

    elif step.run_mode == "single_domain":
        if not domain:
            log_and_print(f"❌ '{step.name}' requires a domain argument.")
            return
        run_domain_step(resolver, step, domain)

    elif step.run_mode == "custom":
        step.qc_func()

    else:
        for domain_name in resolver.get_all_domain_paths():
            run_domain_step(resolver, step, domain_name)
