"""
Plugin registry for Release Manager Tool.

Workflow storage uses core NamedRegistry; metadata queries remain release-specific.
"""

from typing import Any, Callable, Dict, List, Optional

from scriptcraft.layers.layer_0_core.level_0 import NamedRegistry


def _safe_print(message: str) -> None:
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", "replace").decode())


class ReleaseWorkflowRegistry:
    """Registry for managing release workflows keyed by `mode` name."""

    def __init__(self) -> None:
        self._registry = NamedRegistry[Callable](
            registry_name="ReleaseWorkflowRegistry",
            key_label="Mode",
        )
        self._workflow_info: Dict[str, Dict[str, Any]] = {}

    def register_workflow(
        self,
        mode: str,
        workflow: Callable,
        info: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._registry.set(mode, workflow)
        self._workflow_info[mode] = info or {}
        _safe_print(f"🔌 Registered release workflow: {mode}")

    def get_workflow(self, mode: str) -> Optional[Callable]:
        return self._registry.get(mode)

    def list_workflows(self) -> List[str]:
        return self._registry.list_keys()

    def get_workflow_info(self, mode: str) -> Optional[Dict[str, Any]]:
        return self._workflow_info.get(mode)

    def get_workflows_by_feature(self, feature: str) -> List[str]:
        return [
            name
            for name, info in self._workflow_info.items()
            if info.get(feature, False)
        ]

    def get_workflows_by_version_type(self, version_type: str) -> List[str]:
        supported: List[str] = []
        for name, info in self._workflow_info.items():
            version_types = info.get("version_types", [])
            if version_type in version_types:
                supported.append(name)
        return supported

    def unregister_workflow(self, mode: str) -> bool:
        if not self._registry.remove(mode):
            return False
        self._workflow_info.pop(mode, None)
        _safe_print(f"🔌 Unregistered release workflow: {mode}")
        return True

    def clear_workflows(self) -> None:
        self._registry.clear()
        self._workflow_info.clear()
        _safe_print("🔌 Cleared all release workflows")

    def workflow_count(self) -> int:
        return len(self._registry.list_keys())

    def has_workflow(self, mode: str) -> bool:
        return self._registry.contains(mode)
