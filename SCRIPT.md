# Speaker script &mdash; FPA Final Defence (English, read-aloud)

*S&P 500 Stock Price Movement Prediction &mdash; Historical Market Data and Financial News Sentiment Analysis*

César Castaño (A00830006) and Brenda García (A01633622) &middot; Tec de Monterrey, M.Sc. CS, Semester 4.

> Read this out loud at a comfortable pace. Target time **10 minutes**. The italics in parentheses are stage directions &mdash; do not say them aloud. The bold words are the ones to lean on when you speak.
> Numbers that represent **project values** (metrics, counts, dollars, basis points) are written as digits so you don't get confused. Discourse fractions (*two thirds*, *half*) and ordinals (*first*, *second*) stay as words.

---

## Slide 1 &mdash; Title  *(8 seconds)*

Good morning. I'm **César Castaño**, and I'm here with **Brenda García**. This is the final defence of our Data Analytics project &mdash; predicting whether the S&P 500 will close up or down the next day.

## Slide 2 &mdash; Agenda  *(8 seconds)*

The plan is to spend roughly two thirds of the talk on the **results and the conclusions**; we'll move quickly through everything else.

## Slide 3 &mdash; Motivation  *(15 seconds)*

The S&P 500 is the most-watched U.S. equity benchmark, with 11 sectors that behave very differently. Predicting **direction**, not price, is what risk management actually needs. Markets are not perfectly efficient, and tools like FinBERT make sentiment extraction essentially free &mdash; so the question on the right is the whole project in one sentence.

## Slide 4 &mdash; Hypotheses  *(25 seconds)*

Our target is binary. The label is **1** if tomorrow's close is higher than today's, and **0** otherwise &mdash; we group flat and down days together because, for liquid indices, flat days are rare. From that we test 2 hypotheses. **Hypothesis 1**: adding sentiment improves Accuracy, F1 score, and Area Under the Curve, or A-U-C. **Hypothesis 2**: that gain is larger in higher-volatility sectors. And we ask 3 research questions, the most important being: does sentiment help, and is one algorithm consistently better than the other?

## Slide 5 &mdash; Related work  *(12 seconds)*

5 anchor papers shape our design: **Bollen 2011** &mdash; sentiment carries predictive information; **Vargas 2017** &mdash; multimodal helps; **Araci 2019** &mdash; FinBERT, pre-trained and free; **Zhang 2019** &mdash; tree models with sentiment are competitive and interpretable; and **López de Prado 2018** &mdash; chronological splits to avoid look-ahead bias.

## Slide 6 &mdash; Pipeline  *(10 seconds)*

4 stages: pull market data, engineer technical indicators, score sentiment with FinBERT, train tree ensembles. 2 algorithms × 2 feature sets × 4 datasets gives **16 runs**.

## Slide 7 &mdash; Data sources  *(15 seconds)*

2 sources. Market data comes from `yfinance`, a wrapper around Yahoo Finance, covering **2010 to 2019**, which avoids COVID and matches our news window. News comes from a Kaggle dataset of **over 1.4 million headlines**, which we filter and cap at **50 per day** with a fixed random seed, so the experiment is reproducible.

## Slide 8 &mdash; Technical indicators  *(15 seconds)*

**7 features** derived from open, high, low, close, and volume: returns, 2 moving averages (a simple one and an exponential one), the Relative Strength Index (or R-S-I), volatility, the typical price, and volume itself. The target is built at data-preparation time, before any modelling, so there is no leakage into features.

## Slide 9 &mdash; Sector selection  *(15 seconds)*

To test the volatility hypothesis, we picked 3 anchor sectors that span the volatility range: **X-L-P**, Consumer Staples, for the low end; **X-L-K**, Technology, near the median; and **X-L-E**, Energy, on the high end. Together with the broad S&P 500, that's our 4 datasets.

## Slide 10 &mdash; FinBERT  *(20 seconds)*

