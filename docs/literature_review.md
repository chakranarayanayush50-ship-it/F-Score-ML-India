# Literature Review — Related Work Notes

Working notes for the paper's Related Work section. Each entry: what the
paper did, what it found, and how it relates to (or differs from) this study.

---

## 1. Shah et al. — Piotroski F-Score signal sensitivity (India)

**What they did:** Built a Piotroski F-Score portfolio on Indian stocks and
tested sensitivity by removing one of the 9 signals at a time, tracking the
effect on total portfolio growth over the investment period.

**What they found:** The signals are NOT equally important. Baseline
portfolio (all 9 signals): ~1695.86% growth (₹10,00,000 → ₹1,79,58,561.61).

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
shows the 9 signals aren't equally important in an Indian sample, using
portfolio-removal sensitivity testing. It does NOT use a trained ML model
or any explainability method (SHAP/LIME). My study's SHAP-based ranking
can be directly compared against this removal-based ranking as a
cross-validation check — do the two independent methods agree on which
signals matter most?

**Cite as:** closest prior India-specific F-Score sensitivity work; the
paper this study most directly extends.

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

---

## Updated gap statement (for paper Introduction / Related Work)

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

- [ ] Read Shah et al. in full (closest paper — highest priority)
- [ ] Try to access Gimeno et al. (2020) full text via ResearchGate
      request or college library — currently only have the abstract
- [ ] Find 10-15 more general papers (Altman Z-Score/ML papers, other
      Indian fundamental-scoring studies) to round out to 15-25 total
- [ ] Once SHAP results are finalized, add the direct comparison table:
      SHAP ranking vs. Shah et al.'s removal-based ranking, side by side
