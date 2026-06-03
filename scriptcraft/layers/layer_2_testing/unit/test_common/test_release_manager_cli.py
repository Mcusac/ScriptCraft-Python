"""Tests for release_manager mode-first argv parsing."""

from __future__ import annotations

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    parse_release_manager_argv,
)


def test_parse_release_manager_argv_mode_and_flags() -> None:
    parsed = parse_release_manager_argv(
        ["python_package", "--version_type", "patch", "--auto_push", "--force"]
    )
    assert parsed.mode == "python_package"
    assert parsed.kwargs["mode"] == "python_package"
    assert parsed.kwargs["version_type"] == "patch"
    assert parsed.kwargs["auto_push"] is True
    assert parsed.kwargs["force"] is True


def test_parse_release_manager_argv_collects_positional_input_paths() -> None:
    parsed = parse_release_manager_argv(
        ["workspace", "/path/a", "/path/b", "--custom_message", "msg"]
    )
    assert parsed.mode == "workspace"
    assert parsed.kwargs["input_paths"] == ["/path/a", "/path/b"]
    assert parsed.kwargs["custom_message"] == "msg"
