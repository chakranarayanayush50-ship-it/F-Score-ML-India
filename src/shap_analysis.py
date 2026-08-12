"""
Phase 6 — SHAP Explainability

Applies SHAP's TreeExplainer to the trained XGBoost model to determine
which of the 9 F-Score signals actually drive predictions, and how that
compares to Piotroski's original equal-weighting assumption.

Output: a SHAP summary plot (saved to notebooks/ or paper/figures/) and
a ranked feature-importance table for the paper's Results section.
"""

import shap
import matplotlib.pyplot as plt
import pandas as pd

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


def compute_shap_values(model, X: pd.DataFrame):
    explainer = shap.TreeExplainer(model)
    return explainer.shap_values(X)


def ranked_importance(shap_values, X: pd.DataFrame) -> pd.DataFrame:
    """Mean absolute SHAP value per signal, ranked descending."""
    importance = pd.DataFrame({
        "signal": X.columns,
        "mean_abs_shap": abs(shap_values).mean(axis=0),
    }).sort_values("mean_abs_shap", ascending=False)
    importance["signal_label"] = importance["signal"].map(SIGNAL_LABELS)
    return importance


def plot_summary(shap_values, X: pd.DataFrame, save_path: str):
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    # TODO: load trained model + test set from train_model.py,
    # compute SHAP values, save ranked_importance table and summary plot
    pass
