"""
Centralized project constants and lightweight config loading for level_0 consumers.
"""

import os
import yaml

from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional

from layers.layer_1_tools.level_0_infra.level_0.environment import detect_environment
from layers.layer_1_tools.level_0_infra.level_0.path_resolver import build_domain_paths

_CONFIG: Dict[str, Any] = {}


def _load_legacy_config() -> None:
    """
    Populate _CONFIG from the first config.yaml found, env vars, or defaults.
    Uses detect_environment() to identify distributable mode.
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

    # Use the canonical environment detector instead of duplicating the checks.
    if detect_environment() == "production":
        _CONFIG = {
            "study_name":       os.environ.get("STUDY_NAME", "DEFAULT_STUDY"),
            "id_columns":       os.environ.get("ID_COLUMNS", "Med_ID,Visit_ID").split(","),
            "output_dir":       os.environ.get("OUTPUT_DIR", "output"),
            "log_level":        os.environ.get("LOG_LEVEL", "INFO"),
            "domains":          os.environ.get("DOMAINS", "").split(",") if os.environ.get("DOMAINS") else [],
            "folder_structure": {},
        }
        return

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
    if key is None:
        return _CONFIG
    return _CONFIG.get(key, default)


# =============================================================================
# PURE CONSTANTS
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
# PATH-DISCOVERY HELPERS (backward compat; see path_resolver.py for canonical)
# =============================================================================

def get_project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "config.yaml").exists() or (parent / "run_all.py").exists():
            return parent
    return Path(__file__).resolve().parents[2]


def get_domain_paths(project_root: Path) -> Dict[str, Dict[str, Path]]:
    """
    Return standard subdirectory paths for every domain under *project_root/domains/*.
    Delegates to build_domain_paths() — single source of truth for domain keys.
    """
    domain_paths: Dict[str, Dict[str, Path]] = {}
    domains_dir = project_root / "domains"

    if not domains_dir.exists():
        return domain_paths

    for domain_dir in domains_dir.iterdir():
        if domain_dir.is_dir() and not domain_dir.name.startswith("."):
            domain_paths[domain_dir.name] = build_domain_paths(domain_dir)

    return domain_paths


def get_domain_output_path(
    domain_paths: Dict[str, Path],
    filename: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Path:
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
    path = Path(path)
    return path if path.is_absolute() else Path(base_dir) / path