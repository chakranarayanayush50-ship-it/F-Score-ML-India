# Literature Review — Related Work Notes

Working notes for the paper's Related Work section. Each entry: what the
paper did, what it found, and how it relates to (or differs from) this study.

---

## 1. Shah (2025) — "Evaluating the Effectiveness of the Piotroski F-Score in
the Indian Equity Market: Evidence from Nifty 100 (2007–2024)"

**Author:** Ayush Shah, Mumbai, India (published in *Communications on
Applied Nonlinear Analysis*)
**Link:** https://internationalpubls.com/index.php/cana/article/view/6028

**What they did:** Two things, in one paper. (1) Applied the Piotroski
F-Score to Nifty 100 companies from 2007-2024, selecting the top 10
companies each quarter and comparing performance to the broader index.
(2) Separately tested sensitivity by removing one of the 9 signals at a
time from a portfolio, tracking the effect on total portfolio growth.

**What they found:**
- Part 1: firms with higher F-scores delivered stronger returns over time
  and provided a cushion during market downturns.
- Part 2 (signal removal): the signals are NOT equally important.
  Baseline portfolio (all 9 signals): ~1695.86% growth (₹10,00,000 →
  ₹1,79,58,561.61).

| Signal removed | Portfolio value (₹) | Growth | Impact of removing it |
|---|---|---|---|
| Accrual | 99,24,175.26 | 892.42% | **Largest drop — most important signal** |
| ΔLiquidity | 1,55,91,882.47 | 1459.19% | Large drop |
| ROA | 1,53,92,106.27 | 1439.21% | Large drop |
| ΔROA | 1,62,16,426.44 | 1521.64% | Moderate drop |
| ΔLeverage | 1,72,96,236.72 | 1629.62% | Small drop |
| Equity Issuance | 1,79,59,208.68 | 1695.92% | ~No effect |
| Scaled CFO | 1,83,44,698.33 | 1734.47% | Slight increase |
| ΔGross Margin | 1,84,49,537.53 | 1744.95% | Slight increase |
| ΔAsset Turnover | 1,90,12,359.39 | 1801.24% | **Largest increase — removing it helped** |

**Relation to my study:** This is the closest existing work — it already
shows the 9 signals aren't equally important in an Indian sample (Nifty
100, large-cap), using portfolio-removal sensitivity testing. It does NOT
use a trained ML model or any explainability method (SHAP/LIME), and it
covers large-cap (Nifty 100), not small-cap (Nifty Smallcap 250) like my
study. My study's SHAP-based ranking can be directly compared against
this removal-based ranking as a cross-validation check — do the two
independent methods agree on which signals matter most?

**Cite as:** closest prior India-specific F-Score work; the paper this
study most directly extends and differentiates from (small-cap vs.
large-cap, SHAP vs. portfolio-removal, trained ML model vs. no model).

---

## 2. Halkiewicz — Variance estimation in regression (uses F-Score data as example)

**What they did:** A pure econometrics/statistics paper comparing variance
estimators (HC0, HC2, HC3, Cattaneo-Jansson-Newey correction) for
regression under heteroskedasticity. Uses Piotroski F-Score returns in
Central/Eastern European (CEE) markets as an empirical illustration of
their statistical findings.

**What they found:** HC0 is biased downward (over-rejection), HC3
over-corrects, HC2 is closest to exact under most conditions. Not a
finance/F-Score finding — a statistics methodology finding.

**Relation to my study:** Not directly comparable — this is not really an
F-Score paper, the F-Score data is just their example dataset. Relevant
only if discussing choice of statistical/econometric technique, not as a
finance-domain comparison.

**Cite as:** tangential; mention only if discussing econometric method
choices, not in the main F-Score literature comparison.

---

## 3. Kim — GuruAgents: LLM agents emulating investor philosophies

**What they did:** Built 5 LLM agents (GPT-4o backbone), each prompted to
emulate a famous investor's philosophy (Buffett, Piotroski, Altman, etc.),
backtested on NASDAQ-100 constituents, Q4 2023 to Q2 2025.

**What they found:** Buffett-persona agent performed best (42.2% CAGR).
The Piotroski-persona agent showed high turnover, frequently rebalancing
based on signal changes — consistent with the F-Score's periodic,
checklist-driven nature.

**Relation to my study:** Different method entirely — prompting an LLM to
behave like Piotroski, not training a model on the actual 9 signals as
numeric features. Also US large-cap (NASDAQ-100), not India. Useful as a
"related but methodologically distinct AI approach" citation to show the
AI+F-Score space is active, but not a direct comparison point.

**Cite as:** adjacent AI/F-Score work, different method and market.

---

## 4. Gimeno, Lobán & Vicente (2020) — Neural approach to the F-Score (Eurozone/US)

**What they did:** Built a "Neural F-Score" (NF-Score) using network data
envelopment analysis on the largest Eurozone and US non-financial
companies, 2006-2017.

**What they found:** The NF-Score significantly improves short-term
returns of long-short value strategies compared to the plain F-Score.
Importantly: the 9 accounting signals alone are NOT sufficient to
identify winner returns for US large-caps — more sophisticated signals
are needed. They explicitly call for testing this approach in **other
markets** as future research.

**Relation to my study:** The closest methodological cousin. Same core
idea (enhance the F-Score with a smarter model instead of equal
weighting), different technique (network DEA vs. XGBoost), different
market (Eurozone/US large-cap vs. Indian small-cap), and no
explainability layer (no SHAP). Their call for "other markets" is
effectively the direct invitation this study answers for India.

**Cite as:** primary methodological precedent; state clearly how this
study differs (XGBoost + SHAP vs. network DEA, India small-cap vs.
Eurozone/US large-cap, explainability included).

## 5. Meena, Pandey & Garg (2024) — Machine Learning Models Comparison for
Bankruptcy Prediction for Indian Companies (IBC 2016)

**What they did:** Compared logistic regression, decision tree, XGBoost,
SVM, and Altman Z-Score on 65,583 records covering 7,008 Indian companies
(257 bankrupt) under India's Insolvency and Bankruptcy Code, FY2016-2022.

**What they found:** XGBoost performed best (AUC 92%), beating decision
tree (76%), Altman Z-Score (82%), and logistic regression (63%). SVM
underperformed (57%), showing ML isn't automatically better — model choice
matters. Confirms findings from Wang et al. (2012), Barboza et al. (2017),
Chen et al. (2010).

**Relation to my study:** The strongest direct precedent for "ML beats
traditional scoring formula in India" — but for bankruptcy prediction with
Altman Z-Score, not for outperformance prediction with Piotroski F-Score.
Confirms the general pattern I'm testing (ML > traditional formula in
Indian markets) has already held for a *different* formula and *different*
target variable. Strengthens the plausibility of my hypothesis without
overlapping it directly.

**Cite as:** strong supporting precedent — same country, same "ML vs.
traditional formula" question, different formula (Altman not Piotroski)
and different target (bankruptcy not outperformance).

---

## 6. Ghosh & Kapil — Is Altman's Model Efficient in Predicting Bankruptcy?
Altman Z-score vs. DEA vs. ANN (Indian steel companies)

**What they did:** Compared Altman Z-Score, additive DEA (Data Envelopment
Analysis), and ANN (neural network) models on Indian steel companies,
using confusion matrices (classification accuracy, Type-I/Type-II error)
across 2015-2018.

**What they found:** Altman Z-Score had the lowest classification accuracy
in most years (e.g., 85.00% in 2015) compared to DEA (92.69%) and ANN
(91.54%). The Altman model also had the highest average misclassification
cost. Their overall recommendation: DEA and ANN models outperform the
traditional Altman Z-Score for Indian steel companies. One anomaly year
(2017) where DEA underperformed, showing results aren't universally
consistent year-to-year.

**Relation to my study:** Another confirmed case of "traditional formula
underperforms smarter model" in an Indian sector-specific sample —
sector-specific (steel only) rather than broad small-cap, and uses DEA/ANN
rather than XGBoost, with no SHAP explainability. Useful supporting
citation, and the "one anomaly year" finding is worth noting — a reminder
that results can vary year to year, relevant to my own robustness-check
framing (PRE/POST SEBI split).

**Cite as:** further supporting evidence that traditional scoring formulas
underperform smarter models in Indian sector-specific contexts.

---

## 7. Pant, Rahman et al. (2025) — Machine Learning Enabled Early Warning
System for Financial Distress Using Real-Time Digital Signals

**What they did:** Built an ML early-warning system for *household*-level
(not corporate) financial distress in the US, combining macroeconomic
signals (GDP growth, inflation, FX), digital-economy signals (ICT demand,
market volatility), and socioeconomic data across 750 households, 3
monitoring rounds over 13 months. Compared logistic regression, decision
trees, random forest, XGBoost, and LightGBM on both binary distress
detection and 3-level severity classification, with SHAP for
explainability.

**What they found:** Notably, for the binary distress task, ML models did
NOT clearly beat simple baselines — logistic regression scored ROC-AUC
0.50 (essentially random), XGBoost only 0.49, and even LightGBM just
0.46. This is an important honest finding: binary distress prediction was
a "low-signal task" in their data. However, the *severity* classification
(3-level: Low/Medium/High) task performed very well (XGBoost/LightGBM
accuracy ~99.87%). SHAP identified Volatility Index, IoT Device Density,
Emergency Policy Score, Inflation, and SME Finance Score as the top 5
global predictors.

**Relation to my study:** Genuinely useful parallel, for an unexpected
reason: they found binary distress prediction can score at-or-near random
(AUC ~0.46-0.50) even for advanced models like XGBoost, which is similar
to what I found for my own *baseline* (plain F-Score, AUC 0.495) — but in
my case, XGBoost meaningfully beat that baseline (0.570), whereas in their
household-distress binary task, XGBoost did NOT clearly beat the naive
baseline. This is a useful point of contrast to discuss: not every
finance+ML+SHAP study finds ML adds value over baseline — mine does, in
a specific, defensible way (same features, unequal weighting captured by
the model), and I should be careful not to overclaim a "universal ML
wins" narrative given this counter-example exists.

**Cite as:** methodologically similar (XGBoost + SHAP for financial
distress), different domain (household-level, US, not corporate/India),
and a useful honest counter-example showing ML doesn't always beat naive
baselines — supports framing my own result carefully rather than as an
inevitability.

---

**Old framing (before finding Shah et al.):** "No study has shown the F-Score's
9 signals are unequally important in India."

**Corrected, honest framing:** Shah et al. already demonstrated, via
portfolio-removal sensitivity testing, that the F-Score's 9 signals are
not equally important in Indian markets. However, portfolio-removal
testing only reveals the *effect of dropping* a signal on aggregate
returns — it does not use a trained predictive model, and it cannot
show *how much each signal drives individual predictions* at the
company level. Separately, Gimeno et al. (2020) showed that a smarter,
model-based reweighting of the F-Score's signals improves on the plain
equal-weighted version — but only for Eurozone/US large-caps, using
network DEA, without any explainability layer, and explicitly called for
testing in other markets. No existing study combines: (1) a trained ML
model on Piotroski's actual 9 signals, (2) SHAP explainability, and
(3) Indian equities. This study fills that specific combination, and
additionally offers a novel cross-check: comparing SHAP's model-based
signal ranking against Shah et al.'s independent removal-based ranking
to see whether two different methods agree on which signals matter most
in the Indian market.

## Next steps for the literature review

- [x] Shah (2025) — read and logged
- [x] Meena, Pandey & Garg (2024) — read and logged
- [x] Ghosh & Kapil — read and logged
- [x] Pant, Rahman et al. (2025) — read and logged (via full-text fetch)
- [ ] Try to access Gimeno et al. (2020) full text via ResearchGate
      request or college library — currently only have the abstract
- [ ] 7 more papers needed to reach 15 minimum (see link list shared
      earlier — Panchal Altman Z-Score, V4FinBench, Cross-Market SHAP
      paper, Explainable AI Volatility Regime paper, CNN+XAI bankruptcy
      paper, Nguyen/Viviani/Ben Jabeur SHAP bankruptcy paper, and the
      Comparative ML Minority-Class Distress paper are good candidates —
      abstract-level skim is enough for most of these)
- [ ] Once SHAP results are finalized, add the direct comparison table:
      SHAP ranking vs. Shah et al.'s removal-based ranking, side by side
