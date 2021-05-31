import fire
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from sklearn.metrics import precision_recall_curve
from thesis import save_fig, set_aspect_ratio, setup_plotting


def load_data():
    def load(path):
        with open(path, "r") as f:
            return [float(p.strip()) for p in f.readlines()]

    random_forest = load('linux-baseline-ml-probs.txt')
    whitehill = load('linux-whitehill-probs.txt')
    basic = load('linux-basic-probs.txt')
    dot = load('linux-dot-probs.txt')
    useronly = load('linux-useronly-probs.txt')
    y_true = load('linux-labels.txt')

    return random_forest, whitehill, basic, dot, useronly, y_true


def plot_curves(y_true, y_pred, ax, label, **kwargs):
    _xs = np.linspace(0.0, 1.0, num=200)
    # Precision-recall.
    prec, rec, _ = precision_recall_curve(y_true, y_pred)
    f = interp1d(rec, prec)
    ys = f(_xs)
    if ys[0] < 0.5:
        # Sometimes the precision is 0 at recall 0. It looks bad on the plot.
        ax.plot(_xs[1:], ys[1:], linewidth=1.0, label=label, **kwargs)
    else:
        ax.plot(_xs, ys, linewidth=1.0, label=label, **kwargs)


def plot_results(ax):
    # Load data.
    random_forest, whitehill, basic, dot, useronly, y_true = load_data()

    preds = [basic, dot, None, useronly, whitehill, random_forest]
    labels = [
        r'\textsc{interank} \emph{basic}',
        r'\textsc{interank} \emph{full}',
        'Average',
        'User-only',
        'GLAD',
        'Random Forest',
    ]
    linestyle = ['solid', 'solid', 'dotted', 'dotted', 'dashdot', 'dashed']
    colors = ['C1', 'C3', 'black', 'C2', 'C4', 'C0']

    for i in range(len(preds)):
        if labels[i] == 'Average':
            ax.axhline(
                np.mean(y_true),
                label=labels[i],
                color=colors[i],
                ls=linestyle[i],
            )
        else:
            plot_curves(
                y_true,
                preds[i],
                ax,
                labels[i],
                ls=linestyle[i],
                color=colors[i],
            )

    ax.set_xlim(xmin=0.0, xmax=1.0)
    ax.set_ylim(ymin=0.0, ymax=1.0)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper right', labelspacing=0.3)
    # ax.set_title("Linux kernel")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    setup_plotting(size='fraction')

    fig, ax = plt.subplots()
    plot_results(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
