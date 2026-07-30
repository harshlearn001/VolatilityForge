import pandas as pd


def nearest_strike(spot: float, strikes):

    strikes = sorted(strikes)

    return min(
        strikes,
        key=lambda x: abs(x - spot)
    )


def select_atm(option_df: pd.DataFrame):

    spot = option_df.iloc[0]["SPOT_CLOSE"]

    strike = nearest_strike(
        spot,
        option_df["STRIKE_PRICE"].unique()
    )

    ce = option_df[
        (option_df["STRIKE_PRICE"] == strike)
        &
        (option_df["OPT_TYPE"] == "CE")
    ]

    pe = option_df[
        (option_df["STRIKE_PRICE"] == strike)
        &
        (option_df["OPT_TYPE"] == "PE")
    ]

    return strike, ce, pe