import pandas as pd

from engine.atm_selector import select_atm


def test_select_atm_accepts_option_type_column():
    df = pd.DataFrame(
        [
            {
                "TRADE_DATE": "2025-01-02",
                "STRIKE_PRICE": 100.0,
                "SPOT_CLOSE": 100.0,
                "OPTION_TYPE": "CE",
                "IMPLIED_VOL": 0.20,
            },
            {
                "TRADE_DATE": "2025-01-02",
                "STRIKE_PRICE": 100.0,
                "SPOT_CLOSE": 100.0,
                "OPTION_TYPE": "PE",
                "IMPLIED_VOL": 0.18,
            },
            {
                "TRADE_DATE": "2025-01-02",
                "STRIKE_PRICE": 110.0,
                "SPOT_CLOSE": 100.0,
                "OPTION_TYPE": "CE",
                "IMPLIED_VOL": 0.15,
            },
            {
                "TRADE_DATE": "2025-01-02",
                "STRIKE_PRICE": 110.0,
                "SPOT_CLOSE": 100.0,
                "OPTION_TYPE": "PE",
                "IMPLIED_VOL": 0.12,
            },
        ]
    )

    strike, ce, pe = select_atm(df)

    assert strike == 100.0
    assert not ce.empty
    assert not pe.empty
