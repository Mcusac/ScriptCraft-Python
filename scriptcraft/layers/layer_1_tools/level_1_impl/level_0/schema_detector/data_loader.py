import json
import pandas as pd

from pathlib import Path
from typing import Optional

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0.emitter import log_and_print


class DataLoader:
    def __init__(self, sample_size: int):
        self.sample_size = sample_size

    def load(self, file_path: Path) -> Optional[pd.DataFrame]:
        try:
            if file_path.suffix.lower() == ".csv":
                df = pd.read_csv(file_path, nrows=self.sample_size)
                log_and_print(f"📋 Found {len(df.columns)} columns in CSV")
                return df

            if file_path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path, nrows=self.sample_size)
                log_and_print(f"📋 Found {len(df.columns)} columns in Excel")
                return df

            if file_path.suffix.lower() == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                df = pd.DataFrame(data[:self.sample_size]) if isinstance(data, list) else pd.DataFrame([data])
                log_and_print(f"📋 Found {len(df.columns)} columns in JSON")
                return df

            if file_path.suffix.lower() == ".parquet":
                df = pd.read_parquet(file_path)
                log_and_print(f"📋 Found {len(df.columns)} columns in Parquet")
                return df.head(self.sample_size)

            log_and_print(f"❌ Unsupported file format: {file_path.suffix}", level="error")
            return None

        except Exception as e:
            log_and_print(f"❌ Error reading {file_path.name}: {str(e)}", level="error")
            return None