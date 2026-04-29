
from pathlib import Path
from typing import Any

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print


def log_workflow_summary(results: dict[str, Any], output_path: Path) -> None:
    """Log a human-readable summary of dictionary workflow results."""
    log_and_print("📊 Workflow Summary:")

    prepared = results.get("prepared_supplements")
    if prepared is not None:
        log_and_print(f"  📋 Prepared supplements: {len(prepared)} rows")

    domain_supps = results.get("domain_supplements")
    if domain_supps:
        log_and_print(f"  ✂️ Split supplements: {len(domain_supps)} domains")
        for domain, data in domain_supps.items():
            log_and_print(f"    - {domain}: {len(data)} rows")

    enhanced = results.get("enhanced_dictionaries")
    if enhanced:
        log_and_print(f"  🔧 Enhanced dictionaries: {len(enhanced)} files")
        for dict_name, data in enhanced.items():
            log_and_print(f"    - {dict_name}: {len(data)} rows")

    log_and_print(f"  📁 Output directory: {output_path}")

