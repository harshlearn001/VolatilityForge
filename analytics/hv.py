from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_hv(
    df: pd.DataFrame,
    window: int = 20,
) -> pd.DataFrame:
    """
    Historical Volatility (Annualized)

    Parameters
    ----------
    window : int
        Rolling trading days.
        Typical values:
            20
            30
            60
            90
            252
    """

    out = df.copy()

    out = out.sort_values(
        "TRADE_DATE"
    ).reset_index(drop=True)

    # ----------------------------
    # Daily Log Return
    # ----------------------------

    out["LOG_RETURN"] = np.log(
        out["SPOT_CLOSE"] /
        out["SPOT_CLOSE"].shift(1)
    )

    # ----------------------------
    # Historical Volatility
    # ----------------------------

    out["HV"] = (
        out["LOG_RETURN"]
        .rolling(window)
        .std()
        * np.sqrt(252)
    )

    out["HV"] = out["HV"].round(4)

    return out