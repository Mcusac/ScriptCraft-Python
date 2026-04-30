"""
Documentation release steps.

These are placeholders for now, but isolated so the main tool remains clean.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print


def build_docs(*, docs_root: Path, **_: Any) -> None:
    log_and_print("📚 Building documentation...")
    # TODO: NOT IMPLEMENTED — wire later
    log_and_print("✅ Documentation built")


def deploy_docs(*, docs_root: Path, dry_run: bool, **_: Any) -> None:
    log_and_print("🚀 Deploying documentation...")

    if dry_run:
        log_and_print("🔍 DRY RUN: Would deploy docs")
        return

    # TODO: NOT IMPLEMENTED — wire later
    log_and_print("✅ Documentation deployed")

