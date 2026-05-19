"""Generates the result / EDA / model charts used by the Beamer slides.
Output: PNGs written next to this script (figures/).

Sources of truth:
  - datasets_/final_model_comparison.csv  for headline metrics.
  - Feature importances and EDA numbers reproduced with sklearn 1.4.2
    / xgboost 3.2.0 (same as models_demo/metadata.json).
"""
import os, sys, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Tec de Monterrey palette (matches the Beamer deck)
BLUE      = '#0F3D60'
BLUE_DARK = '#082842'
GOLD      = '#C8A951'
GRAY      = '#4A4A4A'
GRAY_LT   = '#A8A8A8'
GREEN     = '#1B7A4B'
RED       = '#B23A48'
LIGHT     = '#F4F6F9'

plt.rcParams.update({
    'font.family':  'DejaVu Sans',
    'font.size':    10.5,
    'axes.edgecolor': GRAY,
    'axes.labelcolor': GRAY,
    'xtick.color': GRAY,
    'ytick.color': GRAY,
    'axes.titlecolor': BLUE_DARK,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
})

OUT = os.path.dirname(os.path.abspath(__file__))

# Datasets & ordering
DATASETS = ['SP500', 'XLP', 'XLK', 'XLE']
VOL_LABEL = {'SP500':'broad index', 'XLP':'low vol', 'XLK':'median vol', 'XLE':'high vol'}

# -------- Results data (from datasets_/final_model_comparison.csv, rounded) --------
TECH = {
    'SP500': {'RF':(0.51,0.60,0.48), 'XGB':(0.52,0.66,0.48)},
    'XLP':   {'RF':(0.51,0.43,0.50), 'XGB':(0.49,0.41,0.49)},
    'XLK':   {'RF':(0.45,0.23,0.50), 'XGB':(0.45,0.27,0.49)},
    'XLE':   {'RF':(0.50,0.52,0.49), 'XGB':(0.48,0.50,0.48)},
}
SENT = {
    'SP500': {'RF':(0.57,0.68,0.51), 'XGB':(0.52,0.64,0.50)},
    'XLP':   {'RF':(0.48,0.35,0.49), 'XGB':(0.50,0.45,0.51)},
    'XLK':   {'RF':(0.45,0.18,0.50), 'XGB':(0.46,0.30,0.48)},
    'XLE':   {'RF':(0.50,0.52,0.50), 'XGB':(0.51,0.51,0.52)},
}

