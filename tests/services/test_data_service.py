from pathlib import Path

import pandas as pd
import pytest

from services.data_service import DataService


def test_load_csv(tmp_path: Path):
    df = pd.DataFrame({
        "TRADE_DATE": ["2025-01-02"],
        "ATM_IV": [15.0],
        "FUTURE_CLOSE": [25000],
    })

    df.to_csv(tmp_path / "NIFTY.csv", index=False)

    service = DataService(tmp_path)

    loaded = service.load("NIFTY")

    assert len(loaded) == 1


def test_load_parquet(tmp_path: Path):
    df = pd.DataFrame({
        "TRADE_DATE": ["2025-01-02"],
        "ATM_IV": [15],
        "FUTURE_CLOSE": [25000],
    })

    df.to_parquet(tmp_path / "NIFTY.parquet")

    service = DataService(tmp_path)

    loaded = service.load("NIFTY")

    assert len(loaded) == 1


def test_missing_symbol(tmp_path: Path):
    service = DataService(tmp_path)

    with pytest.raises(FileNotFoundError):
        service.load("UNKNOWN")


def test_missing_columns(tmp_path: Path):
    df = pd.DataFrame({
        "TRADE_DATE": ["2025-01-01"]
    })

    df.to_csv(tmp_path / "NIFTY.csv", index=False)

    service = DataService(tmp_path)

    with pytest.raises(ValueError):
        service.load("NIFTY")


def test_dates_are_sorted(tmp_path: Path):
    df = pd.DataFrame({
        "TRADE_DATE": ["2025-01-03", "2025-01-01"],
        "ATM_IV": [16, 15],
        "FUTURE_CLOSE": [25100, 25000],
    })

    df.to_csv(tmp_path / "NIFTY.csv", index=False)

    service = DataService(tmp_path)

    loaded = service.load("NIFTY")

    assert loaded.iloc[0]["TRADE_DATE"] < loaded.iloc[1]["TRADE_DATE"]


def test_datetime_conversion(tmp_path: Path):
    df = pd.DataFrame({
        "TRADE_DATE": ["2025-01-01"],
        "ATM_IV": [15],
        "FUTURE_CLOSE": [25000],
    })

    df.to_csv(tmp_path / "NIFTY.csv", index=False)

    service = DataService(tmp_path)

    loaded = service.load("NIFTY")

    assert pd.api.types.is_datetime64_any_dtype(
        loaded["TRADE_DATE"]
    )


def test_empty_dataset(tmp_path: Path):
    df = pd.DataFrame(
        columns=[
            "TRADE_DATE",
            "ATM_IV",
            "FUTURE_CLOSE",
        ]
    )

    df.to_csv(tmp_path / "NIFTY.csv", index=False)

    service = DataService(tmp_path)

    with pytest.raises(ValueError):
        service.load("NIFTY")