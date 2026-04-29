"""
Centralized project constants and lightweight config loading for level_0 consumers.

ARCHITECTURE NOTE
-----------------
This file currently contains four categories of code:

  1. Pure constants           — appropriate for level_0 (keep here).
  2. Legacy config loading    — belongs in a higher-level config module;
                                kept here only for backward compatibility.
  3. Path-discovery helpers   — belong in path_resolver.py or a higher layer;
                                kept here only for backward compatibility.
  4. OutlierMethod enum       — unrelated to paths; should move to a
                                domain/stats module when possible.
"""

import os
import yaml

from enum import Enum
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional

# =============================================================================
# 1. LEGACY CONFIG LOADING
#    Provides fallback constants when the primary Config system is unavailable.
#    TODO: Replace callers with the primary Config loader and delete this block.
# =============================================================================

_CONFIG: Dict[str, Any] = {}


def _load_legacy_config() -> None:
    """
    Populate _CONFIG from the first config.yaml found, env vars, or defaults.

    Search order:
      1. Ancestor directories of this file (up to 5 levels).
      2. Current working directory.
      3. Distributable-mode environment variables.
      4. Hard-coded defaults.
    """
    global _CONFIG

    search_paths = [
        Path(__file__).resolve().parents[i] / "config.yaml"
        for i in range(3, 6)
    ] + [Path.cwd() / "config.yaml"]

    for config_path in search_paths:
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as fh:
                    _CONFIG = yaml.safe_load(fh) or {}
                return
            except Exception:
                continue

    # Distributable mode: read from environment variables set by config.bat.
    if os.environ.get("TOOL_TO_SHIP") or os.environ.get("STUDY_NAME"):
        _CONFIG = {
            "study_name":  os.environ.get("STUDY_NAME", "DEFAULT_STUDY"),
            "id_columns":  os.environ.get("ID_COLUMNS", "Med_ID,Visit_ID").split(","),
            "output_dir":  os.environ.get("OUTPUT_DIR", "output"),
            "log_level":   os.environ.get("LOG_LEVEL", "INFO"),
            "domains":     os.environ.get("DOMAINS", "").split(",") if os.environ.get("DOMAINS") else [],
            "folder_structure": {},
        }
        return

    # Hard-coded fallback defaults.
    _CONFIG = {
        "study_name":       "DEFAULT_STUDY",
        "id_columns":       ["Med_ID", "Visit_ID"],
        "output_dir":       "output",
        "log_level":        "INFO",
        "domains":          [],
        "folder_structure": {},
    }


_load_legacy_config()


def get_legacy_config(key: Any = None, default: Any = None) -> Any:
    """
    Return the full legacy config dict, or a single value by *key*.

    Args:
        key:     Optional key to look up.
        default: Returned when *key* is absent.
    """
    if key is None:
        return _CONFIG
    return _CONFIG.get(key, default)


# =============================================================================
# 2. PURE CONSTANTS  (level_0 appropriate)
# =============================================================================

STUDY_NAME: str = _CONFIG.get("study_name", "DEFAULT_STUDY")
ID_COLUMNS: List[str] = _CONFIG.get("id_columns", ["Med_ID", "Visit_ID"])
OUTPUT_DIR: Path = Path(_CONFIG.get("output_dir", "output"))
LOG_LEVEL: str = _CONFIG.get("log_level", "INFO")
DOMAINS: List[str] = _CONFIG.get("domains", [])
FOLDER_STRUCTURE: Dict[str, str] = _CONFIG.get("folder_structure", {})

STANDARD_KEYS: Dict[str, str] = {
    "input":       "processed_data",
    "output":      "qc_output",
    "dictionary":  "dictionary",
    "merged_data": "merged_data",
}

FILE_PATTERNS: Dict[str, str] = {
    "final_csv":      r"_FINAL\.(csv|xlsx|xls)$",
    "release_dict":   r"_Release\.(csv|xlsx|xls)$",
    "clinical_final": r"Clinical_FINAL\.(csv|xlsx)$",
    "cleaned_dict":   r"_cleaned\.(csv|xlsx)$",
    "supplement":     r"_supplement\.(csv|xlsx|xls)$",
}

COLUMN_ALIASES: Dict[str, List[str]] = {
    "Med_ID":   ["Med ID", "MedID", "Med id", "Med Id"],
    "Visit_ID": ["Visit_ID", "Visit ID", "Visit", "Visit id", "Visit Id"],
}

MISSING_VALUE_CODES: List[int] = [-9999, -8888, -777777]

MISSING_VALUE_STRINGS: FrozenSet[str] = frozenset({
    "-9999", "-9999.0", "-8888", "-8888.0",
    "-777777", "-777777.0",
    "NAN", "NAT", "NONE", "", "MISSING",
})

DEFAULT_ENCODING: str = "utf-8"
FALLBACK_ENCODING: str = "ISO-8859-1"


# =============================================================================
# 3. PATH-DISCOVERY HELPERS
#    TODO: Move to path_resolver.py or a dedicated path-convention module.
#    These encode project structure knowledge and do not belong in a constants
#    file; they are kept here only for backward compatibility.
# =============================================================================

def get_project_root() -> Path:
    """
    Walk ancestor directories to find the project root.

    A directory is considered the root when it contains ``config.yaml``
    or ``run_all.py``.  Falls back to three levels above this file.
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "config.yaml").exists() or (parent / "run_all.py").exists():
            return parent
    return Path(__file__).resolve().parents[2]


def get_domain_paths(project_root: Path) -> Dict[str, Dict[str, Path]]:
    """
    Return standard subdirectory paths for every domain under *project_root/domains/*.

    TODO: Consolidate with WorkspacePathResolver.get_all_domain_paths().
    """
    domain_paths: Dict[str, Dict[str, Path]] = {}
    domains_dir = project_root / "domains"

    if not domains_dir.exists():
        return domain_paths

    for domain_dir in domains_dir.iterdir():
        if domain_dir.is_dir() and not domain_dir.name.startswith("."):
            name = domain_dir.name
            domain_paths[name] = {
                "root":           domain_dir,
                "raw_data":       domain_dir / "raw_data",
                "processed_data": domain_dir / "processed_data",
                "merged_data":    domain_dir / "merged_data",
                "old_data":       domain_dir / "old_data",
                "dictionary":     domain_dir / "dictionary",
                "qc_output":      domain_dir / "qc_output",
                "qc_logs":        domain_dir / "qc_logs",
            }

    return domain_paths


def get_domain_output_path(
    domain_paths: Dict[str, Path],
    filename: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Path:
    """
    Compute the output file path within a domain's ``qc_output`` directory.

    TODO: Move to a higher-level path-convention module.
    """
    output_dir = domain_paths.get("qc_output", Path("output"))

    if filename:
        if suffix:
            stem, _, ext = filename.rpartition(".")
            filename = f"{stem}_{suffix}.{ext}" if stem else f"{filename}_{suffix}"
        return output_dir / filename

    return output_dir


def resolve_path(
    path: "str | Path",
    base_dir: "str | Path",
) -> Path:
    """
    Return *path* resolved relative to *base_dir* if it is not absolute.

    TODO: Use file_ops.make_absolute instead.
    """
    path = Path(path)
    return path if path.is_absolute() else Path(base_dir) / path


# =============================================================================
# 4. OUTLIER METHOD ENUM
#    TODO: Move to a domain/stats constants module — unrelated to paths.
# =============================================================================

class OutlierMethod(Enum):
    """Statistical method used for outlier detection."""
    IQR = "IQR"
    STD = "STD"