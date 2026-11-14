"""Download statements and prices for any NSE constituent CSV (column 'Symbol'). Resumable, skips companies already downloaded."""
import sys, time
import pandas as pd
import yfinance as yf
from config import RAW

def main(csv_path):
    df = pd.read_csv(csv_path)
    col = next(c for c in df.columns if c.strip().lower() == "symbol")
    todo = []
    for s in df[col].astype(str).str.strip():
        t = f"{s}.NS"
        if not (RAW / t.replace(".", "_") / "balance_sheet.csv").exists():
            todo.append(t)
    print("New companies to download:", len(todo))
    for i, t in enumerate(todo, 1):
        folder = RAW / t.replace(".", "_")
        try:
            tk = yf.Ticker(t)
            data = {"financials": tk.financials, "balance_sheet": tk.balance_sheet,
                    "cashflow": tk.cashflow, "history": tk.history(period="max")}
            folder.mkdir(parents=True, exist_ok=True)
            saved = 0
            for name, d in data.items():
                if d is not None and not d.empty:
                    d.to_csv(folder / f"{name}.csv"); saved += 1
            print(("OK   " if saved == 4 else f"PART {saved}/4 ") + t)
        except Exception as e:
            print("FAIL", t, e)
        time.sleep(0.5)
        if i % 25 == 0:
            print(f"  {i}/{len(todo)}")

if __name__ == "__main__":
    main(sys.argv[1])
