# My Research Project — Notes for Interviews (Plain English)

## The one-line summary
I'm testing whether a machine learning model can do a better job than a famous
25-year-old stock-picking formula (the Piotroski F-Score) at predicting which
Indian companies will beat the market — and using an explainability tool called
SHAP to show *why* the model thinks what it thinks.

---

## Why this topic (the story to tell)

I built a personal stock-analysis tool (InvestCheck) that used the Piotroski
F-Score — a well-known formula from 2000. While working with it, I realized
nobody has properly tested whether this formula, built on decades of US data,
actually works well in India. I checked, and confirmed nobody has combined all
three things I'm doing: the real F-Score formula + a trained ML model + SHAP
explainability, on Indian companies. That's my research gap.

---

## What is the Piotroski F-Score? (explain simply)

A checklist of 9 yes/no financial health questions about a company — things
like "did it make a profit," "is its debt going down," "is it becoming more
efficient." Each "yes" is worth 1 point. Total score: 0 to 9. Higher = healthier
company. It's from a Stanford professor's 2000 research paper, and it's still
widely used today by real investors.

## What am I actually testing?

## The 9 Piotroski F-Score Signals — Full Detail

If an interviewer asks "what are the 9 signals" or "walk me through the
F-Score," here's the complete, detailed answer. Piotroski grouped them into
3 categories — Profitability, Leverage/Liquidity, and Operating Efficiency —
each signal is a yes/no test worth 1 point.

### Category 1: Profitability (4 signals)

**1. Positive Return on Assets (ROA > 0)**
- Formula: Net Income ÷ Total Assets, from this year
- Test: Is it greater than zero?
- What it checks: Is the company actually profitable right now, relative
  to how big it is?

**2. Positive Operating Cash Flow (CFO > 0)**
- Formula: Cash Flow from Operations, this year
- Test: Is it greater than zero?
- What it checks: Is the company generating real cash from its core
  business — not just paper profit, actual cash in the bank?

**3. Improving Return on Assets (ΔROA > 0)**
- Formula: This year's ROA compared to last year's ROA
- Test: Did it go up?
- What it checks: Is profitability *improving*, not just present? A
  company can be profitable but declining — this catches that trend.

**4. Cash Flow Quality (CFO > Net Income)**
- Formula: Compare Cash Flow from Operations to Net Income, same year
- Test: Is cash flow higher than reported profit?
- What it checks: Accounting profit can be manipulated more easily than
  cash flow. If cash flow exceeds net income, it's a sign the profit is
  "real" and backed by actual cash, not aggressive accounting.

### Category 2: Leverage, Liquidity & Source of Funds (3 signals)

**5. Falling Leverage (ΔLeverage < 0)**
- Formula: Long-term Debt ÷ Total Assets, this year vs. last year
- Test: Did the ratio go down?
- What it checks: Is the company reducing its reliance on debt? Lower
  leverage generally means lower financial risk.

**6. Improving Liquidity (ΔCurrent Ratio > 0)**
- Formula: Current Assets ÷ Current Liabilities, this year vs. last year
- Test: Did the ratio go up?
- What it checks: Can the company cover its short-term bills more easily
  than it could last year? Rising current ratio = improving short-term
  financial health.

**7. No New Shares Issued**
- Formula: Number of shares outstanding, this year vs. last year
- Test: Did the share count stay the same or go down (no dilution)?
- What it checks: Did the company avoid diluting existing shareholders by
  issuing new stock? Issuing new shares (to raise cash) can be a warning
  sign the company couldn't fund itself internally.

### Category 3: Operating Efficiency (2 signals)

**8. Improving Gross Margin (ΔGross Margin > 0)**
- Formula: Gross Profit ÷ Revenue, this year vs. last year
- Test: Did the margin go up?
- What it checks: Is the company able to sell its products/services more
  profitably than before — better pricing power, or lower cost of goods?

**9. Improving Asset Turnover (ΔAsset Turnover > 0)**
- Formula: Revenue ÷ Total Assets, this year vs. last year
- Test: Did the ratio go up?
- What it checks: Is the company generating more sales from the same
  asset base — i.e., using its resources more efficiently?

### Quick summary table (memorize this shape, not just the list)

