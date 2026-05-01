"""Auto-generated package exports."""


from .comparison_core import (
    ComparisonResult,
    CoreDataFrameComparer,
)

from .constants import OutlierMethod

from .directory_ops import (
    clean_directory,
    ensure_dir,
    list_files,
)

from .emitter import (
    get_handler_paths,
    log,
    log_and_print,
    print_message,
)

from .environment import detect_environment

from .file_ops import (
    copy_file,
    find_latest_file,
    find_matching_file,
    make_absolute,
    move_file,
    resolve_file,
)

from .formatter import (
    DEFAULT_LOG_FORMAT,
    Utf8Formatter,
)

from .handlers import (
    build_file_handler,
    build_stream_handler,
    configure_handler,
    has_handler_type,
)

from .logging_primitives import (
    LogConfig,
    StructuredFormatter,
)

from .logging_schema import LogConfig

from .path_resolver import (
    PathResolver,
    WorkspacePathResolver,
    build_domain_paths,
    create_path_resolver,
)

from .paths_schema import PathConfig

from .typed_plugin_store import get_typed_plugin

from .version import (
    VERSION_INFO,
    get_version,
    get_version_info,
)

from .workspace_schema import WorkspaceConfig

__all__ = [
    "ComparisonResult",
    "CoreDataFrameComparer",
    "DEFAULT_LOG_FORMAT",
    "LogConfig",
    "OutlierMethod",
    "PathConfig",
    "PathResolver",
    "StructuredFormatter",
    "Utf8Formatter",
    "VERSION_INFO",
    "WorkspaceConfig",
    "WorkspacePathResolver",
    "build_domain_paths",
    "build_file_handler",
    "build_stream_handler",
    "clean_directory",
    "configure_handler",
    "copy_file",
    "create_path_resolver",
    "detect_environment",
    "ensure_dir",
    "find_latest_file",
    "find_matching_file",
    "get_handler_paths",
    "get_typed_plugin",
    "get_version",
    "get_version_info",
    "has_handler_type",
    "list_files",
    "log",
    "log_and_print",
    "make_absolute",
    "move_file",
    "print_message",
    "resolve_file",
]
