
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from layers.layer_1_pypi.level_0_infra.level_0.logging_schema import LogConfig
from layers.layer_1_pypi.level_0_infra.level_0.paths_schema import PathConfig
from layers.layer_1_pypi.level_0_infra.level_0.workspace_schema import WorkspaceConfig
from layers.layer_1_pypi.level_0_infra.level_0._version import get_version
from layers.layer_1_pypi.level_0_infra.level_0.path_resolver import PathResolver
from layers.layer_1_pypi.level_0_infra.level_1.framework_schema import FrameworkConfig

@dataclass
class Config:
    framework: FrameworkConfig = field(default_factory=FrameworkConfig)
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)

    tools: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    pipelines: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    tool_configs: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Legacy compatibility fields (deprecated; prefer workspace.*)
    study_name: str = field(default="HABS", init=False)
    default_pipeline: str = field(default="test", init=False)
    log_level: str = field(default="INFO", init=False)
    id_columns: List[str] = field(default_factory=lambda: ["Med_ID", "Visit_ID"], init=False)
    paths: PathConfig = field(default_factory=PathConfig, init=False)
    domains: List[str] = field(default_factory=list, init=False)
    dictionary_checker: Dict[str, Any] = field(default_factory=dict, init=False)
    logging: LogConfig = field(default_factory=LogConfig, init=False)
    template: Dict[str, Any] = field(default_factory=dict, init=False)

    project_name: str = "Release Workspace"
    version: str = field(default_factory=get_version)

    workspace_root: Optional[Path] = None
    _path_resolver: Optional[PathResolver] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        # Legacy compatibility mapping
        self.study_name = self.workspace.study_name
        self.default_pipeline = self.workspace.default_pipeline
        self.log_level = self.workspace.log_level
        self.id_columns = self.workspace.id_columns
        self.domains = self.workspace.domains
        self.dictionary_checker = self.workspace.dictionary_checker
        self.template = self.workspace.template

        if self.workspace.paths:
            self.paths = PathConfig(**self.workspace.paths)

        if self.workspace.logging:
            self.logging = LogConfig(**self.workspace.logging)