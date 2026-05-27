#!/usr/bin/env python3
"""Canonical ScriptCraft release subcommand CLI."""
import argparse
import sys

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import (
  run_git_status_workflow,
  run_git_sync_workflow,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import (
  upload_pypi, 
  upload_testpypi,
  detect_repo_root,
  resolve_version,
  check_git_status,
  Config
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import (
  ReleasePipelineFactory,
)


def _default_config() -> Config:
  config = Config()
  config.workspace.domains = ["default"]
  config.domains = config.workspace.domains
  return config


def _run_python_package_pipeline(*, dry_run: bool) -> bool:
  repo_root = detect_repo_root(start=Path.cwd()) or Path.cwd()
  resolved = resolve_version(repo_root=repo_root)
  pipeline = ReleasePipelineFactory.create_python_package_pipeline(
    _default_config(),
    version=resolved.version,
    dry_run=dry_run,
    root=repo_root,
  )
  pipeline.run()
  return True


def pypi_test(args: argparse.Namespace) -> None:
  log_and_print("Running PyPI test workflow...")
  ok = (
    _run_python_package_pipeline(dry_run=True)
    if args.pipeline
    else upload_testpypi()
  )
  if not ok:
    sys.exit(1)
  log_and_print("PyPI test completed successfully")


def pypi_release(args: argparse.Namespace) -> None:
  log_and_print("Running PyPI release workflow...")
  ok = (
    _run_python_package_pipeline(dry_run=False)
    if args.pipeline
    else upload_pypi()
  )
  if not ok:
    sys.exit(1)
  log_and_print("PyPI release completed successfully")


def git_sync(_: argparse.Namespace) -> None:
  log_and_print("Running Git sync workflow...")
  if not run_git_sync_workflow():
    sys.exit(1)
  log_and_print("Git sync completed successfully")


def git_status(_: argparse.Namespace) -> None:
  log_and_print("Checking Git status...")
  check_git_status()
  if not run_git_status_workflow():
    sys.exit(1)


def full_release(args: argparse.Namespace) -> None:
  log_and_print("Running full release workflow...")
  if args.pipeline:
    if not _run_python_package_pipeline(dry_run=True):
      sys.exit(1)
    if not _run_python_package_pipeline(dry_run=False):
      sys.exit(1)
  else:
    if not upload_testpypi():
      sys.exit(1)
    if not upload_pypi():
      sys.exit(1)
  if not run_git_sync_workflow():
    sys.exit(1)
  log_and_print("Full release completed successfully")


def main() -> None:
  parser = argparse.ArgumentParser(description="ScriptCraft Release CLI")
  subparsers = parser.add_subparsers(dest="command")

  pypi_test_parser = subparsers.add_parser("pypi-test", help="Test PyPI upload")
  pypi_test_parser.add_argument("--pipeline", action="store_true")
  pypi_test_parser.set_defaults(func=pypi_test)

  pypi_release_parser = subparsers.add_parser("pypi-release", help="Release to PyPI")
  pypi_release_parser.add_argument("--pipeline", action="store_true")
  pypi_release_parser.set_defaults(func=pypi_release)

  subparsers.add_parser("git-sync", help="Sync Git repository").set_defaults(func=git_sync)
  subparsers.add_parser("git-status", help="Check Git status").set_defaults(func=git_status)

  full_release_parser = subparsers.add_parser("full-release", help="Full release workflow")
  full_release_parser.add_argument("--pipeline", action="store_true")
  full_release_parser.set_defaults(func=full_release)

  args = parser.parse_args()
  if not args.command:
    parser.print_help()
    sys.exit(1)

  try:
    args.func(args)
  except KeyboardInterrupt:
    log_and_print("Operation cancelled by user")
    sys.exit(1)
  except Exception as exc:
    log_and_print(f"Unexpected error: {exc}", level="error")
    sys.exit(1)


if __name__ == "__main__":
  main()