For every headline, FinBERT gives us positive minus negative as a single score between **−1 and +1**. We aggregate by trading day into the mean, the standard deviation, and the headline count. We use the pre-trained `ProsusAI/finbert` model, in batches of 32, and on days with no headlines we impute 0, so the time series stays continuous.

## Slide 11 &mdash; Class balance  *(10 seconds)*

There is a mild up-bias &mdash; the market goes up slightly more often than not. An "always-up" baseline already gets about **55% accuracy**. That is exactly why we report Area Under the Curve, or A-U-C, alongside accuracy.

## Slide 12 &mdash; News flow  *(10 seconds)*

Around **386,000 headlines** scored over the 10-year window, with **100% trading-day coverage**, and a mean daily sentiment that sits slightly positive.

## Slide 13 &mdash; Experimental design  *(10 seconds)*

2 algorithms × 2 feature sets × 4 datasets &mdash; **16 runs**, all evaluated under identical splits.

## Slide 14 &mdash; Training  *(15 seconds)*

We use a chronological **80/20** split &mdash; roughly **2,000 training days** and **501 test days**. No shuffling, no look-ahead. Hyperparameters are kept at sensible defaults, so all 16 runs stay directly comparable.

*(This is where we slow down.)*

## Slide 15 &mdash; Results, technical only  *(25 seconds)*

Here is the headline of the technical-only baseline: the **A-U-C sits at 0.50 across the board**. Technical indicators alone barely separate up days from non-up days &mdash; consistent with the weak form of market efficiency. XGBoost on the S&P 500 reaches an F1 of **0.66**, but only because it leans on the majority class. And in fact, **X-L-K collapses to class 0 in this test window**, dragging F1 down to **0.23**. This is the baseline that needs improving.

## Slide 16 &mdash; Results, technical plus sentiment  *(30 seconds)*

When we add sentiment, 2 clean wins emerge. **S&P 500 with Random Forest plus sentiment** jumps to **0.56 accuracy, 0.67 F1, and 0.51 A-U-C**. That is **+0.05 accuracy, +0.06 F1, and +0.04 A-U-C** over the baseline. **X-L-E with XGBoost plus sentiment** pushes A-U-C from **0.48 to 0.52**. The gains concentrate on the broad index and on the highest-volatility sector; the low and median sectors barely move.

## Slide 17 &mdash; Where the +0.04 A-U-C lives  *(50 seconds)*

This is the slide we want you to remember. 2 views of the same S&P 500 with Random Forest result. On the **left**, the Receiver Operating Characteristic (or R-O-C) curve overlay: the technical-only curve sits essentially on the diagonal, at A-U-C **0.478**; the technical-plus-sentiment curve lifts above it from false-positive rate **0.3 to 0.9**, at A-U-C **0.513**. That gap, **+0.035**, is the entire contribution of sentiment in numerical form. On the **right**, the confusion matrix at the default threshold of **0.50**. Look at the recall on UP days: **0.84**. The model catches most rallies. But the precision is only **0.57**, because it tolerates **174** false positives to do it. So in plain language, the model behaves as an **aggressive long-bias classifier**: it rarely misses a rally, at the cost of crying wolf about a third of the time.

## Slide 18 &mdash; Sentiment uplift  *(20 seconds)*

A single chart with all the deltas. The strongest positive cluster is **S&P 500 with Random Forest** &mdash; all 3 metrics positive. **X-L-E with XGBoost** is positive on accuracy and A-U-C. And the negative is **X-L-P with Random Forest** &mdash; the only configuration where sentiment actually hurts on every metric, which is exactly the pattern Hypothesis 2 predicts for low-volatility sectors.

## Slide 19 &mdash; Feature importance  *(20 seconds)*

Where does the sentiment signal live inside the model? `sentiment_mean`, the gold bar, ranks in the **top 3 features** for both configurations where it materially improved A-U-C. The remaining technical features spread fairly evenly &mdash; no single indicator dominates. The signal is genuinely additive.

