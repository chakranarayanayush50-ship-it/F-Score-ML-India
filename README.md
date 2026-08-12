# Explainable ML for the Piotroski F-Score — Indian Equities

Research project testing whether a machine learning model, trained on Piotroski's
nine F-Score signals, can better predict future stock returns for Indian equities
than the original equal-weighted score — and using SHAP to reveal which signals
actually matter most in the Indian market.

## Research Question

> Can a machine learning model trained on Piotroski's nine F-Score signals better
> predict future stock returns for Indian equities than the original equal-weighted
> score — and what does SHAP reveal about which signals matter most in the Indian
> market?

## Why This Gap Exists

- The Piotroski F-Score (2000) has been tested in India using traditional statistics
  (t-tests, regression), but never combined with a trained ML model.
- ML-enhanced versions of the F-Score ("neural F-Score") exist for the Eurozone/US,
  never for India.
- SHAP explainability has been applied to bankruptcy/distress models (Altman Z-Score),
  never to the Piotroski F-Score, anywhere.

This project combines all three — Piotroski's actual 9-signal framework, a trained
ML model, and SHAP explainability — on Indian equity data, for the first time.

## Project Status

🚧 In progress — see [`docs/ROADMAP.md`](docs/ROADMAP.md) for the full 8-phase plan.

| Phase | Status |
|---|---|
| 1. Data Collection | Not started |
| 2. Compute F-Score Signals | Not started |
| 3. Define Target Variable | Not started |
| 4. India-Specific Robustness | Not started |
| 5. Train ML Model | Not started |
| 6. SHAP Explainability | Not started |
| 7. Write Paper | Not started |
| 8. Publish | Not started |

## Repository Structure

```
fscore-ml-india/
├── data/
│   ├── raw/            # raw pulled financials & prices (gitignored)
│   └── processed/       # cleaned, feature-engineered datasets (gitignored)
├── src/
│   ├── data_collection.py    # Phase 1 — pull financials & prices
│   ├── fscore_signals.py     # Phase 2 — compute the 9 F-Score signals
│   ├── target_variable.py    # Phase 3 — define forward returns / labels
│   ├── train_model.py        # Phase 5 — baseline + XGBoost training
│   └── shap_analysis.py      # Phase 6 — SHAP explainability
├── notebooks/            # exploratory analysis, plots for the paper
├── docs/
│   └── ROADMAP.md         # full 8-phase execution plan
├── paper/                 # LaTeX/Overleaf source for the final paper
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/<your-username>/fscore-ml-india.git
cd fscore-ml-india
pip install -r requirements.txt --break-system-packages
```

## Data Sources (all free)

- [yfinance](https://pypi.org/project/yfinance/) — price & fundamental data
- [jugaad-data](https://pypi.org/project/jugaad-data/) — NSE-specific data
- NSE/BSE public filings and index constituent lists

## Author

Ayush Chakranarayan — BCA, Deogiri College, Chhatrapati Sambhajinagar
Built alongside [InvestCheck](https://github.com/chakranarayanayush50-ship-it) —
a personal CLI stock analysis tool this project's methodology extends.

## License

MIT
