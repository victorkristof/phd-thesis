import pickle
from datetime import datetime

import fire
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, YearLocator
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH


def load_data():
    with open('basketball-matern32.pickle', 'rb') as f:
        nba = pickle.load(f)

    with open('tennis-matern32.pickle', 'rb') as f:
        atp = pickle.load(f)

    return nba, atp


def _plot_scores(fitters, items, ax, ncol=1):
    colors = iter(plt.cm.tab10(np.linspace(0, 1, 10)))
    first = min(f.ts.min() for f in fitters.values())
    last = max(f.ts.max() for f in fitters.values())
    resolution = 300 / (last - first)
    for name in items:
        color = next(colors)
        # first = min(obs.t for obs in model.item[name].observations)
        # last = max(obs.t for obs in model.item[name].observations)
        first = fitters[name].ts.min()
        last = fitters[name].ts.max()
        ts = np.linspace(first, last, num=int(resolution * (last - first)))
        ms, vs = fitters[name].predict(ts)
        std = np.sqrt(vs)
        ts = [datetime.fromtimestamp(t) for t in ts]
        ax.plot(ts, ms, color=color, label=name)
        ax.fill_between(ts, ms - std, ms + std, color=color, alpha=0.2, lw=0.5)
    ax.grid(alpha=0.5, lw=0.5)
    ax.legend(
        frameon=True, edgecolor='white', ncol=ncol, fontsize=8, columnspacing=1
    )


def plot_scores(axes):
    nba, atp = load_data()

    fmt = DateFormatter('%Y')

    _plot_scores(nba, ['LAL', 'CHI', 'BOS'], axes[0])
    axes[0].xaxis.set_major_locator(YearLocator(base=5))
    axes[0].xaxis.set_major_formatter(fmt)
    axes[0].set_title('NBA basketball (1946–2018)')
    axes[0].set_ylabel('Score', labelpad=0.0)

    subset = [
        'Andre Agassi',
        'Michael Chang',
        'Pete Sampras',
        'Roger Federer',
        'Rafael Nadal',
        'Novak Djokovic',
    ]
    _plot_scores(atp, subset, axes[1], ncol=2)
    axes[1].xaxis.set_major_locator(YearLocator(base=2))
    axes[1].xaxis.set_major_formatter(fmt)
    axes[1].set_title('ATP tennis (1991-2017)')
    axes[1].set_ylabel('Score', labelpad=7.0)


def plot(save_as=None):
    subplots = (2, 1)
    width = TEXT_WIDTH + 0.3
    height = TEXT_WIDTH / GOLDEN_RATIO + 0.3
    setup_plotting(size=(width, height), subplots=subplots)

    fig, axes = plt.subplots(*subplots)
    plot_scores(axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
