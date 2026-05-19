# Speaker script &mdash; FPA Final Defence

*S&P 500 Stock Price Movement Prediction &mdash; Historical Market Data and Financial News Sentiment Analysis*

Authors: **César Castaño (A00830006)** &middot; **Brenda García (A01633622)** &middot; Tec de Monterrey, M.Sc. CS, Semester 4.

> Tone: confident, conversational, ~30&ndash;45 seconds per slide on average.
> *Italic lines* are inline connectors &mdash; say them while clicking forward.

---

## 1. Title slide

Good morning. My name is **César Castaño**, and joining me is **Brenda García**. We are presenting the final defence of our Data Analytics project for the M.Sc. in Computer Science at Tec de Monterrey. The project asks a very specific question: can financial-news sentiment, on top of standard technical indicators, help us predict the **next-day direction** of the S&P 500 and its sectors?

*Let me start by laying out where we are taking you.*

## 2. Agenda

The talk has ten beats. We will spend roughly two thirds of the time on the **methodology** &mdash; framing, data, FinBERT, and experimental design &mdash; and the final third on **results, discussion, and what we would do next**. There is also a live demo near the end where the trained models call tomorrow's direction in real time.

*Let's start with why this question is worth asking.*

## 3. Motivation

The S&P 500 is the most-watched benchmark of U.S. equity health, and its **eleven GICS sectors** behave very differently in volatility and news flow. We are not trying to predict prices &mdash; we are predicting **direction**, which is exactly what matters for risk management and tactical allocation. Markets are not perfectly efficient: behavioural biases and delayed information processing leave room for signal. And on top of that, recent NLP &mdash; specifically **FinBERT** &mdash; makes it cheap to extract structured sentiment from financial text. So the natural question is on the right: does adding sentiment beat a technical-only baseline, and does that gain grow with sector volatility?

*That question splits into two formal hypotheses.*

## 4. Problem statement and hypotheses

The target is binary: **1 if tomorrow's close is above today's, 0 otherwise**. Flat days &mdash; which are rare for liquid indices &mdash; we group with class zero because they are not an upward trend.

We test two hypotheses. **H1**: adding FinBERT-derived sentiment improves Accuracy, F1, and AUC over the technical-only baseline. **H2**: that gain is **larger for higher-volatility sectors**. Three research questions follow from this: does sentiment help, Random Forest or XGBoost, and does sector volatility modulate the benefit.

*Before we go into our pipeline, here is the short tour of the prior work that shaped these choices.*

## 5. Related work

Five anchor references frame our design. **Bollen 2011** showed Twitter mood predicts the Dow with high accuracy &mdash; sentiment does carry predictive information. **Vargas 2017** showed multimodal models on Reuters news beat single-modality baselines, but at significant compute cost. **Araci 2019** released **FinBERT**, which is the state of the art for short-form financial sentiment and ships pre-trained &mdash; we just plug it in. **Zhang 2019** showed that XGBoost with sentiment is competitive with deep models while staying interpretable &mdash; that is exactly why we picked tree ensembles. And **López de Prado 2018** is the source of our **chronological splits** and the look-ahead-bias controls we will discuss in a moment.

*Here is what the pipeline looks like end-to-end.*

## 6. End-to-end methodology

Four stages, left to right. **First**, daily OHLCV from `yfinance` for ten years, 2010 to 2019. **Second**, we engineer the technical indicators and build the binary target. **Third**, we run headline-level FinBERT and aggregate to a daily sentiment score. **Fourth**, we train Random Forest and XGBoost, both with and without sentiment. That last step is what gives us the sixteen experimental runs we will report.

*Let's unpack the data first.*

## 7. Data sources

Two sources. On the **left**, market data: `yfinance` for the S&P 500 index and the eleven GICS sector ETFs. We restrict to **January 2010 through December 2019** &mdash; this avoids COVID distortions and matches the news coverage window. On the **right**, financial news from Kaggle's "Analyst Ratings Processed" dataset: over 1.4 million headlines across 6,000 tickers, with date, headline, and stock. We filter to S&P 500 tickers and the same time window, and to bound FinBERT inference cost we sample up to **50 headlines per day**, with a fixed `random_state` so the experiment is fully reproducible. The block at the bottom lists our validation steps: missing rows dropped, duplicates removed, calendar alignment, and **neutral sentiment imputed when a trading day has no headlines**.

