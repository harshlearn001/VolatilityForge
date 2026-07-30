from dataclasses import dataclass


@dataclass
class DashboardState:
    symbol: str = "NIFTY"

    lookback: int = 252

    hv_window: int = 20

    frv_window: int = 20

    expiry_type: str = "NEAR"

    atm_reference: str = "Futures"

    show_iv: bool = True
    show_hv: bool = True
    show_frv: bool = True
    show_future: bool = True
    show_spot: bool = False
    show_iv_rank: bool = False
    show_iv_percentile: bool = False