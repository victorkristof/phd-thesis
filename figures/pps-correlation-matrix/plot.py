from collections import Counter, defaultdict

import fire
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH


def load_df():
    return pd.read_csv('data.csv')


def get_subsystems(df):
    return df[(df['subsystem'] != 'N/A') & (df['subsystem'] != '')][
        'subsystem'
    ].value_counts()


def compute_contributions(df):
    # Count user contributions to subsystems
    contributions = defaultdict(Counter)
    for row in df[['name', 'subsystem', 'accepted']].itertuples():
        contributions[row.name][row.subsystem] += 1
    return contributions


def get_correlation_matrix(contributions, subsystems):
    # Keep mappings between objects and indices
    idx2subsystem = list(subsystems.keys())
    subsystem2idx = {k: i for i, k in enumerate(idx2subsystem)}
    idx2user = list(contributions.keys())
    user2idx = {k: i for i, k in enumerate(idx2user)}

    # Extract cluster (main subsystem) for each user
    main_subsystem = [c.most_common(1)[0][0] for _, c in contributions.items()]
    useridx2cluster = [subsystem2idx[s] for s in main_subsystem]

    # Number of users
    N = len(contributions)
    # Number of subsystems
    M = len(subsystems)

    # Extract contribution vector for each cluster (subsystem)
    X_clustered = defaultdict(list)
    for i, (u, sub) in enumerate(contributions.items()):
        x = np.zeros((M))
        for s, c in sub.items():
            # Change 1 to c to compute how often a user contributes
            # to a subsystem, and not just a binary indicator
            x[subsystem2idx[s]] = 1
        X_clustered[useridx2cluster[user2idx[u]]].append(x)

    # Flatten the cluster-contributions into a matrix
    X = np.empty((N, M))
    k = 0
    clusters = sorted(X_clustered.keys())
    for cluster in clusters:
        samples = X_clustered[cluster]
        for i, x in enumerate(samples):
            X[k, :] = x
            k += 1

    # Compute and return correlation matrix
    return np.corrcoef(X)


def plot_correlation_matrix(fig, ax):

    # Prepare data.
    df = load_df()
    contributions, subsystems = compute_contributions(df), get_subsystems(df)

    # Plot correlation matrix.
    ax.imshow(get_correlation_matrix(contributions, subsystems), cmap='Greys')

    # Add blue square.
    pos = 1780
    size = 1400
    ax.add_patch(
        patches.Rectangle(
            (pos, pos),  # (x,y)
            size,  # width
            size,  # height
            ls='dotted',
            fill=False,
            lw=1.5,
            color='C0',
        )
    )
    plt.xticks([], [])
    plt.ylabel('Developer IDs')
    set_aspect_ratio(ax, 'equal')


def plot(save_as=None):
    # Make a square figure taking 75% of the width.
    width = TEXT_WIDTH * 0.75
    setup_plotting(size=(width, width))

    fig, ax = plt.subplots()
    plot_correlation_matrix(fig, ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True, dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
