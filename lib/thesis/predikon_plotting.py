from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Ellipse
from sklearn.manifold import TSNE

LANGS = ['de', 'fr', 'it', 'ro']


def svd(M, skip=0):
    M = M - M.mean(axis=0)
    U, S, V = np.linalg.svd(M)
    E = M.dot(V.T[:, skip : skip + 2])
    return E


def tsne(M, seed=0):
    ts = TSNE(random_state=seed)
    E = ts.fit_transform(M)
    return E


def min_max_scale(M, axis=0):
    m_max = M.max(axis=axis)
    m_min = M.min(axis=axis)
    return (M - m_min) / (m_max - m_min)


def lang_color(lang):
    lang_color = {
        'fr': 'purple',
        'de': 'blue',
        'ro': 'green',
        'it': 'red',
        'unknown': 'black',
    }
    if lang not in lang_color:
        return 'yellow'
    return lang_color[lang]


def get_canton_coloring(cantons):
    n = len(cantons)
    if None in cantons:
        n -= 1
        cantons.remove(None)
    cantons = list(cantons)

    def color_canton(cant):
        if cant is None:
            return 1
        else:
            return cantons.index(cant) / (n + 1)

    return color_canton


def plot_svd_with_lang(embedding, languages, colors, labels, fig, ax):
    assert len(embedding) == len(languages)

    # Rescale embeddings.
    embedding = min_max_scale(embedding, axis=0)
    # Get panguages.
    langs = set(languages)
    # Plot municipalities in vote space.
    for lang in langs:
        ixs = [i for i, la in enumerate(languages) if la == lang]
        ax.scatter(
            x=-embedding[ixs, 0],
            y=embedding[ixs, 1],
            alpha=1,
            c=colors[lang],
            s=2,
            linewidths=0.8,
            label=labels[lang],
        )
    # Plot Röstigraben.
    lower, upper = [-0.75, -0.05], [-0.05, 1]
    ax.plot(
        [lower[0], upper[0]],
        [lower[1], upper[1]],
        c='black',
        lw=1,
        linestyle='--',
    )
    ax.text(-0.78, -0.04, '``Röstigraben"', rotation=40, fontsize=9)
    # Remove legend border.
    rcParams.update({'legend.frameon': False})
    # Remove ticks.
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    # Sort legend by alphabetical order.
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    # Configure legend.
    lgnd = ax.legend(
        handles,
        labels,
        loc='best',
        # bbox_to_anchor=(-0.05, -0.02),
        handletextpad=0.0,
        labelspacing=0.2,
    )
    # Set size of points in legend (must be done after legend is set).
    for handle in lgnd.legendHandles:
        handle.set_sizes([10])
    # Set title.
    # ax.set_title('Coloring by Language')


def plot_embedding_with_lang(embedding, languages, colors, labels, fig, ax):
    assert len(embedding) == len(languages)

    # Rescale embeddings.
    embedding = min_max_scale(embedding, axis=0)
    # Get panguages.
    langs = set(languages)

    for lang in langs:
        ixs = [i for i, la in enumerate(languages) if la == lang]
        ax.scatter(
            x=-embedding[ixs, 0],
            y=-embedding[ixs, 1],
            alpha=1,
            c=colors[lang],
            s=2,
            linewidths=0.8,
            label=labels[lang],
        )
    # Highlight Wallis.
    wallis_fr = Ellipse(
        xy=(-0.58, -0.07),
        width=0.15,
        height=0.15,
        color='k',
        fill=False,
        linestyle='--',
        linewidth=0.5,
    )
    ax.add_patch(wallis_fr)
    wallis_de = Ellipse(
        xy=(-0.2, -0.04),
        width=0.15,
        height=0.15,
        color='k',
        fill=False,
        linestyle='--',
        linewidth=0.5,
    )
    ax.add_patch(wallis_de)
    ax.text(-0.46, -0.08, 'Wallis', fontsize=9)
    # Highlight Ticino.
    ticino = plt.Circle(
        (-0.62, -0.95), 0.08, linestyle='--', linewidth=0.5, fill=False
    )
    ax.add_artist(ticino)
    ax.text(-0.52, -0.97, 'Ticino', fontsize=9)
    # Remove legend border.
    rcParams.update({'legend.frameon': False})
    # Remove ticks.
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    # Sort legend by alphabetical order.
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    # Configure legend
    lgnd = ax.legend(
        handles,
        labels,
        loc='lower left',
        bbox_to_anchor=(-0.05, -0.02),
        handletextpad=0.0,
        labelspacing=0.2,
    )
    # Set size of points in legend.
    for handle in lgnd.legendHandles:
        handle.set_sizes([10])
    # Set title.
    ax.set_title('Coloring by Language')


