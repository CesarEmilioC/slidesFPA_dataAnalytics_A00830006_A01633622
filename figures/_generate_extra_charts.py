"""Generates extra charts for the Discussion / Conclusions / honest-framing slides.

Output: PNGs written next to this script (figures/).

Source of truth (re-verified 2026-05-19):
  - ../../FPA_dataAnalytics_finalRepository/datasets_/technical_model_results.csv
  - ../../FPA_dataAnalytics_finalRepository/datasets_/technical_sentiment_score_model_results.csv
(NOT final_model_comparison.csv -- that is an older, off-spec run.)
"""
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------- Source-of-truth AUC values ---------------------
# (dataset, model, feature_set) -> AUC
AUC = {
    ('SP500', 'RF',  'Tech'):       0.476,
    ('SP500', 'RF',  'Tech+Sent'):  0.514,
    ('SP500', 'XGB', 'Tech'):       0.480,
    ('SP500', 'XGB', 'Tech+Sent'):  0.496,
    ('XLP',   'RF',  'Tech'):       0.499,
    ('XLP',   'RF',  'Tech+Sent'):  0.489,
    ('XLP',   'XGB', 'Tech'):       0.488,
    ('XLP',   'XGB', 'Tech+Sent'):  0.514,
    ('XLK',   'RF',  'Tech'):       0.501,
    ('XLK',   'RF',  'Tech+Sent'):  0.501,
    ('XLK',   'XGB', 'Tech'):       0.488,
    ('XLK',   'XGB', 'Tech+Sent'):  0.484,
    ('XLE',   'RF',  'Tech'):       0.494,
    ('XLE',   'RF',  'Tech+Sent'):  0.501,
    ('XLE',   'XGB', 'Tech'):       0.478,
    ('XLE',   'XGB', 'Tech+Sent'):  0.522,
}

