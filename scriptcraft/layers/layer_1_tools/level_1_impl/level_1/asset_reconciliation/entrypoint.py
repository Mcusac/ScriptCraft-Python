"""CLI entrypoint for asset reconciliation (impl L1)."""

import argparse
import sys
from pathlib import Path

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import run


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Asset reconciliation pipeline — produces change-detection CSVs."
    )
    parser.add_argument("--asset_csv", required=True, type=Path, help="Path to asset database CSV")
    parser.add_argument("--form_csv", required=True, type=Path, help="Path to form submissions CSV")
    parser.add_argument("--output_dir", required=True, type=Path, help="Directory for output CSVs")
    parser.add_argument("--debug", action="store_true", help="Print diagnostic information")
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    run(
        asset_csv=str(args.asset_csv),
        form_csv=str(args.form_csv),
        output_dir=args.output_dir,
        debug=args.debug,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
