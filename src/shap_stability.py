"""Step 5: SHAP on OUT-OF-SAMPLE rows, with uncertainty on the ranking.

Trains XGBoost per fold (as in evaluate.py), explains the test rows, pools them, then resamples
companies to get a 95% interval for each signal's mean |SHAP| and how often each signal ranks first.
Outputs results/shap_importance.csv and results/shap_importance.png
"""
import numpy as np
import pandas as pd
import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from config import *
from common import load_sample, folds

LABELS_PRETTY = {
    "positive_roa": "ROA > 0", "positive_cfo": "CFO > 0", "delta_roa": "ΔROA > 0",
    "cfo_exceeds_ni": "CFO > Net income", "delta_leverage": "ΔLeverage < 0",
    "delta_current_ratio": "ΔCurrent ratio > 0", "no_new_shares": "No new shares",
    "delta_gross_margin": "ΔGross margin > 0", "delta_asset_turnover": "ΔAsset turnover > 0",
}


def main(label="label_median"):
    d = load_sample(label)
    S, T = [], []
    for c, tr, te in folds(d):
        m = XGBClassifier(**XGB_PARAMS).fit(tr[SIGNALS], tr["y"])
        sv = shap.TreeExplainer(m).shap_values(te[SIGNALS])
        S.append(np.asarray(sv)); T.append(te["ticker"].values)
    if not S:
        print("No usable fold; cannot compute out-of-sample SHAP."); return
    S, T = np.vstack(S), np.concatenate(T)
    mean_abs = np.abs(S).mean(axis=0)

    rng = np.random.default_rng(SEED)
    idx_by = {t: np.where(T == t)[0] for t in np.unique(T)}
    keys = list(idx_by)
    boots, rank1 = [], np.zeros(len(SIGNALS))
    for _ in range(N_BOOT):
        pick = rng.integers(0, len(keys), len(keys))
        ix = np.concatenate([idx_by[keys[i]] for i in pick])
        v = np.abs(S[ix]).mean(axis=0)
        boots.append(v); rank1[np.argmax(v)] += 1
    boots = np.array(boots)

    prev = d[SIGNALS].mean()
    out = pd.DataFrame({
        "signal": SIGNALS, "label": [LABELS_PRETTY[s] for s in SIGNALS],
        "mean_abs_shap": mean_abs,
        "ci_low": np.percentile(boots, 2.5, axis=0), "ci_high": np.percentile(boots, 97.5, axis=0),
        "share_ranked_first": rank1 / N_BOOT,
        "share_of_rows_signal_is_1": prev.values,
    }).sort_values("mean_abs_shap", ascending=False)
    out["rank"] = range(1, len(out) + 1)
    out.to_csv(RESULTS / "shap_importance.csv", index=False)
    print(out.round(4).to_string(index=False))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    o = out.iloc[::-1]
    ax.barh(o["label"], o["mean_abs_shap"],
            xerr=[o["mean_abs_shap"] - o["ci_low"], o["ci_high"] - o["mean_abs_shap"]], capsize=3)
    ax.set_xlabel("Mean |SHAP| (out-of-sample), 95% bootstrap interval")
    plt.tight_layout(); plt.savefig(RESULTS / "shap_importance.png", dpi=200); plt.close()
    print("\nSaved: results/shap_importance.csv, results/shap_importance.png")
    print("If the intervals overlap heavily, do NOT claim one signal is 'the most important'.")


if __name__ == "__main__":
    main()
