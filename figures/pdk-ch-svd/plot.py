import pickle

import fire
import matplotlib.pyplot as plt
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import TEXT_WIDTH
from thesis.predikon_plotting import plot_svd_with_lang, svd


def load_data():
    with open('ch-votes.pkl', 'rb') as f:
        return pickle.load(f)


def plot_projection(fig, ax):

    # Load data.
    mun_votes, mun_info = load_data()

    # Filter data.
    lang_avail = ~mun_info.language.isna()
    cant_avail = ~mun_info.canton.isna()
    mun_votes = mun_votes[lang_avail & cant_avail]
    mun_info = mun_info[lang_avail & cant_avail]
    mun_info = mun_info.drop([3805, 3810])
    mun_votes = mun_votes.drop([3805, 3810])

    # Compute SVD embedding.
    embedding = svd(mun_votes.values)

    # Define colors.
    colors = {
        'fr': 'C0',
        'de': 'C1',
        'ro': 'C2',
        'it': 'C3',
        'unknown': 'black',
    }

    # Define labels.
    labels = {'fr': 'French', 'de': 'German', 'ro': 'Romansh', 'it': 'Italian'}

    # Plot.
    plot_svd_with_lang(
        embedding=embedding,
        languages=list(mun_info.language),
        colors=colors,
        labels=labels,
        fig=fig,
        ax=ax,
    )


def plot(save_as=None):
    setup_plotting(size='fraction')

    fig, ax = plt.subplots()
    plot_projection(fig, ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
