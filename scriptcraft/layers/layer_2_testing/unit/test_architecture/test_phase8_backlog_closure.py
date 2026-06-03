"""Architecture gates for post-Phase-8 backlog closure."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

_LAYERS = Path(__file__).resolve().parents[3]
_LAYER_0_CORE = _LAYERS / "layer_0_core"
_TOOLS_INFRA = _LAYERS / "layer_1_tools" / "level_0_infra"


def test_c6_05_path_resolver_abc_in_core() -> None:
    from scriptcraft.layers.layer_0_core.level_0.paths import (
        PathResolver,
        build_domain_paths,
    )

    paths = build_domain_paths(Path("/tmp/domain"))
    assert "qc_output" in paths
    assert PathResolver.__abstractmethods__


def test_c6_06_dataframe_comparer_accepts_id_columns() -> None:
    from scriptcraft.layers.layer_1_tools.level_0_infra.level_3.dataframe_comparer import (
        DataFrameComparer,
    )

    df1 = pd.DataFrame({"a": [1], "b": [2]})
    df2 = pd.DataFrame({"a": [1], "b": [2]})
    comparer = DataFrameComparer(df1, df2, id_columns=["a"])
    assert comparer.id_columns == ("a",)


def test_workflow_registry_in_infra() -> None:
    path = _TOOLS_INFRA / "level_0" / "workflow_registry.py"
    assert path.is_file()


def test_legacy_loader_module_removed() -> None:
    assert not (_TOOLS_INFRA / "level_3" / "legacy_loader.py").exists()
