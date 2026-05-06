"""
Schema Detector Tool

Automatically detects and generates database schemas from datasets without reading sensitive data.
"""

import sys
from pathlib import Path
from typing import List

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import setup_logger, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.process_domain_mixins import EngineWrapperToolMixin
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6.argument_parsers import ParserFactory
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7.base_tool import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.schema_detector import SchemaDetector


class SchemaDetectorTool(EngineWrapperToolMixin, BaseTool):
    """🔍 Schema detection tool for datasets"""

    def __init__(self):
        super().__init__(
            name="Schema Detector",
            description="🔍 Analyzes datasets and generates database schemas",
            tool_name="schema_detector",
        )
        self.detector = SchemaDetector()

    # ---------------------------
    # ORCHESTRATION ENTRY POINT
    # ---------------------------
    def run(self, *args, **kwargs) -> None:
        """
        Standard domain-driven execution.
        """
        from scriptcraft.layers.layer_1_tools.level_1_impl.level_2.runtime_loops import (
            run_process_domain_over_input_paths,
        )

        input_paths = kwargs.get("input_paths") or (args[0] if args else None)
        output_dir = kwargs.get("output_dir", self.default_output_dir)
        domain = kwargs.get("domain", "unknown")

        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("input_paths", None)
        extra_kwargs.pop("output_dir", None)
        extra_kwargs.pop("domain", None)

        run_process_domain_over_input_paths(
            self,
            input_paths=input_paths,
            output_dir=output_dir,
            domain=domain,
            dictionary_file=None,
            extra_kwargs=extra_kwargs,
        )

    # ---------------------------
    # ENGINE WRAPPER IMPLEMENTATION
    # ---------------------------
    def _process_domain_impl(
        self,
        domain: str,
        dataset_file: Path,
        output_path: Path,
        **kwargs,
    ) -> None:
        """
        Delegates entirely to SchemaDetector engine.
        """

        log_and_print(f"🔍 Analyzing schema for {domain}: {dataset_file.name}")

        try:
            success = self.detector.run(
                input_paths=[str(dataset_file)],
                output_dir=str(output_path),
                target_database=kwargs.get("target_database", "sqlite"),
                privacy_mode=kwargs.get("privacy_mode", True),
                sample_size=kwargs.get("sample_size", 1000),
                naming_convention=kwargs.get("naming_convention", "pascal_case"),
                output_formats=kwargs.get("output_formats", ["sql", "json", "yaml"]),
            )

            if success:
                log_and_print(f"✅ Schema detection completed for {domain}")
            else:
                log_and_print(f"❌ Schema detection failed for {domain}", level="error")

        except Exception as e:
            log_and_print(f"❌ Error during schema detection for {domain}: {e}", level="error")
            raise

    # ---------------------------
    # STANDALONE MODE (UNCHANGED)
    # ---------------------------
    def run_standalone(
        self,
        input_files: List[str],
        output_dir: str = "output",
        target_database: str = "sqlite",
        **kwargs,
    ) -> bool:

        log_and_print(f"🔍 Starting standalone schema detection...")
        log_and_print(f"📂 Files: {len(input_files)}")
        log_and_print(f"🎯 DB: {target_database}")

        try:
            success = self.detector.run(
                input_paths=input_files,
                output_dir=output_dir,
                target_database=target_database,
                privacy_mode=True,
                **kwargs,
            )

            if success:
                log_and_print("✅ Schema detection completed successfully!")
            else:
                log_and_print("❌ Schema detection failed", level="error")

            return success

        except Exception as e:
            log_and_print(f"❌ Schema detection failed: {e}", level="error")
            return False


# ---------------------------
# ENTRYPOINT
# ---------------------------
def main():
    parser = ParserFactory.create_standard_tool_parser(
        "schema_detector",
        "🔍 Analyzes datasets and generates database schemas",
        input_paths_required=False,
    )

    parser.add_argument("--files", nargs="+")
    parser.add_argument("--output", default="output")
    parser.add_argument("--database", choices=["sqlite", "sqlserver", "postgresql"], default="sqlite")
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--naming", default="pascal_case")
    parser.add_argument("--formats", nargs="+", default=["sql", "json", "yaml"])

    args = parser.parse_args()
    setup_logger("schema_detector")

    tool = SchemaDetectorTool()

    if args.files:
        success = tool.run_standalone(
            input_files=args.files,
            output_dir=args.output,
            target_database=args.database,
            sample_size=args.sample_size,
            naming_convention=args.naming,
            output_formats=args.formats,
        )
        return 0 if success else 1

    tool.run(
        input_paths=args.input_paths,
        output_dir=args.output_dir,
        domain=args.domain,
        output_filename=args.output_filename,
        mode=args.mode,
        target_database=args.database,
        privacy_mode=True,
        sample_size=args.sample_size,
        naming_convention=args.naming,
        output_formats=args.formats,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())