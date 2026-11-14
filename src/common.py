"""Shared helpers: load the analysis sample and generate time-based folds."""
import numpy as np
import pandas as pd
from config import *


def load_sample(label):
    d = pd.read_csv(PROC / "model_dataset.csv", parse_dates=["fiscal_year_end"])
    d = d[d.eligible & d[label].notna()].copy().reset_index(drop=True)
    d["y"] = d[label].astype(int)
    bench = {"label_median": "bench_median", "label_ew": "bench_ew", "label_nifty50": "bench_nifty50"}[label]
    d["excess"] = d["forward_return"] - d[bench]
    return d


def folds(d, min_train=MIN_TRAIN_ROWS, verbose=True):
    """Expanding window: train on all earlier fiscal years, test on one later year."""
    cohorts = sorted(d.cohort.unique())
    for c in cohorts[1:]:
        tr, te = d[d.cohort < c], d[d.cohort == c]
        if len(tr) < min_train or tr.y.nunique() < 2 or te.y.nunique() < 2:
            if verbose:
                print(f"  fold test FY{c}: SKIPPED (train rows {len(tr)}, need >= {min_train} and both classes)")
            continue
        yield c, tr, te
