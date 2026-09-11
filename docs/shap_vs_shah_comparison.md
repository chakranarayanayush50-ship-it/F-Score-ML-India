# SHAP Ranking vs. Shah et al. (2025) Removal-Based Ranking — Comparison

Two completely independent methods, on two different Indian samples,
ranking the same 9 Piotroski signals by importance. This is one of this
study's original contributions: a cross-validation between a model-based
explainability method (SHAP) and a portfolio-based sensitivity method
(signal removal).

## Signal name mapping

The two studies name the signals slightly differently. Mapping (they are
the same underlying Piotroski signal):

| My signal name | Shah et al.'s name |
|---|---|
| CFO > Net Income | Accrual |
| ROA > 0 | ROA |
| Δ Current Ratio > 0 | Δ Liquidity |
| Δ ROA > 0 | Δ ROA |
| Δ Leverage < 0 | Δ Leverage |
| No new shares issued | Equity Issuance |
| CFO > 0 | Scaled CFO |
| Δ Gross Margin > 0 | Δ Gross Margin |
| Δ Asset Turnover > 0 | Δ Asset Turnover |

## The comparison table

| Signal | My SHAP Rank (1=most important) | My SHAP value | Shah's Rank (by portfolio impact) | Shah's growth impact of removal |
|---|---|---|---|---|
| CFO > Net Income (Accrual) | 2 | 0.1888 | 1 | −803.44 pts (biggest drop) |
| ROA > 0 | 7 | 0.0752 | 2 | −256.65 pts |
| Δ Current Ratio (Liquidity) | 3 | 0.1731 | 3 | −236.67 pts |
| Δ ROA | 4 | 0.1305 | 4 | −174.22 pts |
| Δ Leverage | 5 | 0.1164 | 5 | −66.24 pts |
| No new shares (Equity Issuance) | 6 | 0.0908 | 6 | ~0 pts (negligible) |
| CFO > 0 (Scaled CFO) | 9 | 0.0577 | 7 | +38.61 pts (removing helped) |
| Δ Gross Margin | 1 | 0.2326 | 8 | +49.09 pts (removing helped) |
| Δ Asset Turnover | 8 | 0.0735 | 9 | +105.38 pts (removing helped most) |

## Key finding: strong agreement in the middle tier

**4 of 9 signals landed at the exact same rank in both independent
methods:** Δ Liquidity (3=3), Δ ROA (4=4), Δ Leverage (5=5), and Equity
Issuance (6=6). This is a striking result — two completely different
methods (a trained ML model's SHAP values vs. a portfolio's return
sensitivity to removing a signal), on two different samples (my Nifty
Smallcap 250 vs. Shah's Nifty 100), independently agree on the
middle-importance ranking of 4 signals. This cross-validates that these
4 signals have a genuinely moderate, consistent importance in Indian
equities regardless of method or market-cap segment.

## Key finding: two notable disagreements, worth discussing

**1. Δ Gross Margin:** My SHAP ranks it #1 (most important). Shah's
removal ranks it #8 (removing it actually *improved* portfolio returns).
**Possible explanation:** SHAP measures contribution to predicting
*relative* 12-month outperformance vs. benchmark (a classification task)
in small-caps, while Shah measures the effect on *absolute* portfolio
growth from a long-only strategy in large-caps. A signal can be a strong
*predictor* of relative outperformance without being a strong driver of
absolute returns — these are measuring different things. Also plausible:
gross margin trends behave differently in small-cap vs. large-cap Indian
companies.

**2. ROA > 0:** My SHAP ranks it #7 (low importance). Shah's removal
ranks it #2 (very important). **Possible explanation:** the plain
ROA > 0 test may be too coarse a binary signal for an ML model to extract
much marginal predictive value from (once ΔROA, a related but more
informative signal, is already in the model) — but removing it entirely
from a rule-based portfolio strategy has a large effect because Piotroski's
original scoring has no redundancy-handling; ML models often naturally
"absorb" the value of a correlated feature into other features instead.

## What this means for the paper

This comparison is genuine new evidence, not available in either paper
alone:
- The **moderate-importance signals are robust** across method and
  market-cap segment (4/9 exact agreement)
- The **extremes diverge**, and the divergence itself is informative —
  it suggests importance rankings depend on what "important" is being
  measured *for* (relative outperformance prediction vs. absolute
  portfolio return), not just which market/country is being studied

**Suggested framing for Discussion section:** *"To cross-validate our
SHAP-based ranking, we compared it against the only other Indian
signal-importance analysis available (Shah, 2025), which used a
portfolio-removal sensitivity method on a different segment (Nifty 100
large-cap vs. our Nifty Smallcap 250) and different time period. Four of
nine signals — Δ Liquidity, Δ ROA, Δ Leverage, and Equity Issuance —
showed identical rank ordering across both independent methods, lending
convergent validity to their moderate, consistent importance. The two
largest divergences (Δ Gross Margin and ROA) suggest that signal
importance may depend on whether the modeling objective is predicting
relative outperformance (our study) versus absolute portfolio return
(Shah, 2025), an open question for future research."*
