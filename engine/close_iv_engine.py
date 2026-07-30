from __future__ import annotations

import pandas as pd


def build_close_iv(option_chain: pd.DataFrame) -> pd.DataFrame:
    """
    Build closing ATM IV snapshot.
    """

    out = []

    for trade_date, day in option_chain.groupby("TRADE_DATE"):

        spot = day["SPOT_CLOSE"].iloc[0]

        strikes = day["STRIKE_PRICE"].drop_duplicates()

        atm = min(strikes, key=lambda x: abs(x - spot))

        ce = day[
            (day["OPTION_TYPE"] == "CE")
            & (day["STRIKE_PRICE"] == atm)
        ]

        pe = day[
            (day["OPTION_TYPE"] == "PE")
            & (day["STRIKE_PRICE"] == atm)
        ]

        if ce.empty or pe.empty:
            continue

        close_iv = (
            ce["IMPLIED_VOL"].iloc[0]
            + pe["IMPLIED_VOL"].iloc[0]
        ) / 2

        out.append(
            {
                "TRADE_DATE": trade_date,
                "CLOSE_IV": round(close_iv, 4),
            }
        )

    return pd.DataFrame(out)