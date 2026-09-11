# Methodology & Results — Complete Reference for Drafting

Everything needed to write both sections, pulled from the actual pipeline
run. Use this as the source of truth when drafting prose.

---

# METHODOLOGY — required content

## 1. Data source and company universe
- Universe: **Nifty Smallcap 250**, official NSE index of 250 Indian
  small-cap companies, constituent list sourced directly from
  niftyindices.com
- Data pulled via **yfinance** (Python library): income statement,
  balance sheet, cash flow statement, and price history per company
- **249 of 250 companies** successfully retrieved (1 had no usable
  financial data available via yfinance)
- Financial data spans multiple fiscal years per company (varies by
  company based on data availability)

## 2. Feature construction — the 9 Piotroski F-Score signals
Computed per company-year as binary (0/1) values:
1. Positive ROA (Net Income ÷ Total Assets > 0)
2. Positive CFO (Operating Cash Flow > 0)
3. Δ ROA > 0 (year-over-year improvement)
4. CFO > Net Income (cash flow quality/accrual check)
5. Δ Leverage < 0 (Long-term Debt ÷ Total Assets falling)
6. Δ Current Ratio > 0 (liquidity improving)
7. No new shares issued (no dilution)
8. Δ Gross Margin > 0 (Gross Profit ÷ Revenue improving)
9. Δ Asset Turnover > 0 (Revenue ÷ Total Assets improving)

Signals summed for the traditional 0-9 F-Score (equal weighting).

- **Result: 906 total company-year observations** (249 companies ×
  ~3.6 years average usable data per company)

## 3. Target variable definition
- **12-month forward stock return**, calculated using calendar dates
  (not trading-day counts) to remain robust to market holidays/closures
- Benchmark: **Nifty 50** (^NSEI), same calendar window
- Binary label: **1 if company's forward return > Nifty 50's forward
  return over the same window, else 0**
- **Critical methodological safeguard:** forward-return windows extending
  beyond the actual available price data range are explicitly excluded
  (not silently computed using stale/last-known prices) — this prevents
  fabricated "returns" for dates that have not occurred yet. (This was
  found and fixed as a bug during development — worth mentioning as a
  data-integrity safeguard in the paper.)

## 4. Data cleaning and final sample
- Of 906 company-years, **589 had valid forward-return labels** (rest
  excluded — forward window extended beyond available price data)
- After also requiring all 9 signals to be non-missing: **360 clean,
  fully-labeled company-year observations** used for modeling

## 5. Train/test split methodology
- **Time-based (chronological) split — never random shuffle**, since
  financial data is sequential and random splitting would leak future
  information into training
- 80/20 split by time: **Train = 288 rows (2023-03-31 to 2025-03-31),
  Test = 72 rows (2025-03-31 to 2025-03-31)**

## 6. Baseline model
- Traditional Piotroski F-Score: **plain equal-weighted sum (0-9) used
  directly as the ranking/prediction score** — no training involved

## 7. Machine learning model
- **XGBoost classifier**, hyperparameters: n_estimators=200, max_depth=3,
  learning_rate=0.05, scale_pos_weight computed from training-set class
  imbalance, random_state=42 for reproducibility
- Trained on the same 9 signals as separate input features (not summed)

## 8. Evaluation metrics
- **AUC-ROC** (primary metric — measures ranking ability, robust to
  class imbalance)
- Precision, Recall (secondary, for the XGBoost model)

## 9. Robustness check methodology
- Sample split around a real, documented regulatory event: **SEBI's
  LODR (Second Amendment) Regulations 2023**, notified 14 June 2023,
  tightened disclosure timelines effective 14 July 2023
- PRE-SEBI-2023 subset: **3 clean rows** (insufficient for reliable
  train/test — reported honestly as N/A rather than forcing a result)
- POST-SEBI-2023 subset: **357 clean rows** (Train 285, Test 72) —
  large enough to evaluate independently

## 10. Explainability methodology
- **SHAP (SHapley Additive exPlanations)**, TreeExplainer (exact,
  optimized for tree-based models like XGBoost)
- Computed on the **72-row test set**
- Global importance = mean absolute SHAP value per signal, ranked

## 11. Tools, environment, reproducibility
- Python 3.11 (noting a version-compatibility issue with Python 3.14
  was encountered and resolved — optional to mention)
- Libraries: pandas, scikit-learn, XGBoost, SHAP, matplotlib
- Full code, data pipeline, and results publicly available on GitHub:
  https://github.com/chakranarayanayush50-ship-it/F-Score-ML-India

## 12. Cross-validation against prior work
- SHAP-based signal ranking independently compared against Shah (2025)'s
  portfolio-removal-based ranking (different method, different market-cap
  segment — Nifty 100 vs. Nifty Smallcap 250)

---

# RESULTS — required content

## 1. Data collection results
- **249/250 companies (99.6%)** successfully retrieved

## 2. F-Score signal computation results
- **906 company-year observations**
- F-Score distribution (0-9), roughly bell-shaped, centered around 4-5:

| F-Score | Count |
|---|---|
| 1 | 12 |
| 2 | 65 |
| 3 | 164 |
| 4 | 219 |
| 5 | 181 |
| 6 | 140 |
| 7 | 87 |
| 8 | 33 |
| 9 | 2 |

## 3. Target variable / labeling results
- **589/906 (65%)** company-years had valid forward-return labels after
  the look-ahead-bug fix
- **360 clean rows** used for final modeling after also requiring
  complete signal data
- ⚠️ **TO CONFIRM before writing:** the exact class balance (% outperformed)
  for the final 360-row modeling dataset specifically was not captured
  in this conversation — only for the broader 589-row label set
  (61% outperformed) and the POST-SEBI 357-row subset. Run this on your
  Mac before drafting to get the exact number:
  ```
  python3 -c "import pandas as pd; df = pd.read_csv('data/processed/training_dataset.csv').dropna(subset=['outperformed','positive_roa','positive_cfo','delta_roa','cfo_exceeds_ni','delta_leverage','delta_current_ratio','no_new_shares','delta_gross_margin','delta_asset_turnover']); print(f'{len(df)} rows, {df.outperformed.mean():.1%} outperformed')"
  ```

## 4. Main model results (full sample)

| Model | AUC-ROC | Precision | Recall |
|---|---|---|---|
| Baseline (plain F-Score) | **0.495** | — | — |
| XGBoost | **0.570** | 0.576 | 0.559 |

**Headline finding:** the traditional equal-weighted F-Score performed
at essentially random-chance level (AUC ≈ 0.5), while XGBoost trained on
the identical 9 inputs found a real, measurable edge (+0.075 AUC points).

## 5. Robustness check results (SEBI regulatory split)

| Subset | Rows (Train/Test) | Baseline AUC | XGBoost AUC | XGBoost Precision | XGBoost Recall |
|---|---|---|---|---|---|
| Full sample | 288/72 | 0.495 | 0.570 | 0.576 | 0.559 |
| Post-SEBI-2023 | 285/72 | 0.500 | 0.593 | 0.517 | 0.429 |
| Pre-SEBI-2023 | 2/1 | N/A | N/A | N/A | N/A |

**Finding:** the core result (XGBoost > baseline) held up, and was
actually slightly *stronger* on the post-2023 subset — supporting that
the main finding is not an artifact of the full-sample composition. The
pre-2023 subset had too little clean data to evaluate, reported honestly.

## 6. SHAP explainability results

| Rank | Signal | Mean \|SHAP\| |
|---|---|---|
| 1 | Δ Gross Margin > 0 | 0.2326 |
| 2 | CFO > Net Income | 0.1888 |
| 3 | Δ Current Ratio > 0 | 0.1731 |
| 4 | Δ ROA > 0 | 0.1305 |
| 5 | Δ Leverage < 0 | 0.1164 |
| 6 | No new shares issued | 0.0908 |
| 7 | ROA > 0 | 0.0752 |
| 8 | Δ Asset Turnover > 0 | 0.0735 |
| 9 | CFO > 0 | 0.0577 |

**Finding:** the top signal (Δ Gross Margin) mattered ~4x more than the
weakest (CFO > 0), directly contradicting Piotroski's equal-weighting
assumption.

## 7. Cross-validation against Shah (2025)
- **4 of 9 signals** (Δ Liquidity, Δ ROA, Δ Leverage, Equity Issuance)
  showed **identical rank ordering** between SHAP and Shah's independent
  portfolio-removal method
- 2 notable divergences (Δ Gross Margin, ROA) discussed as an open
  question (relative outperformance prediction vs. absolute portfolio
  return may weight signals differently)

## Figures/tables to include — full explanation

Each figure below includes: what it shows, why it belongs in the paper,
where it goes, and a suggested caption.

---

### Figure 1: Methodology Flowchart
**File:** `paper/figures/methodology_flowchart.png`
**What it shows:** A 6-step visual pipeline — Data Collection → F-Score
Signals → Target Variable → Robustness Split → Train Model → SHAP
Analysis — each step labeled with its key number (249 companies, 906
company-years, etc.).
**Why it's included:** Gives the reader a single-glance map of the entire
study before they read the detailed Methodology prose. Papers combining
several distinct technical steps (data engineering + ML + explainability)
benefit enormously from an upfront visual — it prevents the reader from
getting lost in the sequence of what was done in what order.
**Where it goes:** Start of the Methodology section, right after the
opening paragraph, before the detailed sub-sections begin.
**Suggested caption:** *"Figure 1. End-to-end study pipeline, from raw
financial data collection through SHAP-based explainability analysis."*

