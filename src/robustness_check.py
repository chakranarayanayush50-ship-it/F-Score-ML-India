"""
Phase 4 — India-Specific Robustness Check

Splits the training dataset into two sub-periods around a real, documented
SEBI regulatory change: the LODR (Second Amendment) Regulations, 2023,
which tightened listed-company disclosure requirements (notified 14 June
2023, shortened disclosure timeline effective 14 July 2023).

This lets us later check (in Phase 5) whether the model's results are
stable across a genuine regulatory shift, rather than being an artifact
of one specific disclosure regime.

Output:
    data/processed/training_dataset_pre_sebi2023.csv
    data/processed/training_dataset_post_sebi2023.csv

Run from the repo root with your venv active:
    python src/robustness_check.py
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
SEBI_CUTOFF = pd.Timestamp("2023-07-14")  # LODR Second Amendment effective date


def main():
    path = PROCESSED_DIR / "training_dataset.csv"
    if not path.exists():
        print(f"ERROR: {path} not found. Run Phase 3 (target_variable.py) first.")
        return

    df = pd.read_csv(path)
    df["fiscal_year_end"] = pd.to_datetime(df["fiscal_year_end"])

    pre = df[df["fiscal_year_end"] < SEBI_CUTOFF].copy()
    post = df[df["fiscal_year_end"] >= SEBI_CUTOFF].copy()

    pre_path = PROCESSED_DIR / "training_dataset_pre_sebi2023.csv"
    post_path = PROCESSED_DIR / "training_dataset_post_sebi2023.csv"
    pre.to_csv(pre_path, index=False)
    post.to_csv(post_path, index=False)

    def summarize(name, d):
        valid = d.dropna(subset=["outperformed"])
        print(f"\n=== {name} (before {SEBI_CUTOFF.date()}: {name == 'PRE'}) ===")
        print(f"Rows: {len(d)}  |  Valid labels: {len(valid)}")
        if len(valid) > 0:
            print(f"Class balance — outperformed: {valid['outperformed'].mean():.1%}")
        if "fscore" in d.columns:
            print(f"Mean F-Score: {d['fscore'].mean():.2f}  |  Std: {d['fscore'].std():.2f}")

    summarize("PRE", pre)
    summarize("POST", post)

    print(f"\nSaved:\n  {pre_path}\n  {post_path}")
    print("\nUse these two files in Phase 5 to train/evaluate separately and confirm "
          "the model's performance and SHAP findings hold up on both sides of the "
          "regulatory change.")


if __name__ == "__main__":
    main()
