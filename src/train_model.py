"""
Phase 5 — Train the ML Model

Compares the traditional equal-weighted F-Score (baseline) against an
XGBoost classifier trained on the same 9 signals as separate features
(challenger), using a time-based train/test split.

Metrics: AUC-ROC, precision, recall.
"""

import pandas as pd
from sklearn.metrics import roc_auc_score, precision_score, recall_score
from xgboost import XGBClassifier

SIGNAL_COLS = [
    "positive_roa", "positive_cfo", "delta_roa", "cfo_exceeds_ni",
    "delta_leverage", "delta_current_ratio", "no_new_shares",
    "delta_gross_margin", "delta_asset_turnover",
]


def time_based_split(df: pd.DataFrame, split_year: int):
    train = df[df["fiscal_year"] < split_year]
    test = df[df["fiscal_year"] >= split_year]
    return train, test


def evaluate_baseline(df: pd.DataFrame) -> dict:
    """Baseline: plain summed F-Score (0-9) as the prediction score."""
    y_true = df["outperformed"]
    y_score = df[SIGNAL_COLS].sum(axis=1)
    return {
        "auc": roc_auc_score(y_true, y_score),
    }


def train_xgboost(train_df: pd.DataFrame, test_df: pd.DataFrame) -> dict:
    X_train, y_train = train_df[SIGNAL_COLS], train_df["outperformed"]
    X_test, y_test = test_df[SIGNAL_COLS], test_df["outperformed"]

    model = XGBClassifier(
        n_estimators=200, max_depth=3, learning_rate=0.05,
        eval_metric="auc", scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    return {
        "model": model,
        "auc": roc_auc_score(y_test, y_prob),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
    }


if __name__ == "__main__":
    # TODO: load data/processed/labels.csv merged with fscore_signals.csv,
    # run time_based_split, evaluate_baseline, train_xgboost, print comparison
    pass
