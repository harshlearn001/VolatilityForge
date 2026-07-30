import numpy as np


def classify_regime(df):

    out = df.copy()

    conditions = [

        (out["IV_RANK"] >= 80),

        (out["IV_RANK"] >= 60),

        (out["IV_RANK"] >= 30),

        (out["IV_RANK"] < 30),

    ]

    choices = [

        "Extreme",

        "High",

        "Normal",

        "Low",

    ]

    out["VOLATILITY_STATE"] = np.select(
        conditions,
        choices,
        default="Unknown"
    )

    return out