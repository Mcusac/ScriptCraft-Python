"""
Environment detection and setup for Dictionary-Driven Checker Tool.

This module handles the detection of whether the tool is running in
development or distributable mode and sets up the appropriate import paths.
"""

import os

from pathlib import Path

from layers.layer_1_tools.level_1_impl.level_0.env.layout import dev_project_root_from_file

_DEV_ROOT = dev_project_root_from_file(Path(__file__), levels_up=5)


def setup_environment() -> bool:
    """
    Detect if running in distributable mode and set up environment.
    
    Returns:
        bool: True if running in distributable mode, False if in development
    """
    # Check if we're running from a distributable package
    # Distributable packages have a specific structure
    current_file = Path(__file__).resolve()
    
    # Check for distributable indicators
    is_distributable = (
        # Check if we're in a distributable directory structure
        "distributables" in str(current_file) or
        # Check if we're running from a packaged directory
        current_file.parent.name == "scripts" and
        current_file.parent.parent.name in ["distributables", "packages"] or
        # Check if config.yaml is in parent directory (distributable structure)
        (current_file.parent.parent / "config.yaml").exists()
    )
    
    # Set environment variable for other modules
    os.environ["SCRIPTCRAFT_ENV"] = "distributable" if is_distributable else "development"
    
    return is_distributable