# -------- Helper: grouped metrics chart --------
def plot_metrics(table, title, fname):
    fig, ax = plt.subplots(figsize=(10, 4.2))
    metrics = ['Acc','F1','AUC']
    n_dat = len(DATASETS)
    group_w = 0.85
    bw      = group_w / 6.0
    x = np.arange(n_dat)

    # Bars: for each dataset, 6 bars (RF Acc/F1/AUC, XGB Acc/F1/AUC)
    rf_colors  = [BLUE, BLUE, BLUE]
    xgb_colors = [GOLD, GOLD, GOLD]
    hatch_pat  = [None, '//', '..']  # Acc plain, F1 hatched, AUC dotted

    handles = []
    for i, ds in enumerate(DATASETS):
        rf  = table[ds]['RF']
        xgb = table[ds]['XGB']
        for j in range(3):
            ax.bar(x[i] - group_w/2 + (j+0.5)*bw,         rf[j],  bw, color=BLUE, edgecolor='white', linewidth=0.5)
            ax.bar(x[i] - group_w/2 + (3+j+0.5)*bw,       xgb[j], bw, color=GOLD, edgecolor='white', linewidth=0.5)
        # value labels (just AUC + F1 of best one per group, to keep clean)
    ax.axhline(0.50, color=GRAY_LT, linestyle=':', lw=1, zorder=0)
    ax.text(n_dat-0.4, 0.502, '0.50 (coin flip)', color=GRAY, fontsize=8, va='bottom', ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{ds}\n({VOL_LABEL[ds]})' for ds in DATASETS])
    ax.set_ylim(0, 0.85)
    ax.set_ylabel('metric value')
    ax.set_title(title, pad=10)
    legend_handles = [
        Patch(facecolor=BLUE, label='Random Forest'),
        Patch(facecolor=GOLD, label='XGBoost'),
    ]
    ax.legend(handles=legend_handles, loc='upper right', frameon=False)
    ax.text(0.0, -0.18, 'Triplets within each colour: Accuracy / F1 / AUC (left to right)',
            transform=ax.transAxes, color=GRAY, fontsize=8.5)
    plt.tight_layout()
    out = os.path.join(OUT, fname)
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {fname}')

plot_metrics(TECH, 'Results --- technical features only (chronological 80/20 hold-out)', 'results_technical_only.png')
plot_metrics(SENT, 'Results --- technical + FinBERT sentiment', 'results_technical_sentiment.png')

# -------- Sentiment uplift chart --------
fig, ax = plt.subplots(figsize=(10, 4.2))
algorithms = ['RF', 'XGB']
metrics   = ['Acc','F1','AUC']
colors    = [BLUE, GOLD, GREEN]
labels    = ['Accuracy', 'F1', 'AUC']

x_pos = []
x_lbl = []
xi = 0
for alg in algorithms:
    for ds in DATASETS:
        x_pos.append(xi)
        x_lbl.append(f'{ds}')
        xi += 1
    xi += 0.6   # gap between algorithm blocks

deltas = []
for alg in algorithms:
    for ds in DATASETS:
        t = TECH[ds][alg]
        s = SENT[ds][alg]
        deltas.append((s[0]-t[0], s[1]-t[1], s[2]-t[2]))

bw = 0.27
for j, (c, lab) in enumerate(zip(colors, labels)):
    vals = [d[j] for d in deltas]
    ax.bar([p + (j-1)*bw for p in x_pos], vals, bw, color=c, edgecolor='white', linewidth=0.5, label=lab)

ax.axhline(0, color=GRAY, lw=0.8)
# RF / XGB block annotations
half = len(DATASETS)
rf_centre  = (x_pos[0] + x_pos[half-1]) / 2
xgb_centre = (x_pos[half] + x_pos[-1]) / 2
ax.text(rf_centre,  ax.get_ylim()[1]*0.88, 'Random Forest', ha='center', color=BLUE_DARK, fontweight='bold', fontsize=11)
ax.text(xgb_centre, ax.get_ylim()[1]*0.88, 'XGBoost',       ha='center', color=BLUE_DARK, fontweight='bold', fontsize=11)
ax.set_xticks(x_pos)
ax.set_xticklabels(x_lbl)
ax.set_ylabel('delta = (tech + sentiment) - (tech only)')
ax.set_title('Sentiment uplift per dataset, algorithm and metric', pad=10)
ax.legend(loc='upper right', frameon=False)
ax.set_ylim(-0.10, 0.11)
# separator
mid = (x_pos[half-1] + x_pos[half]) / 2
ax.axvline(mid, color=GRAY_LT, linestyle='--', lw=1)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'sentiment_uplift.png'), dpi=160, bbox_inches='tight')
plt.close(fig)
print('wrote sentiment_uplift.png')

# -------- Feature importance --------
# Top configurations where sentiment actually helped: SP500 RF, XLE XGB
FI_SP500_RF = pd.Series({
    'Returns':        0.134,
    'RSI':            0.131,
    'sentiment_mean': 0.130,
    'Volume':         0.128,
    'Volatility':     0.124,
    'SMA_10':         0.119,
    'HLC3':           0.117,
    'EMA_10':         0.116,
}).sort_values()
FI_XLE_XGB = pd.Series({
    'HLC3':           0.141,
    'RSI':            0.129,
    'sentiment_mean': 0.128,
    'SMA_10':         0.127,
    'EMA_10':         0.125,
    'Volatility':     0.123,
    'Volume':         0.116,
    'Returns':        0.111,
}).sort_values()

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharex=True)
for ax, fi, title in zip(axes,
                          [FI_SP500_RF, FI_XLE_XGB],
                          ['SP500 - Random Forest', 'XLE - XGBoost']):
    colors_bar = [GOLD if n == 'sentiment_mean' else BLUE for n in fi.index]
    ax.barh(fi.index, fi.values, color=colors_bar, edgecolor='white')
    for i, (name, v) in enumerate(zip(fi.index, fi.values)):
        ax.text(v + 0.001, i, f'{v:.3f}', va='center', fontsize=8.5, color=BLUE_DARK)
    ax.set_xlim(0, 0.16)
    ax.set_title(title, pad=8)
axes[0].set_xlabel('feature importance')
axes[1].set_xlabel('feature importance')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'feature_importance.png'), dpi=160, bbox_inches='tight')
plt.close(fig)
print('wrote feature_importance.png')

