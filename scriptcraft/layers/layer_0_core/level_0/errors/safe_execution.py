"""Log-agnostic error-swallowing decorator for comparison and similar workflows."""

from functools import wraps
from typing import Any, Callable, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])


def swallow_errors(
    func: _F,
    *,
    on_error: Callable[[Exception, str], None] | None = None,
) -> _F:
    """Return ``func`` wrapped to catch exceptions and return ``None`` on failure."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            if on_error is not None:
                on_error(exc, func.__name__)
            return None

    return wrapper  # type: ignore[return-value]
