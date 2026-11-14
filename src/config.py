"""Central settings. Change a value here, rerun the pipeline, and every number in the paper updates."""
import os
from pathlib import Path

ROOT = Path(os.environ.get("FSCORE_ROOT", Path(__file__).resolve().parent.parent))
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed_v2"      # new folder: old processed files are never overwritten
RESULTS = ROOT / "results"
PROC.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

SIGNALS = [
    "positive_roa", "positive_cfo", "delta_roa", "cfo_exceeds_ni",
    "delta_leverage", "delta_current_ratio", "no_new_shares",
    "delta_gross_margin", "delta_asset_turnover",
]

# --- return window -------------------------------------------------------
START_LAG_MONTHS = 3        # window starts 3 months after fiscal year-end (results are public by then)
HORIZON_MONTHS = 12         # 12-month forward return
MAX_PRICE_GAP_DAYS = 7      # a price older than this vs the target date is treated as missing (no stale prices)

# --- statements ----------------------------------------------------------
MIN_FY_GAP_DAYS, MAX_FY_GAP_DAYS = 330, 400   # previous statement must be ~1 year earlier
SHARES_TOLERANCE = 1.001                       # share count may rise 0.1% (rounding) and still count as "no new shares"
ASSUME_ZERO_DEBT_IF_ROW_ABSENT = True          # if a company has no long-term-debt line at all, treat debt as 0

# --- evaluation ----------------------------------------------------------
SEED = 42
N_BOOT = int(os.environ.get("N_BOOT", 2000))
N_PERM = int(os.environ.get("N_PERM", 2000))
MIN_TRAIN_ROWS = 100
LABELS = ["label_median", "label_ew", "label_nifty50"]
XGB_PARAMS = dict(n_estimators=200, max_depth=3, learning_rate=0.05,
                  eval_metric="logloss", random_state=SEED, n_jobs=1, verbosity=0)