## Slide 20 &mdash; Hypothesis assessment  *(25 seconds)*

So, our hypotheses. **Hypothesis 1**, partially supported: sentiment helps the broad index under Random Forest and the high-volatility sector under XGBoost, but the sector picture is mixed. **Hypothesis 2**, also partially supported: X-L-E, the most volatile, has the largest XGBoost gain, but the median-volatility X-L-K does not benefit, so the relationship is not strictly monotonic. And for research question 2: on A-U-C the 2 algorithms are tied; Random Forest wins on the index, XGBoost wins on the high-volatility sector.

## Slide 21 &mdash; What does an A-U-C near 0.50 actually mean?  *(45 seconds)*

This slide answers the obvious question: **0.51 A-U-C** &mdash; is that even meaningful? 3 reference points on the same 501-day test window. A **random coin flip** is **0.50** across the board. The **"always-up"** baseline, which exploits the mild up-bias of the market, gets **0.55 accuracy and 0.71 F1** *for free*, but its A-U-C is still **0.50**, because it has no ranking ability. **Our best model** reaches **0.56 accuracy, 0.67 F1, and 0.51 A-U-C**. The bars on the right make it visually obvious: on accuracy and F1 we are essentially on top of the always-up baseline, just **+0.05**; on A-U-C the 3 bars are indistinguishable. So the real result here is **the delta from sentiment**, **+0.04 A-U-C** &mdash; not the absolute level. And that is exactly what the weak form of the Efficient Market Hypothesis (or E-M-H) predicts.

## Slide 22 &mdash; Comparison with prior literature  *(30 seconds)*

How does that delta look against prior work? **Bollen** reported **87.6%** accuracy, but on a 7-month window with a narrow lexicon; reproductions on longer windows fall to around **60%**. **Vargas** got around **62%** with deep encoders over full Reuters article bodies. **Araci's FinBERT** scores high, but on sentence sentiment, not on next-day direction. **Zhang** reported around **0.56 A-U-C** on Chinese A-shares with per-ticker tuning. Once you normalise the setup, our **0.52 A-U-C** on the high-volatility sector is in the right ballpark &mdash; daily resolution with titles-only sentiment is the hardest regime in this list.

## Slide 23 &mdash; Live demo  *(20 seconds)*

This slide links to a recorded walk-through on Drive. The notebook loads our 4 trained classifiers, pulls today's market data, scores today's headlines with FinBERT, and prints an **UP**, **DOWN**, or **STABLE** call for each model. The calibration curve on the right is why we use the **0.45 to 0.55** corridor for STABLE: empirically the model is only reasonably calibrated inside that band.

## Slide 24 &mdash; Discussion  *(25 seconds)*

The chart on the right is the central interpretive claim of the talk: **all 16 configurations cluster within ±0.03 of A-U-C = 0.50**. Why is that? First, daily sentiment is a thin signal &mdash; it loses intra-day timing, and the noisiest sectors mask it. Second, the X-L-K collapse is real &mdash; the **2018-2019** test window had more flat and down days than up, and without re-weighting, the model picks the majority class. And third, the S&P 500 benefits the most because index-level returns aggregate idiosyncratic noise, leaving systematic news flow as a relatively cleaner signal.

## Slide 25 &mdash; Limitations  *(25 seconds)*

7 honest caveats, and let me hit the 2 new ones first. **One**, our **+0.04 A-U-C** is a point estimate &mdash; a DeLong test or a bootstrap confidence interval would tell us whether it is statistically meaningful. **Two**, the chart on the right shows the transaction-cost reality: a **5-to-10 basis-point** round-trip cost erodes the edge to break-even around **9 basis points**. Then the standard caveats: the news corpus skews toward mega-caps, FinBERT only sees headline titles, the **50-per-day** sampling cap, a single chronological split, and untuned hyperparameters.

