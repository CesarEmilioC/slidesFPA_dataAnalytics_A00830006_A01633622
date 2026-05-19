"""Generates the prediction-based charts for the FPA deck.

Loads the trained models from ../FPA_dataAnalytics_finalRepository/models_demo/,
replays the chronological 80/20 split on the source feature CSVs to recover the
test-set predicted probabilities, then renders:

  - roc_sp500.png                 (slide 16 -- Results, technical + sentiment)
  - confusion_matrix_sp500.png    (slide 22 -- Live demo support)
  - calibration_sp500.png         (slide 22 -- justifies 0.45 / 0.55 corridor)
  - cumulative_returns_sp500.png  (slide 26 -- Future work / honest tradability)

Source of truth: trained models in models_demo/{DATASET}_models.joblib and the
per-dataset technical CSV in datasets_/{dataset_lower}_technical_features.csv,
plus datasets_/daily_sentiment_features.csv for the sentiment column.
"""
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn.metrics import roc_curve, auc, confusion_matrix
from sklearn.calibration import calibration_curve

# ---------------------------- Paths -----------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES_REPO = os.path.dirname(HERE)                              # FPA_dataAnalytics_finalPresentation
ROOT = os.path.dirname(SLIDES_REPO)                              # FPA_dataAnalytics_A00830006_A01633622
CODE_REPO = os.path.join(ROOT, 'FPA_dataAnalytics_finalRepository')
DATA_DIR = os.path.join(CODE_REPO, 'datasets_')
MODELS_DIR = os.path.join(CODE_REPO, 'models_demo')

# ---------------------------- Palette ---------------------------------------
BLUE      = '#0F3D60'
BLUE_DARK = '#082842'
GOLD      = '#C8A951'
GOLD_DARK = '#A88B3F'
GRAY      = '#4A4A4A'
GRAY_LT   = '#A8A8A8'
GREEN     = '#1B7A4B'
RED       = '#B23A48'
LIGHT     = '#F4F6F9'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size':   10.5,
    'axes.edgecolor': GRAY,
    'axes.labelcolor': GRAY,
    'xtick.color': GRAY,
    'ytick.color': GRAY,
    'axes.titlecolor': BLUE_DARK,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
})

# ---------------------------- Configuration ---------------------------------
FEATURES_TECH = ['Returns', 'SMA_10', 'EMA_10', 'RSI', 'Volatility', 'HLC3', 'Volume']
FEATURES_ALL  = FEATURES_TECH + ['sentiment_mean']
TRAIN_SPLIT = 0.8

