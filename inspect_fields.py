"""
Quick inspection: print the actual row labels (field names) in the raw
financial data, so we can build fscore_signals.py against real field
names instead of guessing.

Run from the repo root with your venv active:
    python inspect_fields.py
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

# Pick a large, well-covered company to inspect — Tata Steel is a safe bet
SAMPLE_COMPANY = "TATASTEEL_NS"


def show_fields(company_dir: Path):
    for filename in ["financials.csv", "balance_sheet.csv", "cashflow.csv"]:
        path = company_dir / filename
        if not path.exists():
            print(f"\n=== {filename} === MISSING")
            continue
        df = pd.read_csv(path, index_col=0)
        print(f"\n=== {filename} ===")
        print(f"Columns (years): {list(df.columns)}")
        print(f"Row labels (fields):")
        for label in df.index.tolist():
            print(f"  - {label}")


if __name__ == "__main__":
    company_dir = RAW_DIR / SAMPLE_COMPANY
    if not company_dir.exists():
        # fallback: just grab the first available company folder
        candidates = [d for d in RAW_DIR.iterdir() if d.is_dir() and d.name != "__pycache__"]
        if not candidates:
            print("No company folders found in data/raw/. Did Phase 1 run correctly?")
            exit(1)
        company_dir = candidates[0]
        print(f"{SAMPLE_COMPANY} not found, using {company_dir.name} instead.\n")

    show_fields(company_dir)
