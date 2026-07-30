from __future__ import annotations

import pandas as pd


def build_morning_iv(option_chain: pd.DataFrame) -> pd.DataFrame:
    """
    Build morning ATM IV snapshot.

    Expected input:
        TRADE_DATE
        STRIKE_PRICE
        SPOT_CLOSE
        OPTION_TYPE
        IMPLIED_VOL
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

        open_iv = (
            ce["IMPLIED_VOL"].iloc[0]
            + pe["IMPLIED_VOL"].iloc[0]
        ) / 2

        out.append(
            {
                "TRADE_DATE": trade_date,
                "OPEN_IV": round(open_iv, 4),
            }
        )

    return pd.DataFrame(out)