# ---------------------------- Data loading ----------------------------------
def load_dataset(dataset_name):
    """Return (X_tech_test, X_all_test, y_test, close_test, dates_test)."""
    tech_path = os.path.join(DATA_DIR, f'{dataset_name.lower()}_technical_features.csv')
    df = pd.read_csv(tech_path, parse_dates=['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    sent = pd.read_csv(os.path.join(DATA_DIR, 'daily_sentiment_features.csv'),
                       parse_dates=['day'])
    sent = sent.rename(columns={'day': 'Date'})
    df = df.merge(sent[['Date', 'sentiment_mean']], on='Date', how='left')
    df['sentiment_mean'] = df['sentiment_mean'].fillna(0.0)

    df = df.dropna(subset=FEATURES_ALL + ['Target']).reset_index(drop=True)

    n = len(df)
    n_train = int(n * TRAIN_SPLIT)
    test = df.iloc[n_train:].reset_index(drop=True)

    return (
        test[FEATURES_TECH].values,
        test[FEATURES_ALL].values,
        test['Target'].values.astype(int),
        test['Close'].values.astype(float),
        test['Date'].values,
    )

def load_models(dataset_name):
    path = os.path.join(MODELS_DIR, f'{dataset_name}_models.joblib')
    return joblib.load(path)

def collect_probs(dataset_name='SP500'):
    X_tech, X_all, y, close, dates = load_dataset(dataset_name)
    models = load_models(dataset_name)
    probs = {
        'rf_tech':  models['rf_tech'].predict_proba(X_tech)[:, 1],
        'rf_all':   models['rf_all'].predict_proba(X_all)[:, 1],
        'xgb_tech': models['xgb_tech'].predict_proba(X_tech)[:, 1],
        'xgb_all':  models['xgb_all'].predict_proba(X_all)[:, 1],
    }
    return y, probs, close, dates

# ---------------------------- Chart 1: ROC overlay --------------------------
def plot_roc():
    y, p, _, _ = collect_probs('SP500')
    fpr_t, tpr_t, _ = roc_curve(y, p['rf_tech'])
    fpr_s, tpr_s, _ = roc_curve(y, p['rf_all'])
    auc_t = auc(fpr_t, tpr_t)
    auc_s = auc(fpr_s, tpr_s)

    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    ax.plot([0, 1], [0, 1], color=GRAY_LT, linestyle='--', lw=1, label='Random (AUC = 0.50)')
    ax.plot(fpr_t, tpr_t, color=BLUE, lw=2.2, label=f'RF Technical only  (AUC = {auc_t:.3f})')
    ax.plot(fpr_s, tpr_s, color=GOLD, lw=2.2, label=f'RF Tech + Sentiment (AUC = {auc_s:.3f})')
    ax.fill_between(fpr_s, fpr_s, tpr_s, where=(tpr_s >= fpr_s), color=GOLD, alpha=0.10)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel('False positive rate')
    ax.set_ylabel('True positive rate')
    ax.set_title('ROC curves -- SP500, Random Forest, 501-day test', pad=10)
    ax.legend(loc='lower right', frameon=False, fontsize=9.5)
    ax.text(0.04, 0.92,
            f'$\\Delta$AUC from sentiment = {auc_s - auc_t:+.3f}',
            ha='left', fontsize=11, color=BLUE_DARK, fontweight='bold')
    plt.tight_layout()
    out = os.path.join(HERE, 'roc_sp500.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}  (AUC tech={auc_t:.3f}, sent={auc_s:.3f})')

# ---------------------------- Chart 2: Confusion matrix ---------------------
def plot_confusion():
    y, p, _, _ = collect_probs('SP500')
    yhat = (p['rf_all'] >= 0.5).astype(int)
    cm = confusion_matrix(y, yhat)
    tn, fp, fn, tp = cm.ravel()
    total = cm.sum()

    fig, ax = plt.subplots(figsize=(5.5, 4.6))
    # Cell colours: blue gradient by count
    norm = cm / cm.max()
    for i in range(2):
        for j in range(2):
            colour_strength = norm[i, j]
            base_rgb = np.array([15, 61, 96]) / 255    # TecBlue
            white_rgb = np.array([244, 246, 249]) / 255  # TecLight
            cell_rgb = white_rgb + (base_rgb - white_rgb) * (0.30 + 0.55 * colour_strength)
            ax.add_patch(plt.Rectangle((j, 1-i), 1, 1, facecolor=cell_rgb, edgecolor='white', lw=2))

    labels = [['TN', 'FP'], ['FN', 'TP']]
    for i in range(2):
        for j in range(2):
            v = cm[i, j]
            pct = 100.0 * v / total
            txt_color = 'white' if norm[i, j] > 0.45 else BLUE_DARK
            ax.text(j + 0.5, 1 - i + 0.62, labels[i][j], ha='center', va='center',
                    fontsize=11, color=txt_color, fontweight='bold')
            ax.text(j + 0.5, 1 - i + 0.40, f'{v}',          ha='center', va='center',
                    fontsize=18, color=txt_color, fontweight='bold')
            ax.text(j + 0.5, 1 - i + 0.18, f'{pct:.1f}%',   ha='center', va='center',
                    fontsize=10, color=txt_color)

    ax.set_xlim(0, 2); ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5]); ax.set_xticklabels(['Predicted DOWN / 0', 'Predicted UP / 1'])
    ax.set_yticks([0.5, 1.5]); ax.set_yticklabels(['Actual UP / 1', 'Actual DOWN / 0'])
    ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title('Confusion matrix -- SP500 + RF + Sentiment ($t=0.50$)', pad=12)

    acc = (tp + tn) / total
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    f1 = 2 * prec * rec / max(prec + rec, 1e-9)
    ax.text(1.0, -0.18,
            f'Acc {acc:.3f}    P {prec:.3f}    R {rec:.3f}    F1 {f1:.3f}',
            ha='center', fontsize=10, color=BLUE_DARK)

    plt.tight_layout()
    out = os.path.join(HERE, 'confusion_matrix_sp500.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}  (acc={acc:.3f}, f1={f1:.3f})')

