from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_forecast_accuracy(
    df: pd.DataFrame,
    horizon: int = 20,
) -> pd.DataFrame:
    """
    Compare implied volatility with future realized volatility.
    """

    out = df.copy()

    frv = f"FRV_{horizon}"

    out["FORECAST_ERROR"] = (
        out[frv] - out["ATM_IV"]
    ).round(4)

    out["ABS_FORECAST_ERROR"] = (
        out["FORECAST_ERROR"]
        .abs()
        .round(4)
    )

    out["SQUARED_ERROR"] = (
        out["FORECAST_ERROR"] ** 2
    ).round(6)

    out["IV_ACCURACY"] = np.where(
        out["ABS_FORECAST_ERROR"].isna(),
        "Not Available",
        np.where(
            out["ABS_FORECAST_ERROR"] <= 0.02,
            "Excellent",
            np.where(
                out["ABS_FORECAST_ERROR"] <= 0.05,
                "Good",
                np.where(
                    out["ABS_FORECAST_ERROR"] <= 0.10,
                    "Fair",
                    "Poor",
                ),
            ),
        ),
    )

    return out