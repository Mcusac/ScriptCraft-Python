from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class WorkspaceConfig:
    study_name: str = "HABS"
    default_pipeline: str = "test"
    log_level: str = "INFO"
    id_columns: List[str] = field(default_factory=lambda: ["Med_ID", "Visit_ID"])
    paths: Dict[str, Any] = field(default_factory=dict)
    domains: List[str] = field(default_factory=lambda: ["Clinical", "Biomarkers", "Genomics", "Imaging"])
    logging: Dict[str, Any] = field(default_factory=dict)
    template: Dict[str, Any] = field(default_factory=dict)
    dictionary_checker: Dict[str, Any] = field(default_factory=dict)