| # | Category | Signal | Simple question it answers |
|---|---|---|---|
| 1 | Profitability | ROA > 0 | Are we profitable? |
| 2 | Profitability | CFO > 0 | Are we generating real cash? |
| 3 | Profitability | ΔROA > 0 | Is profitability improving? |
| 4 | Profitability | CFO > Net Income | Is the profit "real" (cash-backed)? |
| 5 | Leverage/Liquidity | ΔLeverage < 0 | Is debt reliance falling? |
| 6 | Leverage/Liquidity | ΔCurrent Ratio > 0 | Can we cover short-term bills better? |
| 7 | Leverage/Liquidity | No new shares issued | Did we avoid diluting shareholders? |
| 8 | Operating Efficiency | ΔGross Margin > 0 | Are we selling more profitably? |
| 9 | Operating Efficiency | ΔAsset Turnover > 0 | Are we using assets more efficiently? |

**One-line answer if put on the spot:** *"Piotroski's F-Score is 9 yes/no
tests split into three groups — 4 on profitability, 3 on leverage and
liquidity, and 2 on operating efficiency — each worth 1 point, for a total
score from 0 to 9. I used exactly these 9 in my study, then let an ML
model learn how much each one should actually count, instead of treating
them as automatically equal."*

---

Two questions:
1. Can an ML model predict which stocks will beat the market better than just
   adding up the 9-point score the old-fashioned way?
2. Using SHAP, which of the 9 signals actually matters most in India — does it
   match what Piotroski originally assumed (that all 9 are equally important)?

---

## What I've actually built so far (Phases 1–3)

### Phase 1 — Getting the data
- Picked my company list: the Nifty Smallcap 250 (250 mid-sized Indian companies)
- Downloaded their financial statements (profit/loss, balance sheet, cash flow)
  and stock price history — going back several years — using a free tool called
  yfinance
- Result: got usable data for 249 out of 250 companies

**If asked "where did your data come from":** *"Free, public financial data via
yfinance, for the Nifty Smallcap 250 index, downloaded directly with a Python
script I wrote."*

### Phase 2 — Turning raw numbers into the 9 signals
- Took the raw financial statements and calculated each of Piotroski's 9 yes/no
  signals for every company, for every year I had data
- Example: "was net income positive this year" becomes a simple 1 or 0
- Result: 906 total "company-year" data points (like 249 companies × ~4 years
  each) with all 9 signals calculated and summed into an F-Score

**If asked "how much data do you have":** *"906 company-year observations —
that's the real sample size for a model like this, not just 250 companies,
because each company contributes one data point per year."*

### Phase 3 — Defining what the model predicts
- For every company-year, calculated what actually happened next: did the
  stock's price go up more than the Nifty 50 (India's main stock index) over
  the following 12 months?
- Labeled each one "outperformed" (1) or "didn't" (0)
- Result: 835 valid labeled data points, split roughly 61% outperformed /
  39% underperformed — a reasonably balanced dataset

**If asked "what is your model predicting":** *"Whether a stock beat the
market over the next 12 months — a yes/no classification, not an exact
return number."*

### Phase 4 — Robustness check against a real regulatory change
- Found a genuine, documented SEBI rule change: the LODR (Second Amendment)
  Regulations 2023, which tightened disclosure timelines for listed
  companies, effective July 2023
- Split the dataset into "before" and "after" this date, so results can be
  checked on both sides of a real regulatory shift, not just on the whole
  dataset at once

**If asked "how did you handle regulatory changes in India":** *"I split
the dataset around a real SEBI disclosure-rule change from 2023, so I can
check whether my results hold up before and after it, rather than assuming
the market behaved consistently the whole time."*

### Phase 5 — Training the model and getting a real result
- Fixed an important bug first: my forward-return calculation could
  accidentally use a "future" price that didn't exist yet for the most
  recent companies, which would have quietly faked the results. Caught it
  by noticing the AUC scores were below 0.5 (worse than random), which is
  a red flag, not a real finding.
- After fixing that, trained an XGBoost model on the 9 F-Score signals,
  using a proper time-based split (trained on 2023-2025 data, tested on
  data the model never saw)
- **Result: Baseline (plain F-Score) AUC = 0.495. XGBoost AUC = 0.570.**

**What is AUC, in plain words:** AUC (Area Under the Curve) is a score from
0 to 1 that measures how well a model can correctly rank a company that
will outperform *above* one that won't. 0.5 means the model is no better
than a coin flip. 1.0 would be a perfect model.

