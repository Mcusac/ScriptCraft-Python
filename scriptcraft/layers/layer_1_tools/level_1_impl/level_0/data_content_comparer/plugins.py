
import importlib.util
from pathlib import Path
from typing import Callable, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print


def load_mode(mode_name: str, *, plugins_dir: Optional[Path] = None) -> Optional[Callable]:
    """Dynamically load a mode plugin from a `plugins/` directory."""
    try:
        base_dir = plugins_dir or (Path(__file__).resolve().parent / "plugins")
        plugin_file = base_dir / f"{mode_name}.py"

        if not plugin_file.exists():
            log_and_print(f"❌ Mode file '{plugin_file}' not found.")
            return None

        spec = importlib.util.spec_from_file_location(mode_name, plugin_file)
        if spec is None:
            log_and_print(f"❌ Failed to create spec for '{plugin_file}'")
            return None

        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            log_and_print(f"❌ Failed to get loader for '{plugin_file}'")
            return None

        spec.loader.exec_module(module)

        if hasattr(module, "run_mode"):
            return getattr(module, "run_mode")

        log_and_print(f"❌ Mode '{mode_name}' exists but does not define a 'run_mode()' function.")
        return None

    except Exception as e:
        log_and_print(f"❌ Failed to load mode '{mode_name}': {e}")
        return None

