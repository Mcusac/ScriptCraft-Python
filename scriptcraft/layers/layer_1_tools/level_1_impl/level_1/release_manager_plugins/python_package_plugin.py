"""
Python Package Release Plugin for Release Manager Tool.

This plugin handles releasing Python packages with version bumping, building, and PyPI uploading.
"""
import os
import subprocess
import shutil

from pathlib import Path
from typing import List, Optional

from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_2.root_schema import get_config

from layers.layer_1_tools.level_1_impl.level_0.versioning.messages import get_commit_message
from layers.layer_1_tools.level_1_impl.level_0.versioning.semver import bump_version
from layers.layer_1_tools.level_1_impl.level_0.versioning.version_file import (
    get_current_version,
    update_version_file,
)


def run_command(command: str, description: str, cwd: Optional[Path] = None) -> Optional[str]:
    """Run a command and handle errors."""
    log_and_print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, 
            check=True, encoding='utf-8', errors='replace', cwd=cwd
        )
        log_and_print(f"✅ {description} completed")
        return result.stdout.strip() if result.stdout else ""
    except subprocess.CalledProcessError as e:
        log_and_print(f"❌ {description} failed: {e}", level="error")
        if e.stderr:
            # Handle potential encoding issues in stderr
            try:
                error_output = e.stderr
            except UnicodeDecodeError:
                error_output = e.stderr.encode('utf-8', errors='replace').decode('utf-8')
            log_and_print(f"Error output: {error_output}", level="error")
        return None
    except UnicodeDecodeError as e:
        log_and_print(f"❌ {description} failed due to encoding issue: {e}", level="error")
        return None


def _get_workspace_version_strategy() -> str:
    """Determine workspace versioning strategy: mirror | independent | none.

    Priority: ENV WORKSPACE_VERSION_STRATEGY > config.framework.packaging.workspace_version_strategy > 'mirror'
    """
    # 1) Environment override
    env_value = os.environ.get("WORKSPACE_VERSION_STRATEGY")
    if env_value:
        return env_value.strip().lower()

    # 2) Config value if available
    try:
        config = get_config()
        if config is not None:
            framework_cfg = config.get_framework_config() if hasattr(config, 'get_framework_config') else None
            packaging = getattr(framework_cfg, 'packaging', None)
            if isinstance(packaging, dict):
                value = packaging.get('workspace_version_strategy')
                if isinstance(value, str) and value.strip():
                    return value.strip().lower()
    except Exception:
        # Fallback below on any issue
        pass

    # 3) Default
    return 'mirror'


def clean_build_artifacts() -> None:
    """Clean old build artifacts."""
    log_and_print("🧹 Cleaning build artifacts...")
    artifacts = ["dist", "build", "*.egg-info"]
    for artifact in artifacts:
        artifact_path = Path(artifact)
        if artifact_path.exists():
            if artifact_path.is_dir():
                shutil.rmtree(artifact_path)
            else:
                artifact_path.unlink()
            log_and_print(f"🗑️ Removed {artifact}")


def build_package() -> bool:
    """Build the Python package."""
    return run_command("python -m build", "Building package") is not None


def upload_to_pypi() -> bool:
    """Upload package to PyPI."""
    return run_command("python -m twine upload dist/*", "Uploading to PyPI") is not None


