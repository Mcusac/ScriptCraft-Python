"""
Commit message policy for releases.
"""

def get_commit_message(new_version: str, version_type: str, subject: str = "ScriptCraft Python") -> str:
    """Generate a commit message based on version type."""
    if version_type == "major":
        return f"🚀 Major Release: {subject} v{new_version}\n\nBreaking changes and major new features"
    if version_type == "minor":
        return f"✨ Feature Release: {subject} v{new_version}\n\nNew features and improvements"
    return f"🐛 Bug Fix Release: {subject} v{new_version}\n\nBug fixes and minor improvements"

