from src.model_service import FraudModelService


service = FraudModelService()


def test_expected_feature_schema():
    expected_features = (
        ["Time"]
        + [f"V{i}" for i in range(1, 29)]
        + ["Amount"]
    )

    assert service.features == expected_features

import pytest


def test_non_numeric_feature_fails():
    transaction = {
        feature: 0.0
        for feature in service.features
    }

    transaction["Amount"] = "not-a-number"

    with pytest.raises(Exception):
        service.predict(transaction)

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


def test_dataset_schema():
    df = pd.read_csv(
        BASE_DIR / "creditcard.csv",
        nrows=10
    )

    expected_columns = (
        ["Time"]
        + [f"V{i}" for i in range(1, 29)]
        + ["Amount", "Class"]
    )

    assert list(df.columns) == expected_columns


def test_target_is_binary():
    df = pd.read_csv(
        BASE_DIR / "creditcard.csv",
        usecols=["Class"]
    )

    assert set(df["Class"].unique()).issubset({0, 1})

def test_model_matches_config_feature_count():
    assert service.model.n_features_in_ == len(service.features)

def test_sample_data_has_no_missing_features():
    df = pd.read_csv(
        BASE_DIR / "creditcard.csv",
        nrows=1000#1000 rows only bcz dataset is too large so it might take more time 
    )

    assert not df[service.features].isnull().any().any()