from __future__ import annotations

import pandas as pd

from engine.atm_selector import select_atm
from engine.validator import validate_day


def build_daily_iv(
    greeks_df: pd.DataFrame,
    futures_df: pd.DataFrame,
) -> pd.DataFrame:

    records = []

    # ----------------------------------------------------------
    # One trading day at a time
    # ----------------------------------------------------------

    for trade_date, day_df in greeks_df.groupby("TRADE_DATE"):

        # ------------------------------------------------------
        # Nearest expiry available on that day
        # ------------------------------------------------------

        expiry = day_df["EXP_DATE"].min()

        expiry_df = day_df[
            day_df["EXP_DATE"] == expiry
        ]

        strike, ce, pe = select_atm(expiry_df)

        if not validate_day(ce, pe):
            continue

        future = futures_df[
            futures_df["TRADE_DATE"] == trade_date
        ]

        if future.empty:
            continue

        future_close = future.iloc[0]["CLOSE_PRICE"]

        records.append(
            {
                "TRADE_DATE": trade_date,
                "SYMBOL": ce.iloc[0]["SYMBOL"],
                "EXP_DATE": expiry,
                "FUTURE_CLOSE": future_close,
                "SPOT_CLOSE": ce.iloc[0]["SPOT_CLOSE"],
                "ATM_STRIKE": strike,
                "CALL_IV": ce.iloc[0]["IMPLIED_VOL"],
                "PUT_IV": pe.iloc[0]["IMPLIED_VOL"],
                "ATM_IV": (
                    ce.iloc[0]["IMPLIED_VOL"]
                    + pe.iloc[0]["IMPLIED_VOL"]
                ) / 2,
                "DAYS_TO_EXPIRY": ce.iloc[0]["DAYS_TO_EXPIRY"],
            }
        )

    return pd.DataFrame(records)