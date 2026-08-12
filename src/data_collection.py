"""
Phase 1 — Data Collection (full version)

1. Downloads the Nifty Smallcap 250 constituent list directly from NSE Indices.
2. Pulls financials, balance sheet, cash flow, and price history for each company.
3. Saves raw data per company, and logs any failures.

Run with your Python 3.11 venv active:
    python data_collection.py
"""

import time
import requests
import yfinance as yf
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

UNIVERSE_URL = "https://www.niftyindices.com/IndexConstituent/ind_niftysmallcap250list.csv"
UNIVERSE_CSV = RAW_DIR / "company_universe.csv"


def download_universe() -> Path:
    """Download the Nifty Smallcap 250 constituent list if not already saved."""
    if UNIVERSE_CSV.exists():
        print(f"Universe file already exists at {UNIVERSE_CSV}")
        return UNIVERSE_CSV

    headers = {"User-Agent": "Mozilla/5.0"}  # NSE blocks requests with no user-agent
    resp = requests.get(UNIVERSE_URL, headers=headers, timeout=15)
    resp.raise_for_status()
    UNIVERSE_CSV.write_bytes(resp.content)
    print(f"Downloaded universe list to {UNIVERSE_CSV}")
    return UNIVERSE_CSV


def load_company_universe(path: Path) -> list[str]:
    """Load NSE symbols from the CSV and append .NS suffix for yfinance."""
    df = pd.read_csv(path)
    symbol_col = "Symbol" if "Symbol" in df.columns else df.columns[2]  # fallback
    symbols = df[symbol_col].astype(str).str.strip().tolist()
    return [f"{s}.NS" for s in symbols]


def fetch_company_data(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    return {
        "financials": t.financials,
        "balance_sheet": t.balance_sheet,
        "cashflow": t.cashflow,
        "history": t.history(period="7y"),
    }


def save_company_data(ticker: str, data: dict) -> None:
    company_dir = RAW_DIR / ticker.replace(".", "_")
    company_dir.mkdir(parents=True, exist_ok=True)
    for name, df in data.items():
        if df is not None and not df.empty:
            df.to_csv(company_dir / f"{name}.csv")


def main():
    universe_path = download_universe()
    tickers = load_company_universe(universe_path)
    print(f"Loaded {len(tickers)} companies.\n")

    issues = []
    for i, ticker in enumerate(tickers, 1):
        try:
            data = fetch_company_data(ticker)
            save_company_data(ticker, data)
            print(f"[{i}/{len(tickers)}] OK   {ticker}")
        except Exception as e:
            issues.append({"ticker": ticker, "error": str(e)})
            print(f"[{i}/{len(tickers)}] FAIL {ticker}: {e}")
        time.sleep(0.5)  # be polite to yfinance's servers, avoid rate limiting

    if issues:
        issues_path = RAW_DIR / "data_quality_issues.csv"
        pd.DataFrame(issues).to_csv(issues_path, index=False)
        print(f"\n{len(issues)} companies had issues — logged to {issues_path}")

    print(f"\nDone. {len(tickers) - len(issues)}/{len(tickers)} companies pulled successfully.")


if __name__ == "__main__":
    main()
