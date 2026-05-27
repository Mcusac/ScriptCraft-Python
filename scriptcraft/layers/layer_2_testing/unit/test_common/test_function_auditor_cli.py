import argparse

import importlib.util
from pathlib import Path

class _FakeBatchAuditor:
  def __init__(self):
    self.called: list[str] = []

  def get_all_files(self) -> list[str]:
    self.called.append("all")
    return ["a.gd"]

  def get_files_by_pattern(self, pattern: str, base_folder: str) -> list[str]:
    self.called.append(f"pattern:{pattern}:{base_folder}")
    return ["p.gd"]

  def get_files_in_folder(self, folder: str) -> list[str]:
    self.called.append(f"folder:{folder}")
    return ["f.gd"]

  def get_files_by_extension(self, extension: str, base_folder: str) -> list[str]:
    self.called.append(f"ext:{extension}:{base_folder}")
    return ["e.gd"]

  def get_files_by_category(self, category: str) -> list[str]:
    self.called.append(f"cat:{category}")
    return ["c.gd"]


def _args(**overrides) -> argparse.Namespace:
  base = dict(
    all=False,
    pattern=None,
    folder=None,
    extension="gd",
    base_folder="scripts",
    managers=False,
    ui=False,
    utils=False,
    factories=False,
    coordinators=False,
  )
  base.update(overrides)
  return argparse.Namespace(**base)


def test_resolve_batch_target_precedence_all_overrides_others() -> None:
  resolve_batch_target = _load_resolve_batch_target()
  auditor = _FakeBatchAuditor()
  args = _args(all=True, pattern="**/*.gd", folder="x", managers=True, extension="py")
  files = resolve_batch_target(args, auditor)
  assert files == ["a.gd"]
  assert auditor.called == ["all"]


def test_resolve_batch_target_precedence_pattern_over_folder() -> None:
  resolve_batch_target = _load_resolve_batch_target()
  auditor = _FakeBatchAuditor()
  args = _args(pattern="**/*Manager*.gd", folder="scripts/Managers")
  files = resolve_batch_target(args, auditor)
  assert files == ["p.gd"]
  assert auditor.called == ["pattern:**/*Manager*.gd:scripts"]


def test_resolve_batch_target_precedence_folder_over_extension_over_categories() -> None:
  resolve_batch_target = _load_resolve_batch_target()
  auditor = _FakeBatchAuditor()
  args = _args(folder="scripts/UI", extension="py", ui=True)
  files = resolve_batch_target(args, auditor)
  assert files == ["f.gd"]
  assert auditor.called == ["folder:scripts/UI"]


def _load_resolve_batch_target():
  # Load the CLI module by file path to avoid triggering the heavy `level_1_impl` barrel.
  pkg_root = Path(__file__).resolve().parents[3]
  cli_path = (
    pkg_root
    / "level_1_impl"
    / "level_3"
    / "function_auditor"
    / "cli.py"
  )
  spec = importlib.util.spec_from_file_location("function_auditor_cli", cli_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module.resolve_batch_target

