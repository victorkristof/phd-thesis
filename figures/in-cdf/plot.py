import fire
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from thesis import save_fig, set_aspect_ratio, setup_plotting


def plot_cdf(ax):
    # Gaussian.
    mu = 0
    variance = 1
    sigma = np.sqrt(variance)
    offset = 4
    x = np.linspace(mu - offset * sigma, mu + offset * sigma, 100)
    ax.plot(x, stats.norm.cdf(x, mu, sigma), color='black', label='N$(0, 1)$')

    # Gumbel.
    loc = 0
    scale = 1
    x = np.linspace(loc - offset * scale, loc + offset * scale, 100)
    ax.plot(
        x,
        stats.logistic.cdf(x, loc, scale),
        color='black',
        linestyle='--',
        label='Logistic$(0, 1)$',
    )

    # Plot settings.
    ax.legend()
    ax.set_ylabel(r'Cumulative density $F(x)$')
    ax.set_xlabel(r'$x$')
    set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    setup_plotting(size='fraction')

    fig, ax = plt.subplots()
    plot_cdf(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
