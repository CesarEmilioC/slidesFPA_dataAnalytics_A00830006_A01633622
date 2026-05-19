# Speaker script &mdash; FPA Final Defence (English)

*S&P 500 Stock Price Movement Prediction &mdash; Historical Market Data and Financial News Sentiment Analysis*

Authors: **César Castaño (A00830006)** &middot; **Brenda García (A01633622)** &middot; Tec de Monterrey, M.Sc. CS, Semester 4.

> **Target time: 10 minutes.** Emphasis on **results and conclusions** &mdash; setup and methodology are paced quickly; the slides past 15 are where we slow down. *Italic lines* are inline connectors, said while clicking forward.

---

## 1. Title slide &mdash; 10 s

Good morning. **César Castaño** and **Brenda García**. M.Sc. in Computer Science, Tec de Monterrey. We are defending our Data Analytics final project on **S&P 500 next-day direction prediction with news sentiment**.

## 2. Agenda &mdash; 10 s

Ten beats. Quick setup, methodology, then the bulk of the talk is **results, interpretation and conclusions**.

## 3. Motivation &mdash; 30 s

The S&P 500 is the most-watched U.S. equity benchmark, with eleven sectors that behave very differently in volatility and news flow. We predict **direction**, not price &mdash; that is what risk management actually needs. Recent NLP makes structured sentiment from financial text essentially free. The question on the right is the entire project in one sentence.

## 4. Hypotheses &mdash; 25 s

Target: **1 if tomorrow's close is above today's, 0 otherwise**. Two hypotheses: **H1** sentiment improves Acc, F1 and AUC over a technical-only baseline; **H2** the gain grows with sector volatility. Three research questions follow.

## 5. Related work &mdash; 20 s

Five anchors: **Bollen 2011** (sentiment is predictive), **Vargas 2017** (multimodal helps), **Araci 2019** (FinBERT), **Zhang 2019** (XGBoost + sentiment is competitive), **López de Prado 2018** (chronological splits, no look-ahead).

## 6. Pipeline &mdash; 15 s

Four stages: market data, technical features, FinBERT sentiment, tree ensembles &mdash; **sixteen runs total**.

## 7. Data &mdash; 15 s

Market: `yfinance`, 2010-2019. News: Kaggle Analyst Ratings, **1.4M headlines** filtered and capped at 50 per trading day with a fixed seed.

## 8. Technical indicators &mdash; 15 s

Seven OHLCV-derived features: returns, two moving averages, RSI, volatility, HLC3 and volume. Target computed before any modelling &mdash; no leakage.

## 9. Sector selection &mdash; 15 s

Three anchors covering the volatility range: **XLP** Consumer Staples (low), **XLK** Technology (median), **XLE** Energy (high).

## 10. FinBERT &mdash; 20 s

Per headline, FinBERT gives positive minus negative as a score in plus/minus one. Aggregated daily into mean sentiment, std and headline count. Pre-trained `ProsusAI/finbert`, batch 32, neutral on headline-less days.

## 11. EDA &mdash; class balance &mdash; 10 s

**Mild up-bias**: always-up scores ~0.55 accuracy. That is why we report AUC alongside.

## 12. EDA &mdash; news flow &mdash; 10 s

~386K headlines, **100% trading-day coverage**, mean sentiment slightly positive.

## 13. Experimental design &mdash; 10 s

Two algorithms times two feature sets times four datasets &mdash; **sixteen runs** under identical splits.

## 14. Training &mdash; 15 s

Chronological 80/20: ~2,000 train days, **501 test days**. Default hyperparameters so all sixteen runs stay directly comparable.

*Now the results &mdash; this is where we slow down.*

## 15. Results &mdash; technical only &mdash; 25 s

The headline: **AUC clusters at 0.50 across the board**. Technical indicators alone barely separate up from non-up days &mdash; consistent with weak-form market efficiency. XGB on SP500 reaches F1 0.66 only by leaning on the majority class. **XLK collapses to class zero**, F1 down to 0.23. This is the baseline that needs improvement.

