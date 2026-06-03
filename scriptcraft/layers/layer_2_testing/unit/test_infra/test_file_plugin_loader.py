"""Tests for generic file-based workflow plugin loading (Phase 3 Batch A)."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any, Callable

import pytest

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.file_plugin_loader import (
    load_plugins,
)


class _RecordingRegistry:
    def __init__(self) -> None:
        self._workflows: dict[str, Callable[..., Any]] = {}
        self._info: dict[str, dict[str, Any]] = {}

    def has_workflow(self, name: str) -> bool:
        return name in self._workflows

    def register_workflow(
        self,
        name: str,
        workflow: Callable[..., Any],
        info: dict[str, Any],
    ) -> None:
        self._workflows[name] = workflow
        self._info[name] = info


def _write_plugin(path: Path, *, mode: str, body: str = "def run(): return 1") -> None:
    path.write_text(
        textwrap.dedent(
            f"""
            MODE = "{mode}"
            def WORKFLOW():
                {body}
            INFO = {{"feature": True}}
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )


def test_load_plugins_skips_malformed_plugin(tmp_path: Path) -> None:
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    _write_plugin(plugins_dir / "custom_ok.py", mode="ok")
    (plugins_dir / "custom_bad.py").write_text("MODE = 'bad'\n", encoding="utf-8")

    registry = _RecordingRegistry()
    messages: list[str] = []

    loaded = load_plugins(
        registry,
        plugins_dir,
        pattern="custom_*.py",
        on_message=messages.append,
    )

    assert loaded == 1
    assert registry.has_workflow("ok")
    assert not registry.has_workflow("bad")
    assert any("Failed to load plugin custom_bad.py" in m for m in messages)


def test_load_plugins_skips_duplicate_workflow_mode(tmp_path: Path) -> None:
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    _write_plugin(plugins_dir / "custom_first.py", mode="dup")
    _write_plugin(plugins_dir / "custom_second.py", mode="dup")

    registry = _RecordingRegistry()
    messages: list[str] = []

    loaded = load_plugins(
        registry,
        plugins_dir,
        pattern="custom_*.py",
        on_message=messages.append,
    )

    assert loaded == 1
    assert any("Skipping duplicate workflow mode: dup" in m for m in messages)
