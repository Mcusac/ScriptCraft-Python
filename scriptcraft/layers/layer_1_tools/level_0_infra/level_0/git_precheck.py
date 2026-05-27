"""Reusable git operation precheck + execution guard."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GitPrecheckResult:
    ok: bool
    reason: Optional[str] = None
    skip_body: bool = False


def run_git_operation_with_precheck(
    *,
    operation_name: str,
    precheck: Callable[[], GitPrecheckResult],
    body: Callable[[], bool],
    log: Callable[[str], None],
    log_error: Callable[[str], None],
) -> bool:
    """
    Run ``body`` after ``precheck`` passes.

    When ``precheck`` returns ``ok=True`` and ``skip_body=True``, the operation
    succeeds without invoking ``body`` (informational early exit).
    """
    log(f"🚀 Starting Git {operation_name} operation...")

    pre = precheck()
    if not pre.ok:
        log_error(pre.reason or "❌ Precheck failed")
        return False

    if pre.skip_body:
        if pre.reason:
            log(pre.reason)
        return True

    return body()
