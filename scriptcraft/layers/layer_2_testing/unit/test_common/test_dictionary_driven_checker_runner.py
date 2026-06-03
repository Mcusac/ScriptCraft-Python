"""Unit tests for dictionary_driven_checker runner orchestration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from scriptcraft.layers.layer_1_tools.level_0_infra.level_0 import OutlierMethod
from scriptcraft.layers.layer_1_tools.level_1_impl.level_1 import run_dictionary_checker


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    out = tmp_path / "validation_out"
    out.mkdir()
    return out


def test_runner_skips_dictionary_columns_missing_from_dataset(output_dir: Path) -> None:
    df = pd.DataFrame({"Present": ["a"]})
    dict_df = pd.DataFrame(
        [
            {
                "Main Variable": "MissingCol",
                "Value Type": "categorical",
                "Expected Values": "a,b",
            },
            {
                "Main Variable": "Present",
                "Value Type": "categorical",
                "Expected Values": "only-other",
            },
        ]
    )

    with patch(
        "scriptcraft.layers.layer_1_tools.level_1_impl.level_1.dictionary_driven_checker.runner.log_and_print"
    ) as mock_log:
        run_dictionary_checker(
            df=df,
            dict_df=dict_df,
            domain="test",
            output_path=output_dir,
            outlier_method=OutlierMethod.IQR,
        )

    assert (output_dir / "test_validation_results.csv").is_file()
    logged = " ".join(str(call.args[0]) for call in mock_log.call_args_list)
    assert "1 columns skipped" in logged


def test_runner_uses_validator_plugin_when_row_check_passes(output_dir: Path) -> None:
    df = pd.DataFrame({"Code": ["BAD"]})
    dict_df = pd.DataFrame(
        [
            {
                "Main Variable": "Code",
                "Value Type": "pattern",
                "Expected Values": "^[0-9]+$",
            }
        ]
    )

    run_dictionary_checker(
        df=df,
        dict_df=dict_df,
        domain="test",
        output_path=output_dir,
        outlier_method=OutlierMethod.IQR,
    )

    results_path = output_dir / "test_validation_results.csv"
    assert results_path.is_file()
    results = pd.read_csv(results_path)
    assert len(results) == 1
    assert results.iloc[0]["Type"] == "Error"


def test_runner_marks_numeric_issues_as_warnings(output_dir: Path) -> None:
    df = pd.DataFrame({"Score": ["not-a-number"]})
    dict_df = pd.DataFrame(
        [
            {
                "Main Variable": "Score",
                "Value Type": "numeric",
                "Expected Values": "0-100",
            }
        ]
    )

    run_dictionary_checker(
        df=df,
        dict_df=dict_df,
        domain="test",
        output_path=output_dir,
        outlier_method=OutlierMethod.IQR,
    )

    results = pd.read_csv(output_dir / "test_validation_results.csv")
    assert len(results) == 1
    assert results.iloc[0]["Type"] == "Warning"
