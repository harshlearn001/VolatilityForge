import pandas as pd


def nearest_strike(spot: float, strikes):

    strikes = sorted(strikes)

    return min(
        strikes,
        key=lambda x: abs(x - spot)
    )


def _option_type_column(option_df: pd.DataFrame) -> str:
    for column_name in ("OPT_TYPE", "OPTION_TYPE"):
        if column_name in option_df.columns:
            return column_name

    raise KeyError(
        "Expected either 'OPT_TYPE' or 'OPTION_TYPE' in the input DataFrame."
    )


def select_atm(option_df: pd.DataFrame):

    required_columns = {"SPOT_CLOSE", "STRIKE_PRICE"}
    missing_columns = required_columns - set(option_df.columns)
    if missing_columns:
        raise KeyError(
            f"Missing required columns for ATM selection: {sorted(missing_columns)}"
        )

    spot = option_df.iloc[0]["SPOT_CLOSE"]

    strike = nearest_strike(
        spot,
        option_df["STRIKE_PRICE"].unique()
    )

    option_type_column = _option_type_column(option_df)

    ce = option_df[
        (option_df["STRIKE_PRICE"] == strike)
        &
        (option_df[option_type_column] == "CE")
    ]

    pe = option_df[
        (option_df["STRIKE_PRICE"] == strike)
        &
        (option_df[option_type_column] == "PE")
    ]

    return strike, ce, pe