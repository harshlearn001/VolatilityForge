import pandas as pd


def validate_day(ce: pd.DataFrame,
                 pe: pd.DataFrame):

    if ce.empty:
        return False

    if pe.empty:
        return False

    if pd.isna(ce.iloc[0]["IMPLIED_VOL"]):
        return False

    if pd.isna(pe.iloc[0]["IMPLIED_VOL"]):
        return False

    return True