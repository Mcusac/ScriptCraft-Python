"""Plugin system for dictionary-driven validation."""

# === WILDCARD IMPORTS FOR SCALABILITY ===
# Expose the common plugin registry as `registry` so plugins can do:
#   from . import registry
from scriptcraft.common.plugins import registry


def _load_plugins() -> None:
    """Load all plugins after registry is initialized."""
    try:
        from . import validators  # noqa: F401
    except ImportError:
        # Plugins are optional; if they fail to import, continue.
        pass


_load_plugins()
