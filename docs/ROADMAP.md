# Execution Roadmap

Full plan: zero to a published, defensible research paper. ~8–10 weeks.

## Phase 1 — Data Collection
- Define company universe: Nifty Smallcap 250 / Midcap 150 constituent list
- Pull 5–7 years of financial statements (income statement, balance sheet, cash flow)
- Pull matching price history
- Log data quality issues (missing years, delisted companies) as you go
- **Tools:** yfinance, jugaad-data

## Phase 2 — Compute the 9 F-Score Signals
Per company-year, compute 9 binary (0/1) signals across three categories:

**Profitability**
1. ROA > 0
2. CFO > 0
3. ΔROA > 0
4. CFO > Net Income

**Leverage & Liquidity**
5. ΔLeverage < 0
6. ΔCurrent Ratio > 0
7. No new shares issued

**Operating Efficiency**
8. ΔGross Margin > 0
9. ΔAsset Turnover > 0

Sum all 9 → traditional F-Score (0–9). These same 9 columns become ML input features.

## Phase 3 — Define the Target Variable
- 12-month forward stock return (calendar-date based, not trading-day count)
- Benchmark: Nifty 500 or relevant sector index
- Recommended: binary classification — "outperformed benchmark" (1) vs. not (0)

## Phase 4 — India-Specific Robustness
- Holidays: handled automatically since data only contains real trading days
- SEBI policy changes: split sample into sub-periods around a known major reform;
  test whether results hold in both halves
- Document this as both a robustness check (Methodology) and a limitation (Discussion)

## Phase 5 — Train the ML Model
- Time-based train/test split (never random shuffle)
- Handle class imbalance (class weighting / SMOTE if needed)
- Baseline: plain summed F-Score
- Challenger: XGBoost trained on the 9 signals as separate features
- Metrics: AUC-ROC, precision, recall (not just accuracy)

## Phase 6 — SHAP Explainability
- Fit `TreeExplainer` on the trained XGBoost model
- Compute global feature importance across all 9 signals
- Compare SHAP ranking to Piotroski's equal-weight assumption
- Generate SHAP summary plot for the paper's Results section

## Phase 7 — Write the Paper
Standard structure, written in Overleaf (LaTeX):
Abstract → Introduction → Related Work → Data & Methodology → Results →
Discussion & Limitations → Conclusion → References

## Phase 8 — Publish
1. SSRN first — free, no barrier, immediate public timestamp
2. GitHub — clean, documented code (this repo)
3. Submit to 2–3 free undergraduate research journals
4. arXiv — once endorsement is available

**Before finalizing:** re-run the literature search once more to confirm no one
has published this exact combination since work began.
