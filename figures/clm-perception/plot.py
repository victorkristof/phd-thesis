"""WARNING: This script doesn't work! The current version of Matplotlib has
a bug with ax.set_yscale('log'). It works with former versions of the library,
so I generated the plot with the notebook in
~/GitHub/climpact/papr/notebooks/plot-results.ipynb.
"""
import json

import fire
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from thesis import save_fig, set_aspect_ratio, setup_plotting


def get_json(path):
    with open(path) as f:
        data = json.load(f)
    columns = data['fields']
    values = data['values']
    return pd.DataFrame(columns=columns, data=values)


def get_X_y(answers, m=18):
    """Get the matrix X and get the vector y of an array of answers."""
    n = len(answers)  # Number of comparisons.
    X = np.zeros((n, m))
    y = np.zeros(n)

    i = 0
    for index, row in answers.iterrows():

        X[i, row['action_1_id'] - 1] = 1
        X[i, row['action_2_id'] - 1] = -1

        value = row['value']
        if value == 0:
            y[i] = 1
        elif value < 0:  # action_1 > action_2
            y[i] = -value
        else:  # action_2 > action_1
            y[i] = 1 / value
        i += 1

    return X, y


def posterior_mean(answers, actions, sigma_n=1, sigma_p=10, m=18):
    X, y = get_X_y(answers, m=m)
    v = np.array([row['cost'] for index, row in actions.iterrows()])
    c = np.mean(np.log(v))
    print(f'Prior mean: {c}')
    mu = c * np.ones(m)

    y = np.log(y)
    Xt = X.T

    # Posterior covariance matrix.
    Sp = sigma_p * np.identity(m)
    Spinv = np.linalg.inv(Sp)
    S = np.linalg.inv((Xt @ X) / sigma_n + Spinv)

    w = S.dot(Xt.dot(y) / sigma_n + Spinv.dot(mu))
    return np.exp(w)


def plot_perception(ax):
    sessions = get_json('sessions.json')
    answers = get_json('answers.json')
    actions = get_json('actions.json')
    actions = actions.rename(columns={'id': 'action_id'})

    # Keep data with more than one answers only.
    more_than_one = answers.groupby('sid_id').count().id
    more_than_one = set([t[0] for t in more_than_one.items() if t[1] > 1])
    sessions = sessions[sessions.sid.isin(more_than_one)]
    answers = answers[answers.sid_id.isin(more_than_one)]

    print(f'Number of answers: {len(answers)}')
    print(f'Number of session: {len(answers["sid_id"].unique())}')

    ages = sessions.groupby('age').count()
    prop = (ages.sid.iloc[0] + ages.sid.iloc[1]) / sum(ages.sid)
    print(f'Proportion of users in 16-25 years old: {prop*100:.2f}%')

    M = 18
    sigma_p = 10
    sigma_n = 1
    print(f'sigma_p={sigma_p}')
    print(f'sigma_n={sigma_n}')
    # Get posterior mean.
    w = posterior_mean(answers, actions, sigma_n, sigma_p, m=M)

    # Plot.
    ind = np.arange(M)
    width = 0.375

    # True values bar.
    ax.bar(
        ind,
        actions['cost'],
        width,
        label='True values',
        color='gray',
        edgecolor='black',
        zorder=3,
    )
    # Perceived values bar.
    ax.bar(
        ind + width,
        w,
        width,
        label='Perceived values',
        color='white',
        edgecolor='black',
        hatch='////',
        zorder=3,
    )
    plt.ylabel(r'KgCO\textsubscript{2}-equivalent')
    plt.xticks(ind + width / 2, ind + 1)
    plt.xlim([-0.45, 18 - 0.15])
    plt.yscale('log')
    plt.legend(loc='best')
    plt.grid(which='both', axis='y', alpha=1, linewidth=0.3)
    set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    setup_plotting(size=(5.78, 2.6))

    fig, ax = plt.subplots()
    plot_perception(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
