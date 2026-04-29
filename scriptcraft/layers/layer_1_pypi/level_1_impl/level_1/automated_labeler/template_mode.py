"""Template-mode orchestration for the automated labeler tool."""
import pandas as pd

from pathlib import Path
from typing import List, Optional, Tuple
from docx import Document

from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print

from layers.layer_1_pypi.level_1_impl.level_0.automated_labeler.paths import resolve_output_file
from layers.layer_1_pypi.level_1_impl.level_0.automated_labeler.docx_template import (
    fill_full_page,
)
from layers.layer_1_pypi.level_1_impl.level_0.automated_labeler.types import InputPaths, LoaderSaver


ID_COLUMNS = ("RID", "MID", "Visit_ID")
DEFAULT_OUTPUT_NAME = "Labels.docx"


def _require_docx() -> None:
    if Document is None or fill_full_page is None:
        raise ImportError(
            "❌ Template mode requires the optional 'python-docx' dependency. "
            "Install it with: pip install python-docx"
        )


def _resolve_template_file(*, input_paths: InputPaths, template_path: Optional[str]) -> Path:
    if template_path:
        return Path(template_path)
    if len(input_paths) > 1:
        return Path(input_paths[1])
    raise ValueError("❌ Template file required for template mode")


def _extract_id_pairs(data: pd.DataFrame) -> List[Tuple[str, str, str]]:
    available_columns = [col for col in ID_COLUMNS if col in data.columns]
    if not available_columns:
        raise ValueError("❌ No ID columns found in data")

    id_pairs: List[Tuple[str, str, str]] = []
    for _, row in data.iterrows():
        rid = str(row.get("RID", ""))
        mid = str(row.get("MID", ""))
        visit = str(row.get("Visit_ID", ""))
        id_pairs.append((rid, mid, visit))
    return id_pairs


def run_template_mode(
    *,
    tool: LoaderSaver,
    input_paths: InputPaths,
    output_path: Path,
    template_path: Optional[str],
    output_filename: Optional[str],
    sets_per_page: int,
) -> None:
    _require_docx()

    data = tool.load_data_file(input_paths[0])

    template_file = _resolve_template_file(input_paths=input_paths, template_path=template_path)
    if not template_file.exists():
        raise ValueError(f"❌ Template file not found: {template_file}")

    log_and_print(f"📄 Loading template: {template_file}")
    template_doc = Document(template_file)

    log_and_print("🔄 Filling template with data...")
    id_pairs = _extract_id_pairs(data)
    filled_doc = fill_full_page(template_doc, id_pairs, sets_per_page=sets_per_page)

    output_file = resolve_output_file(output_path, output_filename, DEFAULT_OUTPUT_NAME)
    filled_doc.save(output_file)
    log_and_print(f"✅ Filled template saved to: {output_file}")