def run_mode(input_paths: List[Path], output_dir: Path, domain: Optional[str] = None, 
             version_type: Optional[str] = None, auto_push: bool = False, 
             force: bool = False, custom_message: Optional[str] = None, 
             skip_pypi: bool = False, **kwargs) -> None:
    """
    Run Python package release mode.
    
    Args:
        input_paths: List of input paths (not used for this plugin)
        output_dir: Output directory (not used for this plugin)
        domain: Domain context (not used for this plugin)
        version_type: Type of version bump (major, minor, patch)
        auto_push: Whether to push to remote automatically
        force: Force release even if no changes
        custom_message: Custom commit message
        skip_pypi: Skip PyPI upload
        **kwargs: Additional arguments
    """
    log_and_print("🚀 Running Python Package Release Mode...")
    
    # Validate version type
    if not version_type:
        log_and_print("❌ Version type required for Python package release", level="error")
        log_and_print("Usage: --version-type major|minor|patch", level="error")
        return
    
    if version_type not in ["major", "minor", "patch"]:
        log_and_print(f"❌ Invalid version type: {version_type}", level="error")
        log_and_print("Use: major, minor, or patch", level="error")
        return
    
    log_and_print(f"🔧 ScriptCraft Python Package Release Process")
    log_and_print("=" * 50)
    
    # Store original directory for later restoration
    original_cwd = os.getcwd()
    
    # Determine the correct submodule directory
    # If we're already in the python-package directory, use current directory
    if os.path.basename(original_cwd) == "python-package":
        submodule_dir = original_cwd
        log_and_print(f"📁 Already in python-package directory: {submodule_dir}")
    else:
        # Otherwise, try to find the submodule directory
        submodule_dir = Path("implementations/python-package")
        if not submodule_dir.exists():
            # Try relative to current directory
            submodule_dir = Path(original_cwd) / "implementations/python-package"
            if not submodule_dir.exists():
                log_and_print(f"❌ Cannot find python-package directory", level="error")
                return
        log_and_print(f"📁 Working in submodule directory: {submodule_dir}")
        os.chdir(submodule_dir)
    
    # Get current version (now that we're in the submodule directory)
    current_version = get_current_version()
    if not current_version:
        return
    
    # Calculate new version
    new_version = bump_version(current_version, version_type)
    if not new_version:
        return
    
    log_and_print(f"🔄 Updating from {current_version} to {new_version}")
    
    # Step 1: Update version file
    if not update_version_file(new_version):
        return
    
    # Step 2: Clean build artifacts
    clean_build_artifacts()
    
    # Step 3: Build package
    if not build_package():
        log_and_print("❌ Build failed. Aborting release.", level="error")
        return
    
    # Step 4: Upload to PyPI (unless skipped)
    if not skip_pypi:
        if not upload_to_pypi():
            log_and_print("❌ PyPI upload failed. Aborting release.", level="error")
            return
        log_and_print("✅ Successfully uploaded to PyPI!")
    else:
        log_and_print("⏭️ Skipping PyPI upload (--skip-pypi flag)")
    
    # Step 5: Stage all changes (we're now in the submodule directory)
    staging_result = run_command("git add .", "Staging all changes")
    if staging_result is None:
        log_and_print("❌ Failed to stage changes. Aborting release.", level="error")
        return
    
    # Step 6: Check if there are changes to commit
    status = run_command("git status --porcelain", "Checking git status")
    if not status and not force:
        log_and_print("⚠️ No changes to commit. Did you make any changes?", level="warning")
        log_and_print("💡 Use --force flag to continue anyway", level="warning")
        return
    
    # Step 7: Commit with proper message
    commit_message = custom_message if custom_message else get_commit_message(new_version, version_type)
    commit_result = run_command(f'git commit -m "{commit_message}"', "Creating commit")
    if commit_result is None:
        log_and_print("❌ Failed to create commit. Aborting release.", level="error")
        log_and_print("💡 Check git status and ensure changes are staged", level="error")
        return
    
    # Step 8: Create git tag (check if it already exists)
    existing_tag = run_command(f"git tag -l v{new_version}", f"Checking if tag v{new_version} exists")
    if existing_tag:
        log_and_print(f"⚠️ Tag v{new_version} already exists. Skipping tag creation.", level="warning")
    else:
        tag_result = run_command(f"git tag v{new_version}", f"Creating tag v{new_version}")
        if tag_result is None:
            log_and_print("❌ Failed to create tag. Aborting release.", level="error")
            return
    
    # Step 9: Push to remote (if requested)
    if auto_push:
        log_and_print("=" * 50)
        log_and_print("🚀 Pushing to remote repository...")
        push_commits = run_command("git push origin main", "Pushing commits")
        push_tags = run_command(f"git push origin v{new_version}", f"Pushing tag v{new_version}")
        if push_commits is None or push_tags is None:
            log_and_print("⚠️ Failed to push to remote, but release was successful locally", level="warning")
        else:
            log_and_print("✅ Successfully pushed to remote repository!")
    
    # Step 10: Return to original directory and update main workspace
    log_and_print("📁 Returning to main workspace...")
    os.chdir(original_cwd)
    
    # Update the submodule reference in the main workspace
    log_and_print("🔄 Updating submodule reference in main workspace...")
    
    # Check if we're in a submodule (python-package directory)
    if os.path.basename(original_cwd) == "python-package":
        # We're in the submodule, need to go to workspace root
        workspace_root = Path(original_cwd).parent.parent
        log_and_print(f"📁 Switching to workspace root: {workspace_root}")
        os.chdir(workspace_root)
    
    # Now update the submodule reference
    submodule_update = run_command("git submodule update --remote implementations/python-package", "Updating submodule reference")
    if submodule_update is None:
        log_and_print("⚠️ Failed to update submodule reference", level="warning")
    
    # Stage and commit the submodule update in main workspace
    main_staging = run_command("git add implementations/python-package", "Staging submodule update")
    if main_staging is None:
        log_and_print("⚠️ Failed to stage submodule update", level="warning")
    else:
        main_commit = run_command(f'git commit -m "📦 Update python-package submodule to v{new_version}"', "Committing submodule update")
        if main_commit is None:
            log_and_print("⚠️ Failed to commit submodule update", level="warning")
        
        # Push main workspace changes if auto_push is enabled
        if auto_push:
            main_push = run_command("git push origin main", "Pushing main workspace changes")
            if main_push is None:
                log_and_print("⚠️ Failed to push main workspace changes", level="warning")

    # Workspace versioning strategy handling
    strategy = _get_workspace_version_strategy()
    log_and_print(f"🧭 Workspace version strategy: {strategy}")
    if strategy == 'mirror':
        # Write VERSION file, commit, tag, and push (if requested)
        try:
            Path("VERSION").write_text(f"{new_version}\n", encoding='utf-8')
            staged = run_command("git add VERSION", "Staging workspace VERSION file")
            if staged is None:
                log_and_print("⚠️ Failed to stage VERSION file", level="warning")
            else:
                committed = run_command(f'git commit -m " Workspace v{new_version} (mirror python-package)"', "Committing workspace VERSION")
                # Create tag if it doesn't exist
                existing_ws_tag = run_command(f"git tag -l v{new_version}", f"Checking workspace tag v{new_version}")
                if not existing_ws_tag:
                    _ = run_command(f"git tag v{new_version}", f"Creating workspace tag v{new_version}")
                # Push if requested
                if auto_push:
                    _ = run_command("git push origin main", "Pushing workspace VERSION commit")
                    _ = run_command(f"git push origin v{new_version}", f"Pushing workspace tag v{new_version}")
        except Exception as e:
            log_and_print(f"⚠️ Workspace mirroring failed: {e}", level="warning")
    elif strategy in ('independent', 'none'):
        log_and_print("ℹ️ Skipping workspace version mirroring (strategy independent/none)")
    
    # Success!
    log_and_print("=" * 50)
    log_and_print(f"🎉 Successfully released ScriptCraft Python v{new_version}!")
    
    # Show what was done
    log_and_print("\n✅ Completed:")
    log_and_print(f"   • Updated _version.py to {new_version}")
    log_and_print(f"   • Cleaned build artifacts")
    log_and_print(f"   • Built package")
    if not skip_pypi:
        log_and_print(f"   • Uploaded to PyPI")
    log_and_print(f"   • Committed all changes")
    log_and_print(f"   • Created git tag v{new_version}")
    if auto_push:
        log_and_print(f"   • Pushed to remote repository")
    
    # Show next steps
    log_and_print("\n📝 Next steps:")
    if not auto_push:
        log_and_print("   1. Push to remote repository:")
        log_and_print(f"      git push origin main")
        log_and_print(f"      git push origin v{new_version}")
    log_and_print("   2. Test the new package:")
    log_and_print(f"      pip install scriptcraft-python=={new_version}")
    log_and_print("   3. Update embedded Python builds with new version")
    
    # Show current status
    log_and_print(f"\n📊 Current status:")
    log_result = run_command("git log --oneline -1", "Latest commit")
    latest_tag = run_command("git describe --tags --abbrev=0", "Latest tag")
    if latest_tag:
        log_and_print(f"Latest tag: {latest_tag}")
    else:
        log_and_print("Latest tag: None")
