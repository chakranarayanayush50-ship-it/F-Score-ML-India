# Related work and claim rules (checked 14 November 2026)

## Closest prior work found (open and verify every entry before citing)
- Mukai, M. "Can Machine Learning Improve Value Investing? Evidence from Japanese High Book-to-Market Stocks", SSRN (abstract id 7033218). Elastic Net and XGBoost against the F-Score, with SHAP; Japan; positive result.
- Ang, Balachandran and Saraph, "Learning to Identify Winning Stocks", Stanford CS229 project report, 2013 (authors and year taken from the file name; verify). Machine learning on the nine F-Score inputs against the F-Score; US.
- Singh, M. K., "AI-Assisted Piotroski F-score Stock Selection and Robust Portfolio Construction for Indian Equities", SSRN (abstract id 7599618), posted October 2026. Pipeline and portfolio construction on Nifty Total Market.
- "Empirical Asset Pricing via Machine Learning: Evidence from Indian Equity Markets", ResearchGate (authors to be added). Machine learning and SHAP on Indian stocks, with size and momentum style variables.
- Earlier references to verify: Piotroski (2000); Singh and Kaur (2015); Walkshausl (2020); Chen, Cho, Dou and Lev (2022); Gu, Kelly and Xiu (2020); Chen and Guestrin (2016); Lundberg and Lee (2017).

## Claim rules
- Allowed, only after the manual search below is done and dated: "To our knowledge, we did not find prior work that tests this design on Indian mid- and small-cap stocks with these leakage controls."
- Not allowed anywhere (paper, README, GitHub description, LinkedIn): "first", "never", "novel combination", "for the first time", or any claim that SHAP was never applied to the F-Score.
- Report null results as null. No sentence may be stronger than the confidence intervals.

## Manual searches still to run (record the date and what was found)
- Google Scholar and Scopus: "Piotroski" "F-score" "machine learning" India
- Google Scholar and Scopus: "F-score" XGBoost SHAP Indian stocks
- Google Scholar and Scopus: "Nifty Smallcap 250" OR "Nifty Midcap 150" "F-score"

## Statements to prepare before submission
- AI-assistance disclosure: what AI was used for (drafting support, code help), and that the author checked and takes responsibility for everything.
- Data availability: Yahoo Finance data cannot be redistributed; code and result tables are in this repository.
- Conflict of interest and funding: author to confirm (none known).

## Additional related work from Google Scholar searches (15 November 2026)
- Rathore, J. S., "AI-Driven Stock Screening in Indian Equity Markets: A Retail Investor's Framework Using Machine Learning on NSE Data", SSRN (abstract id 6932218), June 2026; also listed in Epistora Journal of Economics and Finance Studies, 2026. Random Forest on six fundamental and momentum features for 50 NSE companies against P/E and P/B screens, 2023 hold-out year. Not the nine F-Score signals; no XGBoost or SHAP in the abstract.
- Yadav, R., Patil, A. and Sengupta, R., "An analysis of Satyam case using bankruptcy and fraud detection models", SocioEconomic Challenges, 2023. Uses financial scoring models including an F score in an Indian case study (verify which F score).
- Nadar, D. and Joshi, T., "Quality investing: Looking for value in quality stocks", NMIMS, 2020. Describes the F-Score in an Indian setting (verify).
- Search note: queries with "F-score" but without "Piotroski" return many stock-prediction papers where F-score means the classification metric. Always put Piotroski in quotes.
