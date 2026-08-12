"""
Phase 2 — Compute the 9 Piotroski F-Score Signals

Reads raw financials/balance_sheet/cashflow CSVs from data/raw/<ticker>/,
computes the 9 binary F-Score signals per company-year, and writes a tidy
dataset to data/processed/fscore_signals.csv.

Run from the repo root with your venv active:
    python src/fscore_signals.py
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Each metric has several possible yfinance field-name variants.
# We try them in order and use the first one that exists.
FIELD_CANDIDATES = {
    "net_income": ["Net Income", "Net Income Common Stockholders",
                   "Net Income From Continuing Operations"],
    "total_revenue": ["Total Revenue", "Operating Revenue"],
    "gross_profit": ["Gross Profit"],
    "total_assets": ["Total Assets"],
    "current_assets": ["Current Assets", "Total Current Assets"],
    "current_liabilities": ["Current Liabilities", "Total Current Liabilities"],
    "long_term_debt": ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"],
    "total_debt": ["Total Debt"],
    "shares_outstanding": ["Ordinary Shares Number", "Share Issued",
                            "Common Stock Shares Outstanding"],
    "operating_cash_flow": ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"],
}


def get_field(df: pd.DataFrame, metric: str) -> pd.Series | None:
    """Find the first matching row label for a metric, return it as a Series (years as index)."""
    if df is None or df.empty:
        return None
    for candidate in FIELD_CANDIDATES[metric]:
        if candidate in df.index:
            return df.loc[candidate]
    return None


def load_company_statements(company_dir: Path) -> dict:
    statements = {}
    for name in ["financials", "balance_sheet", "cashflow"]:
        path = company_dir / f"{name}.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            df.columns = pd.to_datetime(df.columns, errors="coerce")
            statements[name] = df
        else:
            statements[name] = None
    return statements


def compute_signals_for_company(ticker: str, company_dir: Path) -> list[dict]:
    stmts = load_company_statements(company_dir)
    fin, bs, cf = stmts["financials"], stmts["balance_sheet"], stmts["cashflow"]

    net_income = get_field(fin, "net_income")
    revenue = get_field(fin, "total_revenue")
    gross_profit = get_field(fin, "gross_profit")
    total_assets = get_field(bs, "total_assets")
    current_assets = get_field(bs, "current_assets")
    current_liabilities = get_field(bs, "current_liabilities")
    long_term_debt = get_field(bs, "long_term_debt")
    if long_term_debt is None:
        long_term_debt = get_field(bs, "total_debt")
    shares = get_field(bs, "shares_outstanding")
    cfo = get_field(cf, "operating_cash_flow")

    if net_income is None or total_assets is None:
        return []  # can't compute anything meaningful without these two

    # Sort years oldest -> newest so we can compute year-over-year deltas
    years = sorted(net_income.index.dropna())
    rows = []

    for i in range(1, len(years)):  # start at 1 so we always have a prior year for deltas
        y, y_prev = years[i], years[i - 1]

        def safe(series, year):
            if series is None or year not in series.index:
                return None
            val = series[year]
            return float(val) if pd.notna(val) else None

        ni_t, ni_t1 = safe(net_income, y), safe(net_income, y_prev)
        ta_t, ta_t1 = safe(total_assets, y), safe(total_assets, y_prev)
        rev_t, rev_t1 = safe(revenue, y), safe(revenue, y_prev)
        gp_t, gp_t1 = safe(gross_profit, y), safe(gross_profit, y_prev)
        ca_t, ca_t1 = safe(current_assets, y), safe(current_assets, y_prev)
        cl_t, cl_t1 = safe(current_liabilities, y), safe(current_liabilities, y_prev)
        ltd_t, ltd_t1 = safe(long_term_debt, y), safe(long_term_debt, y_prev)
        shares_t, shares_t1 = safe(shares, y), safe(shares, y_prev)
        cfo_t = safe(cfo, y)

        roa_t = ni_t / ta_t if ni_t is not None and ta_t else None
        roa_t1 = ni_t1 / ta_t1 if ni_t1 is not None and ta_t1 else None
        margin_t = gp_t / rev_t if gp_t is not None and rev_t else None
        margin_t1 = gp_t1 / rev_t1 if gp_t1 is not None and rev_t1 else None
        turnover_t = rev_t / ta_t if rev_t is not None and ta_t else None
        turnover_t1 = rev_t1 / ta_t1 if rev_t1 is not None and ta_t1 else None
        cr_t = ca_t / cl_t if ca_t is not None and cl_t else None
        cr_t1 = ca_t1 / cl_t1 if ca_t1 is not None and cl_t1 else None
        leverage_t = ltd_t / ta_t if ltd_t is not None and ta_t else None
        leverage_t1 = ltd_t1 / ta_t1 if ltd_t1 is not None and ta_t1 else None

        def gt(a, b):
            return int(a > b) if a is not None and b is not None else None

        signals = {
            "positive_roa": int(roa_t > 0) if roa_t is not None else None,
            "positive_cfo": int(cfo_t > 0) if cfo_t is not None else None,
            "delta_roa": gt(roa_t, roa_t1),
            "cfo_exceeds_ni": gt(cfo_t, ni_t),
            "delta_leverage": gt(leverage_t1, leverage_t),  # leverage DOWN is good
            "delta_current_ratio": gt(cr_t, cr_t1),
            "no_new_shares": gt(shares_t1, shares_t) if shares_t is not None and shares_t1 is not None
                              else (1 if shares_t is not None else None),
            "delta_gross_margin": gt(margin_t, margin_t1),
            "delta_asset_turnover": gt(turnover_t, turnover_t1),
        }

        rows.append({
            "ticker": ticker,
            "fiscal_year_end": y.date().isoformat(),
            **signals,
        })

    return rows


def main():
    company_dirs = [d for d in RAW_DIR.iterdir()
                     if d.is_dir() and d.name not in ("__pycache__",)]
    print(f"Processing {len(company_dirs)} companies...\n")

    all_rows = []
    skipped = []
    for i, company_dir in enumerate(company_dirs, 1):
        ticker = company_dir.name.replace("_NS", ".NS")
        rows = compute_signals_for_company(ticker, company_dir)
        if rows:
            all_rows.extend(rows)
            print(f"[{i}/{len(company_dirs)}] OK   {ticker}: {len(rows)} year(s)")
        else:
            skipped.append(ticker)
            print(f"[{i}/{len(company_dirs)}] SKIP {ticker}: insufficient data")

    result = pd.DataFrame(all_rows)
    if not result.empty:
        signal_cols = [c for c in result.columns if c not in ("ticker", "fiscal_year_end")]
        result["fscore"] = result[signal_cols].sum(axis=1, skipna=True)

    out_path = PROCESSED_DIR / "fscore_signals.csv"
    result.to_csv(out_path, index=False)

    print(f"\nDone. {len(result)} company-year rows written to {out_path}")
    print(f"{len(skipped)} companies skipped (insufficient data).")
    if skipped:
        pd.Series(skipped, name="ticker").to_csv(PROCESSED_DIR / "skipped_companies.csv", index=False)


if __name__ == "__main__":
    main()
