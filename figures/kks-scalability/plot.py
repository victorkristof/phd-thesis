import fire
import matplotlib.pyplot as plt
import numpy as np
from thesis import save_fig, setup_plotting


def plot_scalability(ax):
    # Data.
    xs = np.array([1, 2, 4, 8, 16])
    ys = np.array([34.087, 20.711, 10.754, 8.292, 5.939])
    # Plot.
    ax.loglog(
        xs,
        ys,
        color='black',
        marker="o",
        markersize=4.0,
        label="ChessBase full",
    )
    ax.set_title("Time per iteration")
    ax.set_ylabel("Time [s]")
    ax.set_xlabel("Number of threads")
    ax.minorticks_off()
    ax.set_xticks([1, 2, 4, 8, 16])
    ax.set_xticklabels([1, 2, 4, 8, 16])
    ax.set_yticks([5, 10, 20, 40])
    ax.set_yticklabels([5.0, 10.0, 20.0, 40.0])
    ax.legend()
    ax.grid(alpha=0.5, linewidth=0.5)


def plot(save_as=None):
    setup_plotting(size='fraction')

    fig, ax = plt.subplots()
    plot_scalability(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
