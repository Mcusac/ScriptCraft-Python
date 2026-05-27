"""Labeling-mode orchestration for the automated labeler tool."""

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import (
    apply_labeling_rules,
    log_and_print,
    resolve_output_file,
    InputPaths,
    LabelingRules,
    LoaderSaver,
)

DEFAULT_OUTPUT_TEMPLATE = "labeled_data.{output_format}"


def run_labeling_mode(
    *,
    tool: LoaderSaver,
    input_paths: InputPaths,
    output_path: Path,
    domain: Optional[str],
    labeling_rules: LabelingRules,
    output_format: str,
    output_filename: Optional[str],
) -> None:
    data = tool.load_data_file(input_paths[0])

    log_and_print("🔄 Applying labeling rules...")
    labeled_data = apply_labeling_rules(data, rules=labeling_rules, domain=domain)

    output_file = resolve_output_file(
        output_path,
        output_filename,
        DEFAULT_OUTPUT_TEMPLATE.format(output_format=output_format),
    )
    tool.save_data_file(labeled_data, output_file, include_index=False)
    log_and_print(f"✅ Labeled data saved to: {output_file}")
