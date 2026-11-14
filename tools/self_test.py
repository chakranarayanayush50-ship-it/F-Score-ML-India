"""Self-test: builds FAKE data shaped like your yfinance files and runs the whole pipeline on it.
It never touches your real data. If this finishes without errors, the code itself works.
(The fake data has a small planted effect, so the models should find AUC a bit above 0.5.)

Run:  python tools/self_test.py
"""
import os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent.parent
tmp = Path(tempfile.mkdtemp(prefix="fscore_selftest_"))
raw = tmp / "data" / "raw"
(raw / "benchmarks").mkdir(parents=True)
rng = np.random.default_rng(1)
N = 140
days = pd.bdate_range("2019-11-01", "2026-11-05")


def walk(drift_by_day, sigma=0.018):
    r = rng.normal(0, sigma, len(days)) + drift_by_day
    return 100 * np.exp(np.cumsum(r))


def hist_csv(path, close):
    df = pd.DataFrame({"Open": close, "High": close, "Low": close, "Close": close, "Volume": 1000}, index=days)
    df.index = [f"{d:%Y-%m-%d} 00:00:00+05:30" for d in days]
    df.to_csv(path)


hist_csv(raw / "benchmarks" / "nifty50.csv", walk(np.full(len(days), 0.0003), 0.008))
sectors = []
for i in range(N):
    tk = f"T{i:03d}"
    fin = i % 9 == 0
    sectors.append((f"{tk}.NS", "Financial Services" if fin else "Industrials", "x"))
    march = not (i % 17 == 0)
    ends = pd.to_datetime([f"{y}-{'03' if march else '12'}-{'31'}" for y in range(2021 if i % 5 else 2022, 2027)])
    gm = np.clip(0.3 + np.cumsum(rng.normal(0, 0.03, len(ends))), 0.05, 0.9)
    rev = 1000 * np.cumprod(1 + rng.normal(0.08, 0.1, len(ends)))
    ta = 2000 * np.cumprod(1 + rng.normal(0.07, 0.08, len(ends)))
    ni = rev * rng.normal(0.06, 0.04, len(ends))
    fin_df = pd.DataFrame({"Net Income": ni, "Total Revenue": rev, "Cost Of Revenue": rev * (1 - gm)}, index=ends).T
    if i % 2 == 0:
        fin_df.loc["Gross Profit"] = rev * gm
    bs = pd.DataFrame({"Total Assets": ta, "Current Assets": ta * rng.uniform(0.3, 0.5, len(ends)),
                       "Current Liabilities": ta * rng.uniform(0.2, 0.4, len(ends)),
                       "Ordinary Shares Number": 1e6 * np.cumprod(1 + np.abs(rng.normal(0, 0.01, len(ends)))),
                       "Long Term Debt": ta * rng.uniform(0.0, 0.3, len(ends))}, index=ends).T
    if i % 4 == 0:
        bs = bs.drop("Long Term Debt")
    cf = pd.DataFrame({"Operating Cash Flow": ni * rng.normal(1.1, 0.5, len(ends))}, index=ends).T
    # planted effect: price drifts up in the 12 months after results if gross margin improved
    drift = np.zeros(len(days))
    for k in range(1, len(ends)):
        start = ends[k] + pd.DateOffset(months=3)
        end = start + pd.DateOffset(months=12)
        mask = (days >= start) & (days < end)
        drift[mask] = 0.0005 if gm[k] > gm[k - 1] else -0.0005
    d = raw / f"{tk}_NS"; d.mkdir()
    for name, df in [("financials", fin_df), ("balance_sheet", bs), ("cashflow", cf)]:
        df.columns = [c.strftime("%Y-%m-%d") for c in df.columns]
        df.to_csv(d / f"{name}.csv")
    hist_csv(d / "history.csv", walk(drift))
pd.DataFrame(sectors, columns=["ticker", "sector", "industry"]).to_csv(raw / "sectors.csv", index=False)

env = dict(os.environ, FSCORE_ROOT=str(tmp), N_BOOT="200", N_PERM="200")
for script in ["build_signals", "build_labels", "build_dataset", "evaluate", "shap_stability", "grouped_cv"]:
    print(f"\n######## {script} ########")
    r = subprocess.run([sys.executable, str(HERE / "src" / f"{script}.py")], env=env)
    if r.returncode != 0:
        sys.exit(f"SELF-TEST FAILED in {script}")
print("\nSELF-TEST PASSED. Fake data lived in:", tmp)
