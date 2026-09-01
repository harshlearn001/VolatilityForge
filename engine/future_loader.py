from pathlib import Path

import pandas as pd


def load_future(csv_file: Path) -> pd.DataFrame:

    df = pd.read_csv(csv_file)

    print("\n" + "=" * 80)
    print("FUTURE FILE :", csv_file)
    print("=" * 80)
    print(df.columns.tolist())
    print("=" * 80)

    df["TRADE_DATE"] = pd.to_datetime(
        df["TRADE_DATE"].astype(str),
        format="%Y%m%d"
    )

    df["EXP_DATE"] = pd.to_datetime(
        df["EXP_DATE"].astype(str),
        format="%Y%m%d"
    )

    if "EXPIRY_TYPE" in df.columns:
        df = df[df["EXPIRY_TYPE"] == "NEAR"].copy()
    else:
        print("[INFO] EXPIRY_TYPE column not found.")

    return df