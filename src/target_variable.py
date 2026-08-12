"""
Phase 3 — Define the Target Variable

Computes 12-month forward returns per company-year (calendar-date based,
not trading-day count) and labels each as outperform/underperform vs.
a benchmark index (e.g. Nifty 500).

Output: data/processed/labels.csv with columns
    ticker, fiscal_year_end, forward_return, benchmark_return, outperformed (0/1)
"""

import pandas as pd


def forward_return(price_series: pd.Series, start_date, months: int = 12) -> float:
    """Calendar-date based forward return, robust to holidays/market closures."""
    end_date = start_date + pd.DateOffset(months=months)
    start_price = price_series.asof(start_date)
    end_price = price_series.asof(end_date)
    if start_price is None or end_price is None or start_price == 0:
        return None
    return (end_price - start_price) / start_price


def label_outperformance(company_return: float, benchmark_return: float) -> int:
    if company_return is None or benchmark_return is None:
        return None
    return int(company_return > benchmark_return)


if __name__ == "__main__":
    # TODO: loop over processed price data + fscore_signals.csv,
    # compute forward_return per company-year, compare to Nifty 500 benchmark,
    # write data/processed/labels.csv
    pass