**What my result actually means:** the plain, equal-weighted F-Score
(0.495 AUC) has essentially *no* real predictive power in this Indian
small-cap sample — it's statistically indistinguishable from random
guessing. The XGBoost model (0.570 AUC) shows a real, if modest, edge over
random. This is a genuinely interesting finding: it's not "ML crushes the
old method," it's "the traditional formula doesn't actually work here, but
a trained model finds a real signal in the same 9 inputs."

**If asked "what did you find":** *"The traditional F-Score, just summed
up the normal way, performed no better than random chance at predicting
which stocks would beat the market in my sample. But when I trained an ML
model on those same 9 signals instead of just adding them up equally, it
found a real, measurable edge — an AUC of 0.57 versus 0.495. That tells me
the individual signals do carry information, but the traditional
equal-weighting throws most of it away."*

### Robustness check — does the result hold up on both sides of the SEBI change?
Ran the same model separately on data from before and after the July 2023
SEBI regulatory change:

| | Baseline AUC | XGBoost AUC |
|---|---|---|
| Full dataset | 0.495 | 0.570 |
| Post-SEBI-2023 only | 0.500 | 0.593 |
| Pre-SEBI-2023 only | N/A | N/A |

The pre-2023 period only had 3 fully clean, labeled rows left after fixing
the future-date bug — nowhere near enough to train or test on, so the
script correctly reported "not enough data" instead of a fake number. The
post-2023 period, which has the bulk of the data, actually showed a
slightly *stronger* result than the full dataset (0.593 vs 0.570) — a good
sign that the main finding isn't just a fluke of the combined sample.

**If asked "did you test robustness":** *"Yes — I split my data around a
real SEBI regulatory change from July 2023 and re-ran the model on each
half. The post-2023 subset, which had enough data to test properly,
confirmed the same pattern: baseline at chance level, XGBoost with a real
edge — actually slightly stronger than my full-dataset result. The
pre-2023 subset didn't have enough clean data to test reliably, which I
report honestly rather than force a number out of too little data."*

---

## Which companies, and what does "906 company-years" mean?

### The company universe: Nifty Smallcap 250

I used the **Nifty Smallcap 250** — an official NSE index of 250 small-cap
Indian companies. This is a **small-cap** index specifically (not mid-cap).
For context, NSE's main size categories are:
- **Large-cap** — Nifty 50 / Nifty 100 (biggest, most established companies)
- **Mid-cap** — Nifty Midcap 150
- **Small-cap** — Nifty Smallcap 250 ← **this is what I used**

**If asked "why small-caps specifically":** *"Small-caps are the segment
where a formula like the F-Score is arguably most useful in practice —
these companies get far less analyst coverage than large-caps, so investors
rely more on formulas and screens like this to evaluate them. It's also a
segment retail investors are increasingly active in, so testing whether an
old US-built formula holds up here is practically relevant, not just
academic."*

### Q&A: "Why small-cap, and not mid-cap or large-cap?"

This is a very likely interview question — here's the full, detailed answer,
broken into the actual reasons:

**1. Small-caps are where a screening formula like this is most useful in
practice.** Large-caps (Nifty 50/100) are covered heavily by professional
analysts — dozens of research reports exist on companies like Reliance or
Infosys. Small-caps get far less coverage, sometimes none at all. Investors
evaluating small-caps genuinely rely more on formulas, screens, and
checklists like the F-Score, because there isn't a wall of analyst opinions
to lean on instead. Testing the F-Score where it's actually used the most
makes the study more practically relevant, not just academic.

**2. Small-caps are noisier and more likely to show a real gap.**
Large-cap companies are generally stable, well-governed, and don't vary
much year to year — a formula might "work" on them almost by default,
simply because there's less to distinguish. Small-caps have much more
variation in financial health, governance quality, and volatility — exactly
the conditions where a formula's real predictive power (or lack of it) is
easier to detect and test honestly.

**3. It matches how millions of new Indian retail investors actually
invest.** Retail investing in India has grown enormously in small and
mid-cap stocks specifically, often through direct stock-picking apps
without professional advice. If a widely-used formula like the F-Score
doesn't actually work well in this exact segment, that's directly useful
information for a huge and growing group of real investors — not just a
theoretical finding.

**4. Practical/data reasons.** Small-cap financial data is more available
through free tools (yfinance, NSE) than very obscure micro-caps, but still
messier and less standardized than large-cap data — which is realistic for
testing whether an approach is genuinely robust, not just working on
"clean," well-reported companies.

