"""
Phase 5 — Train the ML Model

Compares the traditional equal-weighted F-Score (baseline) against an
XGBoost classifier trained on the same 9 signals as separate features
(challenger), using a time-based train/test split (never random shuffle,
since financial data is sequential).

Metrics: AUC-ROC, precision, recall — not just accuracy, since the
classes are imbalanced (~61/39).

Usage:
    python src/train_model.py                                  # main dataset
    python src/train_model.py data/processed/training_dataset_pre_sebi2023.csv
    python src/train_model.py data/processed/training_dataset_post_sebi2023.csv
"""

import sys
import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score, precision_score, recall_score
from xgboost import XGBClassifier

PROCESSED_DIR = Path("data/processed")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

SIGNAL_COLS = [
    "positive_roa", "positive_cfo", "delta_roa", "cfo_exceeds_ni",
    "delta_leverage", "delta_current_ratio", "no_new_shares",
    "delta_gross_margin", "delta_asset_turnover",
]


def load_clean_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["fiscal_year_end"] = pd.to_datetime(df["fiscal_year_end"])
    # drop rows missing the label or any of the 9 signals — can't train/evaluate on these
    df = df.dropna(subset=["outperformed"] + SIGNAL_COLS)
    df["outperformed"] = df["outperformed"].astype(int)
    return df.sort_values("fiscal_year_end")


def time_based_split(df: pd.DataFrame, test_fraction: float = 0.2):
    """Split chronologically — train on the earlier period, test on the most recent."""
    cutoff_idx = int(len(df) * (1 - test_fraction))
    train = df.iloc[:cutoff_idx]
    test = df.iloc[cutoff_idx:]
    return train, test


def evaluate_baseline(test_df: pd.DataFrame) -> dict:
    """Baseline: plain summed F-Score (0-9) used directly as the prediction score."""
    y_true = test_df["outperformed"]
    y_score = test_df[SIGNAL_COLS].sum(axis=1)
    if y_true.nunique() < 2:
        return {"auc": None}
    return {"auc": roc_auc_score(y_true, y_score)}


def train_xgboost(train_df: pd.DataFrame, test_df: pd.DataFrame):
    X_train, y_train = train_df[SIGNAL_COLS], train_df["outperformed"]
    X_test, y_test = test_df[SIGNAL_COLS], test_df["outperformed"]

    pos = (y_train == 1).sum()
    neg = (y_train == 0).sum()
    scale_pos_weight = neg / pos if pos > 0 else 1.0

    model = XGBClassifier(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.05,
        eval_metric="auc",
        scale_pos_weight=scale_pos_weight,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {"auc": None, "precision": None, "recall": None}
    if y_test.nunique() >= 2:
        metrics["auc"] = roc_auc_score(y_test, y_prob)
    metrics["precision"] = precision_score(y_test, y_pred, zero_division=0)
    metrics["recall"] = recall_score(y_test, y_pred, zero_division=0)

    return model, metrics


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PROCESSED_DIR / "training_dataset.csv"
    if not input_path.exists():
        print(f"ERROR: {input_path} not found.")
        return

    print(f"Loading {input_path}...")
    df = load_clean_data(input_path)
    print(f"{len(df)} clean, labeled rows available.\n")

    train_df, test_df = time_based_split(df)
    print(f"Train: {len(train_df)} rows ({train_df['fiscal_year_end'].min().date()} to "
          f"{train_df['fiscal_year_end'].max().date()})")
    print(f"Test:  {len(test_df)} rows ({test_df['fiscal_year_end'].min().date()} to "
          f"{test_df['fiscal_year_end'].max().date()})\n")

    if len(test_df) < 5 or test_df["outperformed"].nunique() < 2:
        print("WARNING: test set is too small or single-class — results below are unreliable. "
              "This can happen on the smaller PRE-SEBI-2023 split.")

    baseline = evaluate_baseline(test_df)
    model, xgb_metrics = train_xgboost(train_df, test_df)

    print("=== RESULTS ===")
    print(f"Baseline (plain F-Score)  — AUC: {fmt(baseline['auc'])}")
    print(f"XGBoost (ML model)        — AUC: {fmt(xgb_metrics['auc'])}  "
          f"Precision: {fmt(xgb_metrics['precision'])}  Recall: {fmt(xgb_metrics['recall'])}")

    if baseline["auc"] is not None and xgb_metrics["auc"] is not None:
        diff = xgb_metrics["auc"] - baseline["auc"]
        winner = "XGBoost" if diff > 0 else "Baseline F-Score"
        print(f"\n{winner} performed better by {abs(diff):.3f} AUC points.")

    # Save the model and predictions for Phase 6 (SHAP)
    suffix = input_path.stem.replace("training_dataset", "").strip("_") or "main"
    model_path = MODEL_DIR / f"xgboost_{suffix}.joblib"
    joblib.dump(model, model_path)
    test_df.assign(
        xgb_predicted_prob=model.predict_proba(test_df[SIGNAL_COLS])[:, 1]
    ).to_csv(PROCESSED_DIR / f"test_predictions_{suffix}.csv", index=False)

    print(f"\nModel saved to {model_path}")
    print(f"Test predictions saved to data/processed/test_predictions_{suffix}.csv")


def fmt(x):
    return f"{x:.3f}" if x is not None else "N/A"


if __name__ == "__main__":
    main()
