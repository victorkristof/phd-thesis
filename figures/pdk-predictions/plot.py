import json

import fire
import matplotlib.pyplot as plt
import numpy as np
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH


def load_data():
    with open('predictions.json') as f:
        data = json.load(f)
    return {int(vote): preds for vote, preds in data.items()}


def print_statistics(preds, title, print_table=False):
    ypred = [p['yes_predicted'] for p in preds]
    count = [p['yes_counted'] for p in preds]
    diff = np.abs(count[-1] - ypred[0])
    if print_table:
        s = title
        s += ' & '
        s += f'{count[-1]:.2f}'
        s += ' & '
        s += f'{ypred[0]:.2f}'
        s += ' & '
        s += f'{diff:.2f}'
        s += ' \\\\'
        print(s)
    else:
        print(title)
        print(f'  Final result: {count[-1]:.2f}%')
        print(f'  First prediction: {ypred[0]:.2f}%')
        print(f'  Absolute difference: {diff:.2f}%')
    return diff


def _plot(preds, ax, labels, colors, linestyles, title, line50, row, col):
    # Get series.
    ypred = np.array([p['yes_predicted'] for p in preds])
    count = np.array([p['yes_counted'] for p in preds])
    progress = [p['counting_population'] for p in preds]
    ys = np.array([count, ypred])
    max_diff = np.max(np.abs(count - count[-1]))

    # Highlight 50%.
    if line50:
        ax.axhline(50, c='gray', linestyle='--', linewidth=2)

    # Plot prediction and averaging.
    for y, label, color, linestyle in zip(ys, labels, colors, linestyles):
        ax.plot(
            progress,
            y,
            linewidth=2,
            label=label,
            linestyle=linestyle,
            color=color,
        )
    # Draw labels.
    if col == 0:
        ax.set_ylabel('Outcome [%]')
    if row == 5:
        ax.set_xlabel('Counting progress [%]')

    # Set plot config.
    ax.set_title(title)
    ax.grid(which='both')
    if row == col == 0:
        ax.legend()

    return max_diff


def plot_predictions(fig, axes):
    data = load_data()

    # Define labels.
    labels = [
        'Averaging',
        r'\textsc{Predikon}',
    ]

    # Define colors.
    colors = [
        'black',
        'C3',
    ]

    # Define line styles.
    linestyles = [
        '-',
        '-',
    ]

    # Define grid.
    rows, cols = axes.shape
    vote_grid = np.array(
        [
            [329, 330],
            [331, 332],
            # [333, 334],
            # [335, 336],
            # [337, 338],
            [335, 338],
            [339, 340],
        ]
    )

    # define vote titles.
    titles = {
        329: 'More Affordable Housing',
        330: 'Ban of Sexual Discrimination',
        331: 'Moderate Immigration',
        332: 'Hunting Act',
        333: 'Tax Deduction of Childcare Expenses',
        334: 'Paternity Leave',
        335: 'New Fighter Aircrafts',
        336: 'Responsible Businesses',
        337: 'Ban on Financing War Material',
        338: 'Ban on Full Face Coverings',
        339: 'e-ID Act',
        340: 'Trade Agreement with Indonesia',
    }

    line50 = set([332, 335, 336, 340])

    max_diff = list()
    progress_region = list()
    progress_population = list()
    for row in range(rows):
        for col in range(cols):
            vote = vote_grid[row, col]
            max_diff.append(
                _plot(
                    data[vote],
                    axes[row, col],
                    labels,
                    colors,
                    linestyles,
                    titles[vote],
                    vote in line50,
                    row,
                    col,
                )
            )
            progress_region.append(data[vote][0]['counting_region'])
            progress_population.append(data[vote][0]['counting_population'])
    diff = list()
    for vote, preds in data.items():
        diff.append(print_statistics(preds, titles[vote], print_table=True))
    prop_reg = np.mean(progress_region)
    prop_pop = np.mean(progress_population)
    print(f'Average proportion of municipalities at 12:01pm: {prop_reg:.2f}%')
    print(f'Average proportion of population at 12:01pm: {prop_pop:.2f}%')
    print(f'Average difference with final result: {np.mean(diff):.2f}%')
    print(
        f'Max. diff. between prediction and averaging: {np.max(max_diff):.2f}%'
    )
    print(f'Average maximum difference: {np.mean(max_diff):.2f}%')


def plot(save_as=None):
    subplots = (4, 2)
    width = TEXT_WIDTH + 0.3
    height = width * 1.3
    setup_plotting(size=(width, height), subplots=subplots)

    fig, axes = plt.subplots(*subplots)
    fig.subplots_adjust(hspace=0.1)
    plot_predictions(fig, axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
