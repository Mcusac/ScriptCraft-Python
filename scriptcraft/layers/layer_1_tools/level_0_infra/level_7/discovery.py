import importlib
import inspect
import pkgutil

from pathlib import Path
from typing import Dict, List, Optional, Type

from layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool


class ToolDiscoveryEngine:
    """
    Pure discovery layer (no registry state).
    """

    def discover_tools(self, paths: List[Path]) -> Dict[str, Type[BaseTool]]:
        discovered: Dict[str, Type[BaseTool]] = {}

        for path in paths:
            if not path.exists():
                continue

            log_and_print(f"🔍 Discovering tools in: {path}")

            for _, name, is_pkg in pkgutil.iter_modules([str(path)]):
                if not is_pkg or name.startswith("_"):
                    continue

                tool_class = self._discover_tool_class(path, name)
                if tool_class:
                    discovered[name] = tool_class
                    log_and_print(f"✅ Discovered tool: {name}")

        return discovered

    def _discover_tool_class(self, path: Path, tool_name: str) -> Optional[Type[BaseTool]]:
        try:
            module_path = f"scriptcraft.{path.name}.{tool_name}"
            module = importlib.import_module(module_path)

            # 1. direct subclass
            for attr in dir(module):
                obj = getattr(module, attr)
                if inspect.isclass(obj) and issubclass(obj, BaseTool) and obj != BaseTool:
                    return obj

            # 2. instance export
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, BaseTool):
                    return type(obj)

            # 3. naming fallback
            for candidate in [
                tool_name.replace("_", "").title(),
                tool_name.title().replace("_", ""),
                tool_name.upper(),
                tool_name.capitalize(),
            ]:
                if hasattr(module, candidate):
                    obj = getattr(module, candidate)
                    if inspect.isclass(obj) and issubclass(obj, BaseTool):
                        return obj

            return None

        except Exception as e:
            log_and_print(f"⚠️ Discovery error {tool_name}: {e}")
            return None