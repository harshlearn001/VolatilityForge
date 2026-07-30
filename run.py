from config.paths import (
    GREEKS_ROOT,
    FUTURES_ROOT,
    DAILY_IV,
)

from engine.loader import load_greeks
from engine.future_loader import load_future
from engine.daily_iv_engine import build_daily_iv
from engine.exporter import export

from analytics.iv_rank import calculate_iv_rank
from analytics.iv_percentile import calculate_iv_percentile
from analytics.hv import calculate_hv
from analytics.iv_hv import calculate_iv_hv
from analytics.frv import calculate_frv
from analytics.forecast_accuracy import calculate_forecast_accuracy

# --------------------------------------------------------
# Symbol
# --------------------------------------------------------

symbol = "NIFTY"

# --------------------------------------------------------
# Load Source Data
# --------------------------------------------------------

greeks = load_greeks(
    GREEKS_ROOT / "INDICES" / f"{symbol}.csv"
)

future = load_future(
    FUTURES_ROOT / "FUTIDX" / f"{symbol}.csv"
)

# --------------------------------------------------------
# Build Daily IV Dataset
# --------------------------------------------------------

daily = build_daily_iv(
    greeks,
    future,
)

# --------------------------------------------------------
# Calculate IV Rank
# --------------------------------------------------------

daily = calculate_iv_rank(
    daily,
    lookback=252,
)
# --------------------------------------------------------
# Calculate IV Percentile
# --------------------------------------------------------
daily = calculate_iv_percentile(
    daily,
    lookback=252,
)

# --------------------------------------------------------
# Calculate HV 
# --------------------------------------------------------
daily = calculate_hv(
    daily,
    window=20
)
# --------------------------------------------------------
# Calculate IV-HV 
# --------------------------------------------------------
daily = calculate_iv_hv(daily)
# --------------------------------------------------------
# Calculate FRV
# --------------------------------------------------------
daily = calculate_frv(daily)

daily = calculate_forecast_accuracy(daily)

# --------------------------------------------------------
# Preview
# --------------------------------------------------------

print("\n===== DAILY IV WITH IV RANK =====\n")

print(
    daily[
        [
            "TRADE_DATE",
            "ATM_IV",
            "FRV_20",
            "FORECAST_ERROR",
            "ABS_FORECAST_ERROR",
            "IV_ACCURACY",
        ]
    ].iloc[150:170]
)
print("\nShape:", daily.shape)

# --------------------------------------------------------
# Export
# --------------------------------------------------------

export(
    daily,
    DAILY_IV / symbol,
)

print(f"\nSaved to: {DAILY_IV}")