*Now the seven features we extract from those raw bars.*

## 8. Technical indicators

Seven indicators from OHLCV. **Returns** is our momentum baseline. **SMA-10** and **EMA-10** capture trend &mdash; the exponential moving average reacts faster to recent moves. **RSI** is Wilder's 14-period overbought/oversold oscillator. **Volatility** is a ten-day rolling standard deviation of returns. **HLC3** is the typical-price proxy, and we keep raw **volume** as the activity signal. The target &mdash; one if tomorrow's close exceeds today's &mdash; is computed once, at data-prep time, before any modelling, so it can never leak into features.

*To test H2 we need datasets of very different volatility profiles.*

## 9. Volatility-based sector selection

This chart shows the annualised volatility of the eleven sector ETFs over our window. We pick three anchor sectors that span the range cleanly: **XLP, Consumer Staples**, the low-volatility extreme; **XLK, Technology**, near the median; and **XLE, Energy**, the high-volatility extreme. Together with the broad **SP500** index, that gives us four datasets covering very different signal-to-noise regimes.

*Now the sentiment side of the pipeline.*

## 10. Sentiment pipeline &mdash; FinBERT

For every headline, FinBERT returns positive, negative, and neutral probabilities. We collapse that to a single number per headline: **positive minus negative**, bounded in minus-one to plus-one. We then aggregate per trading day into the **mean sentiment**, the **standard deviation**, and the **headline count** &mdash; that count becomes news volume in some of our later experiments. Implementation-wise, we use `ProsusAI/finbert` from Hugging Face in batches of 32, weighted by label confidence, and days without headlines are imputed as neutral so the time series stays continuous.

*Before we talk results, two short EDA slides.*

## 11. EDA &mdash; target class balance

There is a **mild but consistent up-bias** &mdash; an "always up" baseline already scores around fifty-five percent accuracy. That is exactly why we report **AUC** alongside accuracy and F1: AUC is threshold-free and immune to the class-balance trick.

*And on the news side&hellip;*

## 12. EDA &mdash; news flow and sentiment distribution

Around 386,000 headlines scored over the ten-year window, sampling up to 50 per trading day. Coverage hits one hundred percent of trading days, and mean daily sentiment sits slightly positive &mdash; plus 0.03 &mdash; with a sigma of 0.17. So sentiment is mostly mild, but it is consistently available.

*With data and features in hand, here is the experimental matrix.*

## 13. Experimental design

Two algorithms &mdash; **Random Forest** and **XGBoost**. Two feature sets &mdash; **technical only** with seven features, and **technical plus `sentiment_mean`** with eight. Four datasets &mdash; **SP500**, plus the low/median/high volatility sectors. That is **sixteen experimental runs**, evaluated under identical splits and metrics.

*A word on how we train and score them.*

## 14. Training protocol and evaluation

Two key choices. **First, a chronological 80/20 split**: roughly 2,000 train days and 501 test days, with no shuffling, so no look-ahead. **Second, three metrics**: Accuracy, F1, and **AUC**. We need all three because a trivial "always up" model can post 0.55 accuracy and 0.70 F1 while having AUC at 0.50 &mdash; pure randomness. Reporting AUC alongside is what protects us from false confidence. Hyperparameters are kept at sensible defaults so all sixteen runs stay directly comparable.

*Now the results &mdash; first the technical-only baseline.*

## 15. Results &mdash; technical features only

The headline: **AUC clusters around 0.50** across the board. So technical indicators alone barely separate up days from non-up days &mdash; consistent with weak-form market efficiency. XGBoost on SP500 reaches an F1 of 0.66, but only because it leans heavily on the majority class. And **XLK actually collapses to class zero** in this test window, dragging F1 down to 0.23 / 0.27. This is the baseline we need sentiment to improve on.

*Now the same runs with FinBERT sentiment added.*

## 16. Results &mdash; technical + sentiment

