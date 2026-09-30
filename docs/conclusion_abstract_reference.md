# Conclusion & Abstract — Reference for Drafting

The last section to write, and the easiest — because both are just
compressed versions of sections you've already written. Write these
absolute last, after everything else is drafted.

---

# CONCLUSION — what to cover

The Conclusion is NOT a new section with new ideas. It's a tight summary
of: what you asked, what you did, what you found, what it means, what's
next. Roughly 150-250 words.

## The 5 things to hit, in order

1. **Restate what you were testing** (1 sentence — your RQ1 + RQ2, in
   plain language, not the formal wording)
2. **What you did** (1 sentence — data, method, in the fewest words
   possible)
3. **What you found** (2-3 sentences — your actual headline numbers:
   AUC 0.495 vs 0.570, the SHAP ranking, the Shah cross-validation)
4. **What it means** (1-2 sentences — the "so what")
5. **Future work** (1-2 sentences — what should happen next)

## Facts to use

- RQ1 answer: yes, ML found a real edge (0.495 → 0.570), confirmed on
  the post-SEBI-2023 subset (0.500 → 0.593)
- RQ2 answer: no, the 9 signals are not equally important (top signal
  ~4x the weakest); improving-trend signals mattered most
- Extra contribution: 4/9 signals matched Shah (2025)'s independent
  ranking exactly
- Future work ideas: test mid-cap/large-cap, test other ML models,
  longer historical window as more data becomes available

## Sentence starters

```
"This study tested whether [RQ1 in plain words] and [RQ2 in plain
words], for Indian small-cap equities."

"Using [N] company-years from [source], we compared [baseline] against
[XGBoost] on a [time-based holdout]."

"The traditional F-Score performed at [result], while XGBoost [result],
a finding that held on [robustness subset]."

"SHAP analysis revealed [key finding about unequal importance]."

"Together, these results suggest [the big-picture takeaway]."

"Future research should [1-2 concrete next steps]."
```

## What NOT to do

- Don't introduce any new information, numbers, or citations here that
  weren't already in Results/Discussion
- Don't repeat your Limitations in detail — one brief nod is enough if
  any
- Don't make it longer than Introduction — if anything, keep it shorter

---

# ABSTRACT — what to cover

Write this **dead last**, after Conclusion. It's the hardest section to
write first and the easiest to write last, because by now you can just
compress your whole paper into ~200 words.

## The formula (6 sentences, roughly one per beat)

1. **Context** — what the F-Score is, one sentence
2. **Gap** — what hasn't been tested (your Introduction's gap, compressed)
3. **What you did** — data + method, one sentence
4. **RQ1 result** — the AUC numbers
5. **RQ2 result** — the SHAP finding
6. **Bonus/closing** — the Shah cross-validation + what it all means

## Facts to use — you already have all of these, just compress them

- The F-Score: 9-signal checklist, 2000, equally-weighted, still widely
  used
- Gap: never tested with ML + SHAP for India
- Method: 249 companies, 906 company-years, Nifty Smallcap 250,
  XGBoost vs. baseline, time-based split
- RQ1 result: baseline AUC 0.495 (random), XGBoost AUC 0.570 (real
  edge), confirmed on post-SEBI-2023 subset
- RQ2 result: signals not equally important, top signal (Δ Gross
  Margin) ~4x the weakest (CFO > 0)
- Bonus: 4/9 signals matched Shah (2025)'s independent ranking

## Sentence starters

```
"The Piotroski F-Score, a [description], remains widely used despite
[the gap]."

"This study tests whether [RQ1] and [RQ2], using [N] company-years from
[N] Indian small-cap companies."

"On a time-based holdout, the traditional F-Score [result], while
[XGBoost result] — a finding that held on [robustness check]."

"SHAP analysis reveals [key finding], with [specific numbers]."

"Cross-validating this ranking against [prior work] shows [agreement
finding]."

"These results suggest [one-sentence big-picture takeaway]."
```

## The one hard rule for Abstracts

**Every sentence in the Abstract should map to something a reader can
find later in the paper.** Don't write anything in the Abstract that
isn't backed up by a real section, number, or citation elsewhere. If you
find yourself writing something new here, it belongs in Discussion
instead — go add it there first, then compress it back into the
Abstract.

## Target length

150-250 words total. If you're over 250, cut adjectives and combine
sentences — don't cut findings.

---

# You're done with references after this

Once you've drafted all 6 sections (Methodology, Discussion+Limitations,
Introduction, Related Work, Results — covered in the Methodology
reference — and now Conclusion+Abstract), you have a complete paper in
your own words. At that point, send me the full draft and I'll give you
section-by-section feedback — consistency checks, clarity notes, and a
final pass on formatting — without rewriting your voice out of it.
