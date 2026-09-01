import numpy as np
import pandas as pd


def validate_daily_iv(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Validate Daily IV dataset.

    Returns
    -------
    (errors, warnings)
    """

    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "TRADE_DATE",
        "ATM_IV",
        "IV_RANK",
        "IV_PERCENTILE",
        "HV_20",
        "IV_HV_RATIO",
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        errors.append(f"Missing columns: {missing}")
        return errors, warnings

    if df.empty:
        errors.append("Dataset is empty")
        return errors, warnings

    # ----------------------------------------------------
    # Duplicate dates
    # ----------------------------------------------------

    if df["TRADE_DATE"].duplicated().any():
        errors.append("Duplicate TRADE_DATE found")

    # ----------------------------------------------------
    # Date order
    # ----------------------------------------------------

    if not df["TRADE_DATE"].is_monotonic_increasing:
        warnings.append("TRADE_DATE is not sorted")

    # ----------------------------------------------------
    # Numeric validation
    # ----------------------------------------------------

    numeric_cols = [
        "ATM_IV",
        "IV_RANK",
        "IV_PERCENTILE",
        "HV_20",
        "IV_HV_RATIO",
    ]

    for col in numeric_cols:

        if df[col].isna().any():
            errors.append(f"{col} contains NaN")

        if np.isinf(df[col]).any():
            errors.append(f"{col} contains infinite values")

    # ----------------------------------------------------
    # Range checks
    # ----------------------------------------------------

    if not df["IV_RANK"].between(0, 100).all():
        errors.append("IV_RANK outside 0-100")

    if not df["IV_PERCENTILE"].between(0, 100).all():
        errors.append("IV_PERCENTILE outside 0-100")

    if (df["ATM_IV"] < 0).any():
        errors.append("Negative ATM_IV")

    if (df["HV_20"] < 0).any():
        errors.append("Negative HV_20")

    if (df["IV_HV_RATIO"] < 0).any():
        errors.append("Negative IV_HV_RATIO")

    # ----------------------------------------------------
    # Optional warnings
    # ----------------------------------------------------

    if df["ATM_IV"].max() > 5:
        warnings.append("Unusually high ATM_IV values detected")

    if len(df) < 100:
        warnings.append("Dataset contains very few observations")

    return errors, warnings