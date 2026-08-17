"""
Phase 6 — SHAP Explainability

Loads the trained XGBoost model and its test set, computes SHAP values,
and ranks the 9 F-Score signals by how much they actually drove the
model's predictions. Compares this ranking to Piotroski's original
assumption that all 9 signals are equally important.

Output:
    paper/figures/shap_summary_<suffix>.png   — visual summary plot
    data/processed/shap_importance_<suffix>.csv — ranked importance table

Usage:
    python src/shap_analysis.py                # main model
    python src/shap_analysis.py pre_sebi2023    # pre-SEBI-2023 model (if trained)
    python src/shap_analysis.py post_sebi2023   # post-SEBI-2023 model
"""

import sys
import joblib
import shap
import matplotlib
matplotlib.use("Agg")  # no display available when run from terminal
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
MODEL_DIR = Path("models")
FIGURES_DIR = Path("paper/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

SIGNAL_COLS = [
    "positive_roa", "positive_cfo", "delta_roa", "cfo_exceeds_ni",
    "delta_leverage", "delta_current_ratio", "no_new_shares",
    "delta_gross_margin", "delta_asset_turnover",
]

SIGNAL_LABELS = {
    "positive_roa": "ROA > 0",
    "positive_cfo": "CFO > 0",
    "delta_roa": "\u0394ROA > 0",
    "cfo_exceeds_ni": "CFO > Net Income",
    "delta_leverage": "\u0394Leverage < 0",
    "delta_current_ratio": "\u0394Current Ratio > 0",
    "no_new_shares": "No new shares issued",
    "delta_gross_margin": "\u0394Gross Margin > 0",
    "delta_asset_turnover": "\u0394Asset Turnover > 0",
}


def main():
    suffix = sys.argv[1] if len(sys.argv) > 1 else "main"

    model_path = MODEL_DIR / f"xgboost_{suffix}.joblib"
    preds_path = PROCESSED_DIR / f"test_predictions_{suffix}.csv"

    if not model_path.exists() or not preds_path.exists():
        print(f"ERROR: missing {model_path} or {preds_path}. Run train_model.py first "
              f"(with matching suffix: python src/train_model.py ... {suffix}).")
        return

    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)

    print(f"Loading test data from {preds_path}...")
    df = pd.read_csv(preds_path)
    X = df[SIGNAL_COLS].dropna()

    if len(X) < 3:
        print(f"ERROR: only {len(X)} usable rows — not enough to compute meaningful SHAP values.")
        return

    print(f"Computing SHAP values for {len(X)} test rows...\n")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # Global importance: mean absolute SHAP value per signal, ranked
    importance = pd.DataFrame({
        "signal": SIGNAL_COLS,
        "signal_label": [SIGNAL_LABELS[s] for s in SIGNAL_COLS],
        "mean_abs_shap": abs(shap_values).mean(axis=0),
    }).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)
    importance["rank"] = importance.index + 1
    importance["piotroski_equal_weight_rank"] = "tied (all equal)"

    print("=== SHAP Feature Importance Ranking ===")
    print(f"{'Rank':<6}{'Signal':<28}{'Mean |SHAP|':<12}")
    for _, row in importance.iterrows():
        print(f"{row['rank']:<6}{row['signal_label']:<28}{row['mean_abs_shap']:.4f}")

    print(f"\nPiotroski's original F-Score treats all 9 signals as EQUALLY important (each worth 1 point).")
    print(f"SHAP shows the model actually relies most heavily on: {importance.iloc[0]['signal_label']}")
    print(f"...and least on: {importance.iloc[-1]['signal_label']}")

    importance_path = PROCESSED_DIR / f"shap_importance_{suffix}.csv"
    importance.to_csv(importance_path, index=False)
    print(f"\nRanked importance table saved to {importance_path}")

    # Summary plot
    plt.figure()
    shap.summary_plot(
        shap_values, X,
        feature_names=[SIGNAL_LABELS[c] for c in SIGNAL_COLS],
        show=False,
    )
    plt.tight_layout()
    plot_path = FIGURES_DIR / f"shap_summary_{suffix}.png"
    plt.savefig(plot_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Summary plot saved to {plot_path}")

    # Bar plot version (often cleaner for a paper figure)
    plt.figure()
    shap.summary_plot(
        shap_values, X,
        feature_names=[SIGNAL_LABELS[c] for c in SIGNAL_COLS],
        plot_type="bar",
        show=False,
    )
    plt.tight_layout()
    bar_path = FIGURES_DIR / f"shap_bar_{suffix}.png"
    plt.savefig(bar_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Bar plot saved to {bar_path}")


if __name__ == "__main__":
    main()
