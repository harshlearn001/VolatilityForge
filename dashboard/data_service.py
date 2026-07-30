from pathlib import Path

import pandas as pd


class DataService:

    def __init__(self):
        self.base = Path(r"H:\VolatilityForge\data\daily_iv")

    def load_symbol(self, symbol: str):

        parquet = self.base / f"{symbol}.parquet"
        csv = self.base / f"{symbol}.csv"

        if parquet.exists():
            return pd.read_parquet(parquet)

        if csv.exists():
            return pd.read_csv(csv)

        raise FileNotFoundError(
            f"No data found for {symbol}"
        )

    def prepare(
        self,
        df: pd.DataFrame,
    ):

        df = df.copy()

        df["TRADE_DATE"] = pd.to_datetime(
            df["TRADE_DATE"]
        )

        df = df.sort_values(
            "TRADE_DATE"
        )

        return df

    def apply_lookback(
        self,
        df,
        lookback,
    ):

        if lookback == "All":
            return df

        return df.tail(int(lookback))

    def latest(
        self,
        df,
    ):

        return df.iloc[-1]