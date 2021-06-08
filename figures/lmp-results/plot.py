import json

import fire
import matplotlib.pyplot as plt
import numpy as np
from thesis import save_fig, setup_plotting
from thesis.plotting import TEXT_WIDTH

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


def plot_results(axes):
    # Define experiments.
    legs = [7, 8]
    models = [
        ('Naive', 'naive'),
        ('Random', 'random'),
        ('WarOfWords', 'no_features'),
        ('WarOfWords', 'all_features'),
        ('WarOfWords', 'no_features-text'),
        ('WarOfWordsLatent', 'no_features'),
        ('WarOfWords', 'all_features-text'),
        ('WarOfWordsLatent', 'all_features'),
        ('WarOfWordsLatent', 'no_features-text'),
        ('WarOfWordsLatent', 'all_features-text'),
    ]
    width = 0.75

    # Get data.
    results = dict()
    for leg in legs:
        results.update(get_data(leg=leg, exp='results'))
    # Build bars.
    bars = list()
    for leg in legs:
        b = list()
        for model in models:
            b.append(results[get_key(*model, leg)])
        bars.append(b)

    xs = np.arange(len(bars[0]))
    # Bar settings.
    patterns = [
        None,
        None,
        None,
        '///',
        '---',
        '\\\\\\',
        '///---',
        'xxx',
        '\\\\\\---',
        '---xxx',
    ]
    colors = [
        'gray',
        'lightgray',
        'white',
        'white',
        'white',
        'white',
        'white',
        'white',
        'white',
        'white',
    ]
    edgecolors = [
        'black',
        'black',
        'black',
        'black',
        'black',
        'black',
        'black',
        'black',
        'black',
        'C3',
    ]
    labels = [
        'Naive',
        'Random',
        r'\textsc{WoW}',
        r'\textsc{WoW}(\em{X})',
        r'\textsc{WoW}(\em{T})',
        r'\textsc{WoW}(\em{L})',
        r'\textsc{WoW}(\em{XT})',
        r'\textsc{WoW}(\em{XL})',
        r'\textsc{WoW}(\em{LT})',
        r'\textsc{WoW}(\em{XLT})',
    ]
    positions = ['top', 'bottom']
    titles = [
        r'7\textsuperscript{th} Legislature',
        r'8\textsuperscript{th} Legislature',
    ]
    # Draw bars.
    for ax, legbars, pos, title in zip(axes, bars, positions, titles):
        lines = list()
        for i, (x, bar) in enumerate(zip(xs, legbars)):
            line = ax.bar(
                x,
                bar,
                width=width,
                color=colors[i],
                linewidth=1,
                edgecolor=edgecolors[i],
                hatch=patterns[i],
                label=labels[i],
            )
            lines.append(line)
        # Draw text.
        for bar in ax.patches:
            height = bar.get_height()
            ax.text(
                bar.get_x() + width / 2,
                height + 0.01,
                f'{height:.3f}',
                ha='center',
                va='bottom',
                rotation=0,
                fontsize=7,
            )
        # Add xticks labels.
        if pos == 'top':
            ax.set_xticks([])
            ax.set_xticklabels([])
        elif pos == 'bottom':
            ax.set_xticks(xs)
            ax.set_xticklabels(labels, rotation=45)

        # Add title.
        ax.set_title(title)

        ax.set_ylim([0.0, 1.0])
        ax.set_ylabel('Average cross entropy')
        # set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    subplots = (2, 1)
    width = TEXT_WIDTH * 0.85
    height = width
    setup_plotting(size=(width, height), subplots=subplots)
    # setup_plotting(size='fraction')

    fig, axes = plt.subplots(*subplots)
    fig.subplots_adjust(hspace=0.1)
    plot_results(axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
