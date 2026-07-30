from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_iv_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate day-over-day IV change.

    Required column:
        ATM_IV
    """

    out = df.copy()

    if "ATM_IV" not in out.columns:
        raise ValueError("ATM_IV column not found.")

    out = out.sort_values("TRADE_DATE").reset_index(drop=True)

    out["PREV_IV"] = out["ATM_IV"].shift(1)

    out["IIV"] = out["ATM_IV"] - out["PREV_IV"]

    out["IIV_PCT"] = np.where(
        out["PREV_IV"] == 0,
        np.nan,
        (out["IIV"] / out["PREV_IV"]) * 100,
    )

    out["IIV_DIRECTION"] = np.select(
        [
            out["IIV"] > 0,
            out["IIV"] < 0,
        ],
        [
            "Expansion",
            "Contraction",
        ],
        default="Flat",
    )

    return out