import pickle

import fire
import matplotlib.pyplot as plt
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import TEXT_WIDTH
from thesis.predikon_plotting import plot_results as _plot


def load_data():
    with open('ch-results.pkl', 'rb') as f:
        return pickle.load(f)


def plot_results(fig, axes):
    # Define type of plot.
    mae = 'mae-outcome'
    acc = 'nat_correct'

    # Set keys to models.
    models = [
        'Weighted Averaging',
        'Matrix Factorization (dim=25,lam_V=0.03,lam_U=31.0)',
        # 'Weighted SubSVD (dim=25,l2=0.1)',
        'Weighted Logistic SubSVD (dim=25,l2=0.1)',
    ]

    # Define labels.
    labels = [
        'Averaging',
        'MF',
        # r'\textsc{SubSVD-Gaussian}',
        r'\textsc{SubSVD-Bernoulli}',
    ]

    # Define line styles.
    lines = [
        '-',
        ':',
        '--',
    ]

    # Define colors.
    colors = ['black', 'black', 'C3']

    # Define plot title.
    title = 'Swiss Referenda'

    # Load data.
    results = load_data()

    # Plot.
    _plot(  # MAE.
        results=results,
        metric=mae,
        title=title,
        models=models,
        labels=labels,
        lines=lines,
        colors=colors,
        regions='municipalities',
        position='top',
        ax=axes[0],
        fig=fig,
        x_logscale=True,
    )
    _plot(  # Accuracy.
        results=results,
        metric=acc,
        title=title,
        models=models,
        labels=labels,
        lines=lines,
        colors=colors,
        position='bottom',
        regions='municipalities',
        ax=axes[1],
        fig=fig,
        x_logscale=True,
    )
    # for ax in axes:
    #     set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    subplots = (2, 1)
    width = TEXT_WIDTH * 0.85
    height = width
    setup_plotting(size=(width, height), subplots=subplots)
    # setup_plotting(size='fraction')

    fig, axes = plt.subplots(*subplots)
    fig.subplots_adjust(hspace=0.1)
    plot_results(fig, axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