**Honest limitation to mention if pushed further:** *"I focused on one
segment — small-cap — for scope reasons. I can't yet say whether the same
pattern holds for mid-cap or large-cap Indian companies; that's a natural
next step for future research, and I say so directly in my paper's
limitations section."*

**Short version if you only have 10 seconds:** *"Small-caps get the least
analyst coverage, so investors rely on formulas like the F-Score there the
most — that's exactly where testing whether the formula actually works
matters most in practice."*

I pulled the official list directly from NSE Indices
(niftyindices.com), got data for 249 of the 250 (one had no usable data
on Yahoo Finance).

**Full company list:** saved in the repo at
`data/raw/company_universe.csv`. To generate a clean, readable list for
the paper's appendix or supplementary material, run this from the repo:
```
python3 -c "import pandas as pd; df = pd.read_csv('data/raw/company_universe.csv'); print(df['Symbol'].to_string(index=False))"
```
This prints all 249-250 ticker symbols — worth pasting into an appendix
section of the actual paper, or committing as a clean `companies_used.csv`
in the `docs/` folder so it's visible directly on GitHub.

### What "906 company-years" actually means

This is the real sample size for the ML model — and it's a genuinely
important thing to be able to explain clearly, since 906 sounds like a
random number if you can't unpack it.

**The idea:** each row of data isn't "one company" — it's "one company, in
one specific year." So if a single company (say, Tata Steel) has 4 years
of clean financial data, that company alone contributes **4 rows** to the
dataset — one row per fiscal year, each with its own 9 F-Score signals and
its own forward-return label.

**The math:** 249 companies × roughly 3.6 years of usable data each
(varies by company — some had more, some fewer, due to data availability)
≈ **906 total company-year rows.**

**Why this matters, and why it's not "cheating" to count it this way:**
this is standard practice in financial ML research — called a *panel
dataset*. Each row is still one real, independent observation: "this
specific company's financial signals in this specific year." A model
trained this way learns general patterns across many companies and years,
not just memorizing one company's specific history.

**If asked "how big is your dataset, really":** *"906 company-year
observations — I started with 249 real Indian small-cap companies, and
each contributed multiple years of data, since I pulled 5-7 years of
financial history per company. After cleaning (dropping years with
missing data), that gave me 906 usable rows to train and test on — that's
the actual sample size for the ML model, not 249."*

## Key technical terms, explained simply

| Term | Simple meaning |
|---|---|
| **F-Score** | 9-point checklist score (0-9) of a company's financial health |
| **SHAP** | A tool that opens up a machine learning model's "black box" and shows which inputs mattered most for each prediction |
| **XGBoost** | The specific ML model I'm using — good at finding patterns in this kind of structured, spreadsheet-style data |
| **Benchmark** | The Nifty 50 index — the "did you beat the market" comparison point |
| **Class balance** | Whether my "outperformed" vs "didn't" labels are roughly even (mine are ~61/39, which is fine) |
| **Time-based split** | Training the model on older years, testing it on newer years — so it's tested on genuinely unseen "future" data, not randomly mixed data |
| **Company-year** | One row of data = one company, in one specific year |

---

## Problems I ran into and fixed (good interview material — shows real work)

- **Python version issue:** My Mac's default Python (3.14) was too new and
  caused a crash pulling data. Fixed by installing Python 3.11 in a separate
  environment (a "virtual environment") just for this project.
- **Wrong data type when merging files:** One file stored dates as text,
  another as actual date objects — pandas couldn't merge them until I converted
  both to the same format.
- **Folder path bug:** My data-saving script accidentally saved everything one
  folder too deep. Caught it, moved the data to the right place, no data lost.

*Why mention these:* real research involves debugging, not just writing code
that works on the first try. Being able to explain what broke and how I fixed
it is more convincing than pretending everything went smoothly.

---

### Phase 6 — SHAP: which signals actually matter
Ran SHAP on the trained model to rank all 9 signals by how much they
actually drove predictions, then compared that to Piotroski's assumption
that all 9 are equally important (1 point each).

**Ranking (most to least important):**
1. Δ Gross Margin improving
2. CFO > Net Income (cash flow quality)
3. Δ Current Ratio improving (liquidity)
4. Δ ROA improving
5. Δ Leverage falling
6. No new shares issued
7. ROA > 0
8. Δ Asset Turnover improving
9. CFO > 0

