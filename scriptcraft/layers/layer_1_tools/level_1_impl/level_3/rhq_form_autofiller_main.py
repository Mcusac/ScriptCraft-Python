"""
RHQ Form Autofiller - Simplified Single-File Implementation

This module provides a complete RHQ Form Autofiller tool with built-in
dual-environment support. It automatically detects whether it's running in
development or distributable mode and imports accordingly.

Usage:
    Development: python -m scripts.tools.rhq_form_autofiller.main [args]
    Distributable:   python main.py [args]
    Pipeline:    Called via main_runner(**kwargs)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time
import argparse

from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print, setup_logger
from layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from layers.layer_1_tools.level_1_impl.level_0.rhq.credentials_io import load_credentials
from layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main
from layers.layer_1_tools.level_1_impl.level_0.rhq_form_autofiller import (
    build_address_data, launch_browser, fill_panel
)
from layers.layer_1_tools.level_1_impl.level_1.rhq_login_actions import (
    attempt_automatic_login,
)
from layers.layer_1_tools.level_1_impl.level_2.rhq_flow import handle_login, submit_form




class RHQFormAutofiller(BaseTool):
    """Tool for automatically filling RHQ forms with address data."""
    
    def __init__(self) -> None:
        """Initialize the tool."""
        super().__init__(
            name="RHQ Form Autofiller",
            description="Automates filling of RHQ forms using pre-processed data from Excel files.",
            tool_name="rhq_form_autofiller"
        )
        self.driver: Optional[webdriver.Remote] = None
        self.logger: Optional[Any] = None
        
        # Get tool-specific configuration
        tool_config = self.get_tool_config()
        self.browser_timeout = tool_config.get("browser_timeout", 60)
        self.form_wait_time = tool_config.get("form_wait_time", 10) 
        self.login_retry_attempts = tool_config.get("login_retry_attempts", 3)
        self.auto_login = tool_config.get("auto_login", True)
    
    def run(self,
            mode: Optional[str] = None,
            input_paths: Optional[List[Union[str, Path]]] = None,
            output_dir: Optional[Union[str, Path]] = None,
            domain: Optional[str] = None,
            output_filename: Optional[str] = None,
            **kwargs: Any) -> None:
        """
        Run the RHQ Form Autofiller's main functionality.
        
        Args:
            mode: Operating mode (not used for this tool)
            input_paths: List of input Excel file paths 
            output_dir: Directory to save outputs
            domain: Domain context (not used for this tool)
            output_filename: Output filename (not used for this tool)
            **kwargs: Additional arguments:
                - debug: Enable debug logging
                - med_id: Filter for specific Med_ID
                - input_excel: Alternative input path specification
        
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        self.log_start()
        
        try:
            # Setup directories
            output_dir = ensure_output_dir(Path(output_dir or self.default_output_dir))
            log_dir = ensure_output_dir(Path(kwargs.get('log_dir', 'logs')))
            
            # Setup logging
            self.logger = setup_logger(
                name=self.name,
                level="DEBUG" if kwargs.get('debug') else "INFO",
                log_file=log_dir / "rhq_form_autofiller.log"
            )
            
            # Determine input file
            input_file = self._resolve_input_file(input_paths, kwargs)
            
            # Load and process data
            log_and_print("🔄 Loading address data...")
            data = build_address_data(input_file, kwargs.get('med_id'))
            log_and_print(f"✅ Loaded data for {len(data)} Med_IDs")
            
            # Launch browser and process forms
            self._process_forms(data)
            
            self.log_completion()
            
        except Exception as e:
            log_and_print(f"❌ Error: {str(e)}", level="error")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                log_and_print("🔄 Browser closed")
    
    def _resolve_input_file(self, input_paths: Optional[List[Union[str, Path]]], kwargs: Dict[str, Any]) -> Path:
        """Resolve the input file from various sources."""
        # Priority: input_paths -> input_excel kwarg -> auto-discovery
        if input_paths and len(input_paths) > 0:
            input_file = Path(input_paths[0])
        elif kwargs.get('input_excel'):
            input_file = Path(kwargs['input_excel'])
        else:
            # Auto-discover input file using DRY method from BaseTool
            # Use explicit input_dir if provided, otherwise use resolve_input_directory
            if 'input_dir' in kwargs:
                input_dir = Path(kwargs['input_dir'])
            else:
                # Add config to kwargs if not already present
                if 'config' not in kwargs:
                    kwargs['config'] = self.config
                input_dir = self.resolve_input_directory(**kwargs)
            
            if not input_dir.exists():
                raise ValueError(f"Input directory not found: {input_dir}")
            
            excel_files = list(input_dir.glob("*.xlsx"))
            if not excel_files:
                raise ValueError("No Excel files found in input directory")
            
            input_file = excel_files[0]
            log_and_print(f"📁 Auto-discovered input file: {input_file}")
        
        if not input_file.exists():
            raise ValueError(f"Input file does not exist: {input_file}")
        
        return input_file
    
    def _process_forms(self, data: Dict[str, Any]) -> None:
        """Process all forms with the loaded data."""
        # Launch browser
        log_and_print("🌐 Launching browser...")
        self.driver = launch_browser()
        
        try:
            # Handle login first
            self._handle_login(data)
            
            # Process each record
            for med_id, panels_data in data.items():
                self._process_single_form(med_id, panels_data)
                
        except Exception as e:
            log_and_print(f"❌ Form processing failed: {str(e)}", level="error")
            raise
    
    def _handle_login(self, data: Dict[str, Any]) -> None:
        """Handle the login process."""
        handle_login(
            self.driver,
            data=data,
            config=self.config,
            logger=self.logger,
            form_wait_time=self.form_wait_time,
            browser_timeout=self.browser_timeout,
            attempt_automatic_login_func=lambda driver, logger=None: attempt_automatic_login(driver, logger),
        )
    
    def _process_single_form(self, med_id: str, panels_data: List[Any]) -> None:
        """Process a single form for one Med_ID."""
        try:
            # Navigate to form
            log_and_print(f"\n🔄 Processing Med_ID: {med_id}")
            url = self.config.tools["rhq_form_autofiller"]["url_template"].format(
                med_id=med_id
            )
            self.driver.get(url)
            log_and_print(f"🌐 Opened page for Med_ID {med_id}")
            
            # Wait for form load - look for expansion panels
            try:
                WebDriverWait(self.driver, self.form_wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "mat-expansion-panel"))
                )
                log_and_print("✅ Form loaded successfully")
            except Exception as e:
                log_and_print(f"❌ Form did not load for {med_id}: {e}", level="error")
                return
            
            # Fill each panel
            for panel_idx, address_blocks in enumerate(panels_data):
                if address_blocks:  # Only process panels with data
                    log_and_print(f"📝 Processing panel {panel_idx} with {len(address_blocks)} blocks")
                    fill_panel(self.driver, panel_idx, address_blocks, logger=self.logger)
            
            # Submit form
            self._submit_form(med_id)
            
            # Wait between submissions
            time.sleep(2)
            
        except Exception as e:
            log_and_print(f"❌ Error processing record {med_id}: {e}", level="error")
    
    def _submit_form(self, med_id: str) -> None:
        """Submit the form for a Med_ID."""
        submit_form(self.driver, med_id)
    
    def run_from_cli(self, args: argparse.Namespace) -> None:
        """
        Run the tool from command line arguments.
        
        Args:
            args: Parsed command line arguments
        """
        kwargs = vars(args).copy()
        
        # Extract known arguments
        input_paths = kwargs.pop('input_path', None)
        if input_paths and not isinstance(input_paths, list):
            input_paths = [input_paths]
        
        output_dir = kwargs.pop('output_dir', self.default_output_dir)
        debug = kwargs.pop('debug', False)
        
        # Run the tool
        self.run(
            input_paths=input_paths,
            output_dir=output_dir,
            debug=debug,
            **kwargs
        )


# === 🔐 Credentials Management ===
def load_credentials() -> Tuple[Optional[str], Optional[str]]:
    """Backwards-compatible wrapper for `rhq_credentials.load_credentials`."""
    cred_file = Path(__file__).parent / "credentials.txt"
    return load_credentials(cred_file)


def attempt_automatic_login(driver: webdriver.Remote, logger: Optional[Any] = None) -> bool:
    """Backwards-compatible wrapper for `rhq_credentials.attempt_automatic_login`."""
    return attempt_automatic_login(driver, logger=logger, credentials_file=Path(__file__).parent / "credentials.txt")


def main():
    """Main entry point for the RHQ form autofiller tool."""
    create_entrypoint_main(
        RHQFormAutofiller,
        tool_name="rhq_form_autofiller",
        description="🏥 Automates filling of RHQ forms with address data from Excel files",
        parser_kind="standard",
    )()


if __name__ == "__main__":
    main()
