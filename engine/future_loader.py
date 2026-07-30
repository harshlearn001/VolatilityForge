from pathlib import Path

import pandas as pd


def load_future(csv_file: Path) -> pd.DataFrame:

    df = pd.read_csv(csv_file)

    df["TRADE_DATE"] = pd.to_datetime(
        df["TRADE_DATE"].astype(str),
        format="%Y%m%d"
    )

    df["EXP_DATE"] = pd.to_datetime(
        df["EXP_DATE"].astype(str),
        format="%Y%m%d"
    )

    df = df[df["EXPIRY_TYPE"] == "NEAR"].copy()

    return df