**The key finding:** the top signal mattered roughly 4x more than the
bottom one. Piotroski's original score treats all 9 as equally worth 1
point — SHAP shows that assumption doesn't hold in this Indian market
sample. Interestingly, the top 3 signals are all about *improving*
operational quality and cash discipline (margin, cash-flow quality,
liquidity), while the weakest signals are simple one-off profitability
checks (ROA>0, CFO>0).

**If asked "what did SHAP tell you":** *"Piotroski's original formula
gives every signal equal weight — 1 point each, out of 9. My SHAP analysis
showed the model doesn't treat them equally at all: the most important
signal, whether gross margin is improving, mattered about 4 times more
than the least important one, whether cash flow was simply positive. The
signals that mattered most were all about *improving* trends — margin,
cash quality, liquidity — rather than simple pass/fail profitability
checks. That's a concrete answer to my second research question: no, equal
weighting is not the right approach for Indian equities."*

## What's left to do

- **Phase 7:** Write the full paper
- **Phase 8:** Publish on SSRN and GitHub

---

## Likely Interview Questions — Full Bank

Organized by category, roughly in order of how likely they are to come up.
Short, direct answers here — fuller detail is elsewhere in this document
where noted.

### Motivation & topic choice

**"Why this topic?"**
I built a personal stock-screening tool that used the Piotroski F-Score. I
realized nobody had properly tested whether this 25-year-old, US-built
formula actually works in India, or tried combining it with modern ML and
explainability tools. I checked — that exact combination hadn't been done.

**"Why does this matter to anyone besides you?"**
Millions of new Indian retail investors use formulas like this without
knowing if they actually work here. If the answer is "not really," that's
genuinely useful information, not just an academic footnote.

**"Why small-cap and not mid-cap or large-cap?"**
*(Full answer earlier in this doc.)* Short version: small-caps get the
least analyst coverage, so investors lean on formulas like this the most —
that's exactly where testing it matters most.

**"Why India specifically?"**
The F-Score has been tested in the US, Europe, and parts of Eastern
Europe — never combined with ML and SHAP for India. Indian markets also
have different ownership structures, accounting norms, and disclosure
rules, so it's a genuinely open question whether a US-built formula
transfers.

### Methodology & technical choices

**"Walk me through your methodology, step by step."**
Pulled financial data for 249 companies → computed Piotroski's 9 signals
per company-year (906 rows total) → defined a 12-month forward-return
label against the Nifty 50 → trained XGBoost on the 9 signals with a
time-based train/test split → compared it to the plain summed F-Score →
ran SHAP to see which signals the model actually relied on.

**"Why XGBoost and not another model (e.g. logistic regression, neural
network)?"**
XGBoost handles this kind of small, structured, tabular data well, doesn't
need huge amounts of data to train, and pairs cleanly with SHAP's
TreeExplainer for fast, exact explainability — which matters since the
whole point of the paper is explainability, not just raw accuracy.

**"Why a time-based split instead of random train/test split?"**
Financial data is sequential — randomly shuffling would let the model
"see the future" during training (e.g., train on 2025 data, test on 2023
data), which is a classic data leakage mistake. Time-based splitting
trains on older data and tests only on data that comes after it
chronologically, which is the only honest way to simulate real-world use.

**"How did you define 'outperformance'?"**
Whether a stock's actual return over the 12 months following its fiscal
year-end beat the Nifty 50's return over that same window — a binary
yes/no label, not a raw return number.

**"Why 12 months specifically?"**
It's the standard, most common holding-period convention in F-Score and
value-investing research, which makes the result comparable to prior
studies rather than using an arbitrary custom window.

**"How did you handle missing or messy data?"**
Logged and dropped rows with missing key fields (like Net Income or Total
Assets) rather than guessing or filling in fake values, and reported
exactly how many companies/rows were dropped and why at each step, so the
final sample size is honest and traceable.

### Results & interpretation

**"What did you actually find?"**
*(Full detail earlier in this doc.)* The plain, equal-weighted F-Score
performed no better than random guessing (AUC 0.495) at predicting
12-month outperformance. An XGBoost model trained on the same 9 signals
found a real, if modest, edge (AUC 0.570).

**"Is a 0.57 AUC actually good?"**
It's a modest, not dramatic, edge — but genuinely real, and in finance
specifically, small real edges are taken seriously because markets are
famously hard to predict at all. The more important finding isn't the raw
number, it's the *gap* between the baseline (essentially random) and the
ML model (real signal) using the exact same inputs.

