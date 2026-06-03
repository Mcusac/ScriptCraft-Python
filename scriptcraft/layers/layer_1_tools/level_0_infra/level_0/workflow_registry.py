"""Generic named-workflow registry mechanics (release-agnostic).

Stable tools-layer alias over ``layer_0_core.level_0.NamedRegistry``. Release and
plugin loaders may depend on this class name; prefer core ``NamedRegistry`` only
for new non-tools code.
"""

from typing import Any, Callable, List, Optional

from scriptcraft.layers.layer_0_core.level_0 import NamedRegistry


class WorkflowRegistry:
    """Registry for named callables using core ``NamedRegistry``."""

    def __init__(
        self,
        *,
        registry_name: str = "WorkflowRegistry",
        key_label: str = "Workflow",
    ) -> None:
        self._registry = NamedRegistry[Callable[..., Any]](
            registry_name=registry_name,
            key_label=key_label,
        )

    def register_workflow(self, name: str, workflow: Callable[..., Any]) -> None:
        self._registry.set(name, workflow)

    def get_workflow(self, name: str) -> Optional[Callable[..., Any]]:
        return self._registry.get(name)

    def list_workflows(self) -> List[str]:
        return self._registry.list_keys()

    def unregister_workflow(self, name: str) -> bool:
        return self._registry.remove(name)

    def clear_workflows(self) -> None:
        self._registry.clear()

    def workflow_count(self) -> int:
        return len(self._registry.list_keys())

    def has_workflow(self, name: str) -> bool:
        return self._registry.contains(name)