# ---------------------------- AUC ceiling visual -----------------------------
# Horizontal-bar plot, one bar per (dataset, model, feature_set), grouped by
# dataset, showing how all 16 AUC values cluster around 0.50 -- with the
# sentiment-improved ones (RF SP500, XGB XLP, XGB XLE) highlighted gold.
def plot_auc_ceiling():
    rows = []
    for (ds, model, fs), auc in AUC.items():
        label = f'{ds} -- {model} ({fs})'
        rows.append((ds, model, fs, label, auc))

    # Order: by dataset (SP500, XLP, XLK, XLE), then RF then XGB, Tech then Tech+Sent
    ds_order   = {'SP500': 0, 'XLP': 1, 'XLK': 2, 'XLE': 3}
    mod_order  = {'RF': 0, 'XGB': 1}
    fs_order   = {'Tech': 0, 'Tech+Sent': 1}
    rows.sort(key=lambda r: (ds_order[r[0]], mod_order[r[1]], fs_order[r[2]]))

    labels = [r[3] for r in rows]
    aucs   = [r[4] for r in rows]
    # Colours: gold if sentiment improved AUC vs same (ds, model) tech-only baseline
    colors = []
    for r in rows:
        ds, model, fs, _, auc = r
        if fs == 'Tech+Sent':
            base = AUC[(ds, model, 'Tech')]
            colors.append(GREEN if auc - base > 0.02 else GOLD if auc > base else RED)
        else:
            colors.append(BLUE)

    fig, ax = plt.subplots(figsize=(10, 5.4))
    y = np.arange(len(rows))
    ax.barh(y, aucs, color=colors, edgecolor='white', linewidth=0.6)
    for yi, (lab, v) in enumerate(zip(labels, aucs)):
        ax.text(v + 0.003, yi, f'{v:.3f}', va='center', fontsize=8.5, color=BLUE_DARK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.axvline(0.50, color=GRAY, lw=1.4, linestyle='--', zorder=0)
    ax.text(0.502, -0.6, '0.50 (random / EMH ceiling)', color=GRAY, fontsize=9, va='bottom')
    ax.set_xlim(0.43, 0.55)
    ax.set_xlabel('AUC-ROC (chronological 501-day test window)')
    ax.set_title('All 16 configurations cluster around AUC = 0.50 -- the deltas are what matter', pad=10)

    legend_handles = [
        Patch(facecolor=BLUE,  label='Technical only'),
        Patch(facecolor=GREEN, label='Tech + Sent. (clear gain, $\\Delta$AUC > +0.02)'),
        Patch(facecolor=GOLD,  label='Tech + Sent. (marginal)'),
        Patch(facecolor=RED,   label='Tech + Sent. (hurt)'),
    ]
    ax.legend(handles=legend_handles, loc='lower right', frameon=False, fontsize=9)

    plt.tight_layout()
    out = os.path.join(OUT, 'auc_ceiling.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}')

# ---------------------------- Honest baseline comparison ---------------------
# Grouped-bar chart with three reference points (random, always-up, our best)
# across Accuracy / F1 / AUC. Visual companion to the slide-20 table.
def plot_honest_baseline():
    metrics  = ['Accuracy', 'F1', 'AUC']
    random_  = [0.50, 0.50, 0.50]
    always_  = [0.55, 0.71, 0.50]
    ours     = [0.56, 0.67, 0.51]

    x = np.arange(len(metrics))
    bw = 0.26

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar(x - bw, random_, bw, color=GRAY_LT, edgecolor='white', label='Random coin flip')
    ax.bar(x,      always_, bw, color=BLUE,    edgecolor='white', label='``Always-up\'\'  (majority class)')
    ax.bar(x + bw, ours,    bw, color=GOLD,    edgecolor='white', label='SP500 + RF + Sentiment (our best)')

    # Value labels
    for xi, v in zip(x - bw, random_):
        ax.text(xi, v + 0.013, f'{v:.2f}', ha='center', fontsize=9, color=BLUE_DARK)
    for xi, v in zip(x, always_):
        ax.text(xi, v + 0.013, f'{v:.2f}', ha='center', fontsize=9, color=BLUE_DARK)
    for xi, v in zip(x + bw, ours):
        ax.text(xi, v + 0.013, f'{v:.2f}', ha='center', fontsize=9, color=BLUE_DARK, fontweight='bold')

    ax.axhline(0.50, color=GRAY, lw=1.0, linestyle=':', zorder=0)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel('metric value')
    ax.set_ylim(0, 0.92)
    ax.set_title('What does our headline result mean? Three reference points', pad=10)
    ax.legend(loc='upper left', frameon=False, fontsize=9)

    plt.tight_layout()
    out = os.path.join(OUT, 'honest_baseline_bars.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}')

# ---------------------------- Transaction-cost erosion -----------------------
# Stylised illustration for the Limitations slide: edge (Acc - 0.55 baseline)
# under a sweep of round-trip transaction-cost assumptions, daily rebalancing.
def plot_transaction_cost():
    # Strategy: long when prob > 0.55, flat otherwise. Assume ~50% of test
    # days are "long" signals -> ~250 trades/year on a 501-day window.
    # Daily edge ~ +0.05 acc * mean abs daily return (~0.9% for SP500 daily).
    gross_edge_pct = 0.05 * 0.9       # 0.045 pct per active day
    trades_per_year = 125              # ~half of 250 active days flip in/out
    edge_pct_year = gross_edge_pct * 252  # gross
    bps = np.linspace(0, 15, 80)       # round-trip cost in basis points
    cost_pct_year = bps / 100.0 * trades_per_year
    net_edge = edge_pct_year - cost_pct_year

    fig, ax = plt.subplots(figsize=(8, 4.0))
    ax.fill_between(bps, 0, net_edge, where=(net_edge >= 0), color=GREEN, alpha=0.25)
    ax.fill_between(bps, 0, net_edge, where=(net_edge <  0), color=RED,   alpha=0.20)
    ax.plot(bps, net_edge, color=BLUE_DARK, lw=2)
    ax.axhline(0, color=GRAY, lw=0.8)
    # break-even
    be_idx = np.argmin(np.abs(net_edge))
    ax.axvline(bps[be_idx], color=GOLD, lw=1.5, linestyle='--')
    ax.text(bps[be_idx]+0.3, ax.get_ylim()[1]*0.92,
            f'break-even $\\approx$ {bps[be_idx]:.1f} bp',
            color=GOLD_DARK, fontsize=9.5, fontweight='bold')
    ax.set_xlabel('round-trip transaction cost (basis points per turnover)')
    ax.set_ylabel('annualised net edge (pct.\\ pts)')
    ax.set_title('Why the +5% accuracy is not yet tradable: cost erosion of the edge', pad=10)
    plt.tight_layout()
    out = os.path.join(OUT, 'transaction_cost_erosion.png')
    plt.savefig(out, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}')

if __name__ == '__main__':
    plot_auc_ceiling()
    plot_honest_baseline()
    plot_transaction_cost()
    print('\nALL OK')
