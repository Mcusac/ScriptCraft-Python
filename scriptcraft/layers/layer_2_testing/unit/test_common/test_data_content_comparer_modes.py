"""Tests for DataContentComparer mode registry lookup."""

from __future__ import annotations

import inspect

import pytest

from scriptcraft.layers.layer_1_tools.level_1_impl.level_2 import (
    MODE_REGISTRY,
    get_mode,
)


def test_get_mode_returns_registered_runner() -> None:
    runner = get_mode("standard")
    assert runner is MODE_REGISTRY.require("standard")
    assert callable(runner)


def test_get_mode_unknown_lists_available_modes() -> None:
    with pytest.raises(ValueError, match="Mode 'bad_mode' not found"):
        get_mode("bad_mode")


def test_mode_registry_contains_expected_modes() -> None:
    assert set(MODE_REGISTRY.list_keys()) == {
        "rhq",
        "standard",
        "release",
        "release_consistency",
        "domain_old_vs_new",
    }


def test_release_consistency_mode_callable_signature() -> None:
    runner = get_mode("release_consistency")
    params = list(inspect.signature(runner).parameters.keys())
    assert "input_paths" in params
    assert "output_dir" in params
