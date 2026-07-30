from pathlib import Path

PROJECT_ROOT = Path(r"H:\VolatilityForge")

GREEKS_ROOT = Path(r"H:\OptionGreeks\data\greeks")
FUTURES_ROOT = Path(r"H:\MarketForge\data\master\Futures_master_three_expiries")

OUTPUT_ROOT = PROJECT_ROOT / "data"

DAILY_IV = OUTPUT_ROOT / "daily_iv"
REPORTS = OUTPUT_ROOT / "reports"
CACHE = OUTPUT_ROOT / "cache"


def ensure_directory(path: Path):
    if path.exists():
        if not path.is_dir():
            raise RuntimeError(
                f"{path} exists but is a file. Delete or rename it."
            )
    else:
        path.mkdir(parents=True, exist_ok=True)


for folder in [OUTPUT_ROOT, DAILY_IV, REPORTS, CACHE]:
    ensure_directory(folder)