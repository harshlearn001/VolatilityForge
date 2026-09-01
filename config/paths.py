from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Shared input data
GREEKS_ROOT = Path(r"H:\OptionGreeks\data\greeks")
FUTURES_ROOT = Path(r"H:\MarketForge\data\master\Futures_master")

# Project output
DATA_ROOT = PROJECT_ROOT / "data"
DAILY_IV = DATA_ROOT / "daily_iv"