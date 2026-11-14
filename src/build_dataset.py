"""Step 3: merge signals + returns + sectors, apply the sample rules, create the labels.

Sample rules (counts for each rule are saved to results/sample_flow.csv for the paper):
  1. fiscal year ends 31 March (the cohort is then one clean window per year)
  2. not a financial firm (banks, NBFCs, insurers...)
  3. a valid 12-month return exists
  4. all nine signals exist

Labels (each stock is compared with others in the same year, or with an index):
  label_median  = return above the median stock of that fiscal year      <- primary
  label_ew      = return above the equal-weighted average of that year
  label_nifty50 = return above the Nifty 50 over the same window
"""
import os
import sys
import numpy as np
import pandas as pd
from config import *


def main():
    sig = pd.read_csv(PROC / "signals.csv", parse_dates=["fiscal_year_end"])
    lab = pd.read_csv(PROC / "labels_raw.csv", parse_dates=["fiscal_year_end", "window_start", "window_end"])
    df = sig.merge(lab, on=["ticker", "fiscal_year_end"], how="left")

    sec_path = RAW / "sectors.csv"
    if sec_path.exists():
        sec = pd.read_csv(sec_path)[["ticker", "sector", "industry"]]
        df = df.merge(sec, on="ticker", how="left")
        df["sector"] = df["sector"].fillna("Unknown")
        print("Firms with unknown sector (kept as non-financial):", df.loc[df.sector == "Unknown", "ticker"].nunique())
    elif os.environ.get("ALLOW_NO_SECTORS") == "1":
        df["sector"], df["industry"] = "Unknown", "Unknown"
        print("WARNING: no sectors.csv; financial firms are NOT excluded.")
    else:
        sys.exit("sectors.csv not found. Run:  python src/fetch_extras.py")

    df["is_march_ye"] = (df.fiscal_year_end.dt.month == 3) & (df.fiscal_year_end.dt.day == 31)
    df["is_financial"] = df["sector"].eq("Financial Services")
    df["cohort"] = df.fiscal_year_end.dt.year
    df["has_return"] = df.forward_return.notna()

    flow = []

    def step(name, d):
        flow.append(dict(step=name, company_years=len(d), companies=d.ticker.nunique()))

    step("1. All company-years with statements", df)
    d = df[df.is_march_ye]; step("2. March year-end firms", d)
    d = d[~d.is_financial]; step("3. Non-financial firms", d)
    d_ret = d[d.has_return]; step("4. With a valid 12-month return window", d_ret)
    d_fin = d_ret[d_ret.all_signals]; step("5. With all nine signals (analysis sample)", d_fin)
    pd.DataFrame(flow).to_csv(RESULTS / "sample_flow.csv", index=False)
    print("\nSAMPLE FLOW"); print(pd.DataFrame(flow).to_string(index=False))

    # benchmarks per cohort, computed on all non-financial March firms with a valid return
    grp = d_ret.groupby("cohort")["forward_return"]
    df["bench_median"] = df["cohort"].map(grp.median())
    df["bench_ew"] = df["cohort"].map(grp.mean())
    df["bench_nifty50"] = df["benchmark_return"]
    ok = df.has_return & df.is_march_ye & ~df.is_financial
    for lbl, b in [("label_median", "bench_median"), ("label_ew", "bench_ew"), ("label_nifty50", "bench_nifty50")]:
        df[lbl] = np.where(ok & df[b].notna(), (df.forward_return > df[b]).astype(float), np.nan)
    df["eligible"] = ok & df.all_signals
    df.to_csv(PROC / "model_dataset.csv", index=False)

    e = df[df.eligible]
    print("\nANALYSIS SAMPLE BY FISCAL YEAR")
    t = e.groupby("cohort").agg(rows=("ticker", "size"), companies=("ticker", "nunique"),
                                outperform_rate_median=("label_median", "mean"),
                                outperform_rate_nifty=("label_nifty50", "mean")).round(3)
    print(t.to_string())
    t.to_csv(RESULTS / "sample_by_year.csv")
    print("\nSaved:", PROC / "model_dataset.csv")


if __name__ == "__main__":
    main()
