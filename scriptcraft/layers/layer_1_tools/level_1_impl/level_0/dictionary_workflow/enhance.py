import pandas as pd

from pathlib import Path
from typing import Any, Dict, List, Optional, Union


from layers.layer_1_tools.level_0_infra.level_0.logging_core import log_and_print
from layers.layer_1_tools.level_0_infra.level_1.data_loading import load_data
from layers.layer_1_tools.level_0_infra.level_1.cleaning import clean_dataframe
from layers.layer_1_tools.level_0_infra.level_3.processing import save_data


def enhance_dictionaries(
    dictionary_paths: List[Union[str, Path]],
    supplement_paths: List[Union[str, Path]],
    output_dir: Union[str, Path],
    domain_mapping: Optional[Dict[str, str]] = None,
    enhancement_strategy: str = "append",
    **kwargs: Any,
) -> Dict[str, pd.DataFrame]:
    """Enhance dictionaries with domain-specific supplements."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    log_and_print(f"🔄 Enhancing {len(dictionary_paths)} dictionaries...")

    dictionaries: Dict[str, pd.DataFrame] = {}
    for path in dictionary_paths:
        path = Path(path)
        if not path.exists():
            log_and_print(f"⚠️ Warning: Dictionary not found: {path}")
            continue

        try:
            data = load_data(path, **kwargs)
            dictionaries[path.stem] = data
            log_and_print(f"✅ Loaded dictionary: {path.name} ({len(data)} rows)")
        except Exception as e:
            log_and_print(f"❌ Error loading dictionary {path}: {e}")

    if not dictionaries:
        raise ValueError("❌ No valid dictionaries loaded")

    supplements: Dict[str, pd.DataFrame] = {}
    for path in supplement_paths:
        path = Path(path)
        if path.is_dir():
            for supplement_file in path.glob("*.csv"):
                domain = supplement_file.stem.replace("supplements_", "")
                try:
                    data = load_data(supplement_file, **kwargs)
                    supplements[domain] = data
                    log_and_print(f"✅ Loaded supplement: {supplement_file.name} ({len(data)} rows)")
                except Exception as e:
                    log_and_print(f"❌ Error loading supplement {supplement_file}: {e}")
            continue

        if not path.exists():
            log_and_print(f"⚠️ Warning: Supplement not found: {path}")
            continue

        try:
            data = load_data(path, **kwargs)
            domain = domain_mapping.get(str(path), path.stem) if domain_mapping else path.stem
            supplements[domain] = data
            log_and_print(f"✅ Loaded supplement: {path.name} ({len(data)} rows)")
        except Exception as e:
            log_and_print(f"❌ Error loading supplement {path}: {e}")

    enhanced_dictionaries: Dict[str, pd.DataFrame] = {}
    for dict_name, dict_data in dictionaries.items():
        log_and_print(f"🔄 Enhancing dictionary: {dict_name}")

        matching_supplements: List[pd.DataFrame] = []
        for domain, supplement_data in supplements.items():
            if str(domain).lower() in dict_name.lower() or dict_name.lower() in str(domain).lower():
                matching_supplements.append(supplement_data)

        if not matching_supplements:
            log_and_print(f"⚠️ No matching supplements found for {dict_name}")
            enhanced_dictionaries[dict_name] = dict_data
            continue

        combined_supplements = (
            matching_supplements[0]
            if len(matching_supplements) == 1
            else pd.concat(matching_supplements, ignore_index=True, sort=False).drop_duplicates()
        )

        if enhancement_strategy == "append":
            enhanced_data = pd.concat([dict_data, combined_supplements], ignore_index=True, sort=False)
        elif enhancement_strategy == "merge":
            common_columns = set(dict_data.columns) & set(combined_supplements.columns)
            if common_columns:
                enhanced_data = pd.merge(dict_data, combined_supplements, on=list(common_columns), how="outer")
            else:
                enhanced_data = pd.concat([dict_data, combined_supplements], ignore_index=True, sort=False)
        else:
            enhanced_data = combined_supplements

        enhanced_data = clean_dataframe(enhanced_data)

        enhanced_filename = f"{dict_name}_enhanced.csv"
        enhanced_path = output_dir / enhanced_filename
        save_data(enhanced_data, enhanced_path)

        enhanced_dictionaries[dict_name] = enhanced_data
        log_and_print(f"✅ Enhanced {dict_name}: {len(dict_data)} -> {len(enhanced_data)} rows -> {enhanced_path}")

    log_and_print(f"✅ Enhanced {len(enhanced_dictionaries)} dictionaries")
    return enhanced_dictionaries