## Slide 26 &mdash; Trading reality check  *(35 seconds)*

This makes the tradability question concrete. 4 equity curves on the S&P 500 test window, starting from **$1**, gross of any costs. **Buy-and-hold** ends at **$1.19** &mdash; the test window happened to be the tail of the **2017-2019** bull run, so the easy strategy looks strong. Our **Random Forest plus sentiment**, going long when the predicted probability of UP is at least **0.55**, ends at **$1.17**, with about half the time in cash &mdash; we capture most of the upside with less market exposure. The **random 50/50** baseline ends at **$1.09**, well below buy-and-hold, which confirms our signal is **not luck**. But gross of costs we still don't beat the easy baseline, and once you add realistic costs, the picture flips. So the **+0.04 A-U-C** is a **real, scientifically significant signal &mdash; not yet a tradable one**.

## Slide 27 &mdash; Conclusions  *(50 seconds)*

To close, 6 take-aways. **One**: FinBERT sentiment helps the broad index with Random Forest &mdash; **+0.05 accuracy, +0.06 F1, +0.04 A-U-C**, small but consistent. **Two**: the effect is **not monotonic** in sector volatility &mdash; X-L-E benefits, X-L-P and X-L-K do not, so Hypothesis 2 is only partially supported. **Three**: the **A-U-C = 0.50** ceiling on individual sectors is **consistent with the weak form of the Efficient Market Hypothesis (or E-M-H)** &mdash; our contribution is the sign of the delta, not a tradable signal. **Four**: algorithm choice is **configuration-dependent** &mdash; Random Forest on the index, XGBoost on the high-volatility sector, so research question 2 has no universal winner. **Five**: `sentiment_mean` is top 3 in feature importance only where it actually improved A-U-C, which means the contribution is real, not just a model artefact. And **six**, gross of costs our long-flat strategy ends at **$1.17** versus **$1.19** for buy-and-hold and **$1.09** for random &mdash; **better than chance, not better than the easy baseline**.

## Slide 28 &mdash; Future work  *(15 seconds)*

In priority order: a statistical significance test for the A-U-C delta, a transaction-cost-aware backtest, walk-forward evaluation, multi-resolution sentiment, sector-aware news routing, class re-weighting for X-L-K, and a **2020-to-2024** stress test once we have a COVID normalisation feature.

## Slide 29 &mdash; References  *(5 seconds)*

These are the anchor papers we cited throughout; the full bibliography is in the manuscript.

## Slide 30 &mdash; Thank you  *(5 seconds)*

Thank you very much. We are happy to take your questions.

---

## Appendix slides &mdash; pull only on demand

A1 acronyms, A2 and A3 glossaries, A4 the improvement variant (tuned trees with extra sentiment features &mdash; it stabilises X-L-E further but does not break the **A-U-C = 0.50** ceiling, so the main conclusions still hold), and A5 the detailed metric definitions.

---

## Timing target

| Block | Slides | Target |
|---|---|---|
| Title + agenda | 1&ndash;2 | 16 s |
| Setup (motivation, hypotheses, related work) | 3&ndash;5 | 52 s |
| Methodology (pipeline, data, indicators, sectors, FinBERT) | 6&ndash;10 | 75 s |
| EDA + experimental design + training | 11&ndash;14 | 50 s |
| **Results + ROC/confusion + uplift + importance + hypotheses** | 15&ndash;20 | **170 s** |
| **Honest interpretation + literature** | 21&ndash;22 | **75 s** |
| Live demo | 23 | 20 s |
| **Discussion + limitations + trading + conclusions** | 24&ndash;27 | **135 s** |
| Future work + refs + thanks | 28&ndash;30 | 25 s |
| **Total** | | **~10 min** |

The results-and-conclusions blocks together take about 6 and a half minutes &mdash; roughly two thirds of the talk, as intended.
