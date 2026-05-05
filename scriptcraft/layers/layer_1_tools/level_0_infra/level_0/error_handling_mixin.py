from typing import Any, Callable


class ErrorHandlingMixin:
    """Handles execution wrappers."""

    def run_with_error_handling(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        self.log_start()
        try:
            result = func(*args, **kwargs)
            self.log_completion()
            return result
        except Exception as e:
            self.log_error(e)
            raise