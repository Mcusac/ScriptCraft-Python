#!/usr/bin/env python3
"""
Build a Kaggriculture submission archive.

The Kaggriculture strategy registry is the single source of truth for
strategy identity and selection.

The submission does not contain one agent adapter per strategy. Instead,
the generated Kaggle entrypoint uses the generic Layer 3 agent adapter:

    make_agent("<registered-strategy-name>")

This keeps local testing, strategy selection, and submission building
aligned around the same registry.

Usage:

    python build_submission.py
    python build_submission.py --strategy wheat
    python build_submission.py --strategy melon_maxxer
    python build_submission.py --list-strategies
    python build_submission.py --dry-run
    python build_submission.py --strategy wheat --keep-staging
"""


# ============================================================================
# IMPORTS
# ============================================================================

import argparse
import ast
import shutil
import sys
import tarfile
import tempfile

from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================

SCRIPT_PATH = Path(__file__).resolve()

LAYER_TESTS_DIR = SCRIPT_PATH.parent

KAGGRICULTURE_DIR = LAYER_TESTS_DIR.parent.parent


PYTHON_PACKAGE_DIR: Path | None = None

for candidate in KAGGRICULTURE_DIR.parents:
    if (candidate / "scriptcraft").is_dir():
        PYTHON_PACKAGE_DIR = candidate
        break


if PYTHON_PACKAGE_DIR is None:
    raise RuntimeError(
        "Could not locate the python-package directory containing "
        "'scriptcraft'."
    )


SCRIPTCRAFT_DIR = PYTHON_PACKAGE_DIR / "scriptcraft"

KAGGRICULTURE_RELATIVE = KAGGRICULTURE_DIR.relative_to(
    SCRIPTCRAFT_DIR
)

WORKSPACE_DIR = PYTHON_PACKAGE_DIR.parents[2]

OUTPUT_DIR = WORKSPACE_DIR / "workspace" / "output"

SUBMISSION_SUBDIR = OUTPUT_DIR / "kaggriculture"


# ============================================================================
# REGISTRY
#
# IMPORTANT:
# The registry is the canonical source of strategy names.
# Do not duplicate strategy names in this build script.
# ============================================================================

REGISTRY_MODULE = (
    "scriptcraft.layers.layer_1_competition.level_1_impl."
    "level_kaggriculture.layer_3_agents.level_0.registry"
)


# ============================================================================
# GENERIC AGENT ADAPTER
#
# This is the canonical Layer 3 adapter that converts a registered strategy
# into a Kaggle-compatible agent.
# ============================================================================

AGENT_MODULE = (
    "scriptcraft.layers.layer_1_competition.level_1_impl."
    "level_kaggriculture.layer_3_agents.level_1.agent"
)


# ============================================================================
# SUBMISSION EXCLUSIONS
# ============================================================================

EXCLUDED_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".DS_Store",
}


EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
}


EXCLUDED_FILES = {
    "build_submission.py",
}


EXCLUDED_DIR_NAMES = {
    "layer_tests",
    "tests",
}


# ============================================================================
# OUTPUT
# ============================================================================

def log(message: str) -> None:
    """Print a build message."""

    print(f"[build] {message}")


def fail(message: str) -> None:
    """Abort the build with a clear error."""

    print(
        f"[build] ERROR: {message}",
        file=sys.stderr,
    )

    raise SystemExit(1)


# ============================================================================
# REGISTRY HELPERS
# ============================================================================

def load_registry():
    """
    Load the canonical Kaggriculture strategy registry.

    The import occurs here rather than maintaining a second copy of the
    registry in this build script.
    """

    try:
        from scriptcraft.layers.layer_1_competition.level_1_impl.level_kaggriculture.layer_3_agents.level_0.registry import (
            DEFAULT_STRATEGY,
            available_strategies,
        )

    except ImportError as exc:
        fail(
            "Could not import the Kaggriculture strategy registry.\n\n"
            f"Expected registry module:\n"
            f"    {REGISTRY_MODULE}\n\n"
            f"Import error:\n"
            f"    {exc}"
        )

    return DEFAULT_STRATEGY, available_strategies


