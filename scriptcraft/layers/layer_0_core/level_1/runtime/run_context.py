"""Shared run-context extraction for orchestrated workflows."""

from dataclasses import dataclass, field
from typing import Any, Optional, Sequence, Union

from scriptcraft.layers.layer_0_core.level_0 import PathLike


@dataclass
class RunContext:
    input_paths: Optional[Union[PathLike, Sequence[PathLike]]] = None
    output_dir: Optional[PathLike] = None
    domain: Optional[str] = None
    domains: Optional[Union[str, Sequence[str]]] = None
    dataset_file: Optional[PathLike] = None
    dictionary_file: Optional[PathLike] = None
    extra_kwargs: dict[str, Any] = field(default_factory=dict)


def build_run_context(*args: Any, **kwargs: Any) -> RunContext:
    """Extract standard run fields from args/kwargs and return leftover extras."""
    ctx = RunContext()
    extra = dict(kwargs)

    if "input_paths" in extra:
        ctx.input_paths = extra.pop("input_paths")
    elif args:
        ctx.input_paths = args[0]

    if "output_dir" in extra:
        ctx.output_dir = extra.pop("output_dir")

    if "domain" in extra:
        ctx.domain = extra.pop("domain")

    if "domains" in extra:
        ctx.domains = extra.pop("domains")
    elif args and "input_paths" not in kwargs and len(args) == 1:
        ctx.domains = args[0]

    if "dataset_file" in extra:
        ctx.dataset_file = extra.pop("dataset_file")
    elif len(args) >= 1 and "input_paths" not in kwargs:
        ctx.dataset_file = args[0]

    if "dictionary_file" in extra:
        ctx.dictionary_file = extra.pop("dictionary_file")
    elif len(args) >= 2:
        ctx.dictionary_file = args[1]

    ctx.extra_kwargs = extra
    return ctx