## 16. Results &mdash; technical + sentiment &mdash; 30 s

Two clean wins. **SP500 + Random Forest + sentiment**: 0.56 accuracy, 0.67 F1, **0.51 AUC** &mdash; that is plus 0.05, plus 0.06, plus 0.04 over the baseline. **XLE + XGBoost + sentiment**: AUC moves from 0.48 to 0.52. Gains concentrate on the broad index and the highest-volatility sector. Low and median sectors are largely unmoved.

## 17. Where the +0.04 AUC lives &mdash; ROC + confusion &mdash; 50 s

Two views of the same SP500 + Random Forest result. **Left**: the ROC overlay. Technical-only sits on the diagonal at AUC 0.478; **technical + sentiment** lifts above it from FPR 0.3 to 0.9, AUC 0.513. That gap, plus 0.035, is the entire contribution of sentiment. **Right**: confusion matrix at threshold 0.5. **Recall on UP days is 0.84** &mdash; the model catches most rallies &mdash; but precision is 0.57 because it tolerates 174 false positives. So it behaves as an **aggressive long-bias classifier**: rarely misses an UP day, cries wolf about a third of the time.

## 18. Sentiment uplift &mdash; 20 s

Every bar is a delta. **SP500 + RF positive across all three metrics**, **XLE + XGB positive on Acc and AUC**, **XLP + RF the standout negative** &mdash; exactly the pattern H2 predicts for low-volatility sectors.

## 19. Feature importance &mdash; 20 s

`sentiment_mean`, in gold, is **top three** for the two configurations where it materially improved AUC. Technical features spread evenly &mdash; the sentiment signal is genuinely additive.

## 20. Hypothesis assessment &mdash; 25 s

**H1 partially supported** &mdash; works on the index and high-vol sector, sector picture mixed. **H2 partially supported** &mdash; XLE most volatile shows the largest XGBoost gain, but XLK median-vol does not benefit, so the gradient is not strictly monotonic. **RQ2**: tied on AUC; Random Forest wins on the index, XGBoost wins on the high-vol sector.

## 21. What does an AUC ≈ 0.50 actually mean? &mdash; 45 s

Three reference points on the same 501-day test. **Random coin flip**: 0.50 / 0.50 / 0.50. **Always-up**: 0.55 accuracy, 0.71 F1 *for free*, AUC still 0.50 (no ranking ability). **Our best**: 0.56, 0.67, 0.51. The bars make it visually obvious: on accuracy and F1 we are **on top of the always-up baseline**, plus 0.05, plus 0.06; on AUC the three bars are indistinguishable. **The real result is the delta from sentiment**, plus 0.04 AUC, not the level. Exactly what the weak form of EMH predicts.

## 22. Comparison with prior literature &mdash; 30 s

Bollen 87.6% on the Dow with Twitter mood, but a seven-month window; reproductions on longer windows fall to ~60%. Vargas ~62% with deep encoders over full body Reuters text. Araci's FinBERT is **sentence sentiment, not next-day direction**. Zhang ~0.56 AUC on Chinese A-shares with per-ticker tuning. Once you normalise the setup, **our 0.52 AUC on the high-volatility sector is in the right ballpark** &mdash; daily plus titles-only is the hardest regime above.

## 23. Live demo &mdash; 20 s

Recorded walk-through on Drive. The Colab notebook loads the four classifiers, pulls today's OHLCV, scores today's headlines with FinBERT, and prints UP / DOWN / STABLE per model. The calibration plot on the right justifies the 0.45-to-0.55 corridor we use for STABLE.

## 24. Discussion &mdash; 25 s

