import pickle

import fire
import matplotlib.pyplot as plt
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH
from thesis.predikon_plotting import plot_results as _plot


def load_data():
    with open('us-results.pkl', 'rb') as f:
        return pickle.load(f)


def plot_results(fig, axes):
    # Define type of plot.
    mae = 'mae-outcome'
    acc = 'nat_correct'

    # Set keys to models.
    models = [
        'Weighted Averaging',
        'Matrix Factorization (dim=5,lam_V=0.01,lam_U=0.01)',
        # 'Weighted SubSVD (dim=5,l2=0.001)',
        'Weighted Logistic SubSVD (dim=5,l2=0.001)',
        # 'SubSVD (dim=5,l2=0.001)',
        # 'Logistic SubSVD (dim=5,l2=0.001)',
    ]

    # Define labels.
    labels = [
        'Averaging',
        'MF',
        # r'\textsc{SubSVD-Gaussian}',
        r'\textsc{SubSVD-Bernoulli}',
        # r'\textsc{UWSubSVD-Gaussian}',
        # r'\textsc{UWSubSVD-Bernoulli}',
    ]

    # Define line styles.
    lines = [
        '-',
        ':',
        '--',
        # '-.',
        # '-',
        # '-',
    ]

    # Define colors.
    colors = [
        'black',
        'black',
        'C3',
        # 'C1',
        # 'C0',
        # 'C4',
    ]

    # Define plot title.
    title = 'U.S. Presidential Election 2016'

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
        regions='states',
        position='top',
        ax=axes[0],
        fig=fig,
        x_logscale=False,
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
        regions='states',
        ax=axes[1],
        fig=fig,
        x_logscale=False,
    )
    # for ax in axes:
    #     set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    subplots = (2, 1)
    width = TEXT_WIDTH * 0.85
    height = 4
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
