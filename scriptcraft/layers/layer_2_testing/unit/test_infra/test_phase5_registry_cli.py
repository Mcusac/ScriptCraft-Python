"""Phase 5 registry and CLI dispatch integration tests."""

from argparse import Namespace
from typing import Optional, Type

import pytest

from scriptcraft.layers.layer_1_tools.level_0_infra.level_1 import ensure_tools_discovered
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool
from scriptcraft.layers.layer_1_tools.level_0_infra.level_8 import unified_registry
from scriptcraft.layers.layer_1_tools.level_0_infra.level_10 import (
    InfraRegistryToolLookup,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_11 import dispatch_tool_by_name


class _SuccessTool(BaseTool):
    description = "Success tool"

    def __init__(self) -> None:
        super().__init__(name="success", description="Success tool")

    def run(self, **kwargs):
        return True


class _FailureTool(BaseTool):
    description = "Failure tool"

    def __init__(self) -> None:
        super().__init__(name="failure", description="Failure tool")

    def run(self, **kwargs):
        return False


class _StubLookup:
    def __init__(self, tool_class: Optional[Type[BaseTool]]) -> None:
        self._tool_class = tool_class

    def get_tool_class(self, tool_name: str) -> Optional[Type[BaseTool]]:
        return self._tool_class


def test_dispatch_tool_by_name_success() -> None:
    lookup = _StubLookup(_SuccessTool)
    assert dispatch_tool_by_name("success", Namespace(), lookup=lookup, exit_on_failure=False)


def test_dispatch_tool_by_name_failure_exits_when_configured() -> None:
    lookup = _StubLookup(_FailureTool)
    with pytest.raises(SystemExit) as exc_info:
        dispatch_tool_by_name("failure", Namespace(), lookup=lookup, exit_on_failure=True)
    assert exc_info.value.code == 1


def test_dispatch_tool_by_name_missing_tool() -> None:
    lookup = _StubLookup(None)
    with pytest.raises(SystemExit):
        dispatch_tool_by_name("missing", Namespace(), lookup=lookup, exit_on_failure=True)


def test_infra_registry_tool_lookup_is_adapter_only() -> None:
    lookup = InfraRegistryToolLookup()
    assert hasattr(lookup, "get_tool_class")
    assert not hasattr(lookup, "list_tool_descriptions")


def test_ensure_tools_discovered_is_idempotent() -> None:
    unified_registry.refresh()
    ensure_tools_discovered(unified_registry)
    first = dict(unified_registry.get_available_tools())
    ensure_tools_discovered(unified_registry)
    second = dict(unified_registry.get_available_tools())
    assert first == second
