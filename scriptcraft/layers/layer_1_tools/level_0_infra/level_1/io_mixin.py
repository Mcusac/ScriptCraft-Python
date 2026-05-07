import pandas as pd

from pathlib import Path
from typing import Union

from scriptcraft.layers.layer_1_tools.level_0_infra.level_6.argument_parsers import ArgumentValidator


class IOMixin:
    """Handles file loading/saving."""

    def load_data_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        file_path = Path(file_path)

        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        self.log_message(f"📂 Loaded {file_path.name}: {df.shape}")
        return df

    def save_data_file(
        self,
        data: pd.DataFrame,
        output_path: Union[str, Path],
        include_index: bool = False,
    ) -> Path:
        output_path = Path(output_path)
        ArgumentValidator.ensure_output_dir(output_path.parent)

        if output_path.suffix.lower() == '.csv':
            data.to_csv(output_path, index=include_index)
        else:
            data.to_excel(output_path, index=include_index)

        self.log_message(f"💾 Saved: {output_path}")
        return output_path