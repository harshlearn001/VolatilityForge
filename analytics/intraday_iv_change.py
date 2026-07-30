from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_intraday_iv_change(
    df: pd.DataFrame,
    open_column: str = "OPEN_IV",
    close_column: str = "CLOSE_IV",
) -> pd.DataFrame:
    """
    Calculate Intraday IV Change (IIV).

    IIV = Close IV - Open IV

    Positive  -> IV Expanded
    Negative  -> IV Contracted
    """

    out = df.copy()

    required = [open_column, close_column]

    missing = [c for c in required if c not in out.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # -------------------------------------------------
    # Absolute Change
    # -------------------------------------------------

    out["IIV"] = (
        out[close_column] -
        out[open_column]
    ).round(4)

    # -------------------------------------------------
    # Percentage Change
    # -------------------------------------------------

    out["IIV_PCT"] = np.where(
        out[open_column] == 0,
        np.nan,
        (
            out["IIV"] /
            out[open_column]
        ) * 100
    )

    out["IIV_PCT"] = out["IIV_PCT"].round(2)

    # -------------------------------------------------
    # Direction
    # -------------------------------------------------

    out["IIV_DIRECTION"] = np.where(
        out["IIV"] > 0,
        "Expansion",
        np.where(
            out["IIV"] < 0,
            "Contraction",
            "Flat",
        ),
    )

    return out