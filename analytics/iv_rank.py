from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_iv_rank(
    df: pd.DataFrame,
    lookback: int = 252,
) -> pd.DataFrame:
    """
    Calculate rolling IV Rank.

    IV Rank =
    (Current IV - Lowest IV) /
    (Highest IV - Lowest IV) * 100
    """

    out = df.copy()

    out["IV_LOW"] = (
        out["ATM_IV"]
        .rolling(window=lookback, min_periods=1)
        .min()
    )

    out["IV_HIGH"] = (
        out["ATM_IV"]
        .rolling(window=lookback, min_periods=1)
        .max()
    )

    denominator = out["IV_HIGH"] - out["IV_LOW"]

    out["IV_RANK"] = np.where(
        denominator == 0,
        0.0,
        ((out["ATM_IV"] - out["IV_LOW"]) / denominator) * 100,
    )

    out["IV_RANK"] = out["IV_RANK"].round(2)

    return out