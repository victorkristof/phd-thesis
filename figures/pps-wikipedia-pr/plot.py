import pickle

import fire
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from sklearn.metrics import precision_recall_curve
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH


def load_data():
    def load(path, key, data_dict):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        data_dict[key] = dict()
        data_dict[key]['y_true'] = (data['y_true'] < 0.5).astype(int)
        if key == 'ores':
            data_dict[key]['y_pred'] = data['y_pred']
        else:
            data_dict[key]['y_pred'] = 1 - data['y_pred']

    data_fr, data_tr = dict(), dict()

    # Load French Wikipedia data.
    load('frwiki-basic-pred.pickle', 'basic', data_fr)
    load('frwiki-dot-pred.pickle', 'dot', data_fr)
    load('frwiki-ores-reverted-pred.pickle', 'ores', data_fr)
    load('frwiki-useronly-pred.pickle', 'user', data_fr)
    load('frwiki-whitehill-pred.pickle', 'whitehill', data_fr)

    # Load Turkish Wikipedia data.
    load('trwiki-basic-pred.pickle', 'basic', data_tr)
    load('trwiki-dot-pred.pickle', 'dot', data_tr)
    load('trwiki-ores-reverted-pred.pickle', 'ores', data_tr)
    load('trwiki-useronly-pred.pickle', 'user', data_tr)
    load('trwiki-whitehill-pred.pickle', 'whitehill', data_tr)

    return data_fr, data_tr


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


def plot_results(ax1, ax2):
    # Load data.
    data_fr, data_tr = load_data()

    # Map key to name.
    model2name = {
        'basic': r'\textsc{interank} \emph{basic}',
        'dot': r'\textsc{interank} \emph{full}',
        'ores': 'ORES reverted',
        'user': 'User-only',
        'whitehill': 'GLAD',
    }

    for edition, data, ax in (
        ('Turkish Wikipedia', data_tr, ax1),
        ('French Wikipedia', data_fr, ax2),
    ):
        for model, c, ls in (('basic', 'C1', 'solid'), ('dot', 'C3', 'solid')):
            info = data[model]
            plot_curves(
                info['y_true'],
                info['y_pred'],
                ax,
                model2name[model],
                color=c,
                ls=ls,
            )
        y = data['dot']['y_true'].mean()
        ax.axhline(y, label='Average', color='k', ls=':', linewidth=1.0)
        for model, c, ls in (
            ('user', 'C2', 'dotted'),
            ('whitehill', 'C4', 'dashdot'),
            ('ores', 'C0', 'dashed'),
        ):
            info = data[model]
            plot_curves(
                info['y_true'],
                info['y_pred'],
                ax,
                model2name[model],
                color=c,
                ls=ls,
            )
        # ax.set_aspect('equal')
        ax.set_xlim(xmin=0.0, xmax=1.0)
        ax.set_ylim(ymin=0.0, ymax=1.0)
        ax.set_title(edition)
        ax.set_xlabel('Recall')
        set_aspect_ratio(ax, 'equal')
    ax1.set_ylabel('Precision')
    # Draw legend on right plot.
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, labels, labelspacing=0.3)


def plot(save_as=None):
    subplots = (1, 2)
    width = 5.78
    height = width / GOLDEN_RATIO
    setup_plotting(size=(width, height), subplots=subplots)

    fig, (ax1, ax2) = plt.subplots(*subplots, sharex=True, sharey=True)
    plot_results(ax1, ax2)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
