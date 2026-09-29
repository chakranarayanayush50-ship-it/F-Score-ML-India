# Related Work — Reference for Drafting

Pulls from your `literature_review.md` (15 papers), reorganized into the
4 clusters your paper actually needs, with sentence starters. Write each
cluster as its own short paragraph (or two) — don't try to cover every
paper in equal depth.

---

## The 4 clusters to write, in this order

1. The F-Score itself and its direct extensions (3 papers — deep detail)
2. ML vs. traditional formulas in India (3 papers — medium detail)
3. SHAP in financial distress/bankruptcy (5-6 papers — brief, grouped)
4. Adjacent AI approaches (1-2 papers — one sentence each)
5. Close with your explicit gap statement (most important paragraph)

---

## Cluster 1: The F-Score and its extensions (write this first, in most detail)

**Papers:** Piotroski (2000), Shah (2025), Gimeno et al. (2020)

**Facts to use:**
- Piotroski (2000): built the F-Score on U.S. data, 1976-1996, equal
  weighting was a simplification, not a proven-optimal choice
- Shah (2025): tested F-Score on Nifty 100 (2007-2024), found high
  F-Score portfolios beat the index; ALSO did signal-removal sensitivity
  testing — found signals unequal (Accrual removal hurt most, Asset
  Turnover removal helped) — no ML model used, large-cap only
- Gimeno et al. (2020): built "Neural F-Score" with network DEA,
  Eurozone/US large-caps, found plain 9 signals insufficient alone,
  explicitly called for testing in other markets

**Sentence starters:**
```
"Piotroski (2000) developed the F-Score using [data/period], finding
[headline result]. The nine signals were weighted equally, a choice
the author described as [a simplification]."

"Building on this, Gimeno et al. (2020) proposed [what they built],
finding [result], and called explicitly for [testing in new markets]."

"Most directly relevant to this study, Shah (2025) [what they did on
Nifty 100], finding [result]. Critically, [describe the removal
analysis and finding] — though this analysis did not use [what's
missing: trained model]."
```

---

## Cluster 2: ML vs. traditional formulas in India (medium detail)

**Papers:** Meena et al. (2024), Ghosh & Kapil, Panchal (2022)

**Facts to use:**
- Meena et al. (2024): 65,583 records, 7,008 Indian companies, IBC
  bankruptcy data — XGBoost AUC 0.92 vs. Altman Z-Score 0.82 vs. LR 0.63
  — but SVM underperformed (0.57), showing ML isn't automatically better
- Ghosh & Kapil: Indian steel companies, Altman Z-Score had lowest
  accuracy vs. DEA and ANN models, most years
- Panchal (2022): plain Altman Z-Score on 5 large Indian firms, several
  incorrectly flagged as "distressed" despite being healthy

**Sentence starters:**
```
"A separate literature has tested whether machine learning models
outperform the Altman Z-Score specifically, for Indian companies.
Meena et al. (2024) compared [models] on [N] records, finding
[XGBoost result] versus [Altman result] — though [SVM caveat]."

"Similarly, Ghosh and Kapil found [result] for Indian steel companies."

"Panchal (2022) applied the plain Altman Z-Score to [N] firms, finding
[surprising result] — suggesting [Western thresholds may not transfer]."

"Together, these studies establish a consistent pattern: [your own
one-sentence synthesis]. This study tests whether the same pattern
holds for the F-Score specifically."
```

---

## Cluster 3: SHAP in financial distress (brief — group these together)

**Papers:** Nguyen et al. (2025), Cross-Market SHAP paper, Explainable
AI Volatility Regime paper, Comparative ML Minority-Class paper, CNN+XAI
paper, Fasano et al., Pant/Rahman et al.

**Facts to use (pick 3-4 most useful, don't cover all 7 in depth):**
- Nguyen et al.: established SHAP as standard for bankruptcy model
  interpretability
- Cross-market paper: SHAP top predictors differ by country (US:
  operational efficiency, China: leverage) — supports the idea Indian
  markets might weight differently too
- Volatility regime paper: SHAP importance shifts across time periods —
  relevant to your own PRE/POST SEBI robustness check
- Pant/Rahman: XGBoost did NOT beat baseline in their household-distress
  setting — important counter-example, save this one for Discussion
  instead of using it here

**Sentence starters:**
```
"SHAP has become a standard explainability tool in financial ML
research. Nguyen et al. (2025) [what they showed]."

"Notably, [cross-market paper] found that SHAP-identified predictors
differ by country, [specific finding] — supporting the plausibility
that Indian markets may weight the F-Score's signals differently than
the U.S. context Piotroski originally studied."

"[Volatility regime paper] further showed that SHAP importance is not
stable over time, [finding] — directly relevant to this study's own
regulatory-change robustness check."
```

---

## Cluster 4: Adjacent approaches (one sentence, don't overdo this)

**Paper:** Kim (2025) — GuruAgents

**Sentence starter:**
```
"A methodologically distinct approach applies large language models
rather than trained classifiers: Kim (2025) built LLM agents prompted
to emulate famous investors, including a Piotroski-persona agent that
[finding]. This differs fundamentally from training a model directly
on signal values, but confirms AI+F-Score is an active research area."
```

---

## The closing gap paragraph — THE MOST IMPORTANT PARAGRAPH IN THIS SECTION

This is what an examiner/reviewer will look for. Say explicitly, in one
tight paragraph:

- What exists (list the 4 pieces: F-Score research, ML-vs-traditional
  in India, SHAP-in-finance, AI+F-Score approaches)
- What's never been combined (your exact 4-part gap: real 9-signal
  F-Score + trained ML model + SHAP + Indian equities)
- What extra thing you did that nobody else has (the Shah cross-
  validation)

**Sentence starter:**
```
"No existing study combines: (1) [X], (2) [Y], (3) [Z], applied to (4)
[W]. This study fills that specific combination and, additionally,
offers [your Shah cross-validation contribution]."
```

---

## Suggested length

Related Work is usually one of the longer sections — aim for 500-700
words total across all 4 clusters plus the closing gap paragraph. Don't
feel you need to write a full paragraph per paper — clusters 2-4 can be
2-3 sentences covering multiple papers together.
