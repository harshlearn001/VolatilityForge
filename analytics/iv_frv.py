import numpy as np
import pandas as pd


def calculate_iv_frv(df: pd.DataFrame) -> pd.DataFrame:

    out = df.copy()

    out["IV_MINUS_FRV"] = (
        out["ATM_IV"] - out["FRV_20"]
    ).round(4)

    out["IV_FRV_RATIO"] = np.where(
        out["FRV_20"] == 0,
        np.nan,
        out["ATM_IV"] / out["FRV_20"],
    )

    out["IV_FRV_RATIO"] = out["IV_FRV_RATIO"].round(3)

    return out