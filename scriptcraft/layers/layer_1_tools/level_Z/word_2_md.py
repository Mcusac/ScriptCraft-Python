from pathlib import Path
import subprocess
import shutil
import sys

# === CONFIG ===
INPUT_FILE = Path(
    r"C:\Users\mdc0431\OneDrive - UNT System\Documents\Projects\ScriptCraft-Workspace\workspace\input\Clean HABS Veterans consent March 2026.pdf (stamped).docx"
)

# === LOGIC ===
def find_pandoc() -> str:
    # 1. Try PATH
    pandoc = shutil.which("pandoc")
    if pandoc:
        return pandoc

    # 2. Try default Windows install location
    default_path = Path(r"C:\Program Files\Pandoc\pandoc.exe")
    if default_path.exists():
        return str(default_path)

    raise RuntimeError(
        "Pandoc not found. Install it or add it to PATH.\n"
        "Download: https://pandoc.org/installing.html"
    )


def convert():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    output_file = INPUT_FILE.with_suffix(".md")
    media_dir = INPUT_FILE.parent / "media"

    pandoc_path = find_pandoc()

    cmd = [
        pandoc_path,
        str(INPUT_FILE),
        "-o",
        str(output_file),
        "--wrap=none",
        f"--extract-media={media_dir}",
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    print(f"\n✅ Done: {output_file}")


if __name__ == "__main__":
    try:
        convert()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)