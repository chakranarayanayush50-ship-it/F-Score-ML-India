"""
Phase 2 — Compute the 9 Piotroski F-Score Signals

Turns raw financial statements (data/raw/) into 9 binary (0/1) columns
per company-year, saved to data/processed/fscore_signals.csv.

Signals:
    1. ROA > 0
    2. CFO > 0
    3. Delta ROA > 0
    4. CFO > Net Income
    5. Delta Leverage < 0
    6. Delta Current Ratio > 0
    7. No new shares issued
    8. Delta Gross Margin > 0
    9. Delta Asset Turnover > 0
"""

import pandas as pd

# TODO: implement each signal function once raw data shape is confirmed
# from a real Phase 1 pull (yfinance field names vary by company).


def roa(net_income: float, total_assets: float) -> float:
    return net_income / total_assets if total_assets else None


def signal_positive_roa(roa_value: float) -> int:
    return int(roa_value > 0) if roa_value is not None else 0


def signal_positive_cfo(cfo: float) -> int:
    return int(cfo > 0) if cfo is not None else 0


def signal_delta_roa(roa_t: float, roa_t1: float) -> int:
    return int(roa_t > roa_t1) if None not in (roa_t, roa_t1) else 0


def signal_cfo_exceeds_ni(cfo: float, net_income: float) -> int:
    return int(cfo > net_income) if None not in (cfo, net_income) else 0


def signal_delta_leverage(leverage_t: float, leverage_t1: float) -> int:
    return int(leverage_t < leverage_t1) if None not in (leverage_t, leverage_t1) else 0


def signal_delta_current_ratio(cr_t: float, cr_t1: float) -> int:
    return int(cr_t > cr_t1) if None not in (cr_t, cr_t1) else 0


def signal_no_new_shares(shares_t: float, shares_t1: float) -> int:
    return int(shares_t <= shares_t1) if None not in (shares_t, shares_t1) else 0


def signal_delta_gross_margin(gm_t: float, gm_t1: float) -> int:
    return int(gm_t > gm_t1) if None not in (gm_t, gm_t1) else 0


def signal_delta_asset_turnover(at_t: float, at_t1: float) -> int:
    return int(at_t > at_t1) if None not in (at_t, at_t1) else 0


def compute_fscore(signals: dict) -> int:
    """Sum all 9 binary signals into the traditional 0-9 F-Score."""
    return sum(signals.values())


if __name__ == "__main__":
    # TODO: loop over data/raw/<ticker>/ folders, compute signals per year,
    # and write a tidy DataFrame to data/processed/fscore_signals.csv
    pass
