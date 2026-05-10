from pathlib import Path
from typing import Any, Dict, List


class AuditorReporter:
    """Handles audit output."""

    @staticmethod
    def print_report(
        target_file: Path,
        project_root: Path,
        result: Dict[str, List[Dict[str, Any]]],
    ) -> None:
        unused = result["unused"]
        used = result["used"]

        print("=" * 80)
        print("📊 FUNCTION USAGE AUDIT REPORT")
        print("=" * 80)

        try:
            rel = target_file.relative_to(project_root)
        except Exception:
            rel = target_file

        print(f"📁 File: {rel}")
        print(f"📋 Total functions: {len(unused) + len(used)}")
        print(f"✅ Used: {len(used)}")
        print(f"❌ Unused: {len(unused)}")
        print()

        if unused:
            print("🚨 UNUSED FUNCTIONS:")
            for f in unused:
                print(f"   ❌ {f['name']} (line {f['line']})")
            print()