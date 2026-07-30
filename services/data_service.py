"""
VolatilityForge

Market data loading service.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class DataService:
    """
    Service responsible for loading and validating market data.
    """

    REQUIRED_COLUMNS = {
        "TRADE_DATE",
        "ATM_IV",
        "FUTURE_CLOSE",
    }

    def __init__(self, data_directory: Path):
        self._data_directory = Path(data_directory)

        if not self._data_directory.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self._data_directory}"
            )

    def load(self, symbol: str) -> pd.DataFrame:
        """
        Load market data for a symbol.

        Preference:
            1. parquet
            2. csv
        """

        file_path = self._find_file(symbol)

        logger.info("Loading %s", file_path.name)

        if file_path.suffix.lower() == ".parquet":
            df = pd.read_parquet(file_path)
        else:
            df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(f"{symbol} dataset is empty.")

        self._validate_columns(df)

        df["TRADE_DATE"] = pd.to_datetime(df["TRADE_DATE"])

        df = (
            df.sort_values("TRADE_DATE")
              .reset_index(drop=True)
        )

        return df

    def _find_file(self, symbol: str) -> Path:
        symbol = symbol.upper()

        parquet = self._data_directory / f"{symbol}.parquet"
        csv = self._data_directory / f"{symbol}.csv"

        if parquet.exists():
            return parquet

        if csv.exists():
            return csv

        raise FileNotFoundError(
            f"No data found for symbol '{symbol}'."
        )

    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing = self.REQUIRED_COLUMNS - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )