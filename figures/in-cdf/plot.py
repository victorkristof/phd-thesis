import fire
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from thesis import setup_plotting


def plot_cdf(ax):
    # Gaussian.
    mu = 0
    variance = 1
    sigma = np.sqrt(variance)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
    ax.plot(x, stats.norm.cdf(x, mu, sigma), color='black', label='N$(0, 1)$')

    # Gumbel.
    loc = 0
    scale = 1
    x = np.linspace(loc - 4 * scale, loc + 4 * scale, 100)
    ax.plot(
        x,
        stats.logistic.cdf(x, loc, scale),
        color='black',
        linestyle='--',
        label='Gumbel$(0, 1)$',
    )

    # Plot settings.
    ax.set_title('Cumulative density functions')
    ax.legend()
    ax.set_ylabel(r'$F(x)$')
    ax.set_xlabel(r'$x$')


def plot(save_as=None):
    setup_plotting(size='single')

    fig, ax = plt.subplots()
    plot_cdf(ax)

    if save_as is not None:
        plt.savefig(save_as)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
