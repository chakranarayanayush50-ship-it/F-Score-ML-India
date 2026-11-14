"""Step 1: raw statements -> the nine Piotroski signals per company-year.

Rules (all documented in README):
 * a signal is NaN (missing), never silently 0, when its inputs are missing
 * change signals need the previous statement to be ~1 year earlier
 * F-Score is computed ONLY when all nine signals exist (otherwise NaN)
 * ROA and asset turnover use end-of-year total assets (history is too short for beginning-of-year assets)
"""
import numpy as np
import pandas as pd
from config import *

ITEM_MAP = {
    "net_income": ("fin", ["Net Income", "Net Income Common Stockholders",
                           "Net Income From Continuing Operation Net Minority Interest"]),
    "revenue": ("fin", ["Total Revenue", "Operating Revenue"]),
    "gross_profit": ("fin", ["Gross Profit"]),
    "cost_of_revenue": ("fin", ["Cost Of Revenue", "Reconciled Cost Of Revenue"]),
    "total_assets": ("bs", ["Total Assets"]),
    "current_assets": ("bs", ["Current Assets", "Total Current Assets"]),
    "current_liabilities": ("bs", ["Current Liabilities", "Total Current Liabilities"]),
    "long_term_debt": ("bs", ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"]),
    "shares": ("bs", ["Ordinary Shares Number", "Share Issued"]),
    "cfo": ("cf", ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities",
                   "Total Cash From Operating Activities"]),
}


def folder_to_ticker(name):
    return name[:-3] + ".NS" if name.endswith("_NS") else name


def read_statement(path):
    if not path.exists():
        return None
    df = pd.read_csv(path, index_col=0)
    if df.empty:
        return None
    df.columns = pd.to_datetime(df.columns, errors="coerce")
    df = df.loc[:, ~df.columns.isna()]
    df.index = df.index.astype(str).str.strip()
    df = df[~df.index.duplicated(keep="first")]
    return df.apply(pd.to_numeric, errors="coerce")


def pull(df, names):
    if df is None:
        return None
    for n in names:
        if n in df.index and df.loc[n].notna().any():
            return df.loc[n]
    return None


def extract(folder):
    src = {"fin": read_statement(folder / "financials.csv"),
           "bs": read_statement(folder / "balance_sheet.csv"),
           "cf": read_statement(folder / "cashflow.csv")}
    cols = {}
    for item, (kind, names) in ITEM_MAP.items():
        s = pull(src[kind], names)
        if s is not None:
            cols[item] = s
    if not cols:
        return None, False
    d = pd.DataFrame(cols).sort_index()
    d = d[~d.index.duplicated(keep="first")]
    ltd_assumed = False
    if (ASSUME_ZERO_DEBT_IF_ROW_ABSENT and "long_term_debt" not in d.columns
            and "total_assets" in d.columns and src["bs"] is not None):
        d["long_term_debt"] = 0.0
        ltd_assumed = True
    return d, ltd_assumed


def ratios(row):
    g = (lambda k: row[k] if (row is not None and k in row.index) else np.nan)
    ni, ta, rev = g("net_income"), g("total_assets"), g("revenue")
    cfo, ca, cl = g("cfo"), g("current_assets"), g("current_liabilities")
    ltd, sh = g("long_term_debt"), g("shares")
    gp = g("gross_profit")
    if pd.isna(gp) and not pd.isna(rev) and not pd.isna(g("cost_of_revenue")):
        gp = rev - g("cost_of_revenue")
    return dict(
        ni=ni, cfo=cfo, sh=sh,
        roa=ni / ta if ta > 0 else np.nan,
        cr=ca / cl if cl > 0 else np.nan,
        lev=ltd / ta if ta > 0 else np.nan,
        gm=gp / rev if rev > 0 else np.nan,
        at=rev / ta if (ta > 0 and rev > 0) else np.nan,
    )


def sig(f, *vals):
    if any(pd.isna(v) for v in vals):
        return np.nan
    return float(f(*vals))


def main():
    folders = sorted(p for p in RAW.iterdir()
                     if p.is_dir() and p.name != "benchmarks" and (p / "balance_sheet.csv").exists())
    rows, skipped = [], 0
    for f in folders:
        d, ltd_assumed = extract(f)
        if d is None:
            skipped += 1
            continue
        dates = list(d.index)
        for i, dt in enumerate(dates):
            cur = ratios(d.loc[dt])
            prev = None
            if i > 0 and MIN_FY_GAP_DAYS <= (dt - dates[i - 1]).days <= MAX_FY_GAP_DAYS:
                prev = ratios(d.loc[dates[i - 1]])
            p = prev if prev is not None else {k: np.nan for k in cur}
            s = {
                "positive_roa": sig(lambda x: x > 0, cur["roa"]),
                "positive_cfo": sig(lambda x: x > 0, cur["cfo"]),
                "delta_roa": sig(lambda a, b: a > b, cur["roa"], p["roa"]),
                "cfo_exceeds_ni": sig(lambda a, b: a > b, cur["cfo"], cur["ni"]),
                "delta_leverage": sig(lambda a, b: a < b, cur["lev"], p["lev"]),
                "delta_current_ratio": sig(lambda a, b: a > b, cur["cr"], p["cr"]),
                "no_new_shares": sig(lambda a, b: a <= b * SHARES_TOLERANCE, cur["sh"], p["sh"]),
                "delta_gross_margin": sig(lambda a, b: a > b, cur["gm"], p["gm"]),
                "delta_asset_turnover": sig(lambda a, b: a > b, cur["at"], p["at"]),
            }
            vals = [s[k] for k in SIGNALS]
            n_ok = sum(0 if pd.isna(v) else 1 for v in vals)
            rows.append(dict(ticker=folder_to_ticker(f.name), fiscal_year_end=dt, **s,
                             n_signals=n_ok, all_signals=(n_ok == 9),
                             fscore=(sum(vals) if n_ok == 9 else np.nan),
                             ltd_assumed_zero=ltd_assumed))
    out = pd.DataFrame(rows)
    out.to_csv(PROC / "signals.csv", index=False)
    avail = out[SIGNALS].notna().mean().round(3).rename("share_available").to_frame()
    avail.to_csv(PROC / "signal_availability.csv")
    print("Companies with statements:", out.ticker.nunique(), "| skipped folders:", skipped)
    print("Company-years:", len(out), "| with all 9 signals:", int(out.all_signals.sum()))
    print("Debt assumed zero (no debt line) in company-years:", int(out.ltd_assumed_zero.sum()))
    print("\nShare of company-years where each signal is available:")
    print(avail.to_string())


if __name__ == "__main__":
    main()
