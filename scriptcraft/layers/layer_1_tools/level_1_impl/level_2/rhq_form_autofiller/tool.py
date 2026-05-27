import argparse

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
  attempt_automatic_login,
  launch_chrome,
  log_and_print,
  setup_logger,
  RHQContext
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import build_address_data
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import handle_login
from scriptcraft.layers.layer_1_tools.level_0_infra.level_4 import (
  RHQFormService,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_6 import ArgumentValidator
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool


class RHQFormAutofiller(BaseTool):
  def __init__(self) -> None:
    super().__init__(
      name="RHQ Form Autofiller",
      description="Automates filling RHQ forms using Excel-derived data.",
      tool_name="rhq_form_autofiller",
    )
    cfg = self.get_tool_config()
    self.browser_timeout = cfg.get("browser_timeout", 60)
    self.form_wait_time = cfg.get("form_wait_time", 10)

  def run(self, input_paths=None, output_dir=None, **kwargs):
    self.log_start()
    ctx: Optional[RHQContext] = None
    try:
      ctx = self._build_context(input_paths, output_dir, kwargs)
      self._initialize_logging(ctx, kwargs)
      self._load_data(ctx, kwargs)
      self._run_stages(ctx)
      self.log_completion()
    except Exception as e:
      log_and_print(f"❌ Error: {e}", level="error")
      raise
    finally:
      self._cleanup(ctx)

  def _run_stages(self, ctx: RHQContext) -> None:
    service = RHQFormService(self.config, self.form_wait_time)
    self._stage_launch_browser(ctx)
    self._stage_login(ctx)
    service.process_all(ctx)

  def _stage_launch_browser(self, ctx: RHQContext) -> None:
    log_and_print("🌐 Launching browser...")
    ctx.driver = launch_chrome()

  def _stage_login(self, ctx: RHQContext) -> None:
    handle_login(
      ctx.driver,
      data=ctx.data,
      config=self.config,
      logger=ctx.logger,
      form_wait_time=self.form_wait_time,
      browser_timeout=self.browser_timeout,
      attempt_automatic_login_func=attempt_automatic_login,
    )

  def _build_context(self, input_paths, output_dir, kwargs) -> RHQContext:
    resolved_output_dir = ArgumentValidator.ensure_output_dir(
      Path(output_dir or self.default_output_dir),
    )
    log_dir = ArgumentValidator.ensure_output_dir(Path(kwargs.get("log_dir", "logs")))
    input_file = self._resolve_input_file(input_paths, kwargs)
    return RHQContext(
      input_file=input_file,
      output_dir=resolved_output_dir,
      log_dir=log_dir,
      data={},
    )

  def _initialize_logging(self, ctx: RHQContext, kwargs) -> None:
    ctx.logger = setup_logger(
      name=self.name,
      level="DEBUG" if kwargs.get("debug") else "INFO",
      log_file=ctx.log_dir / "rhq_form_autofiller.log",
    )

  def _load_data(self, ctx: RHQContext, kwargs) -> None:
    log_and_print("🔄 Loading address data...")
    ctx.data = build_address_data(ctx.input_file, kwargs.get("med_id"))
    log_and_print(f"✅ Loaded data for {len(ctx.data)} Med_IDs")

  def _cleanup(self, ctx: Optional[RHQContext]) -> None:
    if ctx and ctx.driver:
      ctx.driver.quit()
      log_and_print("🔄 Browser closed")

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

  def run_from_cli(self, args: argparse.Namespace) -> None:
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
      **kwargs,
    )