Two clear wins. **SP500 with Random Forest plus sentiment** jumps to **0.56 Accuracy, 0.67 F1, and 0.51 AUC** &mdash; that is plus 0.05 accuracy, plus 0.06 F1, and plus 0.04 AUC over the baseline. **XLE with XGBoost plus sentiment** moves AUC from 0.48 to **0.52**. Notice though: the gains concentrate on the broad index and on the highest-volatility sector. The low and median sectors are largely unmoved.

*Before the uplift chart, two diagnostic plots make the SP500 + RF + sentiment story concrete.*

## 17. Where the +0.04 AUC lives &mdash; ROC and confusion matrix

Two views of the same SP500 + Random Forest result. On the **left**, the ROC overlay: the **technical-only** curve (blue) sits essentially on the diagonal (AUC 0.478); the **technical + sentiment** curve (gold) lifts above it in the false-positive-rate range 0.3 to 0.9 (AUC 0.513). That gap, plus 0.035 in AUC, is the entire contribution of sentiment in numerical form. On the **right**, the confusion matrix at the default 0.5 threshold: **recall on UP days is 0.84** &mdash; the model catches most rallies &mdash; but precision is 0.57 because it tolerates 174 false positives to do it. So the model behaves as an **aggressive long-bias classifier**: it rarely misses an UP day, at the cost of crying wolf about a third of the time.

*And here is what that aggressiveness looks like across the four datasets.*

## 18. Sentiment uplift at a glance

This is the delta plot: every bar is the change in a metric when sentiment is added. The **strongest positive cluster is SP500 + Random Forest** across all three metrics, plus **XLE + XGBoost** on accuracy and AUC. The standout negative is **XLP under Random Forest** &mdash; the only configuration where sentiment hurts on every metric, which is exactly the pattern H2 predicts for low-volatility sectors.

*Where does that sentiment signal actually live inside the model?*

## 19. Feature importance

`sentiment_mean`, in gold, ranks in the **top three features** for the two configurations where it materially improved AUC &mdash; SP500 with Random Forest and XLE with XGBoost. Beyond that, importance is spread fairly evenly across the seven technical indicators &mdash; no single technical feature dominates. The signal is genuinely additive.

*Time to confront the hypotheses head-on.*

## 20. Hypothesis assessment

**H1** &mdash; sentiment helps &mdash; is **partially supported**: it works at the index level under Random Forest and at the high-volatility sector under XGBoost, but the sector-level picture is inconsistent. **H2** &mdash; higher volatility means larger gain &mdash; is also **partially supported**: XLE, the most volatile, shows the largest positive XGBoost delta, but the median-volatility XLK does not benefit, so the gradient is not strictly monotonic. And for **RQ2**, on AUC the two algorithms are tied: **Random Forest wins on the index**, **XGBoost wins on the high-volatility sector**.

*Before going on, let me address the obvious question: an AUC of 0.51 &mdash; is that even meaningful?*

## 21. What does an AUC ≈ 0.50 actually mean?

This slide answers that question honestly. We anchor our best run against two natural baselines on the same 501-day test window, with the **bar chart on the right** as a visual companion to the table on the left. **A random coin flip** sits at 0.50 accuracy, 0.50 F1, 0.50 AUC. The **"always-up"** rule, which exploits the mild up-bias of the market, gets accuracy 0.55 and F1 0.71 *for free* &mdash; but its AUC is still 0.50, because it has no ranking ability. **Our best model**, SP500 + Random Forest + sentiment, reaches 0.56 accuracy, 0.67 F1, 0.51 AUC. The bars make it visually obvious: on Accuracy/F1 we are essentially **on top of the always-up baseline** (+0.05 / +0.06); on AUC the three bars are indistinguishable around 0.50. **The real result is the delta from sentiment** &mdash; plus 0.04 AUC &mdash; not the absolute level. That is exactly what the weak form of the Efficient Market Hypothesis predicts: daily price-only signals leave at most a marginal edge.

*Put differently &mdash; is that delta competitive with what the literature reports?*

## 22. Where do our results sit vs.\ prior literature?

