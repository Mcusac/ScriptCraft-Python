import argparse

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2.root_schema import Config
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.release_pipelines.factory import ReleasePipelineFactory


def main():
    parser = argparse.ArgumentParser(description="Release Pipeline Runner")

    parser.add_argument("pipeline", choices=["python_package", "git_repo", "docs", "full"])
    parser.add_argument("--version", help="Version to release")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--config")

    args = parser.parse_args()

    config = Config.from_yaml(args.config) if args.config else None

    pipeline_map = {
        "python_package": ReleasePipelineFactory.create_python_package_pipeline,
        "git_repo": ReleasePipelineFactory.create_git_release_pipeline,
        "docs": ReleasePipelineFactory.create_documentation_pipeline,
        "full": ReleasePipelineFactory.create_full_release_pipeline
    }

    pipeline = pipeline_map[args.pipeline](config)

    log_and_print(f"🚀 Starting {args.pipeline} release pipeline...")
    pipeline.run()
    log_and_print(f"✅ {args.pipeline} release pipeline completed!")


if __name__ == "__main__":
    main()