# ---------------------------- Chart 3: Calibration --------------------------
def plot_calibration():
    y, p, _, _ = collect_probs('SP500')
    frac_pos, mean_pred = calibration_curve(y, p['rf_all'], n_bins=8, strategy='quantile')

    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    ax.plot([0, 1], [0, 1], color=GRAY_LT, linestyle='--', lw=1, label='Perfect calibration')
    # Highlight the 0.45-0.55 "uncertain" corridor used by the live demo
    ax.axvspan(0.45, 0.55, color=GOLD, alpha=0.12, label='Demo ``uncertain\'\' corridor $[0.45,\\,0.55]$')
    ax.plot(mean_pred, frac_pos, color=BLUE, marker='o', lw=2, markersize=7,
            label='SP500 + RF + Sentiment')

    # Histogram of predictions, secondary axis
    ax2 = ax.twinx()
    ax2.hist(p['rf_all'], bins=20, color=BLUE, alpha=0.12, density=False)
    ax2.set_ylabel('# test days', color=GRAY, fontsize=9)
    ax2.spines['top'].set_visible(False)
    ax2.tick_params(axis='y', colors=GRAY, labelsize=8.5)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel('Predicted probability of UP')
    ax.set_ylabel('Observed frequency of UP days')
    ax.set_title('Calibration of SP500 + RF + Sentiment on the 501-day test set', pad=10)
    ax.legend(loc='upper left', frameon=False, fontsize=9.5)
    plt.tight_layout()
    out = os.path.join(HERE, 'calibration_sp500.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}')

# ---------------------------- Chart 4: Cumulative returns -------------------
def plot_cumulative_returns():
    y, p, close, dates = collect_probs('SP500')
    # Realised next-day return: close[t+1]/close[t] - 1, last value undefined
    rets = np.diff(close) / close[:-1]
    # Align: predictions at day t use indicators through day t, signal applies to day t+1
    signal_long = (p['rf_all'][:-1] >= 0.55).astype(int)
    signal_long_50 = (p['rf_all'][:-1] >= 0.50).astype(int)
    # Always-long (buy-and-hold) and random (50/50 daily) baselines
    rng = np.random.default_rng(42)
    signal_random = rng.integers(0, 2, size=len(rets))

    def equity_curve(signal):
        # Long when signal==1, flat (0% return) otherwise
        strat_rets = signal * rets
        return np.cumprod(1.0 + strat_rets)

    eq_buyhold  = np.cumprod(1.0 + rets)
    eq_signal55 = equity_curve(signal_long)
    eq_signal50 = equity_curve(signal_long_50)
    eq_random   = equity_curve(signal_random)

    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    x = pd.to_datetime(dates[:-1])
    ax.plot(x, eq_buyhold,   color=BLUE,    lw=2.0, label=f'Always-long (buy \\& hold) -- end \\${eq_buyhold[-1]:.2f}')
    ax.plot(x, eq_signal50,  color=GOLD,    lw=2.0, label=f'Model long if $P\\geq 0.50$ -- end \\${eq_signal50[-1]:.2f}')
    ax.plot(x, eq_signal55,  color=GOLD_DARK,lw=2.0, label=f'Model long if $P\\geq 0.55$ -- end \\${eq_signal55[-1]:.2f}')
    ax.plot(x, eq_random,    color=GRAY_LT, lw=1.4, linestyle='--', label=f'Random 50/50 daily -- end \\${eq_random[-1]:.2f}')
    ax.axhline(1.0, color=GRAY, lw=0.7)

    ax.set_xlabel('test-set date')
    ax.set_ylabel('cumulative return (\\$1 initial, gross of costs)')
    ax.set_title('Cumulative return on the 501-day SP500 test window  (gross, no transaction costs)', pad=10)
    ax.legend(loc='upper left', frameon=False, fontsize=9.5)
    plt.tight_layout()
    out = os.path.join(HERE, 'cumulative_returns_sp500.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}')

if __name__ == '__main__':
    plot_roc()
    plot_confusion()
    plot_calibration()
    plot_cumulative_returns()
    print('\nALL OK')
