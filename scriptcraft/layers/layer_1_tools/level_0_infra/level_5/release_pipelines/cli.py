import argparse
from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
    Config,
    detect_repo_root,
    resolve_version,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
    create_docs_pipeline,
    create_full_pipeline,
    create_git_repo_pipeline,
    create_python_package_pipeline,
    resolve_release_context,
)


def main():
    parser = argparse.ArgumentParser(description="Release Pipeline Runner")

    parser.add_argument("pipeline", choices=["python_package", "git_repo", "docs", "full"])
    parser.add_argument("--version", help="Version to release")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--config")

    args = parser.parse_args()

    config = Config.from_yaml(args.config) if args.config else None
    repo_root = detect_repo_root(start=Path.cwd()) or Path.cwd()
    resolved = resolve_version(repo_root=repo_root)
    effective_version = args.version or resolved.version

    prepared, version, dry_run, root = resolve_release_context(
        config=config,
        version=effective_version,
        dry_run=args.dry_run,
        root=repo_root,
    )

    pipeline_map = {
        "python_package": create_python_package_pipeline,
        "git_repo": create_git_repo_pipeline,
        "docs": create_docs_pipeline,
        "full": create_full_pipeline,
    }

    pipeline = pipeline_map[args.pipeline](
        config=prepared,
        version=version,
        dry_run=dry_run,
        root=root,
    )

    log_and_print(f"🚀 Starting {args.pipeline} release pipeline...")
    log_and_print(f"📌 Repo root: {repo_root}")
    log_and_print(f"🏷️ Version: {effective_version} (source: {resolved.source})")
    if args.dry_run:
        log_and_print("🔍 DRY RUN MODE - No actual changes will be made")
    pipeline.run()
    log_and_print(f"✅ {args.pipeline} release pipeline completed!")


if __name__ == "__main__":
    main()
