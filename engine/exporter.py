from pathlib import Path

import pandas as pd


def export(df: pd.DataFrame,
           output: Path):

    df.to_csv(
        output.with_suffix(".csv"),
        index=False
    )

    df.to_parquet(
        output.with_suffix(".parquet"),
        index=False
    )