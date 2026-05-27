import time

from typing import Any, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
  log_and_print,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import fill_panel
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import submit_form


class RHQFormService:
  def __init__(self, config, form_wait_time: int):
    self.config = config
    self.form_wait_time = form_wait_time

  def process_all(self, ctx: Any) -> None:
    for med_id, panels in ctx.data.items():
      self.process_single(ctx, med_id, panels)

  def process_single(self, ctx: Any, med_id: str, panels_data: List[Any]) -> None:
    try:
      log_and_print(f"\n🔄 Processing Med_ID: {med_id}")

      url = self.config.tools["rhq_form_autofiller"]["url_template"].format(
        med_id=med_id,
      )
      ctx.driver.get(url)
      self._wait_for_form(ctx)
      self._fill_panels(ctx, panels_data)
      submit_form(ctx.driver, med_id)
      time.sleep(2)
    except Exception as e:
      log_and_print(f"❌ Error processing {med_id}: {e}", level="error")

  def _wait_for_form(self, ctx: Any) -> None:
    WebDriverWait(ctx.driver, self.form_wait_time).until(
      EC.presence_of_element_located((By.TAG_NAME, "mat-expansion-panel")),
    )

  def _fill_panels(self, ctx: Any, panels_data: List[Any]) -> None:
    for idx, blocks in enumerate(panels_data):
      if not blocks:
        continue
      log_and_print(f"📝 Panel {idx}: {len(blocks)} blocks")
      fill_panel(ctx.driver, idx, blocks, logger=ctx.logger)

