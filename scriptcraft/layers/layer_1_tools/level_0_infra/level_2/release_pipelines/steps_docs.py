import subprocess
import sys

from pathlib import Path

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.release_pipelines.utils import build_context

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
    ctx = build_context(**kwargs)

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