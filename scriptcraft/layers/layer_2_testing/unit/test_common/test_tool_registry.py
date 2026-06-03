"""Tests for the level_9 ToolRegistry facade."""

from typing import Optional, Type

import pytest

from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool
from scriptcraft.layers.layer_1_tools.level_0_infra.level_9 import ToolRegistry


class _ListedTool(BaseTool):
    description = "Listed tool"

    def run(self, **kwargs):
        return True


class _StubRegistry:
    def __init__(self, tools: dict[str, Type[BaseTool]]) -> None:
        self._tools = tools

    def get_available_tools(self) -> dict[str, Type[BaseTool]]:
        return dict(self._tools)


def test_tool_registry_get_tool(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = _StubRegistry({"listed": _ListedTool})
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry.unified_registry",
        stub,
    )
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry.ensure_tools_discovered",
        lambda _registry: None,
    )
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry.get_available_tools",
        stub.get_available_tools,
    )

    registry = ToolRegistry()
    tool_class = registry.get_tool("listed")
    assert tool_class is _ListedTool
    assert registry.get_tool("missing") is None


def test_tool_registry_list_tools_uses_description_helper(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub = _StubRegistry({"listed": _ListedTool})
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry.unified_registry",
        stub,
    )
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry.ensure_tools_discovered",
        lambda _registry: None,
    )
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry.get_available_tools",
        stub.get_available_tools,
    )
    monkeypatch.setattr(
        "scriptcraft.layers.layer_1_tools.level_0_infra.level_9.tool_registry._description_for",
        lambda tool_name: f"desc:{tool_name}",
    )

    registry = ToolRegistry()
    assert registry.list_tools() == {"listed": "desc:listed"}
