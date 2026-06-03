"""Pytest fixtures and path setup for layer_2_testing."""

import os
import sys
from pathlib import Path
from typing import Any, Generator

import pytest

PACKAGE_PATH = Path(__file__).resolve().parents[2]
if str(PACKAGE_PATH) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PATH))


def pytest_configure(config) -> None:
    if os.environ.get("SCRIPTCRAFT_REQUIRE_VENV") != "1":
        return
    exe = Path(sys.executable).resolve()
    if "venv" not in exe.parts and ".venv" not in exe.parts:
        raise RuntimeError(
            "Run tests with the project venv Python. "
            "From implementations/python/python-package:\n"
            '  & ".venv\\Scripts\\python.exe" -m pytest scriptcraft/layers/layer_2_testing -q'
        )


@pytest.fixture
def package_path() -> Path:
    return PACKAGE_PATH


@pytest.fixture
def test_data_dir() -> Path:
    data = PACKAGE_PATH / "data"
    data.mkdir(parents=True, exist_ok=True)
    return data


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    out = tmp_path / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out


@pytest.fixture
def sample_paths(test_data_dir: Path) -> dict[str, Path]:
    return {"data": test_data_dir}


@pytest.fixture
def sample_excel_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.xlsx"
    path.write_bytes(b"")
    return path


@pytest.fixture
def sample_docx_template(tmp_path: Path) -> Path:
    path = tmp_path / "template.docx"
    path.write_bytes(b"")
    return path


@pytest.fixture
def sample_comparison_files(tmp_path: Path) -> tuple[Path, Path]:
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    a.write_text("col\n1\n", encoding="utf-8")
    b.write_text("col\n1\n", encoding="utf-8")
    return a, b


@pytest.fixture
def scriptcraft_import() -> Any:
    import scriptcraft

    return scriptcraft