# -------- Sector volatility --------
vol = pd.Series({
    'XLP':  0.119,
    'XLU':  0.139,
    'XLRE': 0.146,
    'XLV':  0.149,
    'XLY':  0.163,
    'XLK':  0.171,
    'XLI':  0.173,
    'XLC':  0.188,
    'XLB':  0.192,
    'XLF':  0.197,
    'XLE':  0.217,
})
selected = {'XLP':'low', 'XLK':'median', 'XLE':'high'}
fig, ax = plt.subplots(figsize=(10, 4.0))
colors_bar = [GOLD if t in selected else BLUE for t in vol.index]
ax.bar(vol.index, vol.values, color=colors_bar, edgecolor='white')
for t, v in vol.items():
    ax.text(list(vol.index).index(t), v + 0.003, f'{v:.3f}', ha='center', fontsize=8.5, color=BLUE_DARK)
    if t in selected:
        ax.text(list(vol.index).index(t), v + 0.018, selected[t],
                ha='center', color=GOLD, fontstyle='italic', fontweight='bold', fontsize=9)
ax.set_ylim(0, 0.245)
ax.set_ylabel('annualised volatility')
ax.set_title('GICS sector ETF volatility, 2010-2019', pad=10)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'sector_volatility.png'), dpi=160, bbox_inches='tight')
plt.close(fig)
print('wrote sector_volatility.png')

# -------- Class balance --------
class_bal = pd.DataFrame({
    'Dataset':  DATASETS,
    'Up':       [0.547, 0.539, 0.557, 0.509],
    'Down':     [0.453, 0.461, 0.443, 0.491],
})
fig, ax = plt.subplots(figsize=(6.5, 3.6))
y = np.arange(len(class_bal))
ax.barh(y, class_bal['Up'],   color=BLUE, label='Up')
ax.barh(y, class_bal['Down'], left=class_bal['Up'], color=GOLD, label='Not up')
for i, row in class_bal.iterrows():
    ax.text(row['Up']/2, i,         f"{row['Up']*100:.1f}%",  ha='center', va='center', color='white', fontsize=9.5, fontweight='bold')
    ax.text(row['Up'] + row['Down']/2, i, f"{row['Down']*100:.1f}%", ha='center', va='center', color=BLUE_DARK, fontsize=9.5, fontweight='bold')
ax.set_yticks(y)
ax.set_yticklabels([f"{d}\n({VOL_LABEL[d]})" for d in class_bal['Dataset']])
ax.set_xlim(0, 1)
ax.set_xlabel('share of trading days')
ax.set_title('Target class balance (2010-2019)', pad=10)
ax.legend(loc='lower right', frameon=False)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'class_balance.png'), dpi=160, bbox_inches='tight')
plt.close(fig)
print('wrote class_balance.png')

# -------- Sentiment distribution / news volume --------
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))

# Left: news volume per year (sum)
news_year = pd.Series({
    2010: 13616, 2011: 14179, 2012: 13833, 2013: 14317, 2014: 13833,
    2015: 14345, 2016: 13581, 2017: 13664, 2018: 13858, 2019: 13938,
})
axes[0].bar(news_year.index.astype(str), news_year.values, color=BLUE)
axes[0].set_title('News headlines sampled per year', pad=8)
axes[0].set_ylim(0, max(news_year.values)*1.18)
for i, v in enumerate(news_year.values):
    axes[0].text(i, v + 200, f'{v:,}', ha='center', fontsize=8.5, color=BLUE_DARK)
axes[0].set_ylabel('headlines (after stratified sampling)')

# Right: daily sentiment distribution (descriptive)
parts = pd.Series({
    'positive (>0)': 0.569,
    'neutral (=0)':  1.0 - 0.569 - 0.345,
    'negative (<0)': 0.345,
})
colors_pie = [GREEN, GRAY_LT, RED]
axes[1].pie(parts.values, labels=parts.index, autopct='%1.1f%%', colors=colors_pie,
            textprops={'fontsize':9, 'color':BLUE_DARK}, startangle=90, wedgeprops={'edgecolor':'white'})
axes[1].set_title('Days by mean FinBERT sentiment sign (2010-2019)', pad=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'eda_news_sentiment.png'), dpi=160, bbox_inches='tight')
plt.close(fig)
print('wrote eda_news_sentiment.png')

print('\nALL OK')
