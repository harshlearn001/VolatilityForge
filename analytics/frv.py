from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_frv(
    df: pd.DataFrame,
    windows=(10, 20, 30),
) -> pd.DataFrame:
    """
    Calculate Forward Realized Volatility (FRV).

    FRV is the annualized volatility of future log returns.
    """

    out = df.copy()

    out = out.sort_values("TRADE_DATE").reset_index(drop=True)

    log_returns = np.log(
        out["SPOT_CLOSE"] / out["SPOT_CLOSE"].shift(1)
    )

    for window in windows:

        values = []

        for i in range(len(out)):

            future_returns = log_returns.iloc[i + 1 : i + 1 + window]

            if len(future_returns) < window:
                values.append(np.nan)
                continue

            frv = future_returns.std() * np.sqrt(252)

            values.append(round(float(frv), 4))

        out[f"FRV_{window}"] = values

    return out