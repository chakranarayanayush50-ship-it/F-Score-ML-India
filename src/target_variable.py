"""
Phase 3 — Define the Target Variable

For each company-year row in fscore_signals.csv, computes the 12-month
forward stock return (calendar-date based) and compares it to the Nifty 50
benchmark's return over the same period. Labels each row as "outperformed"
(1) or "underperformed" (0).

Output: data/processed/labels.csv — this merges with fscore_signals.csv
to become the final training dataset for Phase 5.

Run from the repo root with your venv active:
    python src/target_variable.py
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
BENCHMARK_TICKER = "^NSEI"  # Nifty 50 — most reliably available benchmark on yfinance


def load_benchmark_history() -> pd.Series:
    """Download Nifty 50 price history to use as the benchmark."""
    print("Downloading Nifty 50 benchmark history...")
    bench = yf.Ticker(BENCHMARK_TICKER)
    hist = bench.history(period="10y")["Close"]
    hist.index = pd.to_datetime(hist.index).tz_localize(None)
    return hist


def load_company_price_history(ticker: str) -> pd.Series | None:
    company_dir = RAW_DIR / ticker.replace(".", "_")
    path = company_dir / "history.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_datetime(df.index, errors="coerce").tz_localize(None)
    return df["Close"] if "Close" in df.columns else None


def forward_return(price_series: pd.Series, start_date: pd.Timestamp, months: int = 12) -> float | None:
    """Calendar-date based forward return — robust to holidays/market closures."""
    if price_series is None or price_series.empty:
        return None
    end_date = start_date + pd.DateOffset(months=months)

    # asof finds the most recent available price on/before the given date
    start_price = price_series.asof(start_date)
    end_price = price_series.asof(end_date)

    if pd.isna(start_price) or pd.isna(end_price) or start_price == 0:
        return None
    return (end_price - start_price) / start_price


def main():
    signals_path = PROCESSED_DIR / "fscore_signals.csv"
    if not signals_path.exists():
        print(f"ERROR: {signals_path} not found. Run Phase 2 (fscore_signals.py) first.")
        return

    signals = pd.read_csv(signals_path)
    signals["fiscal_year_end"] = pd.to_datetime(signals["fiscal_year_end"])

    benchmark = load_benchmark_history()

    results = []
    tickers_processed = 0
    price_cache = {}

    for i, row in signals.iterrows():
        ticker = row["ticker"]
        start_date = row["fiscal_year_end"]

        if ticker not in price_cache:
            price_cache[ticker] = load_company_price_history(ticker)
            tickers_processed += 1
        price_series = price_cache[ticker]

        company_ret = forward_return(price_series, start_date)
        bench_ret = forward_return(benchmark, start_date)

        outperformed = None
        if company_ret is not None and bench_ret is not None:
            outperformed = int(company_ret > bench_ret)

        results.append({
            "ticker": ticker,
            "fiscal_year_end": row["fiscal_year_end"].date().isoformat(),
            "forward_return": company_ret,
            "benchmark_return": bench_ret,
            "outperformed": outperformed,
        })

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(signals)} rows...")

    labels = pd.DataFrame(results)
    labels["fiscal_year_end"] = pd.to_datetime(labels["fiscal_year_end"])
    valid = labels.dropna(subset=["outperformed"])

    out_path = PROCESSED_DIR / "labels.csv"
    labels.to_csv(out_path, index=False)

    print(f"\nDone. {len(labels)} rows written to {out_path}")
    print(f"{len(valid)}/{len(labels)} rows have a valid label "
          f"(the rest are missing price data for that forward window).")
    if len(valid) > 0:
        print(f"Class balance — outperformed: {valid['outperformed'].mean():.1%}")

    # Merge with fscore_signals.csv into the final training dataset
    merged = signals.merge(
        labels[["ticker", "fiscal_year_end", "forward_return", "benchmark_return", "outperformed"]],
        on=["ticker", "fiscal_year_end"], how="left"
    )
    merged.to_csv(PROCESSED_DIR / "training_dataset.csv", index=False)
    print(f"Merged training dataset written to data/processed/training_dataset.csv")


if __name__ == "__main__":
    main()
