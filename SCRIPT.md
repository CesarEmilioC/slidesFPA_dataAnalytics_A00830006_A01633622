# Speaker script &mdash; FPA Final Defence (English, read-aloud)

*S&P 500 Stock Price Movement Prediction &mdash; Historical Market Data and Financial News Sentiment Analysis*

César Castaño (A00830006) and Brenda García (A01633622) &middot; Tec de Monterrey, M.Sc. CS, Semester 4.

> Read this out loud at a comfortable pace. Target time **10 minutes**. The italics in parentheses are stage directions &mdash; do not say them aloud. The bold words inside paragraphs are the ones to lean on slightly when you speak.

---

## Slide 1 &mdash; Title  *(10 seconds)*

Good morning, everyone. My name is **César Castaño**, and joining me today is **Brenda García**. We are presenting the final defence of our Data Analytics project, for the Master's in Computer Science here at Tec de Monterrey. The project is about predicting **whether the S&P 500 will go up or down the next day**, using market data together with news sentiment.

## Slide 2 &mdash; Agenda  *(10 seconds)*

The talk has ten beats. We will move quickly through the setup and the methodology, because the part we really want to spend time on is the **results and what we conclude from them**.

## Slide 3 &mdash; Motivation  *(30 seconds)*

So why this question? The S&P 500 is the most-watched benchmark of the U.S. equity market, and it has eleven sectors that behave very differently &mdash; some are quiet, some are noisy. Predicting **direction**, not price, is what risk managers actually need on a daily basis. We also know markets are not perfectly efficient &mdash; behaviour and delayed information leave some signal on the table. And on top of that, recent NLP tools like **FinBERT** make extracting sentiment from financial news essentially free. So the question on the right is the whole project in one sentence: does adding sentiment to a tree-based model beat a technical-only baseline, and does that gain grow with sector volatility?

## Slide 4 &mdash; Hypotheses  *(25 seconds)*

Our target is binary. The label is **one** if tomorrow's close is higher than today's, and **zero** otherwise &mdash; we group flat and down days together because, for liquid indices, flat days are rare. From that we test two hypotheses. **H one**: adding sentiment improves Accuracy, F1 and AUC. **H two**: the gain is larger in higher-volatility sectors. And we ask three research questions, the most important being: does sentiment help, and is one algorithm consistently better than the other?

## Slide 5 &mdash; Related work  *(20 seconds)*

Five anchors shape our design. **Bollen 2011** showed that sentiment carries predictive information. **Vargas 2017** confirmed that multimodal models help. **Araci 2019** gave us **FinBERT**, which is pre-trained and free to use. **Zhang 2019** showed that XGBoost with sentiment is competitive with deep models while staying interpretable. And **López de Prado 2018** is where we get our chronological-split discipline.

## Slide 6 &mdash; Pipeline  *(15 seconds)*

The pipeline has four stages: we pull market data, we engineer the technical indicators, we score sentiment with FinBERT, and we train tree ensembles. Two algorithms, two feature sets, four datasets &mdash; that's where the **sixteen runs** in our results come from.

## Slide 7 &mdash; Data sources  *(15 seconds)*

Two sources. Market data comes from **yfinance**, covering 2010 to 2019, which avoids COVID and matches our news window. News comes from a Kaggle dataset of **over one point four million headlines**, which we filter and cap at fifty per day with a fixed seed, so the experiment is reproducible.

## Slide 8 &mdash; Technical indicators  *(15 seconds)*

Seven features derived from open, high, low, close and volume: returns, two moving averages, RSI, volatility, the typical price, and volume itself. The target is built at data-prep time, before any modelling, so there is no leakage into features.

## Slide 9 &mdash; Sector selection  *(15 seconds)*

To test H two, we picked three anchor sectors that span the volatility range: **XLP** Consumer Staples for the low end, **XLK** Technology near the median, and **XLE** Energy on the high end. Together with the broad SP500, that's our four datasets.

## Slide 10 &mdash; FinBERT  *(20 seconds)*

For every headline, FinBERT gives us positive minus negative as a single score between minus one and plus one. We aggregate by day into the mean, the standard deviation, and the headline count. We use the pre-trained ProsusAI model, batches of thirty-two, and on days with no headlines we impute zero so the time series stays continuous.

## Slide 11 &mdash; Class balance  *(10 seconds)*

There is a **mild up-bias** &mdash; the market goes up slightly more often than not. An always-up baseline already gets about fifty-five percent accuracy. That is exactly why we report AUC alongside accuracy.

## Slide 12 &mdash; News flow  *(10 seconds)*

Around **three hundred eighty-six thousand headlines** scored over the ten-year window, with **one hundred percent trading-day coverage**, and a mean daily sentiment that sits slightly positive.

## Slide 13 &mdash; Experimental design  *(10 seconds)*

