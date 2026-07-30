from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_iv_hv(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare Implied Volatility with Historical Volatility.
    """

    out = df.copy()

    # -------------------------------------------------------
    # Absolute Difference
    # -------------------------------------------------------

    out["IV_MINUS_HV"] = (
        out["ATM_IV"] - out["HV"]
    ).round(4)

    # -------------------------------------------------------
    # Ratio
    # -------------------------------------------------------

    out["IV_HV_RATIO"] = np.where(
        out["HV"] == 0,
        np.nan,
        out["ATM_IV"] / out["HV"],
    )

    out["IV_HV_RATIO"] = out["IV_HV_RATIO"].round(3)

    # -------------------------------------------------------
    # Premium %
    # -------------------------------------------------------

    out["IV_PREMIUM_PCT"] = np.where(
        out["HV"] == 0,
        np.nan,
        (
            (out["ATM_IV"] - out["HV"])
            / out["HV"]
        ) * 100,
    )

    out["IV_PREMIUM_PCT"] = out["IV_PREMIUM_PCT"].round(2)

    # -------------------------------------------------------
    # Volatility Regime
    # -------------------------------------------------------

    conditions = [
        out["IV_HV_RATIO"] >= 1.20,
        out["IV_HV_RATIO"].between(1.00, 1.20, inclusive="left"),
        out["IV_HV_RATIO"].between(0.80, 1.00, inclusive="left"),
        out["IV_HV_RATIO"] < 0.80,
    ]

    choices = [
        "Very Rich",
        "Rich",
        "Fair",
        "Cheap",
    ]

    out["VOL_REGIME"] = np.select(
        conditions,
        choices,
        default="Unknown",
    )

    return out