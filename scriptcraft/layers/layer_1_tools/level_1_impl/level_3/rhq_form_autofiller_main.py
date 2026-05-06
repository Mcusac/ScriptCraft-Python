"""
RHQ Form Autofiller - Pipeline-Driven Implementation

Improvements:
- True DAG-style pipeline
- Separation of orchestration vs execution
- Stateless stage functions
- Dedicated form processing service
- Single source of truth (context)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import argparse

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.directory_ops import ensure_output_dir
from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print, setup_logger
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6.base_tool import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.rhq_form_autofiller import (
    build_address_data, launch_browser, fill_panel
)
from scriptcraft.layers.layer_1_tools.level_1_impl.level_0.main_common import create_entrypoint_main
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1.rhq_login_actions import attempt_automatic_login
from scriptcraft.layers.layer_1_tools.level_1_impl.level_2.rhq_flow import handle_login, submit_form


# ============================================================
# CONTEXT
# ============================================================

@dataclass
class RHQContext:
    input_file: Path
    output_dir: Path
    log_dir: Path
    data: Dict[str, Any]
    driver: Optional[webdriver.Remote] = None
    logger: Optional[Any] = None


# ============================================================
# PIPELINE ENGINE
# ============================================================

class Pipeline:
    def __init__(self):
        self.stages: List[Callable[[RHQContext], None]] = []

    def add_stage(self, fn: Callable[[RHQContext], None]):
        self.stages.append(fn)

    def run(self, ctx: RHQContext):
        for stage in self.stages:
            stage(ctx)


# ============================================================
# FORM PROCESSING SERVICE (isolated domain logic)
# ============================================================

class RHQFormService:

    def __init__(self, config, form_wait_time: int):
        self.config = config
        self.form_wait_time = form_wait_time

    def process_all(self, ctx: RHQContext):
        for med_id, panels in ctx.data.items():
            self.process_single(ctx, med_id, panels)

    def process_single(self, ctx: RHQContext, med_id: str, panels_data: List[Any]):
        try:
            log_and_print(f"\n🔄 Processing Med_ID: {med_id}")

            url = self.config.tools["rhq_form_autofiller"]["url_template"].format(
                med_id=med_id
            )

            ctx.driver.get(url)

            self._wait_for_form(ctx)

            self._fill_panels(ctx, panels_data)

            submit_form(ctx.driver, med_id)

            time.sleep(2)

        except Exception as e:
            log_and_print(f"❌ Error processing {med_id}: {e}", level="error")

    def _wait_for_form(self, ctx: RHQContext):
        WebDriverWait(ctx.driver, self.form_wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "mat-expansion-panel"))
        )

    def _fill_panels(self, ctx: RHQContext, panels_data: List[Any]):
        for idx, blocks in enumerate(panels_data):
            if not blocks:
                continue

            log_and_print(f"📝 Panel {idx}: {len(blocks)} blocks")

            fill_panel(ctx.driver, idx, blocks, logger=ctx.logger)


# ============================================================
# MAIN TOOL
# ============================================================

class RHQFormAutofiller(BaseTool):

    def __init__(self) -> None:
        super().__init__(
            name="RHQ Form Autofiller",
            description="Automates filling RHQ forms using Excel-derived data.",
            tool_name="rhq_form_autofiller"
        )

        cfg = self.get_tool_config()
        self.browser_timeout = cfg.get("browser_timeout", 60)
        self.form_wait_time = cfg.get("form_wait_time", 10)

    # ========================================================
    # ENTRYPOINT
    # ========================================================

    def run(self, input_paths=None, output_dir=None, **kwargs):

        self.log_start()

        ctx = None

        try:
            ctx = self._build_context(input_paths, output_dir, kwargs)

            self._initialize_logging(ctx, kwargs)
            self._load_data(ctx, kwargs)

            pipeline = self._build_pipeline()
            pipeline.run(ctx)

            self.log_completion()

        except Exception as e:
            log_and_print(f"❌ Error: {e}", level="error")
            raise

        finally:
            self._cleanup(ctx)

    # ========================================================
    # PIPELINE DEFINITION
    # ========================================================

    def _build_pipeline(self) -> Pipeline:
        service = RHQFormService(self.config, self.form_wait_time)

        pipeline = Pipeline()

        pipeline.add_stage(self._stage_launch_browser)
        pipeline.add_stage(self._stage_login)
        pipeline.add_stage(service.process_all)

        return pipeline

    # ========================================================
    # STAGES
    # ========================================================

    def _stage_launch_browser(self, ctx: RHQContext):
        log_and_print("🌐 Launching browser...")
        ctx.driver = launch_browser()

    def _stage_login(self, ctx: RHQContext):
        handle_login(
            ctx.driver,
            data=ctx.data,
            config=self.config,
            logger=ctx.logger,
            form_wait_time=self.form_wait_time,
            browser_timeout=self.browser_timeout,
            attempt_automatic_login_func=attempt_automatic_login,
        )

    # ========================================================
    # SETUP
    # ========================================================

    def _build_context(self, input_paths, output_dir, kwargs) -> RHQContext:
        output_dir = ensure_output_dir(Path(output_dir or self.default_output_dir))
        log_dir = ensure_output_dir(Path(kwargs.get("log_dir", "logs")))

        input_file = self._resolve_input_file(input_paths, kwargs)

        return RHQContext(
            input_file=input_file,
            output_dir=output_dir,
            log_dir=log_dir,
            data={}
        )

    def _initialize_logging(self, ctx: RHQContext, kwargs):
        ctx.logger = setup_logger(
            name=self.name,
            level="DEBUG" if kwargs.get("debug") else "INFO",
            log_file=ctx.log_dir / "rhq_form_autofiller.log"
        )

    def _load_data(self, ctx: RHQContext, kwargs):
        log_and_print("🔄 Loading address data...")
        ctx.data = build_address_data(ctx.input_file, kwargs.get("med_id"))
        log_and_print(f"✅ Loaded data for {len(ctx.data)} Med_IDs")

    # ========================================================
    # CLEANUP
    # ========================================================

    def _cleanup(self, ctx: Optional[RHQContext]):
        if ctx and ctx.driver:
            ctx.driver.quit()
            log_and_print("🔄 Browser closed")

    # ========================================================
    # INPUT RESOLUTION (unchanged)
    # ========================================================

    def _resolve_input_file(self, input_paths, kwargs) -> Path:
        if input_paths:
            return Path(input_paths[0])

        if kwargs.get("input_excel"):
            return Path(kwargs["input_excel"])

        if "input_dir" in kwargs:
            input_dir = Path(kwargs["input_dir"])
        else:
            if "config" not in kwargs:
                kwargs["config"] = self.config
            input_dir = self.resolve_input_directory(**kwargs)

        if not input_dir.exists():
            raise ValueError(f"Input directory not found: {input_dir}")

        files = list(input_dir.glob("*.xlsx"))
        if not files:
            raise ValueError("No Excel files found")

        return files[0]

    # ========================================================
    # CLI
    # ========================================================

    def run_from_cli(self, args: argparse.Namespace):
        kwargs = vars(args).copy()

        input_paths = kwargs.pop("input_path", None)
        if input_paths and not isinstance(input_paths, list):
            input_paths = [input_paths]

        output_dir = kwargs.pop("output_dir", self.default_output_dir)
        debug = kwargs.pop("debug", False)

        self.run(
            input_paths=input_paths,
            output_dir=output_dir,
            debug=debug,
            **kwargs
        )


# ============================================================
# ENTRYPOINT
# ============================================================

def main():
    create_entrypoint_main(
        RHQFormAutofiller,
        tool_name="rhq_form_autofiller",
        description="🏥 Automates RHQ form filling",
        parser_kind="standard",
    )()


if __name__ == "__main__":
    main()