from __future__ import annotations

import pandas as pd


def build_intraday_iv(
    morning: pd.DataFrame,
    closing: pd.DataFrame,
) -> pd.DataFrame:

    return morning.merge(
        closing,
        on="TRADE_DATE",
        how="inner",
    )