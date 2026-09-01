from pathlib import Path

import pandas as pd

from dashboard.data_service import DataService


def test_load_symbol_uses_configured_directory(tmp_path: Path):
    data_dir = tmp_path / "daily_iv"
    data_dir.mkdir()

    df = pd.DataFrame(
        {
            "TRADE_DATE": ["2025-01-02"],
            "ATM_IV": [0.2],
            "FUTURE_CLOSE": [100.0],
        }
    )
    df.to_csv(data_dir / "NIFTY.csv", index=False)

    service = DataService(data_dir)
    loaded = service.load_symbol("NIFTY")

    assert len(loaded) == 1
    assert loaded.iloc[0]["ATM_IV"] == 0.2
