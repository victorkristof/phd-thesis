import pickle

import fire
import matplotlib.pyplot as plt
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH
from thesis.predikon_plotting import plot_results as _plot


def load_data(kind):
    with open(f'de-{kind}.pkl', 'rb') as f:
        return pickle.load(f)


def plot_state(fig, ax1, ax2):
    # Define type of plot.
    mae = 'mae-outcome'
    dis = 'displacement'

    # Set keys to models.
    models = [
        'Averaging',
        # 'SubSVD (dim=7,l2=0.01)',
        'Logistic SubSVD (dim=7,l2=0.01)',
    ]

    # Define labels.
    labels = [
        'Averaging',
        # r'\textsc{SubSVD-Gaussian}',
        r'\textsc{SubSVD-Categ.}',
    ]

    # Define line styles.
    lines = [
        '-',
        # ':',
        '--',
    ]

    # Define colors.
    colors = [
        'black',
        # 'C3',
        'C3',
    ]

    # Define plot title.
    title = 'German Election by State'

    # Load data.
    results = load_data('state')

    # Plot by states.
    _plot(  # MAE.
        results=results,
        metric=mae,
        title=title,
        models=models,
        labels=labels,
        lines=lines,
        colors=colors,
        position='top',
        regions='states',
        ax=ax1,
        fig=fig,
        x_logscale=False,
        legend=False,
    )
    _plot(  # Displacement.
        results=results,
        metric=dis,
        title=title,
        models=models,
        labels=labels,
        lines=lines,
        colors=colors,
        position='bottom',
        regions='states',
        ax=ax2,
        fig=fig,
        x_logscale=False,
    )


def plot_district(fig, ax1, ax2):
    # Define type of plot.
    mae = 'mae-outcome'
    dis = 'displacement'

    # Set keys to models.
    models = [
        'Averaging',
        # 'SubSVD (dim=11,l2=0.01)',
        'Logistic SubSVD (dim=11,l2=0.01)',
    ]

    # Define labels.
    labels = [
        'Averaging',
        # r'\textsc{SubSVD-Gaussian}',
        r'\textsc{SubSVD-Categ.}',
    ]

    # Define line styles.
    lines = [
        '-',
        # ':',
        '--',
    ]

    # Define colors.
    colors = [
        'black',
        # 'C3',
        'C3',
    ]

    # Define plot title.
    title = 'German Election by District'

    # Load data.
    results = load_data('district')

    # Plot by districts.
    _plot(  # MAE.
        results=results,
        metric=mae,
        title=title,
        models=models,
        labels=labels,
        lines=lines,
        colors=colors,
        position='top',
        regions='districts',
        ax=ax1,
        fig=fig,
        ylim=(-0.0025, 0.06),
        x_logscale=True,
        ylabel=False,
    )
    _plot(  # Displacement.
        results=results,
        metric=dis,
        title=title,
        models=models,
        labels=labels,
        lines=lines,
        colors=colors,
        position='bottom',
        regions='districts',
        ax=ax2,
        fig=fig,
        ylim=(-0.05, 1.12),
        x_logscale=True,
        ylabel=False,
    )


def plot(save_as=None):
    subplots = (2, 2)
    width = TEXT_WIDTH
    height = 4.5
    setup_plotting(size=(width, height), subplots=subplots)

    # Setup figure layout.
    gridspec = dict(wspace=0.1, bottom=0.2, right=0.95)
    fig, axes = plt.subplots(
        *subplots,
        sharex=False,
        sharey='row',
        gridspec_kw=gridspec,
    )

    # Plot district and state results.
    plot_state(fig, axes[0, 0], axes[1, 0])
    plot_district(fig, axes[0, 1], axes[1, 1])

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
