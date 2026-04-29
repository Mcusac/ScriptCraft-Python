
import inspect

from collections.abc import Callable
from typing import Any


def filter_kwargs_for_callable(func: Callable[..., Any], kwargs: dict[str, Any]) -> dict[str, Any]:
    """
    Filter kwargs to only those accepted by `func`, unless it has **kwargs.
    This avoids breaking tools whose `run()` signatures don't accept extra args.
    """
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return kwargs

    params = list(sig.parameters.values())
    has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)
    if has_var_kw:
        return kwargs

    accepted = {
        p.name
        for p in params
        if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
        and p.name != "self"
    }
    return {k: v for k, v in kwargs.items() if k in accepted}

