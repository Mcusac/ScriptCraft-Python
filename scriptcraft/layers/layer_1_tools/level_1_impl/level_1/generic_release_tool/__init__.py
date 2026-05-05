"""Auto-generated package exports."""


from .pipelines import (
    StepCallable,
    create_docs_pipeline,
    create_full_pipeline,
    create_git_repo_pipeline,
    create_python_package_pipeline,
)

from .steps_git import (
    check_git_status,
    create_git_tag,
    push_to_remote,
)

from .version_resolver import (
    VersionResolution,
    detect_repo_root,
    resolve_version,
)

__all__ = [
    "StepCallable",
    "VersionResolution",
    "check_git_status",
    "create_docs_pipeline",
    "create_full_pipeline",
    "create_git_repo_pipeline",
    "create_git_tag",
    "create_python_package_pipeline",
    "detect_repo_root",
    "push_to_remote",
    "resolve_version",
]
