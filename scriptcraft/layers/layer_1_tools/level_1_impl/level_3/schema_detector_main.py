"""
Schema Detector Tool

Automatically detects and generates database schemas from datasets without reading sensitive data.
"""

import argparse
import sys

from pathlib import Path
from typing import Optional, List

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import setup_logger, log_and_print
from layers.layer_1_pypi.level_0_infra.level_6.argument_parsers import ParserFactory
from layers.layer_1_pypi.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_pypi.level_1_impl.level_0.schema_detector import SchemaDetector
from layers.layer_1_pypi.level_1_impl.level_2.runtime_loops import run_process_domain_over_input_paths


class SchemaDetectorTool(BaseTool):
    """🔍 Schema detection tool for datasets"""
    
    def __init__(self):
        super().__init__(
            name="Schema Detector",
            description="🔍 Analyzes datasets and generates database schemas",
            tool_name="schema_detector"
        )
        # Initialize the actual schema detector
        self.detector = SchemaDetector()
    
    def run(self, *args, **kwargs) -> None:
        """
        Run the schema detection process.
        
        Args:
            *args: Positional arguments (can include input_paths, domain)
            **kwargs: Keyword arguments including:
                - input_paths: List of input file paths
                - output_dir: Output directory
                - domain: Domain to process
                - target_database: Target database type
                - privacy_mode: Whether to use privacy-safe mode
                - sample_size: Sample size for analysis
                - naming_convention: Naming convention to use
                - output_formats: List of output formats
        """
        input_paths = kwargs.get("input_paths") or (args[0] if args else None)
        output_dir = kwargs.get("output_dir", self.default_output_dir)
        domain = kwargs.get("domain", "unknown")
        target_database = kwargs.get("target_database", "sqlite")
        privacy_mode = kwargs.get("privacy_mode", True)
        sample_size = kwargs.get("sample_size", 1000)
        naming_convention = kwargs.get("naming_convention", "pascal_case")
        output_formats = kwargs.get("output_formats", ["sql", "json", "yaml"])

        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("input_paths", None)
        extra_kwargs.pop("output_dir", None)
        extra_kwargs.pop("domain", None)
        extra_kwargs["target_database"] = target_database
        extra_kwargs["privacy_mode"] = privacy_mode
        extra_kwargs["sample_size"] = sample_size
        extra_kwargs["naming_convention"] = naming_convention
        extra_kwargs["output_formats"] = output_formats

        run_process_domain_over_input_paths(
            self,
            input_paths=input_paths,
            output_dir=output_dir,
            domain=domain,
            dictionary_file=None,
            extra_kwargs=extra_kwargs,
        )
    
    def process_domain(self, domain: str, dataset_file: Path, dictionary_file: Optional[Path], 
                      output_path: Path, **kwargs) -> None:
        """
        Process a single domain for schema detection.
        
        Args:
            domain: The domain to process
            dataset_file: Path to dataset file
            dictionary_file: Not used for this tool
            output_path: Path to output directory
            **kwargs: Additional arguments
        """
        log_and_print(f"🔍 Analyzing schema for {domain} dataset: {dataset_file.name}")
        
        try:
            # Run schema detection on the dataset file
            success = self.detector.run(
                input_paths=[str(dataset_file)],
                output_dir=str(output_path),
                target_database=kwargs.get('target_database', 'sqlite'),
                privacy_mode=kwargs.get('privacy_mode', True),
                sample_size=kwargs.get('sample_size', 1000),
                naming_convention=kwargs.get('naming_convention', 'pascal_case'),
                output_formats=kwargs.get('output_formats', ['sql', 'json', 'yaml'])
            )
            
            if success:
                log_and_print(f"✅ Schema detection completed for {domain}")
            else:
                log_and_print(f"❌ Schema detection failed for {domain}", level="error")
                
        except Exception as e:
            log_and_print(f"❌ Error during schema detection for {domain}: {e}", level="error")
            raise
    
    def run_standalone(self, input_files: List[str], output_dir: str = "output", 
                      target_database: str = "sqlite", **kwargs) -> bool:
        """
        Run schema detection in standalone mode (not through domain processing).
        
        Args:
            input_files: List of files to analyze
            output_dir: Output directory
            target_database: Target database type
            **kwargs: Additional configuration options
            
        Returns:
            True if successful, False otherwise
        """
        log_and_print(f"🔍 Starting standalone schema detection...")
        log_and_print(f"📂 Files to analyze: {len(input_files)}")
        log_and_print(f"🎯 Target database: {target_database}")
        
        try:
            success = self.detector.run(
                input_paths=input_files,
                output_dir=output_dir,
                target_database=target_database,
                privacy_mode=True,
                **kwargs
            )
            
            if success:
                log_and_print("✅ Schema detection completed successfully!")
            else:
                log_and_print("❌ Schema detection failed", level="error")
                
            return success
            
        except Exception as e:
            log_and_print(f"❌ Schema detection failed: {e}", level="error")
            return False


def main():
    """Main entry point for the schema detector tool."""
    parser = ParserFactory.create_standard_tool_parser(
        "schema_detector",
        "🔍 Analyzes datasets and generates database schemas",
        input_paths_required=False,
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Standalone mode: files to analyze (bypasses domain iteration)",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Standalone mode output directory (default: output)",
    )
    parser.add_argument(
        "--database",
        choices=["sqlite", "sqlserver", "postgresql"],
        default="sqlite",
        help="Target database type (default: sqlite)",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=1000,
        help="Maximum rows to analyze (default: 1000)",
    )
    parser.add_argument(
        "--naming",
        default="pascal_case",
        help="Naming convention (default: pascal_case)",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        default=["sql", "json", "yaml"],
        help="Output formats (default: sql json yaml)",
    )

    args = parser.parse_args()

    setup_logger("schema_detector")

    # Create the tool
    tool = SchemaDetectorTool()
    
    # Check if standalone mode is requested (files provided directly)
    if args.files:
        # Standalone mode with direct file input
        log_and_print("🛠 Running standalone schema detection mode...")
        success = tool.run_standalone(
            input_files=args.files,
            output_dir=getattr(args, 'output', 'output'),
            target_database=getattr(args, 'database', 'sqlite'),
            sample_size=getattr(args, 'sample_size', 1000),
            naming_convention=getattr(args, 'naming', 'pascal_case'),
            output_formats=getattr(args, 'formats', ['sql', 'json', 'yaml'])
        )
        return 0 if success else 1
    else:
        # Standard domain mode
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