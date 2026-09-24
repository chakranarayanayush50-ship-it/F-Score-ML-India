# Discussion & Limitations — Reference for Drafting

Same idea as the Methodology/Results reference: these are the facts and
angles to cover, as bullet points. Turn them into your own sentences —
don't copy them directly. Use the sentence starters from
`how_to_draft_yourself.md` if you get stuck.

---

# DISCUSSION — what to cover

## 1. The core interpretation (say this first)
- The traditional F-Score's equal-weighting assumption does NOT hold for
  Indian small-cap equities
- Evidence: baseline AUC (0.495) ≈ random chance; XGBoost (0.570) found
  real signal in the exact same 9 inputs
- This means: the 9 signals DO carry real information — the old formula
  just wastes most of it by treating them as equally important

## 2. How this connects to prior work (use your literature_review.md)
- This extends a pattern already seen with the Altman Z-Score in India:
  Meena et al. (2024), Ghosh & Kapil, and Panchal (2022) all found ML/
  alternative models beat the traditional formula for Indian companies
  — this study shows the same pattern for the F-Score specifically,
  which nobody had tested before
- This builds directly on Gimeno et al. (2020), who explicitly asked
  future researchers to test their "smarter F-Score" idea in other
  markets — this study is answering that call for India

## 3. Be honest about the SIZE of the improvement
- AUC going from 0.495 to 0.570 is a real gain, but not huge — say this
  plainly, don't oversell it
- Context that makes it still meaningful: financial markets are
  notoriously hard to predict; even small, genuine edges matter in this
  field (unlike, say, image recognition, where 0.57 would be a poor
  score)

## 4. The important caution — don't overclaim "ML always wins"
- Mention the Pant/Rahman household-distress paper: they found XGBoost
  did NOT beat a naive baseline in their setting
- Why mention this against yourself: it shows you understand your result
  is a specific finding, not a universal law — this makes you look more
  credible, not less

## 5. What the SHAP ranking actually tells us
- The signals that mattered most (Δ Gross Margin, CFO > Net Income,
  Δ Current Ratio) all share something: they measure IMPROVING TRENDS,
  not just a one-time snapshot
- The signals that mattered least (ROA > 0, CFO > 0) are simple yes/no
  checks on a single year, no trend involved
- Your own interpretation to develop: why might "is this getting
  better" matter more than "is this currently fine" for small-cap
  companies specifically? (Hint: small-caps are more volatile
  year-to-year than large stable companies — a snapshot might not mean
  much if next year looks completely different)

## 6. The Shah (2025) cross-validation — your most original point
- 4 of 9 signals matched exactly in rank between your SHAP method and
  Shah's completely different removal-based method
- Why this matters: two independent methods, two different market-cap
  segments, agreeing on 4 signals is NOT a coincidence — it's real
  evidence those 4 signals are genuinely, consistently important
- The 2 disagreements (Δ Gross Margin, ROA) are also worth discussing —
  not as a failure, but as an interesting open question: maybe
  "important for predicting relative outperformance" (your study) isn't
  the same as "important for absolute portfolio returns" (Shah's study)

---

# LIMITATIONS — what to cover

List these honestly, as their own short paragraph or bullet each. Don't
hide them — a reviewer/interviewer respects seeing them stated plainly.

## 1. Small-cap only
- You tested Nifty Smallcap 250 only
- Mid-cap and large-cap Indian companies remain untested — you don't
  know if the same pattern holds there

## 2. Single country
- India only — no comparison to other emerging markets performed

## 3. Short historical window
- ~3.6 years of usable data per company on average
- This is shorter than ideal for this kind of study — a limitation of
  free data availability, not of your study design

## 4. Small test set sizes
- Main test set: 72 observations
- PRE-SEBI-2023 subset: only 3 observations — too small to evaluate at
  all, and you should say so directly

## 5. Only one ML model tested
- You used XGBoost only
- You don't know if other models (random forest, logistic regression,
  neural networks) would rank the signals the same way or find a
  similar/different AUC improvement

## 6. The fiscal-year-end clustering issue (NEW — from your own question)
- Nearly all Indian companies report fiscal year-end on March 31
- This means your "time-based" test set is really just one specific
  fiscal-year cohort, not a spread of different dates
- Worth stating this explicitly so a reader understands exactly what
  the train/test split actually represents

## 7. Shah (2025) comparison is across two different studies
- Different sample, different time period, different market-cap segment
- It's suggestive, not a fully controlled head-to-head test — be
  upfront about that

---

# Suggested paragraph order for Discussion (once you've drafted each idea)

1. Core interpretation (point 1)
2. Connect to prior India-ML-vs-traditional-formula literature (point 2)
3. Be honest about effect size (point 3)
4. The "don't overclaim" caution (point 4)
5. What SHAP reveals about *which* signals and why (point 5)
6. The Shah cross-validation as your most original contribution (point 6)

Limitations can just be a clean list — doesn't need the same narrative
flow as Discussion.
