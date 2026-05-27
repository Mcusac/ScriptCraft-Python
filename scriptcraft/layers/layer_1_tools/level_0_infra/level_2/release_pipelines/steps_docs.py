import subprocess
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    ReleasePipelineContext,
)

def build_docs(**kwargs) -> None:
    log_and_print("📚 Building documentation...")

    if Path("docs").exists():
        if Path("docs/conf.py").exists():
            result = subprocess.run([sys.executable, "-m", "sphinx", "docs", "docs/_build"],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                log_and_print(f"❌ Sphinx build failed: {result.stderr}", level="error")
                return

        elif Path("mkdocs.yml").exists():
            result = subprocess.run([sys.executable, "-m", "mkdocs", "build"],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                log_and_print(f"❌ MkDocs build failed: {result.stderr}", level="error")
                return

    log_and_print("✅ Documentation built")


def deploy_docs(**kwargs) -> None:
    ctx = ReleasePipelineContext(
        version=kwargs.get("version", "0.0.0"),
        dry_run=kwargs.get("dry_run", False),
        repo_root=kwargs.get("repo_root"),
        package_root=kwargs.get("package_root"),
        docs_root=kwargs.get("docs_root"),
        timestamp=kwargs.get("timestamp"),
        extras=kwargs,
    )

    log_and_print("🚀 Deploying documentation...")

    if ctx.dry_run:
        log_and_print("🔍 DRY RUN: Would deploy docs")
        return

    if Path("mkdocs.yml").exists():
        result = subprocess.run([sys.executable, "-m", "mkdocs", "gh-deploy"],
                                capture_output=True, text=True)

        if result.returncode != 0:
            log_and_print(f"❌ MkDocs deployment failed: {result.stderr}", level="error")
            return

    log_and_print("✅ Documentation deployed")