from pathlib import Path

from scriptcraft.layers.layer_0_core.level_1 import (
    run_domains,
    build_run_context
)

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import DomainMappedToolMixin, log_and_print
from scriptcraft.layers.layer_1_tools.level_0_infra.level_7 import BaseTool

from scriptcraft.layers.layer_1_tools.level_1_impl.level_0 import FILENAME_MAP, run_medvisit_integrity_check


class MedVisitIntegrityValidator(BaseTool, DomainMappedToolMixin):
  """Validator for checking Med_ID and Visit_ID integrity between old and new datasets."""

  def __init__(self):
    super().__init__(
      name="MedVisit Integrity Validator",
      description="Validates the integrity of Med_ID and Visit_ID combinations between datasets",
      tool_name="medvisit_integrity_validator",
    )

  def run(self, *args, **kwargs) -> None:
    ctx = build_run_context(*args, **kwargs)

    def _per_domain(domain: str, output_path: Path) -> None:
      if domain not in FILENAME_MAP:
        log_and_print(f"⚠️ Skipping {domain} — no file mapping found.")
        return
      domain_output = output_path / f"{domain}_medvisit_integrity.xlsx"
      self.process_domain(
        domain,
        dataset_file=None,
        dictionary_file=None,
        output_path=domain_output,
        **ctx.extra_kwargs,
      )

    run_domains(
      self,
      domains=ctx.domains,
      default_domains=list(FILENAME_MAP.keys()),
      output_dir=ctx.output_dir,
      per_domain_callable=_per_domain,
    )

  def _process_domain_impl(self, domain: str, output_path: Path, **_kwargs) -> None:
    filenames = FILENAME_MAP.get(domain)
    if not filenames:
      log_and_print(f"⏩ Skipping {domain} — no file mapping found.")
      return
    run_medvisit_integrity_check(domain=domain, filenames=filenames, output_path=output_path)

