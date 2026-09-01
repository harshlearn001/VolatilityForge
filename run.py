from time import perf_counter

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

from validator.daily_iv_validator import validate_daily_iv


# ============================================================
# Process One Symbol
# ============================================================

def process_symbol(symbol: str) -> bool:
    """Run complete Daily IV pipeline for one symbol."""

    start = perf_counter()

    greeks_path = GREEKS_ROOT / "INDICES" / f"{symbol}.csv"
    futures_path = FUTURES_ROOT / "FUTIDX" / f"{symbol}.csv"

    if not greeks_path.exists():
        print(f"[SKIP] Greeks file not found : {greeks_path}")
        return False

    if not futures_path.exists():
        print(f"[SKIP] Futures file not found: {futures_path}")
        return False

    try:

        # ----------------------------------------------------
        # Load Data
        # ----------------------------------------------------

        greeks = load_greeks(greeks_path)
        future = load_future(futures_path)

        # ----------------------------------------------------
        # Daily IV
        # ----------------------------------------------------

        daily = build_daily_iv(greeks, future)

        # ----------------------------------------------------
        # Analytics
        # ----------------------------------------------------

        daily = calculate_iv_rank(
            daily,
            lookback=252,
        )

        daily = calculate_iv_percentile(
            daily,
            lookback=252,
        )

        daily = calculate_hv(
            daily,
            window=20,
        )

        daily = calculate_iv_hv(daily)

        daily = calculate_frv(daily)

        daily = calculate_forecast_accuracy(daily)

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        errors, warnings = validate_daily_iv(daily)

        if warnings:

            print()

            for warning in warnings:
                print(f"[WARNING] {symbol}: {warning}")

        if errors:

            print()

            print(f"[FAILED] Validation failed for {symbol}")

            for err in errors:
                print(f"   • {err}")

            return False

        # ----------------------------------------------------
        # Export
        # ----------------------------------------------------

        export(
            daily,
            DAILY_IV / symbol,
        )

        elapsed = perf_counter() - start

        latest = daily.iloc[-1]

        print(
            f"[OK] {symbol:<12}"
            f" Rows={len(daily):>5}"
            f" Date={latest['TRADE_DATE'].date()}"
            f" ATM_IV={latest['ATM_IV']:.2f}"
            f" IVRank={latest['IV_RANK']:.2f}"
            f" IVPct={latest['IV_PERCENTILE']:.2f}"
            f" Time={elapsed:.2f}s"
        )

        return True

    except Exception as exc:

        print(f"[FAILED] {symbol}: {exc}")

        return False


# ============================================================
# Main
# ============================================================

def main():

    indices_dir = GREEKS_ROOT / "INDICES"

    if not indices_dir.exists():
        raise FileNotFoundError(
            f"Directory not found:\n{indices_dir}"
        )

    symbols = sorted(
        p.stem
        for p in indices_dir.glob("*.csv")
    )

    if not symbols:
        raise RuntimeError(
            "No symbols found."
        )

    print("=" * 65)
    print("VOLATILITY FORGE DAILY IV PIPELINE")
    print("=" * 65)

    success = 0
    failed = 0

    pipeline_start = perf_counter()

    for index, symbol in enumerate(symbols, start=1):

        print()

        print(
            f"[{index}/{len(symbols)}] Processing {symbol}"
        )

        if process_symbol(symbol):
            success += 1
        else:
            failed += 1

    elapsed = perf_counter() - pipeline_start

    print()
    print("=" * 65)
    print("SUMMARY")
    print("=" * 65)

    print(f"Processed : {len(symbols)}")
    print(f"Success   : {success}")
    print(f"Failed    : {failed}")
    print(f"Elapsed   : {elapsed:.2f} sec")
    print(f"Average   : {elapsed / len(symbols):.2f} sec/symbol")
    print(f"Output    : {DAILY_IV}")

    print()

    if failed == 0:

        print("✅ ALL SYMBOLS PROCESSED SUCCESSFULLY")

    else:

        print("❌ SOME SYMBOLS FAILED")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()