import json

import fire
import matplotlib.pyplot as plt
import numpy as np
from thesis import save_fig, set_aspect_ratio, setup_plotting

PATH = 'ep{leg}-{exp}.json'


def get_key(model, data, leg=None):
    if leg is None:
        return (model, data)
    else:
        return (model, f'ep{leg}-{data}')


def get_data(leg, exp):
    res = dict()
    path = PATH.format(leg=leg, exp=exp)
    with open(path, 'r') as f:
        for ln in f.readlines():
            r = json.loads(ln)
            key = get_key(r['model'], r['data'])
            res[key] = r['log-loss']
    return res


def plot_improvement(ax):
    # Define experiments.
    legs = [7, 8]
    baseline = 'no_features'
    datasets = [
        'dossier_features',
        'mep_features',
        'edit_features',
        'rapporteur_advantage',
        'all_features',
    ]
    model = 'WarOfWords'

    # Get data.
    results = dict()
    for leg in legs:
        results.update(get_data(leg=leg, exp='results'))
    # Build bars.
    bars = list()
    for dataset in datasets:
        b = list()
        for leg in legs:
            base = results[get_key(model, baseline, leg)]
            # For visual purposes.
            if dataset == 'dossier_features':
                base += 0.001
            key = get_key(model, dataset, leg)
            r = float(f'{results[key]:.3f}')
            b.append(r - float(f'{base:.3f}'))
        bars.append(b)

    # Bar settings.
    width = 0.12
    offset = 0.02
    patterns = ['', '///', '\\\\\\', '---', 'xxx']
    colors = ['white', 'white', 'white', 'white', 'white']
    edgecolors = ['black', 'black', 'black', 'black', 'black']
    labels = [
        r'\textsc{WoW}(\em{D})',
        r'\textsc{WoW}(\em{M})',
        r'\textsc{WoW}(\em{E})',
        r'\textsc{WoW}(\em{R})',
        r'\textsc{WoW}(\em{X})',
    ]
    # Get x positions.
    x0 = np.arange(len(bars[0]))
    xs = [
        [x * 0.75 + i * width + i * offset for x in x0]
        for i in range(len(bars))
    ]
    # Draw bars.
    lines = list()
    for i, (x, bar) in enumerate(zip(xs, bars)):
        line = plt.bar(
            x,
            bar,
            width=width,
            color=colors[i],
            linewidth=1.0,
            edgecolor=edgecolors[i],
            hatch=patterns[i],
            label=labels[i],
        )
        lines.append(line)
    # Draw text.
    for i, bars in enumerate(lines):
        for bar in bars:
            height = bar.get_height()
            # For visual pruposes.
            if i == 0:
                text = '0.000'
            else:
                text = f'{height:.3f}'
            ax.text(
                bar.get_x() + width / 2,
                height - 0.001,
                text,
                ha='center',
                va='top',
                rotation=0,
                fontsize=7,
            )
    # Add xticks on the middle of the group bars
    plt.xticks(
        [x * 0.75 + 1.5 * width + 1 * offset for x in range(len(x0))],
        ['EP7', 'EP8'],
    )
    # Set yticks.
    rng = -np.arange(
        0,
        0.06,
        0.01,
    )
    plt.yticks(rng, ['0.00'] + list(rng[1:]))
    plt.ylim([-0.055, 0.0])
    # Title and legend.
    # plt.title(r'Difference in cross entropy loss over \textsc{WoW}($\cdot$)')
    plt.ylabel(r'Difference in cross-entropy loss')
    plt.legend(
        lines,
        labels,
        loc='lower left',
        frameon=True,
        fontsize='x-small',
        framealpha=0.8,
        markerscale=0.1,
    )
    set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    setup_plotting(size=(5.78, 2.6))

    fig, ax = plt.subplots()
    plot_improvement(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
