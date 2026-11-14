# Analysis plan and research log (frozen 8 November 2026)

Project: Piotroski F-Score signals, machine learning and Indian mid- and small-cap returns.
Rule: nothing in this file is changed after results are seen. New decisions are appended to the log at the bottom, with the date.

## 1. Question
Do the nine F-Score signals, used by XGBoost, rank next-12-month outperformers better than the plain F-Score?

## 2. Primary (confirmatory) analysis. Exactly one test.
- Universe: Nifty Smallcap 250 and Nifty Midcap 150 constituents (current lists).
- Sample rules: fiscal year ends 31 March; Financial Services firms excluded; a valid 12-month return exists; all nine signals exist.
- Label: return above the median stock of the same fiscal year.
- Return window: starts 3 months after fiscal year-end, lasts 12 months; prices must exist within 7 days of both dates; windows past the last price date are excluded.
- Design: expanding window, train on earlier years, test on a later year (folds with fewer than 100 training rows are skipped and reported).
- Models: F-Score (baseline), logistic regression, random forest, XGBoost (settings in src/config.py and src/evaluate.py).
- Test: pooled out-of-sample AUC of XGBoost minus AUC of the F-Score, 95% interval from a company-level bootstrap (2,000 resamples).
- Success rule: the interval excludes 0. Otherwise the result is reported as null.

## 3. Exploratory analyses (reported in full, labelled exploratory, no selection of the best)
- Two other labels: above the equal-weighted mean; above the Nifty 50.
- Logistic regression and random forest against the F-Score.
- Top-quintile minus bottom-quintile excess return (no costs).
- SHAP importance on out-of-sample rows, with bootstrap intervals; no importance ranking is claimed if intervals overlap or the ranking changes between runs.
- Company-grouped cross-validation over all usable years (added after seeing the primary result; not a forward test).
- Multiple tests: all of the above are reported together; no single exploratory p-value is presented as a finding.

## 4. If longer history is obtained
The pipeline is rerun unchanged. The two-year analysis becomes a pilot. The primary analysis is then an expanding window with at least four test years.

## 5. Research log (what was done, in order, including changes made after seeing results)
1. Earlier pipeline (not reproducible, code not recovered): reported AUC 0.570 vs 0.495. Found to have look-ahead bias (return window started at fiscal year-end), possible stale prices, F-Score computed on missing signals, and a 72-row test set. Discarded; archived.
2. Rebuilt pipeline, Nifty Smallcap 250 only (249 companies): XGBoost AUC 0.573 [0.488, 0.661], F-Score 0.545, one test year (FY2025). Not significant.
3. Universe widened to Smallcap 250 plus Midcap 150 (392 companies) AFTER seeing result 2, to increase sample size. Result: XGBoost 0.555 [0.484, 0.629], F-Score 0.552 [0.481, 0.621], difference +0.003 [-0.105, 0.115]. Not significant. An earlier suggestive result (XGBoost vs Nifty 50 label, 0.588) did not hold.
4. Company-grouped cross-validation added AFTER seeing result 3, to reduce uncertainty. Exploratory.

## 6. Known limits (to be stated in the paper)
Two usable fiscal years (FY2024, FY2025) and one forward test year; current constituent lists (survivorship bias); free Yahoo Finance data of limited depth and quality; no transaction costs.
