import pandas as pd

from pathlib import Path
from typing import Any, Dict, List, Optional, Union


from layers.layer_1_pypi.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_pypi.level_0_infra.level_1.data_loading import load_data
from layers.layer_1_pypi.level_0_infra.level_1.cleaning import clean_dataframe
from layers.layer_1_pypi.level_0_infra.level_3.processing import save_data
from layers.layer_1_pypi.level_0_infra.level_3.processing import process_domain_data


def prepare_supplements(
    input_paths: List[Union[str, Path]],
    output_path: Optional[Union[str, Path]] = None,
    merge_strategy: str = "outer",
    clean_data: bool = True,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Prepare supplements by merging multiple files and cleaning the data.

    Notes:
    - `merge_strategy` is reserved for future behavior (currently concatenates rows).
    """
    _ = merge_strategy  # extension point

    if not input_paths:
        raise ValueError("❌ No input paths provided")

    log_and_print(f"🔄 Preparing supplements from {len(input_paths)} files...")

    supplements: List[pd.DataFrame] = []
    for path in input_paths:
        path = Path(path)
        if not path.exists():
            log_and_print(f"⚠️ Warning: File not found: {path}")
            continue

        try:
            data = load_data(path, **kwargs)
            supplements.append(data)
            log_and_print(f"✅ Loaded: {path.name} ({len(data)} rows)")
        except Exception as e:
            log_and_print(f"❌ Error loading {path}: {e}")

    if not supplements:
        raise ValueError("❌ No valid supplement files loaded")

    log_and_print(f"🔄 Merging {len(supplements)} supplement files...")
    merged_data = supplements[0] if len(supplements) == 1 else pd.concat(supplements, ignore_index=True, sort=False)

    if clean_data:
        log_and_print("🧹 Cleaning merged supplements...")
        merged_data = clean_dataframe(merged_data)

    log_and_print(f"✅ Prepared supplements: {len(merged_data)} rows")

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_data(merged_data, output_path)
        log_and_print(f"💾 Saved prepared supplements to: {output_path}")

    return merged_data


def split_supplements_by_domain(
    supplements_data: pd.DataFrame,
    output_dir: Union[str, Path],
    domain_column: str = "domain",
    split_strategy: str = "standard",
    **kwargs: Any,
) -> Dict[str, pd.DataFrame]:
    """
    Split supplements by domain and save to separate files.

    Notes:
    - `split_strategy` is reserved for future behavior.
    """
    _ = split_strategy  # extension point

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    log_and_print("🔄 Splitting supplements by domain...")

    if domain_column not in supplements_data.columns:
        raise ValueError(f"❌ Domain column '{domain_column}' not found in supplements data")

    domains = supplements_data[domain_column].dropna().unique()
    log_and_print(f"📊 Found {len(domains)} domains: {', '.join(domains)}")

    domain_data: Dict[str, pd.DataFrame] = {}
    for domain in domains:
        domain_mask = supplements_data[domain_column] == domain
        domain_df = supplements_data[domain_mask].copy()

        if len(domain_df) == 0:
            log_and_print(f"⚠️ Warning: No data for domain '{domain}'")
            continue

        domain_df = process_domain_data(domain_df, domain, **kwargs)

        domain_filename = f"supplements_{str(domain).lower()}.csv"
        domain_path = output_dir / domain_filename
        save_data(domain_df, domain_path)

        domain_data[str(domain)] = domain_df
        log_and_print(f"✅ Domain '{domain}': {len(domain_df)} rows -> {domain_path}")

    log_and_print(f"✅ Split supplements into {len(domain_data)} domain files")
    return domain_data

