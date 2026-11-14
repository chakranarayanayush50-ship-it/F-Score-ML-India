"""Step 2: 12-month forward returns, starting AFTER results are public, with no stale prices.

For each company-year:
  window start = fiscal year-end + START_LAG_MONTHS
  window end   = window start + HORIZON_MONTHS
A return is produced only if
  * the window end is on or before the last available price date (no unfinished windows), and
  * a real price exists within MAX_PRICE_GAP_DAYS before both the start and the end date.
Otherwise the return is missing and the reason is recorded.
"""
import numpy as np
import pandas as pd
from config import *


def load_prices(path):
    if not path.exists():
        return None
    h = pd.read_csv(path, index_col=0)
    if "Close" not in h.columns:
        return None
    idx = pd.to_datetime(h.index.astype(str).str[:10], errors="coerce")   # keep the local calendar date
    s = pd.Series(pd.to_numeric(h["Close"], errors="coerce").values, index=idx).dropna()
    s = s[~s.index.isna()]
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s if len(s) else None


def price_on_or_before(s, target):
    i = s.index.searchsorted(target, side="right") - 1
    if i < 0:
        return np.nan, None
    return float(s.iloc[i]), s.index[i]


def window_return(s, start, end):
    """Return (forward_return, reason). reason == 'ok' when valid."""
    if s is None:
        return np.nan, "no_history"
    if end > s.index[-1]:
        return np.nan, "window_beyond_data"
    p0, d0 = price_on_or_before(s, start)
    p1, d1 = price_on_or_before(s, end)
    if d0 is None or (start - d0).days > MAX_PRICE_GAP_DAYS or not p0 > 0:
        return np.nan, "start_price_missing"
    if d1 is None or (end - d1).days > MAX_PRICE_GAP_DAYS:
        return np.nan, "end_price_missing"
    return p1 / p0 - 1.0, "ok"


def main():
    sig = pd.read_csv(PROC / "signals.csv", parse_dates=["fiscal_year_end"])
    bench = load_prices(RAW / "benchmarks" / "nifty50.csv")
    if bench is None:
        print("WARNING: no Nifty 50 file found; label_nifty50 will be empty (run fetch_extras.py).")
    cache, rows = {}, []
    for r in sig[["ticker", "fiscal_year_end"]].itertuples(index=False):
        if r.ticker not in cache:
            cache[r.ticker] = load_prices(RAW / r.ticker.replace(".", "_") / "history.csv")
        start = r.fiscal_year_end + pd.DateOffset(months=START_LAG_MONTHS)
        end = start + pd.DateOffset(months=HORIZON_MONTHS)
        fr, why = window_return(cache[r.ticker], start, end)
        br, _ = window_return(bench, start, end) if bench is not None else (np.nan, "no_benchmark")
        rows.append(dict(ticker=r.ticker, fiscal_year_end=r.fiscal_year_end,
                         window_start=start, window_end=end,
                         forward_return=fr, benchmark_return=br, return_status=why))
    out = pd.DataFrame(rows)
    out.to_csv(PROC / "labels_raw.csv", index=False)
    print("Company-years:", len(out))
    print(out["return_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
