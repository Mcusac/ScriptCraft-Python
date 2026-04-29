"""
Run-loop scaffolding for tools.
"""

from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence, Union

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_1_impl.level_0.runtime.protocols import DomainLoopTool, PathLike, ProcessDomainTool
from layers.layer_1_pypi.level_1_impl.level_1.runtime_normalize import normalize_list


def run_process_domain_over_input_paths(
    tool: ProcessDomainTool,
    *,
    input_paths: Optional[Union[PathLike, Sequence[PathLike]]],
    output_dir: Optional[PathLike],
    domain: Optional[str],
    dictionary_file: Optional[PathLike] = None,
    extra_kwargs: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Standard `run()` loop for tools that call:
      tool.process_domain(domain, dataset_file, dictionary_file, output_path, **kwargs)
    """
    tool.log_start()
    extra_kwargs = extra_kwargs or {}

    try:
        normalized = normalize_list(input_paths)
        if not normalized:
            raise ValueError("❌ No input paths provided")

        if not tool.validate_input_files(normalized):
            raise ValueError("❌ Invalid input files")

        output_path = tool.resolve_output_directory(output_dir)
        resolved_domain = domain or "unknown"

        for input_path in normalized:
            dataset_file = Path(input_path)
            log_and_print(f"🔍 Processing: {dataset_file}")
            tool.process_domain(resolved_domain, dataset_file, dictionary_file, output_path, **extra_kwargs)

        tool.log_completion()

    except Exception as e:
        tool.log_error(e)
        raise


def run_process_domain_for_single_pair(
    tool: ProcessDomainTool,
    *,
    dataset_file: Optional[PathLike],
    dictionary_file: Optional[PathLike],
    output_dir: Optional[PathLike],
    domain: Optional[str],
    extra_kwargs: Optional[Dict[str, Any]] = None,
) -> None:
    """Standard `run()` for tools that operate on one dataset + one dictionary file."""
    tool.log_start()
    extra_kwargs = extra_kwargs or {}

    try:
        if not dataset_file or not dictionary_file:
            raise ValueError("❌ Both dataset_file and dictionary_file are required")

        dataset_path = Path(dataset_file)
        dictionary_path = Path(dictionary_file)

        if not dataset_path.exists():
            raise FileNotFoundError(f"❌ Dataset file not found: {dataset_path}")
        if not dictionary_path.exists():
            raise FileNotFoundError(f"❌ Dictionary file not found: {dictionary_path}")

        output_path = tool.resolve_output_directory(output_dir)
        resolved_domain = domain or "unknown"

        tool.process_domain(resolved_domain, dataset_path, dictionary_path, output_path, **extra_kwargs)
        tool.log_completion()

    except Exception as e:
        tool.log_error(e)
        raise


def run_domains(
    tool: DomainLoopTool,
    *,
    domains: Optional[Union[str, Sequence[str]]],
    default_domains: Sequence[str],
    output_dir: Optional[PathLike],
    per_domain_callable: Callable[[str, Path], None],
) -> None:
    """Standard `run()` loop for tools that iterate domains and compute per-domain outputs."""
    tool.log_start()

    try:
        if domains is None:
            domain_list = list(default_domains)
        elif isinstance(domains, str):
            domain_list = [domains]
        else:
            domain_list = list(domains)

        output_path = tool.resolve_output_directory(output_dir)

        for domain in domain_list:
            per_domain_callable(domain, output_path)

        tool.log_completion()

    except Exception as e:
        tool.log_error(e)
        raise

