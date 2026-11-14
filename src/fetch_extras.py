"""Step 0 (needs internet): download each company's sector and the Nifty 50 index history.

Sector is needed to exclude banks/NBFCs/insurers (they have no current ratio or gross margin).
Safe to stop and rerun: sectors already downloaded are kept.
"""
import time
import pandas as pd
import yfinance as yf
from config import RAW


def folder_to_ticker(name: str) -> str:
    return name[:-3] + ".NS" if name.endswith("_NS") else name


def main():
    folders = sorted(p for p in RAW.iterdir()
                     if p.is_dir() and p.name != "benchmarks" and (p / "balance_sheet.csv").exists())
    print("Company folders:", len(folders))

    sec_path = RAW / "sectors.csv"
    done = {}
    if sec_path.exists():
        old = pd.read_csv(sec_path)
        done = {r.ticker: (r.sector, r.industry) for r in old.itertuples()}
    for i, f in enumerate(folders, 1):
        t = folder_to_ticker(f.name)
        if t in done and done[t][0] != "Unknown":
            continue
        try:
            info = yf.Ticker(t).info
            done[t] = (info.get("sector") or "Unknown", info.get("industry") or "Unknown")
        except Exception as e:
            print("sector failed:", t, e)
            done[t] = ("Unknown", "Unknown")
        time.sleep(0.4)
        if i % 25 == 0:
            pd.DataFrame([(k, *v) for k, v in done.items()], columns=["ticker", "sector", "industry"]).to_csv(sec_path, index=False)
            print(f"  {i}/{len(folders)}")
    out = pd.DataFrame([(k, *v) for k, v in done.items()], columns=["ticker", "sector", "industry"])
    out.to_csv(sec_path, index=False)
    print("Sectors saved:", sec_path)
    print(out["sector"].value_counts().to_string())

    (RAW / "benchmarks").mkdir(exist_ok=True)
    h = yf.Ticker("^NSEI").history(period="10y")
    h.to_csv(RAW / "benchmarks" / "nifty50.csv")
    print("Nifty 50 rows:", len(h), "| last date:", str(h.index[-1])[:10])


if __name__ == "__main__":
    main()
