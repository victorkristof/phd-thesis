import fire
import kickscore as ks
import matplotlib.pyplot as plt
import numpy as np
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH


def sample_and_plot(ax, kernel, name):
    ts = np.linspace(0, 10, num=80)
    xs = kernel.simulate(ts)
    ax.plot(ts, xs, linewidth=1.0)
    ax.grid(axis="y", alpha=0.5, linewidth=0.5)
    ax.set_title(name)
    ax.set_ylim(ymin=-4, ymax=4)


def plot_covariances(axes):

    # Plot.
    np.random.seed(0)

    sample_and_plot(axes[0, 0], ks.kernel.Constant(var=1.0), "Constant")

    sample_and_plot(
        axes[0, 1],
        ks.kernel.PiecewiseConstant(var=1.0, bounds=[2.3, 4, 6]),
        "Piecewise constant",
    )

    sample_and_plot(
        axes[0, 2],
        ks.kernel.Affine(var_offset=10.0, t0=0.0, var_slope=0.1),
        "Constant + linear",
    )

    sample_and_plot(
        axes[1, 0], ks.kernel.Wiener(var=0.3, t0=0.0, var_t0=0.0), "Wiener"
    )

    sample_and_plot(
        axes[1, 1], ks.kernel.Exponential(var=1.0, lscale=5.0), "Matérn 1/2"
    )

    sample_and_plot(
        axes[1, 2], ks.kernel.Matern52(var=1.0, lscale=2.0), "Matérn 5/2"
    )


def plot(save_as=None):
    subplots = (2, 3)
    width = TEXT_WIDTH + 0.3
    height = TEXT_WIDTH / GOLDEN_RATIO
    setup_plotting(size=(width, height), subplots=subplots)

    fig, axes = plt.subplots(*subplots)
    plot_covariances(axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