def plot_embedding_with_canton_and_lang(
    embedding, cantons, languages, fig, ax
):
    assert len(embedding) == len(cantons)

    # Rescale embeddings.
    embedding = min_max_scale(embedding, axis=0)
    unique_cantons = set(cantons)
    cant_color = get_canton_coloring(unique_cantons)

    labeled = {c: False for c in unique_cantons}
    for lang in LANGS:
        lixs = [i for i, la in enumerate(languages) if la == lang]
        for canton in unique_cantons:
            ixs = [i for i in lixs if cantons[i] == canton]
            c = np.array([plt.cm.tab20(cant_color(canton))])
            label = canton if not labeled[canton] else None
            ax.scatter(
                x=-embedding[ixs, 0],  # Reverse (x, y) for display purposes.
                y=-embedding[ixs, 1],
                alpha=1,
                c=c,
                vmin=0,
                vmax=1,
                s=2,
                linewidths=0.8,
                label=label,
                # marker=lang_markers[lang]
            )
            labeled[canton] = True
    # Highlight Wallis.
    wallis_fr = Ellipse(
        xy=(-0.58, -0.07),
        width=0.15,
        height=0.15,
        color='white',
        fill=False,
        linestyle='--',
        linewidth=0.5,
    )
    ax.add_patch(wallis_fr)
    wallis_de = Ellipse(
        xy=(-0.2, -0.04),
        width=0.15,
        height=0.15,
        color='white',
        fill=False,
        linestyle='--',
        linewidth=0.5,
    )
    ax.add_patch(wallis_de)
    # Highlight Ticino.
    ticino = plt.Circle(
        (-0.62, -0.95),
        0.08,
        color='white',
        linestyle='--',
        linewidth=0.5,
        fill=False,
    )
    ax.add_artist(ticino)
    # Remove legend border.
    rcParams.update({'legend.frameon': False})
    # Remove ticks.
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    # Set title.
    ax.set_title('Coloring by Canton')


def plot_results(
    results,
    metric,
    title,
    models,
    labels,
    lines,
    colors,
    position,
    regions='regions',
    ax=None,
    fig=None,
    ylim=None,
    x_logscale=False,
    ylabel=True,
    xlabel=True,
    legend=True,
):
    # Extract data from results.
    x = results['x']
    all_models = results['models']
    values = results['results'][metric]
    if 'displacement' in metric:
        values = -(values * 5 / 2 - 5 / 2)
    mean = values.mean(axis=(1, 2))
    std = values.std(axis=(1, 2))
    std = std / sqrt(values.shape[1] * values.shape[2])  # Standard error.

    # Plot each model results.
    for model, label, line, color in zip(models, labels, lines, colors):
        i = all_models.index(model)
        y, yerr = mean[i], std[i]
        # Draw lines.
        ax.plot(x, y, label=label, c=color, lw=2, linestyle=line)
        ax.fill_between(x, y1=y + yerr, y2=y - yerr, alpha=0.2, color=color)

    # Set log scales.
    if x_logscale:
        ax.set_xscale('log')
    # if y_logscale:
    #     ax.set_yscale('log')

    # Axes settings.
    if position == 'bottom':
        s = f'Number of observed {regions}'
        ax.set_xlabel(s + r' $|\mathcal{O}|$')
    elif position == 'top':
        if legend:
            ax.legend()
        # Hide x-tick labels.
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        # Set title.
        ax.set_title(title)
    # Set y-axis label.
    if ylabel:
        if 'mae' in metric:
            ax.set_ylabel(r'$\mathrm{MAE}$ [\%]')
        elif 'displacement' in metric:
            ax.set_ylabel('Average Displacement')
        else:
            ax.set_ylabel(r'Accuracy [\%]')
    # Set limits and ticks of y-axis.
    if ylim is not None:
        ax.set_ylim(ylim)
    ticks = ax.get_yticks()
    if 'displacement' in metric:
        ax.set_yticklabels([f'{t:.1f}' for t in ticks])
    else:
        ax.set_yticklabels([f'{t*100:.0f}' for t in ticks])
    # ax.minorticks_off()  # Remove minor ticks.
    ax.grid()
    # ax.xaxis.grid(True, which='both')
    # ax.yaxis.grid(True, which='major')
