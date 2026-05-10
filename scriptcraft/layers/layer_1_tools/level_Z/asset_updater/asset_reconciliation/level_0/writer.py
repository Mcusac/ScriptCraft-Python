# ============================================================
# writer.py — CSV output layer
# ============================================================

<<<<<<< HEAD
import pandas as pd

from pathlib import Path
=======
from pathlib import Path
import pandas as pd
>>>>>>> 182d6be043d82fdc23c5fc4c567ad4e195b94c00


def write_outputs(
    outputs: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:

    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, df in outputs.items():
        df.to_csv(output_dir / filename, index=False)