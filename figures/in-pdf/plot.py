import fire
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from thesis import save_fig, set_aspect_ratio, setup_plotting


def plot_pdf(ax):
    # Gaussian.
    mu = 0
    variance = 1
    sigma = np.sqrt(variance)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color='black', label='N$(0, 1)$')

    # Gumbel.
    loc = 0
    scale = 1
    x = np.linspace(loc - 4 * scale, loc + 4 * scale, 100)
    ax.plot(
        x,
        stats.gumbel_r.pdf(x, loc, scale),
        color='black',
        linestyle='--',
        label='Gumbel$(0, 1)$',
    )

    # Plot settings.
    ax.legend()
    ax.set_ylabel(r'Probability density $f(x)$')
    ax.set_xlabel(r'$x$')
    set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    setup_plotting(size='fraction')

    fig, ax = plt.subplots()
    plot_pdf(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
