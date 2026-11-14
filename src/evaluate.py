"""Step 4: honest out-of-sample evaluation.

For each label definition:
  * expanding-window time split (train on earlier years, test on a later year)
  * models: plain F-Score (baseline), logistic regression, random forest, XGBoost
  * pooled out-of-sample AUC with a 95% bootstrap interval (resampling COMPANIES, so a company's
    repeated years stay together) and a permutation p-value (labels shuffled within each year)
  * paired bootstrap of AUC(model) - AUC(F-Score)
  * top-quintile minus bottom-quintile excess return (no transaction costs)
Outputs: results/metrics.csv, results/fold_auc.csv, results/oos_predictions_<label>.csv
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from config import *
from common import load_sample, folds


def make_models():
    return {
        "logit": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "rf": RandomForestClassifier(n_estimators=500, max_depth=4, min_samples_leaf=5,
                                     random_state=SEED, n_jobs=-1),
        "xgb": XGBClassifier(**XGB_PARAMS),
    }


def cluster_bootstrap(df, stat_fn, B, seed=SEED):
    rng = np.random.default_rng(seed)
    groups = {t: g.index.values for t, g in df.groupby("ticker")}
    keys = list(groups)
    out = []
    for _ in range(B):
        pick = rng.integers(0, len(keys), len(keys))
        idx = np.concatenate([groups[keys[i]] for i in pick])
        try:
            out.append(stat_fn(df.loc[idx]))
        except ValueError:
            continue
    return np.array(out)


def auc_fn(col):
    return lambda s: roc_auc_score(s["y"], s[col])


def spread_fn(col):
    def f(s):
        p = s.groupby("cohort")[col].rank(pct=True, method="average")
        top, bot = s.loc[p > 0.8, "excess"].mean(), s.loc[p <= 0.2, "excess"].mean()
        if np.isnan(top) or np.isnan(bot):
            raise ValueError
        return top - bot
    return f


def perm_p(df, col, B, seed=SEED):
    rng = np.random.default_rng(seed)
    obs = roc_auc_score(df["y"], df[col])
    cohort_idx = [g.index.values for _, g in df.groupby("cohort")]
    y0, sc, cnt = df["y"].values, df[col].values, 0
    for _ in range(B):
        y = y0.copy()
        for ix in cohort_idx:
            y[ix] = rng.permutation(y[ix])
        if roc_auc_score(y, sc) >= obs:
            cnt += 1
    return (cnt + 1) / (B + 1)


def run(label):
    d = load_sample(label)
    print(f"\n=== {label}: {len(d)} labeled rows with all nine signals, {d.ticker.nunique()} companies ===")
    preds, fold_rows = [], []
    for c, tr, te in folds(d):
        out = te[["ticker", "cohort", "y", "excess"]].copy()
        out["score_fscore"] = te["fscore"].values
        for name, m in make_models().items():
            m.fit(tr[SIGNALS], tr["y"])
            out[f"score_{name}"] = m.predict_proba(te[SIGNALS])[:, 1]
        preds.append(out)
        for col in [c_ for c_ in out.columns if c_.startswith("score_")]:
            fold_rows.append(dict(label=label, test_fy=c, model=col[6:], n_train=len(tr), n_test=len(te),
                                  auc=roc_auc_score(out["y"], out[col])))
    if not preds:
        print("No usable fold. Not enough labeled years yet.")
        return []
    P = pd.concat(preds).reset_index(drop=True)
    P.to_csv(RESULTS / f"oos_predictions_{label}.csv", index=False)
    cols = [c_ for c_ in P.columns if c_.startswith("score_")]
    rows = []
    for col in cols:
        name = col[6:]
        boots = cluster_bootstrap(P, auc_fn(col), N_BOOT)
        r = dict(label=label, model=name, test_years=",".join(map(str, sorted(P.cohort.unique()))),
                 n_test=len(P), auc=roc_auc_score(P["y"], P[col]),
                 auc_ci_low=np.percentile(boots, 2.5), auc_ci_high=np.percentile(boots, 97.5),
                 perm_p_auc_gt_0_5=perm_p(P, col, N_PERM))
        if name != "fscore":
            diffs = cluster_bootstrap(P, lambda s, c_=col: roc_auc_score(s["y"], s[c_]) - roc_auc_score(s["y"], s["score_fscore"]), N_BOOT)
            r.update(diff_vs_fscore=r["auc"] - roc_auc_score(P["y"], P["score_fscore"]),
                     diff_ci_low=np.percentile(diffs, 2.5), diff_ci_high=np.percentile(diffs, 97.5))
        if name in ("fscore", "xgb"):
            sp = cluster_bootstrap(P, spread_fn(col), N_BOOT)
            r.update(q5_minus_q1_excess=spread_fn(col)(P),
                     spread_ci_low=np.percentile(sp, 2.5), spread_ci_high=np.percentile(sp, 97.5))
        rows.append(r)
    return rows, fold_rows


def main():
    all_rows, all_folds = [], []
    for label in LABELS:
        try:
            res = run(label)
        except Exception as e:
            print(f"{label}: skipped ({e})")
            continue
        if res:
            all_rows += res[0]; all_folds += res[1]
    if not all_rows:
        print("\nNothing to report."); return
    m = pd.DataFrame(all_rows)
    m.to_csv(RESULTS / "metrics.csv", index=False)
    pd.DataFrame(all_folds).to_csv(RESULTS / "fold_auc.csv", index=False)
    show = ["label", "model", "n_test", "auc", "auc_ci_low", "auc_ci_high", "perm_p_auc_gt_0_5", "diff_vs_fscore", "diff_ci_low", "diff_ci_high"]
    print("\n" + m[[c for c in show if c in m.columns]].round(3).to_string(index=False))
    print("\nSaved: results/metrics.csv, results/fold_auc.csv")
    print("READ THIS: an AUC is only evidence of skill if its interval excludes 0.5 and the permutation p is small.")


if __name__ == "__main__":
    main()
