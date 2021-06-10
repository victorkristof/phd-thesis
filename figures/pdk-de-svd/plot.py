import pickle

import fire
import matplotlib.pyplot as plt
from matplotlib import rcParams
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH
from thesis.predikon_plotting import min_max_scale, plot_svd_with_lang, svd


def load_embedding():
    with open('de-embedding.pkl', 'rb') as f:
        return pickle.load(f)


def plot_nth_scatter(
    embedding, n, ax, colorixs, colors, parties, title, print_names=True
):
    # Rescale embeddings.
    embedding = min_max_scale(embedding, axis=0)

    # Get items to plot.
    cols = [colors[c[-n]] for c in colorixs]
    labels = [parties[c[-n]] for c in colorixs]
    xs, ys = embedding[:, 0], embedding[:, 1]
    for x, y, c, label in zip(xs, ys, cols, labels):
        ax.scatter(
            x=x,
            y=y,
            c=c,
            label=label,
            s=2,
            lw=0.8,
        )
    # Display Berlin on the map.
    if n == 1:  # Get plot with first party.
        arrow = dict(width=0.1, headwidth=4, headlength=4, facecolor='black')
        ax.annotate(
            'Berlin', xy=(0.3, 0.585), xytext=(0.42, 0.57), arrowprops=arrow
        )
    # Plot "Historical East/West" on plot with third parties.
    elif n == 3:  # Get plot with third party.
        lower, upper = [-0.05, 0.2], [1, 0.8]
        ax.plot(
            [lower[0], upper[0]],
            [lower[1], upper[1]],
            c='black',
            lw=1,
            linestyle='--',
        )
        ax.text(-0.08, 0.23, 'Historical East/West', rotation=29, fontsize=9)
    # Set title.
    ax.set_title(title)
    # # Remove legend border.
    rcParams.update({'legend.frameon': False})
    # Remove ticks.
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    # Sort legend by alphabetical order.
    handles, labels = ax.get_legend_handles_labels()
    # Keep only on label.
    unique = [
        (h, l)
        for i, (h, l) in enumerate(zip(handles, labels))
        if l not in labels[:i]
    ]
    handles, labels = zip(*sorted(unique, key=lambda t: t[1]))
    # Configure legend.
    if n == 1:
        lgnd = ax.legend(
            handles,
            labels,
            loc='lower right',
            handletextpad=0.0,
            labelspacing=0.2,
        )
    elif n == 3:
        lgnd = ax.legend(
            handles, labels, loc='best', handletextpad=0.0, labelspacing=0.2
        )
    # Set size of points in legend (must be done after legend is set).
    for handle in lgnd.legendHandles:
        handle.set_sizes([10])
    # set_aspect_ratio(ax, 'equal')


def plot_projection(axes):
    parties = ['SPD', 'CDU/CSU', 'Greens', 'FDP', 'Left']
    colors = ['C3', 'C0', 'C2', 'C1', 'C6']

    # Get SVD embedding.
    (embedding, colorixs) = load_embedding()

    # Plot.
    plot_nth_scatter(
        embedding=embedding,
        n=1,
        ax=axes[0],
        colorixs=colorixs,
        colors=colors,
        parties=parties,
        title='Coloring by First Party',
        print_names=True,
    )
    plot_nth_scatter(
        embedding=embedding,
        n=3,
        ax=axes[1],
        colorixs=colorixs,
        colors=colors,
        parties=parties,
        title='Coloring by Third Party',
        print_names=True,
    )


def plot(save_as=None):
    subplots = (1, 2)
    width = TEXT_WIDTH
    height = TEXT_WIDTH / GOLDEN_RATIO
    setup_plotting(size=(width + 0.35, height - 0.35), subplots=subplots)
    # setup_plotting(size='fraction')

    fig, axes = plt.subplots(*subplots)
    plot_projection(axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
