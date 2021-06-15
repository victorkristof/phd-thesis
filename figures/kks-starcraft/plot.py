import json

import fire
import matplotlib.pyplot as plt
import numpy as np
from thesis import save_fig, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH


def plot_starcraft(axes):
    # Data.
    with open('starcraft-wol.json') as f:
        wol = json.load(f)
    with open('starcraft-hots.json') as f:
        hots = json.load(f)
    # Plot.
    axes[0].set_ylim(ymin=0.4, ymax=0.6)
    axes[1].set_ylim(ymin=0.4, ymax=0.6)
    axes[0].set_ylabel("Log loss")

    models = ["naive", "bt", "bc", "intransitive"]
    labels = ["Naive", "Logit", "B.-C.", "Kickscore"]
    hatches = [None, '///', '---', 'xxx']
    colors = ['gray', 'white', 'white', 'white']
    edges = ['black', 'black', 'black', 'C3']

    idx = np.arange(len(models))
    for ax, title, data in zip(
        axes, ("StarCraft HotS", "StarCraft WoL"), (hots, wol)
    ):
        vals = [-data[m] for m in models]
        bars = ax.bar(idx, vals, width=0.6, linewidth=1)
        for bar, hatch, color, edge in zip(bars, hatches, colors, edges):
            bar.set_hatch(hatch)
            bar.set_color(color)
            bar.set_edgecolor(edge)
        ax.set_xticks(idx)
        ax.set_xticklabels(labels)
        ax.set_title(title)
        if 'WoL' in title:
            ax.set_yticklabels([])


def plot(save_as=None):
    subplots = (1, 2)
    width = TEXT_WIDTH
    height = TEXT_WIDTH / 2
    setup_plotting(size=(width + 0.3, height), subplots=subplots)

    fig, axes = plt.subplots(*subplots)
    plot_starcraft(axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