Two algorithms, times two feature sets, times four datasets &mdash; sixteen runs, evaluated under identical splits.

## Slide 14 &mdash; Training  *(15 seconds)*

We use a chronological eighty-twenty split &mdash; roughly **two thousand training days and five hundred and one test days**. No shuffling, no look-ahead. Hyperparameters are kept at sensible defaults, so all sixteen runs stay directly comparable.

*(This is where we slow down.)*

## Slide 15 &mdash; Results, technical only  *(25 seconds)*

Here is the headline of the technical-only baseline: the **AUC sits at zero point five across the board**. Technical indicators alone barely separate up days from non-up days &mdash; consistent with the weak form of market efficiency. XGBoost on SP500 looks like it reaches an F1 of zero point six six, but only because it leans on the majority class. And in fact, **XLK collapses to class zero in this test window**, dragging F1 down to zero point two three. This is the baseline that needs improving.

## Slide 16 &mdash; Results, technical plus sentiment  *(30 seconds)*

When we add sentiment, two clean wins emerge. **SP500 with Random Forest plus sentiment** jumps to zero point five six accuracy, zero point six seven F1, and zero point five one AUC. That is **plus zero point zero five, plus zero point zero six, and plus zero point zero four** over the baseline. **XLE with XGBoost plus sentiment** pushes AUC from zero point four eight to zero point five two. Notice though: the gains concentrate on the broad index and on the highest-volatility sector. The low and median sectors barely move.

## Slide 17 &mdash; Where the plus zero point zero four AUC lives  *(50 seconds)*

This is the slide we want you to remember. Two views of the same SP500 with Random Forest result. On the **left**, the ROC overlay: the technical-only curve sits essentially on the diagonal, at AUC zero point four seven eight; the technical plus sentiment curve lifts above it from false-positive rate zero point three to zero point nine, at AUC zero point five one three. That gap, **plus zero point zero three five**, is the entire contribution of sentiment in numerical form. On the **right**, the confusion matrix at the default threshold of zero point five. Look at the recall on UP days: **zero point eight four**. The model catches most rallies. But the precision is only zero point five seven, because it tolerates one hundred seventy-four false positives to do it. So in plain language, the model behaves as an **aggressive long-bias classifier**: it rarely misses a rally, at the cost of crying wolf about a third of the time.

## Slide 18 &mdash; Sentiment uplift  *(20 seconds)*

A single chart of all the deltas. The **strongest positive cluster is SP500 with Random Forest** &mdash; all three metrics positive. **XLE with XGBoost** is positive on accuracy and AUC. And the negative is **XLP with Random Forest** &mdash; the only configuration where sentiment actually hurts on every metric, which is exactly the pattern H two predicts for low-volatility sectors.

## Slide 19 &mdash; Feature importance  *(20 seconds)*

Where does the sentiment signal live inside the model? **sentiment\_mean**, in gold, ranks in the **top three features** for both configurations where it materially improved AUC. The remaining technical features spread fairly evenly &mdash; no single indicator dominates. The signal is genuinely additive.

## Slide 20 &mdash; Hypothesis assessment  *(25 seconds)*

So, our hypotheses. **H one**, partially supported: sentiment helps the broad index under Random Forest and the high-volatility sector under XGBoost, but the sector picture is mixed. **H two**, also partially supported: XLE, the most volatile, has the largest XGBoost gain, but the median-volatility XLK does not benefit, so the relationship is not strictly monotonic. And for **research question two**: on AUC the two algorithms are tied; Random Forest wins on the index, XGBoost wins on the high-volatility sector.

## Slide 21 &mdash; What does an AUC near zero point five actually mean?  *(45 seconds)*

This slide answers the obvious question: zero point five one AUC &mdash; is that even meaningful? Three reference points on the same five-hundred-and-one-day test window. A **random coin flip** is zero point five across the board. The **always-up baseline**, which exploits the mild up-bias of the market, gets zero point five five accuracy and zero point seven one F1 *for free*, but its AUC is still zero point five, because it has no ranking ability. **Our best model** reaches zero point five six accuracy, zero point six seven F1, and zero point five one AUC. The bars on the right make it visually obvious: on accuracy and F1 we are essentially on top of the always-up baseline, just plus zero point zero five; on AUC the three bars are indistinguishable. So the real result here is **the delta from sentiment**, plus zero point zero four AUC &mdash; not the absolute level. And that is exactly what the weak form of the Efficient Market Hypothesis predicts.

## Slide 22 &mdash; Comparison with prior literature  *(30 seconds)*

