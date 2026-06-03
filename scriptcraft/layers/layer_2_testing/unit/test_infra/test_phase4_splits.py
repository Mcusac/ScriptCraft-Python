"""Unit tests for Phase 4 infra module splits."""

import pandas as pd
import pytest

from scriptcraft.layers.layer_0_core.level_0.validation import (
    column_sets,
    content_differences,
    dtype_mismatches,
)
from scriptcraft.layers.layer_1_tools.level_0_infra.level_2 import PipelineStep
from scriptcraft.layers.layer_1_tools.level_0_infra.level_3 import compare_dataframes


@pytest.mark.parametrize(
    "column_sets_fn",
    [column_sets],
    ids=["core_level0_validation"],
)
def test_column_sets_finds_only_in_second(column_sets_fn) -> None:
    df1 = pd.DataFrame({"a": [1], "b": [2]})
    df2 = pd.DataFrame({"a": [1], "c": [3]})
    common, only_a, only_b = column_sets_fn(df1, df2)
    assert common == {"a"}
    assert only_a == {"b"}
    assert only_b == {"c"}


@pytest.mark.parametrize(
    "dtype_mismatches_fn",
    [dtype_mismatches],
    ids=["core_level0_validation"],
)
def test_dtype_mismatches_detects_difference(dtype_mismatches_fn) -> None:
    df1 = pd.DataFrame({"x": [1]})
    df2 = pd.DataFrame({"x": [1.0]})
    mismatches = dtype_mismatches_fn(df1, df2)
    assert "x" in mismatches


@pytest.mark.parametrize(
    "content_differences_fn",
    [content_differences],
    ids=["core_level0_validation"],
)
def test_content_differences_none_when_identical(content_differences_fn) -> None:
    df = pd.DataFrame({"a": [1, 2]})
    assert content_differences_fn(df, df) is None


def test_pipeline_step_custom_mode_accepts_custom_run_mode() -> None:
    def noop() -> None:
        pass

    step = PipelineStep(
        name="custom_step",
        log_filename="custom.log",
        qc_func=noop,
        input_key="raw_data",
        run_mode="custom",
    )
    assert step.run_mode == "custom"


def test_compare_dataframes_runs_columns_step() -> None:
    df1 = pd.DataFrame({"a": [1]})
    df2 = pd.DataFrame({"a": [1]})
    result = compare_dataframes(df1, df2, steps=["columns"])
    assert "a" in result.common
