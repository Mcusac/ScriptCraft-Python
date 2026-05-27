import subprocess
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ReleasePipelineContext,
)


def upload_to_pypi(**kwargs) -> None:
    ctx = ReleasePipelineContext(
        version=kwargs.get("version", "0.0.0"),
        dry_run=kwargs.get("dry_run", False),
        repo_root=kwargs.get("repo_root"),
        package_root=kwargs.get("package_root"),
        docs_root=kwargs.get("docs_root"),
        timestamp=kwargs.get("timestamp"),
        extras=kwargs,
    )

    log_and_print("📦 Uploading to PyPI...")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would upload to PyPI")
        return

    try:
        result = subprocess.run([sys.executable, "-m", "twine", "upload", "dist/*"],
                                capture_output=True, text=True)

        if result.returncode != 0:
            log_and_print(f"❌ Upload failed: {result.stderr}", level="error")
            return

    except FileNotFoundError:
        log_and_print("❌ twine not found. Install with: pip install twine", level="error")
        return

    log_and_print("✅ Package uploaded to PyPI")