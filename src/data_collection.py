"""
Phase 1 — Data Collection

Pulls financial statements and price history for the defined company
universe (Nifty Smallcap 250 / Midcap 150) via yfinance, and saves raw
data to data/raw/.

Usage:
    python src/data_collection.py
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_company_universe(path: str) -> list[str]:
    """Load NSE symbols from a CSV of index constituents and append .NS suffix."""
    df = pd.read_csv(path)
    symbols = df["Symbol"].astype(str).str.strip().tolist()
    return [f"{s}.NS" for s in symbols]


def fetch_company_data(ticker: str) -> dict:
    """Pull financials, balance sheet, cash flow, and price history for one company."""
    t = yf.Ticker(ticker)
    return {
        "financials": t.financials,
        "balance_sheet": t.balance_sheet,
        "cashflow": t.cashflow,
        "history": t.history(period="7y"),
    }


def save_company_data(ticker: str, data: dict) -> None:
    """Save each data component as a separate CSV under data/raw/<ticker>/."""
    company_dir = RAW_DIR / ticker.replace(".", "_")
    company_dir.mkdir(parents=True, exist_ok=True)
    for name, df in data.items():
        if df is not None and not df.empty:
            df.to_csv(company_dir / f"{name}.csv")


def main():
    # TODO: point this at your downloaded Nifty Smallcap 250 / Midcap 150 CSV
    universe_path = "data/raw/company_universe.csv"
    issues = []

    tickers = load_company_universe(universe_path)
    for ticker in tickers:
        try:
            data = fetch_company_data(ticker)
            save_company_data(ticker, data)
            print(f"OK   {ticker}")
        except Exception as e:
            issues.append({"ticker": ticker, "error": str(e)})
            print(f"FAIL {ticker}: {e}")

    if issues:
        pd.DataFrame(issues).to_csv(RAW_DIR / "data_quality_issues.csv", index=False)


if __name__ == "__main__":
    main()