Quick read of the table, top to bottom. **Bollen 2011** is famous for 87.6% accuracy on the Dow with Twitter mood, but on a seven-month window and a narrow lexicon &mdash; reproductions on longer windows fall to about 60%. **Vargas 2017** reports ~62% accuracy on the S&P 500 with deep encoders over full Reuters headline bodies; we use FinBERT on titles only, aggregated daily, which is a strictly harder setup. **Araci 2019** &mdash; FinBERT itself &mdash; scores F1 0.86 on the Financial Phrasebank, but that is **sentence-level sentiment**, not next-day direction; we test the downstream task. **Zhang 2019** gets AUC around 0.56 on Chinese A-shares with XGBoost + sentiment, but with per-ticker tuning; we keep defaults so all sixteen runs stay directly comparable. So **our 0.52 AUC on the high-volatility sector is the right order of magnitude** once you normalise the setup &mdash; daily resolution with headline-only sentiment is the hardest regime in this comparison.

*Now I can show you the live system before we synthesise.*

## 23. Live demo

This slide links to a recorded walk-through on Drive. The Colab notebook loads our four trained classifiers, pulls today's OHLCV from `yfinance`, rebuilds the seven indicators in real time, fetches today's Yahoo Finance headlines, scores them with FinBERT, aggregates the daily sentiment, and prints an **UP / DOWN / STABLE** call from each model. The **calibration plot on the right** justifies the 0.45-to-0.55 corridor we use to flag "stable / uncertain" predictions: empirically the model is reasonably calibrated only inside that band, and our predictions cluster there, so collapsing to a UP/DOWN/STABLE call rather than to a raw probability is the honest thing to do. If we have time, we can play the recording at the end; otherwise the QR-equivalent link is on the slide.

*What does all of this actually mean?*

## 24. Discussion

The chart on the right makes our central interpretive claim visible: **all 16 configurations sit within plus-or-minus 0.03 of AUC = 0.50** &mdash; the line is the EMH ceiling. The colour, not the level, is what carries the story. Four reads. **First**, AUC near 0.50 lines up with the weak form of the Efficient Market Hypothesis &mdash; price-only signals give at most a marginal edge. **Second**, daily-aggregated sentiment is a thin signal: it loses intra-day timing, and the noisiest sectors mask it. **Third**, the XLK class collapse is real: the 2018-2019 test window had more flat/down than up days, and without re-weighting the model takes the easy route. **Fourth**, the reason SP500 benefits the most is that index-level returns **aggregate idiosyncratic noise**, leaving systematic news flow as a cleaner signal.

*We are also honest about where this study is limited.*

## 25. Limitations

Seven honest caveats &mdash; I will hit the two new ones first, and the chart on the right is the visual case for one of them. **First**, we report the plus-0.04 AUC delta as a **point estimate**: a DeLong test or bootstrap confidence interval on the 501-day test set is needed to confirm it is not noise. **Second**, even if accuracy holds at plus-five percent, the chart on the right shows that a 5-to-10 basis-point round-trip transaction cost erodes the edge to break-even around 9 bp on a daily long/flat strategy &mdash; our results are **scientific, not yet tradable**. Then the standard ones: Kaggle news corpus **skews toward mega-caps**; FinBERT scores **headlines only**; the fifty-headlines-per-day cap is a **compute-driven compromise**; we use a **single chronological split** &mdash; a walk-forward backtest would be stronger evidence; and hyper-parameters are kept at defaults so all sixteen runs stay directly comparable.

*The next slide makes the tradability claim concrete with an actual equity curve.*

## 26. Trading reality check

Four equity curves on the SP500 test window, all starting from one dollar, gross of any transaction costs. **Always-long buy-and-hold** ends at \$1.19 &mdash; the test window happened to be the tail of the 2017-2019 bull run, so the easy strategy looks strong. Our **Random Forest plus sentiment**, going long only when the probability of UP is at least 0.55, ends at \$1.17, while spending roughly half the time in cash &mdash; the model is **capturing most of the upside with less market exposure**. Loosening the threshold to 0.50 gives \$1.15. The **random 50/50 daily** baseline ends at \$1.09 &mdash; well below buy-and-hold &mdash; which confirms that our model is **not** just luck. But notice: gross of costs, we still do not beat buy-and-hold; adding even 5-to-10 basis-point round-trip costs from the previous slide flips the picture against us. So the plus-0.04 AUC is a **real, scientifically significant signal**, but it is not yet a tradable one.