The chart on the right makes the central claim visible: **all sixteen configurations within ±0.03 of AUC = 0.50**. Daily sentiment is a thin signal &mdash; loses intra-day timing, noisy sectors mask it. XLK class collapse is the test window's class skew. SP500 benefits the most because index returns aggregate idiosyncratic noise into a cleaner systematic signal.

## 25. Limitations &mdash; 25 s

Two new ones first. **Significance**: the +0.04 AUC is a point estimate &mdash; a DeLong test or bootstrap CI is needed. **Transaction-cost reality**, on the chart: a 5-to-10 basis-point round-trip cost erodes the edge to break-even around 9 bp. Then the standard caveats: news coverage skew, headline-only sentiment, sampling cap, single chronological split, default hyperparameters.

## 26. Trading reality check &mdash; 35 s

Four equity curves on the 501-day test, dollar one start, gross of costs. **Always-long** ends at **\$1.19** &mdash; the test window was the tail of the 2017-2019 bull run. Our **RF + sentiment at probability 0.55** ends at **\$1.17** with about half the time in cash &mdash; **most of the upside, less exposure**. Random ends at \$1.09 &mdash; well below buy-and-hold, which confirms our signal is **not luck**. Gross of costs we still don't beat the easy baseline; with realistic costs the picture flips. The plus-0.04 AUC is a **real signal, not yet a tradable one**.

## 27. Conclusions &mdash; 50 s

Six take-aways. **One**: FinBERT headline sentiment helps at the index level with Random Forest, plus 0.05 accuracy, plus 0.06 F1, plus 0.04 AUC &mdash; **small but consistent**. **Two**: the effect is **not monotonic in sector volatility** &mdash; XLE benefits, XLP and XLK do not, H2 only partially supported. **Three**: the AUC-equals-0.50 ceiling is **consistent with weak-form EMH** &mdash; our contribution is the **sign of the delta**, not a tradable signal. **Four**: algorithm choice is **configuration-dependent** &mdash; Random Forest on the index, XGBoost on the high-vol sector, RQ2 has no universal winner. **Five**: `sentiment_mean` ranks top three in feature importance **only** where it actually improved AUC &mdash; the contribution is real, not a model artefact. **Six**: gross of costs our long/flat strategy reaches \$1.17 vs \$1.19 buy-and-hold and \$1.09 random &mdash; **better than chance, not better than the easy baseline**.

## 28. Future work &mdash; 15 s

In priority order: **significance test** with DeLong / bootstrap, **transaction-cost-aware backtest**, walk-forward, multi-resolution sentiment, sector-aware news routing, class re-weighting, 2020-2024 stress test.

## 29. References &mdash; 5 s

The anchors cited; the full bibliography is in the manuscript.

## 30. Thank you &mdash; 5 s

Thank you. Questions, please.

---

## Appendix slides &mdash; on demand only

A1 acronyms, A2/A3 glossaries, A4 improvement variant (tuned trees + extra sentiment features &mdash; stabilises XLE but does not break the AUC = 0.50 ceiling), A5 metric definitions. Pull these only if a question asks for them.

---

## Timing target

| Block | Slides | Target |
|---|---|---|
| Title + agenda | 1&ndash;2 | 20 s |
| Setup (motivation, hypotheses, related work) | 3&ndash;5 | 75 s |
| Methodology (pipeline, data, indicators, sectors, FinBERT) | 6&ndash;10 | 80 s |
| EDA + experimental design + training | 11&ndash;14 | 50 s |
| **Results + ROC/confusion + uplift + importance + hypotheses** | 15&ndash;20 | **170 s** |
| **Honest interpretation + literature** | 21&ndash;22 | **75 s** |
| Live demo | 23 | 20 s |
| **Discussion + limitations + trading + conclusions** | 24&ndash;27 | **135 s** |
| Future work + refs + thanks | 28&ndash;30 | 25 s |
| **Total** | | **~10 min** |

The results-and-conclusions blocks together take ~6.5 minutes &mdash; roughly two thirds of the talk, as intended.
