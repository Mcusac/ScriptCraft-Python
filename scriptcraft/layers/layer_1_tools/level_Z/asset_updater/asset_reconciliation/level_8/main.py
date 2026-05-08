#!/usr/bin/env python3
# ============================================================
# main.py — CLI entry point
#
# Usage:
#   python main.py --asset_csv path/to/assets.csv \
#                  --form_csv  path/to/form.csv    \
#                  --output_dir path/to/out/
# ============================================================

import argparse

from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_Z.asset_updater.asset_reconciliation.level_7.runner import run


# -----------------------------
# ARG PARSING
# -----------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Asset reconciliation pipeline — produces change-detection CSVs."
    )

    parser.add_argument(
        "--asset_csv",
        required=True,
        type=Path,
        help="Path to asset database CSV",
    )

    parser.add_argument(
        "--form_csv",
        required=True,
        type=Path,
        help="Path to form submissions CSV",
    )

    parser.add_argument(
        "--output_dir",
        required=True,
        type=Path,
        help="Directory for output CSVs",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Print diagnostic information during the run",
    )

    return parser.parse_args()


# -----------------------------
# ENTRYPOINT
# -----------------------------

def main() -> None:
    args = _parse_args()

    run(
        asset_csv=args.asset_csv,
        form_csv=args.form_csv,
        output_dir=args.output_dir,
        debug=args.debug,
    )


if __name__ == "__main__":
    main()