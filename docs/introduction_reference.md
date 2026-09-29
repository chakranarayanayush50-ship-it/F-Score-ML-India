# Introduction — Reference for Drafting

Same approach as before: bullet points and angles to cover, not finished
sentences. Write it yourself using these as your source material.
Introduction is written AFTER Methodology, Results, Related Work, and
Discussion — you write it last because now you actually know what your
paper says.

---

## The job of an Introduction (4 things, in this order)

1. **Set the scene** — what is the F-Score, why do people use it
2. **Create the gap** — what hasn't been tested/done before
3. **State your research questions** — RQ1 and RQ2, clearly
4. **Preview your contribution** — one sentence on what you actually did

Don't explain your results here. Don't explain your methodology in
detail here. Just enough to make the reader understand *why this paper
needed to be written*.

---

## 1. Setting the scene — facts to use

- The Piotroski F-Score is a 9-signal checklist, created in 2000, still
  widely used by value investors today
- It scores companies 0–9 based on profitability, leverage/liquidity,
  and operating efficiency signals
- Every signal is worth exactly 1 point — Piotroski treated them as
  equally important, but admitted this was a simplification, not a
  proven-optimal weighting
- It was built and tested on U.S. companies only

**Sentence starters:**
```
"Value investors have long relied on [X] to identify..."
"Among these tools, the Piotroski F-Score [describe it]..."
"Despite its continued use, the F-Score was built using [context]..."
```

---

## 2. Creating the gap — facts to use

- Indian retail investing has grown a lot recently — millions of new
  investors, often without professional analyst coverage to rely on
- India differs from the U.S. in ownership structure, disclosure norms,
  regulatory environment — so a US-built formula might not transfer
  cleanly
- What's ALREADY been tested (be specific, this is your literature
  review doing its job):
  - Shah (2025) tested the plain F-Score on Nifty 100, found signals
    aren't equally important (via portfolio removal) — but no ML model
  - Gimeno et al. (2020) built an ML-enhanced F-Score, but only for
    Eurozone/US large-caps, no SHAP, different method (network DEA)
  - Several papers show ML beats the Altman Z-Score in India — but
    nobody tested this for the F-Score specifically
- **The exact gap, stated plainly:** nobody has combined (1) the real
  9-signal F-Score, (2) a trained ML model, (3) SHAP explainability,
  and (4) Indian equities — all four together

**Sentence starters:**
```
"However, [specific gap] remains unexamined."
"Prior work has tested [X] but not [Y]."
"To our knowledge, no study combines [list the 4 elements]."
```

---

## 3. Your research questions (already finalized — just format them)

```
RQ1: Can a machine learning model trained on Piotroski's nine F-Score
signals better predict 12-month stock outperformance for Indian
small-cap equities than the traditional equal-weighted score?

RQ2: Using SHAP, which of the nine signals actually drive predictions
most in the Indian small-cap context, and does this ranking match
Piotroski's assumption of equal importance?
```

You can use these exactly as written, or rephrase slightly in your own
words — either is fine, since these were built from your own study
design.

---

## 4. Previewing your contribution — facts to use

- You tested 249 companies, 906 company-years, Nifty Smallcap 250
- You compared baseline F-Score vs. XGBoost on a proper time-based
  holdout
- You applied SHAP to interpret the trained model
- You additionally cross-validated your SHAP ranking against Shah
  (2025)'s independent method — this is your most original extra piece,
  worth flagging here even briefly

**Sentence starters:**
```
"This study addresses this gap by [what you did, one sentence]."
"Using [N] company-years from [source], we [method summary]."
"We additionally [the Shah cross-validation, as a bonus contribution]."
```

---

## Suggested paragraph order

1. Paragraph 1: Set the scene (what is F-Score, why it matters)
2. Paragraph 2: Narrow to the India-specific open questions
3. Paragraph 3: Walk through what prior work has/hasn't done (your gap)
4. Paragraph 4: State RQ1 and RQ2 explicitly
5. Paragraph 5: One paragraph previewing your method and contribution

That's roughly 5 paragraphs, ~400-500 words total — Introductions are
usually shorter than people expect. Don't pad it.

---

## Common mistake to avoid

Don't summarize your Results in the Introduction. Save every number
(AUC values, SHAP rankings) for the Results section. The Introduction's
job is only to make the reader understand **why** you did this study —
not **what you found**.
