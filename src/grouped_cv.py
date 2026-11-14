"""Step 6 (SECONDARY, exploratory): company-grouped cross-validation over all usable years.

Why: the forward-in-time test has only one test year (about 250 rows), so its intervals are wide.
This pools both usable years and predicts every row out-of-fold, with all rows of one company kept
in the same fold (no company appears in both training and test).

Caveat to state in the paper: this is NOT a forward-in-time test (training folds can contain later
years than the test fold). Labels are relative to the same year's median, which removes year effects,
but this analysis was added after seeing the main result, so call it exploratory.

Outputs: results/grouped_cv_metrics.csv, results/grouped_cv_stability.csv
"""
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from config import *
from common import load_sample
from evaluate import make_models, cluster_bootstrap, auc_fn, spread_fn, perm_p

N_SPLITS = 5
N_STABILITY_SEEDS = 10


def fold_ids(tickers, seed, k=N_SPLITS):
    u = np.array(sorted(set(tickers)))
    np.random.default_rng(seed).shuffle(u)
    m = {t: i % k for i, t in enumerate(u)}
    return np.array([m[t] for t in tickers])


def out_of_fold(d, seed, models=None):
    fid = fold_ids(d["ticker"].values, seed)
    out = d[["ticker", "cohort", "y", "excess"]].copy()
    out["score_fscore"] = d["fscore"].values
    names = list(make_models()) if models is None else models
    for n in names:
        out[f"score_{n}"] = np.nan
    for f in range(N_SPLITS):
        te = fid == f
        for n in names:
            m = make_models()[n]
            m.fit(d.loc[~te, SIGNALS], d.loc[~te, "y"])
            out.loc[te, f"score_{n}"] = m.predict_proba(d.loc[te, SIGNALS])[:, 1]
    return out


def main():
    rows = []
    for label in LABELS:
        try:
            d = load_sample(label)
        except Exception as e:
            print(label, "skipped:", e); continue
        if d.y.nunique() < 2 or len(d) < 100:
            print(label, "skipped: not enough rows"); continue
        print(f"\n=== {label}: {len(d)} rows, {d.ticker.nunique()} companies, years {[int(x) for x in sorted(d.cohort.unique())]} ===")
        P = out_of_fold(d, SEED)
        for col in [c for c in P.columns if c.startswith("score_")]:
            name = col[6:]
            boots = cluster_bootstrap(P, auc_fn(col), N_BOOT)
            r = dict(label=label, model=name, n=len(P), auc=roc_auc_score(P["y"], P[col]),
                     auc_ci_low=np.percentile(boots, 2.5), auc_ci_high=np.percentile(boots, 97.5),
                     perm_p_auc_gt_0_5=perm_p(P, col, N_PERM))
            if name != "fscore":
                dd = cluster_bootstrap(P, lambda s, c=col: roc_auc_score(s["y"], s[c]) - roc_auc_score(s["y"], s["score_fscore"]), N_BOOT)
                r.update(diff_vs_fscore=r["auc"] - roc_auc_score(P["y"], P["score_fscore"]),
                         diff_ci_low=np.percentile(dd, 2.5), diff_ci_high=np.percentile(dd, 97.5))
            if name in ("fscore", "xgb"):
                sp = cluster_bootstrap(P, spread_fn(col), N_BOOT)
                r.update(q5_minus_q1_excess=spread_fn(col)(P),
                         spread_ci_low=np.percentile(sp, 2.5), spread_ci_high=np.percentile(sp, 97.5))
            rows.append(r)
    if not rows:
        print("Nothing to report."); return
    m = pd.DataFrame(rows)
    m.to_csv(RESULTS / "grouped_cv_metrics.csv", index=False)
    show = ["label", "model", "n", "auc", "auc_ci_low", "auc_ci_high", "perm_p_auc_gt_0_5", "diff_vs_fscore", "diff_ci_low", "diff_ci_high", "q5_minus_q1_excess"]
    print("\n" + m[[c for c in show if c in m.columns]].round(3).to_string(index=False))

    # stability: does the AUC depend on which companies land in which fold?
    d = load_sample("label_median")
    st = []
    for s in range(1, N_STABILITY_SEEDS + 1):
        P = out_of_fold(d, 1000 + s)
        st.append({"seed": s, **{c[6:]: roc_auc_score(P["y"], P[c]) for c in P.columns if c.startswith("score_")}})
    st = pd.DataFrame(st)
    st.to_csv(RESULTS / "grouped_cv_stability.csv", index=False)
    print("\nAUC across 10 random company-to-fold assignments (label_median):")
    print(st.drop(columns="seed").agg(["mean", "std", "min", "max"]).round(3).to_string())
    print("\nSaved: results/grouped_cv_metrics.csv, results/grouped_cv_stability.csv")
    print("Exploratory analysis: report it as secondary, never as the main result.")


if __name__ == "__main__":
    main()