*With that picture in mind, here is what we conclude.*

## 27. Conclusions

Three take-aways. **One**, FinBERT headline sentiment **helps at the index level** when paired with Random Forest: plus 0.05 accuracy, plus 0.06 F1, plus 0.04 AUC over the technical-only baseline &mdash; small but consistent. **Two**, the sentiment effect is **not monotonic** in sector volatility &mdash; high-vol XLE benefits, low-vol XLP does not, and median-vol XLK also fails to benefit, so H2 is only partially supported. **Three**, the AUC-equals-0.50 ceiling on individual sectors is **consistent with the weak form of EMH** &mdash; the contribution of this work is the **sign and direction** of the delta from sentiment, not a tradable signal. Said honestly: the model is *slightly* better than always-up; it confirms sentiment carries information without breaking the daily-resolution ceiling.

*Which leads directly into the future work.*

## 28. Future work

Seven concrete next steps, in priority order. **Statistical significance** &mdash; DeLong test and bootstrap CIs on the plus-0.04 AUC delta. **Transaction-cost-aware backtest** of SP500 + RF + sentiment as a long/flat signal net of 5-to-10 basis-point costs. **Walk-forward evaluation** with expanding training windows. **Multi-resolution sentiment** &mdash; daily aggregates paired with K-day moving averages and event-time deltas. **Sector-aware news routing**, weighting each headline by its issuer's sector weight. **Class re-weighting** to fix XLK's collapse onto the majority class. And finally a **2020-to-2024 out-of-sample stress test** once we add a COVID-normalisation feature.

*Quick pointer to the papers we built on.*

## 29. Selected references

These are the anchors we cited throughout the talk &mdash; Bollen, Vargas, Araci's FinBERT, Zhang, López de Prado, plus Breiman and Chen-Guestrin for the algorithms, Fama for EMH, and Mostafavi 2025 for the technical-indicator menu. The full bibliography is in the manuscript.

*And with that&hellip;*

## 30. Thank you

Thank you. We are happy to take questions.

---

## Appendix &mdash; on demand

The appendix slides are not part of the main delivery; pull them up only if a question asks for definitions, the improvement variant, or the exact metric formulas.

### A1. Acronyms

> *"For reference &mdash; every acronym used in the talk."* Skim only if asked.

### A2. Glossary 1/2 &mdash; finance and indicators

> *"S&P 500, GICS, OHLCV, RSI, EMH, HLC3, volatility &mdash; the financial-side definitions."* Useful if a non-finance member of the committee asks for clarification.

### A3. Glossary 2/2 &mdash; NLP and machine learning

> *"FinBERT, target definition, Random Forest, XGBoost, chronological split, precision/recall/F1, AUC-ROC, look-ahead bias."* Use if asked how we built or evaluated the models.

### A4. Improvement variant

> *"We did explore a tuned variant &mdash; more estimators, deeper trees, class-balanced weights, plus `sentiment_std` and `news_volume`. It stabilises XLE further but does not break the AUC-equals-0.50 ceiling, so the main conclusions hold."*

### A5. Detailed metric definitions

> *"Here are the exact formulas behind Accuracy, Precision, Recall, F1, and AUC-ROC. The key point is that an always-up classifier hits 0.55 accuracy and 0.71 F1 with AUC at 0.50 &mdash; which is why we report all three."*

---

## Timing target

| Block | Slides | Target |
|---|---|---|
| Setup (motivation, hypotheses, related work) | 3&ndash;5 | ~3 min |
| Methodology (pipeline, data, indicators, volatility, FinBERT) | 6&ndash;10 | ~5 min |
| EDA + experimental design + training | 11&ndash;14 | ~3 min |
| Results + ROC / confusion + uplift + feature importance + hypothesis check | 15&ndash;20 | ~4.5 min |
| Honest interpretation + literature comparison | 21&ndash;22 | ~2 min |
| Live demo + calibration | 23 | ~1.5 min |
| Discussion + limitations + trading check + conclusions + future work | 24&ndash;28 | ~4 min |
| References + close | 29&ndash;30 | ~1 min |
| **Total** | | **~24 min** |
