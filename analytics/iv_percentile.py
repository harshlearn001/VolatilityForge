from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_iv_percentile(
    df: pd.DataFrame,
    lookback: int = 252,
) -> pd.DataFrame:
    """
    Calculate rolling IV Percentile.

    IV Percentile =
    Percentage of observations in the lookback
    window having IV lower than today's IV.
    """

    out = df.copy()

    out = out.sort_values(
        "TRADE_DATE"
    ).reset_index(drop=True)

    ivp = []

    iv = out["ATM_IV"].to_numpy()

    for i in range(len(out)):

        start = max(0, i - lookback + 1)

        window = iv[start:i + 1]

        current = iv[i]

        percentile = (
            np.sum(window < current)
            / len(window)
        ) * 100

        ivp.append(round(percentile, 2))

    out["IV_PERCENTILE"] = ivp

    return out