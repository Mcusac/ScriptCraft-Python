"""Domain-loop scaffolding using core lifecycle contracts."""

from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence, Union

from scriptcraft.layers.layer_0_core.level_0 import (
    get_logger,
    DomainLoopTool,
    PathLike,
    ProcessDomainTool,
)

_logger = get_logger(__name__)


def _normalize_list(
    values: Optional[Union[PathLike, Sequence[PathLike]]],
) -> list[Path]:
    if values is None:
        return []
    if isinstance(values, (str, Path)):
        return [Path(values)]
    return [Path(v) for v in values]


def run_process_domain_over_input_paths(
    tool: ProcessDomainTool,
    *,
    input_paths: Optional[Union[PathLike, Sequence[PathLike]]],
    output_dir: Optional[PathLike],
    domain: Optional[str],
    dictionary_file: Optional[PathLike] = None,
    extra_kwargs: Optional[Dict[str, Any]] = None,
) -> None:
    """Standard loop for tools that process each input path as a dataset file."""
    tool.log_start()
    extra_kwargs = extra_kwargs or {}

    try:
        normalized = _normalize_list(input_paths)
        if not normalized:
            raise ValueError("No input paths provided")

        if not tool.validate_input_files(normalized):
            raise ValueError("Invalid input files")

        output_path = tool.resolve_output_directory(output_dir)
        resolved_domain = domain or "unknown"

        for input_path in normalized:
            dataset_file = Path(input_path)
            _logger.info("Processing: %s", dataset_file)
            tool.process_domain(
                resolved_domain,
                dataset_file,
                dictionary_file,
                output_path,
                **extra_kwargs,
            )

        tool.log_completion()

    except Exception as exc:
        tool.log_error(exc)
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
    """Standard loop for one dataset + one dictionary file."""
    tool.log_start()
    extra_kwargs = extra_kwargs or {}

    try:
        if not dataset_file or not dictionary_file:
            raise ValueError("Both dataset_file and dictionary_file are required")

        dataset_path = Path(dataset_file)
        dictionary_path = Path(dictionary_file)

        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
        if not dictionary_path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {dictionary_path}")

        output_path = tool.resolve_output_directory(output_dir)
        resolved_domain = domain or "unknown"

        tool.process_domain(
            resolved_domain,
            dataset_path,
            dictionary_path,
            output_path,
            **extra_kwargs,
        )
        tool.log_completion()

    except Exception as exc:
        tool.log_error(exc)
        raise


def run_domains(
    tool: DomainLoopTool,
    *,
    domains: Optional[Union[str, Sequence[str]]],
    default_domains: Sequence[str],
    output_dir: Optional[PathLike],
    per_domain_callable: Callable[[str, Path], None],
) -> None:
    """Iterate domains and invoke per-domain work."""
    tool.log_start()

    try:
        if domains is None:
            domain_list = list(default_domains)
        elif isinstance(domains, str):
            domain_list = [domains]
        else:
            domain_list = list(domains)

        output_path = tool.resolve_output_directory(output_dir)

        for domain_name in domain_list:
            per_domain_callable(domain_name, output_path)

        tool.log_completion()

    except Exception as exc:
        tool.log_error(exc)
        raise