def get_available_strategies() -> tuple[str, ...]:
    """Return all strategy names from the canonical registry."""

    _, available_strategies = load_registry()

    strategies = tuple(available_strategies())

    if not strategies:
        fail(
            "The Kaggriculture strategy registry contains no strategies."
        )

    return strategies


def get_default_strategy() -> str:
    """Return the default strategy from the canonical registry."""

    default_strategy, _ = load_registry()

    return default_strategy


def validate_strategy(strategy_name: str) -> None:
    """
    Validate that a strategy exists in the canonical registry.
    """

    available = get_available_strategies()

    if strategy_name not in available:

        formatted = "\n".join(
            f"    {name}"
            for name in available
        )

        fail(
            f"Unknown Kaggriculture strategy '{strategy_name}'.\n\n"
            f"Registered strategies:\n"
            f"{formatted}\n\n"
            f"Build with:\n"
            f"    python build_submission.py --strategy <name>"
        )


def list_strategies() -> None:
    """Print registered strategies and the registry default."""

    default_strategy = get_default_strategy()

    strategies = get_available_strategies()

    print()
    print("Available Kaggriculture strategies:")

    for strategy in strategies:

        marker = " <- default" if strategy == default_strategy else ""

        print(
            f"  {strategy}{marker}"
        )

    print()


# ============================================================================
# FILE FILTERING
# ============================================================================

def should_exclude(path: Path) -> bool:
    """Determine whether a path should be excluded from the submission."""

    if path.name in EXCLUDED_NAMES:
        return True

    if path.name in EXCLUDED_DIR_NAMES:
        return True

    if path.name in EXCLUDED_FILES:
        return True

    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True

    return False


def copy_filtered_tree(
    source: Path,
    destination: Path,
) -> list[Path]:
    """
    Copy source recursively while excluding development/test artifacts.
    """

    copied: list[Path] = []

    for path in source.rglob("*"):

        relative = path.relative_to(source)

        if any(
            part in EXCLUDED_NAMES
            for part in relative.parts
        ):
            continue

        if any(
            part in EXCLUDED_DIR_NAMES
            for part in relative.parts
        ):
            continue

        if path.is_file():

            if should_exclude(path):
                continue

            target = destination / relative

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                path,
                target,
            )

            copied.append(target)

    return copied


# ============================================================================
# PYTHON VALIDATION
# ============================================================================

def validate_python_syntax(root: Path) -> None:
    """
    Compile every Python source file without executing it.
    """

    log("Checking Python syntax...")

    files = [
        path
        for path in root.rglob("*.py")
        if not should_exclude(path)
        and not any(
            part in EXCLUDED_DIR_NAMES
            for part in path.relative_to(root).parts
        )
    ]

    if not files:
        fail(
            "No Python files were found in the Kaggriculture package."
        )

    errors: list[str] = []

    for path in files:

        try:

            source = path.read_text(
                encoding="utf-8"
            )

            compile(
                source,
                str(path),
                "exec",
            )

        except SyntaxError as exc:

            errors.append(
                f"{path}: "
                f"line {exc.lineno}: "
                f"{exc.msg}"
            )

    if errors:

        print()

        for error in errors:
            print(
                f"    {error}",
                file=sys.stderr,
            )

        print()

        fail(
            "Python syntax validation failed for "
            f"{len(errors)} file(s)."
        )

    log(
        f"Syntax OK ({len(files)} Python files checked)."
    )