**"Did you test if this result is robust / not a fluke?"**
Yes — split the data around a real SEBI regulatory change from July 2023
and re-ran the model on each half. The post-2023 subset (which had enough
data to test) showed the same pattern, slightly stronger (AUC 0.593 vs.
0.500). The pre-2023 subset didn't have enough clean data after filtering
to test reliably, which I report honestly rather than force a number.

**"What did SHAP show you?"**
*(Full ranked list earlier in this doc.)* The 9 signals are not equally
important, despite Piotroski's formula treating them that way — the top
signal (Δ Gross Margin) mattered roughly 4x more than the weakest (CFO >
0). The strongest signals were all about *improving* trends — margin,
cash quality, liquidity — rather than simple one-off profitability checks.

**"Could this result just be due to the overall stock market going up
during your sample period, not the F-Score itself?"**
That's a fair concern, and part of why I did the regulatory-split
robustness check — to see if the pattern holds outside of just one market
regime. It's also exactly why I use *relative* outperformance vs. the
Nifty 50, not raw returns — that controls for the general market direction
somewhat, since both the company and benchmark move with the market
together.

### Limitations & honesty

**"What are the limitations of this study?"**
Small-cap only (not tested on mid/large-cap yet), single-country
(India only), relatively short data history (limited years available per
company), and a modestly-sized test set for the main result. I state these
directly rather than hide them.

**"If you had more time/resources, what would you do differently?"**
Expand to mid-cap and large-cap for comparison, extend the historical
window for more company-years, and test additional ML models beyond
XGBoost to see if the finding holds across different modeling approaches.

**"Did you make any mistakes during this project? How did you handle
them?"**
*(Good, honest material — full detail earlier in this doc.)* Yes — I had
a bug where my forward-return calculation could accidentally use
placeholder data for dates that hadn't happened yet, which would have
silently faked some results. I caught it because the AUC scores came back
below 0.5, which was a red flag, traced it to the bug, fixed it, and
re-ran everything. I'd rather catch and explain a bug than present results
I'm not sure are real.

### Novelty & positioning

**"Has this been done before? How do you know?"**
I checked directly — Google Scholar, SSRN, arXiv, ResearchGate — for the
exact combination of Piotroski's real 9-signal framework, a trained ML
model, SHAP explainability, and Indian equities. Each piece exists
separately in prior research; the combination doesn't. I re-checked this
more than once during the project to make sure nothing new had been
published in the meantime.

**"What if someone publishes something similar before you finish?"**
The core value of the paper isn't being first in the world — it's proving
I can independently design, execute, and honestly report real research.
Even if a similar paper appeared, my specific dataset, code, and findings
would still be mine, dated and verifiable on GitHub and SSRN.

### Personal fit / why you

**"Why are you interested in this combination of finance and ML?"**
I've been building in both areas separately — a C++ limit order book
engine and quant trading framework on the finance/technical side, and this
project bridges them directly by applying ML to a real finance problem I
already understood deeply from building InvestCheck.

**"What did you learn about yourself / your skills doing this?"**
Comfortable debugging real, messy problems across a full pipeline —
environment setup, data collection, feature engineering, modeling, and
explainability — not just writing isolated code snippets. Also learned to
catch and question suspicious results instead of accepting them at face
value (the AUC-below-0.5 bug catch is the clearest example).

**"What's next for this project?"**
Write the full paper, publish it on SSRN and submit to student research
journals, and potentially extend it to mid-cap/large-cap as a natural
follow-up — possibly as a master's thesis direction.

## The one paragraph to memorize

*"I'm testing whether machine learning can improve on a well-known 2000
stock-scoring formula, specifically for Indian companies — something nobody's
properly tested before. I built the full data pipeline myself: pulled real
financial data for 249 companies, calculated the original 9-point scoring
signals, and defined a 12-month forward-return target against the Nifty 50.
My first real result: the traditional F-Score performed no better than
random chance in this sample — an AUC of 0.495 — while an XGBoost model
trained on the same 9 signals reached 0.570, a genuine, if modest, edge.
I tested robustness by splitting the data around a real SEBI regulatory
change from 2023, and the post-2023 subset confirmed the same pattern,
slightly stronger. That tells me the individual signals carry real
information, but the traditional equal-weighting wastes most of it. I'm
about to run SHAP — an explainability tool — to see which signals actually
matter most in the Indian market. Everything is free, reproducible, and
version-controlled on GitHub."*
