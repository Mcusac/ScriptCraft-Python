import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT))


@contextmanager
def _pushd(path: Path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


class TestSharedEnv(unittest.TestCase):
    def _import_shared(self):
        shared_path = (
            _PACKAGE_ROOT
            / "scriptcraft"
            / "layers"
            / "layer_1_pypi"
            / "level_1_impl"
            / "level_0"
            / "env_base.py"
        )
        spec = spec_from_file_location("env_base_under_test", shared_path)
        assert spec is not None
        assert spec.loader is not None
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_basic_indicators_scripts_dir(self):
        se = self._import_shared()

        with tempfile.TemporaryDirectory() as td:
            scripts_dir = Path(td) / "scripts"
            scripts_dir.mkdir()

            with _pushd(scripts_dir):
                is_dist = se.is_distributable_from_cwd(se.cwd_indicators_basic("automated_labeler"))
                self.assertTrue(is_dist)

    def test_pypi_indicators_embed_dir(self):
        se = self._import_shared()

        with tempfile.TemporaryDirectory() as td:
            cwd = Path(td)
            (cwd / "embed_py311").mkdir()

            with _pushd(cwd):
                is_dist = se.is_distributable_from_cwd(se.cwd_indicators_pypi_distributable())
                self.assertTrue(is_dist)

    def test_pypi_indicators_tool_to_ship_env(self):
        se = self._import_shared()

        old = os.environ.get("TOOL_TO_SHIP")
        os.environ["TOOL_TO_SHIP"] = "1"
        try:
            with tempfile.TemporaryDirectory() as td:
                with _pushd(Path(td)):
                    is_dist = se.is_distributable_from_cwd(se.cwd_indicators_pypi_distributable())
                    self.assertTrue(is_dist)
        finally:
            if old is None:
                os.environ.pop("TOOL_TO_SHIP", None)
            else:
                os.environ["TOOL_TO_SHIP"] = old

    def test_distributable_base_dir_scripts_parent(self):
        se = self._import_shared()

        with tempfile.TemporaryDirectory() as td:
            base = Path(td) / "tool_root"
            scripts = base / "scripts"
            scripts.mkdir(parents=True)

            resolved = se.resolve_distributable_base_dir(cwd=scripts)
            self.assertEqual(resolved, base)


if __name__ == "__main__":
    unittest.main()