def inspect_absolute_scriptcraft_imports(
    package_root: Path,
) -> set[str]:
    """
    Inspect Kaggriculture source files for absolute imports beginning
    with 'scriptcraft'.
    """

    imports: set[str] = set()

    for python_file in [
        path
        for path in package_root.rglob("*.py")
        if not should_exclude(path)
    ]:

        try:

            source = python_file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(
                source,
                filename=str(python_file),
            )

        except (
            UnicodeDecodeError,
            SyntaxError,
        ):
            continue

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    if (
                        alias.name == "scriptcraft"
                        or alias.name.startswith(
                            "scriptcraft."
                        )
                    ):
                        imports.add(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.level != 0:
                    continue

                if not node.module:
                    continue

                if (
                    node.module == "scriptcraft"
                    or node.module.startswith(
                        "scriptcraft."
                    )
                ):
                    imports.add(node.module)

    return imports


# ============================================================================
# SUBMISSION ENTRYPOINT
# ============================================================================

def create_root_main(
    staging_dir: Path,
    strategy_name: str,
) -> None:
    """
    Generate the root-level Kaggle main.py.

    The generated entrypoint delegates strategy construction to the
    canonical Layer 3 generic agent adapter.

    This intentionally does NOT import a strategy implementation directly.
    """

    wrapper = f'''"""
Kaggriculture Kaggle submission entrypoint.

Strategy:
    {strategy_name}

Generated by:
    build_submission.py

The strategy is resolved through the canonical Kaggriculture registry.
"""

from {AGENT_MODULE} import make_agent


agent = make_agent("{strategy_name}")


__all__ = ["agent"]
'''

    target = staging_dir / "main.py"

    target.write_text(
        wrapper,
        encoding="utf-8",
    )

    log(
        "Generated main.py "
        f"for registered strategy '{strategy_name}'."
    )


def validate_generated_main(
    staging_dir: Path,
) -> None:
    """
    Verify that the generated main.py can be parsed.
    """

    main_py = staging_dir / "main.py"

    if not main_py.is_file():
        fail(
            "Generated main.py not found in staging directory."
        )

    log("Validating generated main.py...")

    try:

        source = main_py.read_text(
            encoding="utf-8"
        )

        compile(
            source,
            str(main_py),
            "exec",
        )

    except SyntaxError as exc:

        fail(
            "Syntax error in generated main.py:\n"
            f"  {exc}"
        )

    log("main.py validation passed.")


# ============================================================================
# ARCHIVE VALIDATION
# ============================================================================

def validate_archive(
    archive_path: Path,
) -> None:
    """Validate the final tar.gz archive."""

    log("Validating submission archive...")

    with tarfile.open(
        archive_path,
        "r:gz",
    ) as archive:

        names = archive.getnames()

    normalized = {
        name.rstrip("/")
        for name in names
    }

    if "main.py" not in normalized:

        fail(
            "Submission archive does not contain "
            "main.py at its root."
        )

    forbidden_fragments = (
        "/layer_tests/",
        "/tests/",
        "__pycache__/",
        ".pytest_cache/",
    )

    bad_entries = [
        name
        for name in names
        if any(
            fragment in f"/{name}/"
            for fragment in forbidden_fragments
        )
    ]

    if bad_entries:

        print(
            "[build] WARNING: archive contains "
            "development/test paths:",
            file=sys.stderr,
        )

        for name in bad_entries:
            print(
                f"    {name}",
                file=sys.stderr,
            )

    log(
        f"Archive OK: {archive_path}"
    )


# ============================================================================
# ARCHIVE CREATION
# ============================================================================

def create_archive(
    staging_dir: Path,
    output_path: Path,
) -> None:
    """Create the final gzip-compressed tar archive."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if output_path.exists():
        output_path.unlink()

    log(
        f"Creating archive: {output_path}"
    )

    with tarfile.open(
        output_path,
        mode="w:gz",
    ) as archive:

        for path in sorted(
            staging_dir.rglob("*")
        ):

            if path.is_file():

                archive.add(
                    path,
                    arcname=path.relative_to(
                        staging_dir
                    ),
                    recursive=False,
                )


# ============================================================================
# BUILD
# ============================================================================

def build(
    strategy_name: str,
    output_path: Path,
    keep_staging: bool,
    dry_run: bool,
) -> None:
    """
    Execute the complete submission build.
    """

    log(
        "Starting Kaggriculture submission build."
    )

    print()

    log(
        f"Strategy: {strategy_name}"
    )

    log(
        f"Output: {output_path}"
    )

    print()

    # ------------------------------------------------------------------------
    # Validate strategy against registry.
    # ------------------------------------------------------------------------

    validate_strategy(
        strategy_name
    )

    log(
        "Strategy registry validation passed."
    )

    # ------------------------------------------------------------------------
    # Validate source package.
    # ------------------------------------------------------------------------

    validate_python_syntax(
        KAGGRICULTURE_DIR
    )

    # ------------------------------------------------------------------------
    # Inspect imports.
    # ------------------------------------------------------------------------

    scriptcraft_imports = (
        inspect_absolute_scriptcraft_imports(
            KAGGRICULTURE_DIR
        )
    )

    if scriptcraft_imports:

        log(
            "Detected ScriptCraft imports:"
        )

        for module in sorted(
            scriptcraft_imports
        ):
            log(
                f"    {module}"
            )

    # ------------------------------------------------------------------------
    # Dry run.
    # ------------------------------------------------------------------------

    if dry_run:

        print()

        log(
            "DRY RUN: no archive was created."
        )

        return

    # ------------------------------------------------------------------------
    # Create temporary staging directory.
    # ------------------------------------------------------------------------

    staging_parent = Path(
        tempfile.mkdtemp(
            prefix="kaggriculture_submission_",
            dir=str(WORKSPACE_DIR),
        )
    )

    staging_dir = (
        staging_parent / "submission"
    )

    staging_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:

        # --------------------------------------------------------------------
        # Copy Kaggriculture package.
        # --------------------------------------------------------------------

        destination_scriptcraft = (
            staging_dir / "scriptcraft"
        )

        destination_kaggriculture = (
            destination_scriptcraft
            / KAGGRICULTURE_RELATIVE
        )

        destination_kaggriculture.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Instead of copy_filtered_tree, explicitly copy the production layers
        production_layers = ["layer_0_reality", "layer_2_strategy", "layer_3_agents"]

        for layer_name in production_layers:
            src_layer = KAGGRICULTURE_DIR / layer_name
            dst_layer = destination_kaggriculture / layer_name
            
            if src_layer.is_dir():
                log(f"Copying {layer_name}...")
                shutil.copytree(
                    src_layer,
                    dst_layer,
                    ignore=shutil.ignore_patterns(
                        "__pycache__",
                        "*.pyc",
                        ".pytest_cache",
                    ),
                )
            else:
                fail(f"Production layer not found: {src_layer}")

        copied_files = [
            f for f in destination_kaggriculture.rglob("*.py")
        ]

        log(f"Copied {len(copied_files)} Python files from production layers.")

        # --------------------------------------------------------------------
        # Preserve required __init__.py files above Kaggriculture.
        # --------------------------------------------------------------------

        current_source = SCRIPTCRAFT_DIR

        current_destination = (
            destination_scriptcraft
        )

        if (
            current_source / "__init__.py"
        ).is_file():

            shutil.copy2(
                current_source / "__init__.py",
                current_destination
                / "__init__.py",
            )

        for part in (
            KAGGRICULTURE_RELATIVE.parts[:-1]
        ):

            current_source = (
                current_source / part
            )

            current_destination = (
                current_destination / part
            )

            current_destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            init_file = (
                current_source
                / "__init__.py"
            )

            if init_file.is_file():

                shutil.copy2(
                    init_file,
                    current_destination
                    / "__init__.py",
                )

        # --------------------------------------------------------------------
        # Generate root Kaggle entrypoint.
        # --------------------------------------------------------------------

        create_root_main(
            staging_dir=staging_dir,
            strategy_name=strategy_name,
        )

        # --------------------------------------------------------------------
        # Show submission contents.
        # --------------------------------------------------------------------

        print()

        log(
            "Submission contents:"
        )

        submission_files = sorted(
            path.relative_to(
                staging_dir
            )
            for path in staging_dir.rglob("*")
            if path.is_file()
        )

        for path in submission_files[:20]:

            print(
                f"    {path}"
            )

        if len(submission_files) > 20:

            print(
                "    ... and "
                f"{len(submission_files) - 20} "
                "more files"
            )

        print()

        # --------------------------------------------------------------------
        # Validate generated entrypoint.
        # --------------------------------------------------------------------

        validate_generated_main(
            staging_dir
        )

        print()

        # --------------------------------------------------------------------
        # Create archive.
        # --------------------------------------------------------------------

        create_archive(
            staging_dir=staging_dir,
            output_path=output_path,
        )

        # --------------------------------------------------------------------
        # Validate archive.
        # --------------------------------------------------------------------

        validate_archive(
            output_path
        )

        # --------------------------------------------------------------------
        # Check archive size.
        # --------------------------------------------------------------------

        size_bytes = (
            output_path.stat().st_size
        )

        size_mib = (
            size_bytes
            / (1024 * 1024)
        )

        print()

        log(
            "Submission size: "
            f"{size_bytes:,} bytes "
            f"({size_mib:.2f} MiB)"
        )

        if size_mib >= 100:

            fail(
                "Submission exceeds "
                "Kaggle's 100 MiB limit."
            )

        # --------------------------------------------------------------------
        # Success.
        # --------------------------------------------------------------------

        print()

        log(
            "BUILD SUCCESSFUL"
        )

        log(
            f"Strategy: {strategy_name}"
        )

        log(
            f"Submission: {output_path}"
        )

        print()

        print(
            "Next steps:"
        )

        print()

        print(
            "  1. Verify archive contents:"
        )

        print(
            f"     tar -tzf {output_path} | head -20"
        )

        print()

        print(
            "  2. Submit to Kaggle:"
        )

        print(
            f'     kaggle competitions submit '
            f'kaggriculture -f "{output_path}" '
            f'-m "{strategy_name} submission"'
        )

        print()

        print(
            "  3. Check submission status:"
        )

        print(
            "     kaggle competitions submissions "
            "kaggriculture"
        )

        print()

        # --------------------------------------------------------------------
        # Preserve staging if requested.
        # --------------------------------------------------------------------

        if keep_staging:

            persistent_staging = (
                SUBMISSION_SUBDIR
                / "submission_staging"
            )

            if persistent_staging.exists():

                shutil.rmtree(
                    persistent_staging
                )

            shutil.copytree(
                staging_dir,
                persistent_staging,
            )

            log(
                "Staging directory preserved at:"
            )

            log(
                f"    {persistent_staging}"
            )

    finally:

        shutil.rmtree(
            staging_parent,
            ignore_errors=True,
        )


# ============================================================================
# CLI
# ============================================================================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Build a self-contained Kaggriculture "
            "Kaggle submission using the strategy registry."
        )
    )

    parser.add_argument(
        "--strategy",
        metavar="NAME",
        default=None,
        help=(
            "Registered strategy to submit. "
            "Defaults to the registry's DEFAULT_STRATEGY."
        ),
    )

    parser.add_argument(
        "--list-strategies",
        action="store_true",
        help=(
            "List registered strategies and exit."
        ),
    )

    parser.add_argument(
        "--output",
        metavar="FILE",
        type=Path,
        default=None,
        help=(
            "Output tar.gz path. "
            f"Default: "
            f"{SUBMISSION_SUBDIR}/submission.tar.gz"
        ),
    )

    parser.add_argument(
        "--keep-staging",
        action="store_true",
        help=(
            "Keep a copy of the staged submission "
            "in output/kaggriculture/submission_staging/"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate the strategy and package "
            "without creating an archive."
        ),
    )

    return parser.parse_args()


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """CLI entrypoint."""

    args = parse_args()

    # ------------------------------------------------------------------------
    # List registry.
    # ------------------------------------------------------------------------

    if args.list_strategies:

        list_strategies()

        return

    # ------------------------------------------------------------------------
    # Resolve strategy from registry.
    # ------------------------------------------------------------------------

    if args.strategy is None:

        strategy_name = (
            get_default_strategy()
        )

    else:

        strategy_name = args.strategy

    # ------------------------------------------------------------------------
    # Validate strategy before doing any build work.
    # ------------------------------------------------------------------------

    validate_strategy(
        strategy_name
    )

    # ------------------------------------------------------------------------
    # Resolve output.
    # ------------------------------------------------------------------------

    if args.output is None:

        output_path = (
            SUBMISSION_SUBDIR
            / "submission.tar.gz"
        )

    else:

        output_path = args.output

        if not output_path.is_absolute():

            output_path = (
                WORKSPACE_DIR
                / output_path
            )

    # ------------------------------------------------------------------------
    # Build.
    # ------------------------------------------------------------------------

    build(
        strategy_name=strategy_name,
        output_path=output_path,
        keep_staging=args.keep_staging,
        dry_run=args.dry_run,
    )


# ============================================================================
# ENTRYPOINT
# ============================================================================

if __name__ == "__main__":
    main()