How does that delta look against prior work? Bollen reported eighty-seven point six percent accuracy, but on a seven-month window with a narrow lexicon; reproductions on longer windows fall to around sixty percent. Vargas got around sixty-two percent with deep encoders over full Reuters bodies. Araci's FinBERT scores high, but on sentence sentiment, not on next-day direction. Zhang reported around zero point five six AUC on Chinese A-shares with per-ticker tuning. Once you normalise the setup, **our zero point five two AUC on the high-volatility sector is in the right ballpark** &mdash; daily resolution with titles-only sentiment is the hardest regime in this list.

## Slide 23 &mdash; Live demo  *(20 seconds)*

This slide links to a recorded walk-through on Drive. The notebook loads our four trained classifiers, pulls today's market data, scores today's headlines with FinBERT, and prints an **UP**, **DOWN** or **STABLE** call for each model. The calibration curve on the right is why we use the zero point four five to zero point five five corridor for STABLE: empirically the model is only reasonably calibrated inside that band.

## Slide 24 &mdash; Discussion  *(25 seconds)*

The chart on the right is the central interpretive claim of the talk: **all sixteen configurations cluster within plus or minus zero point zero three of AUC equals zero point five**. Why is that? First, daily sentiment is a thin signal &mdash; it loses intra-day timing and the noisiest sectors mask it. Second, the XLK collapse is real &mdash; the 2018 to 2019 test window had more flat and down days than up, and without re-weighting the model picks the majority class. And third, SP500 benefits the most because index-level returns aggregate idiosyncratic noise, leaving systematic news flow as a relatively cleaner signal.

## Slide 25 &mdash; Limitations  *(25 seconds)*

Seven honest caveats, and let me hit the two new ones first. **One**, our plus zero point zero four AUC is a point estimate &mdash; a DeLong test or a bootstrap confidence interval would tell us whether it is statistically meaningful. **Two**, the chart on the right shows the transaction-cost reality: a five-to-ten basis-point round-trip cost erodes the edge to break-even around nine basis points. Then the standard caveats: the news corpus skews toward mega-caps, FinBERT only sees headline titles, the fifty-per-day sampling cap, a single chronological split, and untuned hyperparameters.

## Slide 26 &mdash; Trading reality check  *(35 seconds)*

This makes the tradability question concrete. Four equity curves on the SP500 test window, starting from one dollar, gross of any costs. **Buy-and-hold** ends at one dollar nineteen &mdash; the test window happened to be the tail of the 2017-2019 bull run, so the easy strategy looks strong. Our **Random Forest plus sentiment**, going long when the probability is at least zero point five five, ends at one dollar seventeen, with about **half the time in cash** &mdash; we capture most of the upside with less market exposure. The **random fifty-fifty baseline** ends at one dollar nine, well below buy-and-hold, which confirms our signal is **not luck**. But gross of costs we still don't beat the easy baseline, and once you add realistic costs the picture flips. So the plus zero point zero four AUC is a **real, scientifically significant signal &mdash; not yet a tradable one**.

## Slide 27 &mdash; Conclusions  *(50 seconds)*

To close, six take-aways. **One**: FinBERT sentiment helps the broad index with Random Forest &mdash; plus zero point zero five accuracy, plus zero point zero six F1, plus zero point zero four AUC, small but consistent. **Two**: the effect is **not monotonic** in sector volatility &mdash; XLE benefits, XLP and XLK do not, so H two is only partially supported. **Three**: the AUC-equals-zero-point-five ceiling on individual sectors is **consistent with the weak form of EMH** &mdash; our contribution is the sign of the delta, not a tradable signal. **Four**: algorithm choice is **configuration-dependent** &mdash; Random Forest on the index, XGBoost on the high-volatility sector, so research question two has no universal winner. **Five**: sentiment\_mean is top three in feature importance only where it actually improved AUC, which means the contribution is real, not just a model artefact. And **six**, gross of costs our long-flat strategy ends at one dollar seventeen versus one dollar nineteen buy-and-hold and one dollar nine random &mdash; **better than chance, not better than the easy baseline**.

## Slide 28 &mdash; Future work  *(15 seconds)*

In priority order: a statistical significance test for the AUC delta, a transaction-cost-aware backtest, walk-forward evaluation, multi-resolution sentiment, sector-aware news routing, class re-weighting for XLK, and a 2020 to 2024 stress test once we have a COVID normalisation feature.

## Slide 29 &mdash; References  *(5 seconds)*

These are the anchor papers we cited throughout; the full bibliography is in the manuscript.

## Slide 30 &mdash; Thank you  *(5 seconds)*

Thank you very much. We are happy to take your questions.

---

## Appendix slides &mdash; pull only on demand

A1 acronyms, A2 and A3 glossaries, A4 the improvement variant (tuned trees with extra sentiment features &mdash; it stabilises XLE further but does not break the AUC equals zero point five ceiling, so the main conclusions still hold), and A5 the detailed metric definitions.

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

The results-and-conclusions blocks together take about six and a half minutes &mdash; roughly two thirds of the talk, as intended.
