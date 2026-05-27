"""Unit tests for mode runner and PipelineResult normalization."""

import importlib.util
import sys
from pathlib import Path

import pytest

_CORE = Path(__file__).resolve().parents[3] / "layer_0_core"


def _load_module(relative: str, name: str):
    path = _CORE / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module


_named_registry = _load_module(
    "level_0/abstractions/named_registry.py",
    "scriptcraft.layers.layer_0_core.level_0.abstractions.named_registry",
)
_pipeline_result = _load_module(
    "level_0/abstractions/pipeline_result.py",
    "scriptcraft.layers.layer_0_core.level_0.abstractions.pipeline_result",
)
_mode_execution = _load_module(
    "level_1/runtime/mode_execution.py",
    "scriptcraft.layers.layer_0_core.level_1.runtime.mode_execution",
)

ModeRegistry = _mode_execution.ModeRegistry
execute_mode = _mode_execution.execute_mode
get_mode = _mode_execution.get_mode


def test_execute_mode_normalizes_dict() -> None:
    def runner(**_kwargs):
        return {"mode": "demo", "status": "success", "outputs": [1]}

    result = execute_mode(runner, mode="demo")
    assert result.success is True
    assert result.metadata.get("outputs") == [1]


def test_mode_registry_get_unknown_raises() -> None:
    registry = ModeRegistry()
    registry.register("a", lambda **k: None)
    with pytest.raises(ValueError):
        get_mode(registry, "missing")