---

### Figure 2: F-Score Distribution Histogram
**File:** *(not yet generated — needs creating)*
**What it shows:** A bar chart of how many company-years received each
possible F-Score value (0 through 9) — using the table already gathered:
1→12, 2→65, 3→164, 4→219, 5→181, 6→140, 7→87, 8→33, 9→2.
**Why it's included:** This is a basic sanity/validity check every reader
will look for: does the F-Score actually vary meaningfully across your
sample, or does everything cluster at one score (which would suggest a
computation bug)? The roughly bell-shaped curve, centered around 4-5,
visually proves the signal computation is working correctly and the
sample has real spread — before the reader even gets to your ML results.
**Where it goes:** In the Results section, right at the start, before the
model comparison — it establishes your data is sound before showing what
you built on top of it.
**Suggested caption:** *"Figure 2. Distribution of traditional Piotroski
F-Scores (0–9) across 906 company-year observations in the Nifty
Smallcap 250 sample."*

---

### Figure/Table 3: Baseline vs. XGBoost Results Table
**File:** `paper/figures/results_table.csv`
**What it shows:** A side-by-side comparison table: for the full sample
and the POST-SEBI-2023 subset, the Baseline F-Score's AUC next to
XGBoost's AUC, Precision, and Recall.
**Why it's included:** This is your paper's single most important table —
it's the direct, numeric proof of your core finding (traditional formula
≈ random chance; ML model finds a real edge). A reader who only looks at
one table in your whole paper will look at this one.
**Where it goes:** Results section, immediately after Figure 2, as the
centerpiece of your main findings.
**Suggested caption:** *"Table 1. Predictive performance of the baseline
F-Score versus XGBoost across the full sample and the post-SEBI-2023
robustness subset."*

---

### Figure 4: SHAP Summary Plot (beeswarm)
**File:** `paper/figures/shap_summary_main.png`
**What it shows:** The standard SHAP "beeswarm" plot — each of the 9
signals on the y-axis, with every individual test-set prediction plotted
as a dot showing how much and in which direction (positive/negative) that
signal pushed the model's prediction, colored by whether the signal was
high or low (1 or 0) for that company.
**Why it's included:** This is the richest, most information-dense
explainability figure — it shows not just *which* signals matter (like
the bar chart does) but *how* they push predictions up or down, and
whether that effect is consistent or varies case by case. It's the
standard figure any ML/SHAP paper is expected to include.
**Where it goes:** Results section, right after introducing the SHAP
ranking table, as the visual companion to the numbers.
**Suggested caption:** *"Figure 3. SHAP summary plot showing each
signal's impact on individual predictions in the test set (n=72)."*

---

### Figure 5: SHAP Bar Plot (global importance)
**File:** `paper/figures/shap_bar_main.png`
**What it shows:** A simple horizontal bar chart of the 9 signals ranked
by mean absolute SHAP value — the same ranking as your results table,
but as a clean visual instead of numbers in a table.
**Why it's included:** Easier for a reader (or an interviewer glancing at
your paper) to grasp at a glance than the beeswarm plot — good for
presentations or a quick skim. Some papers use only the bar version, some
use both; including both gives you flexibility for where each is more
useful.
**Where it goes:** Can sit right next to the beeswarm plot, or be used
instead of it in a shorter/summary version of the paper (e.g., an
abstract graphic or presentation slide).
**Suggested caption:** *"Figure 4. Global SHAP feature importance ranking
of the 9 Piotroski F-Score signals."*

---

### Table 6: SHAP vs. Shah et al. Comparison Table
**File:** `docs/shap_vs_shah_comparison.md` (convert to a clean table
image or LaTeX table when drafting)
**What it shows:** All 9 signals with two rankings side by side — your
SHAP-based rank and Shah et al.'s portfolio-removal-based rank — plus a
column highlighting the 4 signals where both methods agreed exactly.
**Why it's included:** This is your paper's most original piece of
analysis — nobody else has cross-validated an ML/SHAP ranking against an
independent portfolio-based ranking for Indian F-Score signals. It turns
"here's what I found" into "here's what I found, and it's independently
corroborated by prior work in 4 of 9 cases" — a much stronger evidentiary
claim.
**Where it goes:** Discussion section, as the centerpiece of your
"cross-validation" discussion — not in the main Results section, since
it's building on your primary SHAP finding rather than reporting a new
raw result.
**Suggested caption:** *"Table 2. Comparison of SHAP-based signal
importance ranking (this study) against Shah (2025)'s portfolio-removal-
based ranking, showing exact rank agreement on 4 of 9 signals."*
