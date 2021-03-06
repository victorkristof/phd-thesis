import pickle

import fire
import matplotlib.pyplot as plt
from thesis import save_fig, set_aspect_ratio, setup_plotting
from thesis.plotting import GOLDEN_RATIO, TEXT_WIDTH
from thesis.predikon_plotting import (plot_embedding_with_canton_and_lang,
                                      plot_embedding_with_lang, tsne)


def load_data():
    with open('ch-votes.pkl', 'rb') as f:
        return pickle.load(f)


def plot_projection(fig, axes):

    # Load data.
    mun_votes, mun_info = load_data()

    # Filter data.
    lang_avail = ~mun_info.language.isna()
    cant_avail = ~mun_info.canton.isna()
    mun_votes = mun_votes[lang_avail & cant_avail]
    mun_info = mun_info[lang_avail & cant_avail]
    mun_info = mun_info.drop([3805, 3810])
    mun_votes = mun_votes.drop([3805, 3810])

    # Compute t-SNE embedding.
    seed = 13
    embedding = tsne(mun_votes.values, seed=seed)

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
    plot_embedding_with_lang(
        embedding=embedding,
        languages=list(mun_info.language),
        colors=colors,
        labels=labels,
        fig=fig,
        ax=axes[0],
    )
    set_aspect_ratio(axes[0], 'equal')
    plot_embedding_with_canton_and_lang(
        embedding=embedding,
        cantons=list(mun_info.canton),
        languages=list(mun_info.language),
        fig=fig,
        ax=axes[1],
    )
    set_aspect_ratio(axes[1], 'equal')


def plot(save_as=None):
    subplots = (1, 2)
    width = TEXT_WIDTH
    height = TEXT_WIDTH * GOLDEN_RATIO
    setup_plotting(size=(width + 0.35, height), subplots=subplots)
    # setup_plotting(size='fraction')

    fig, axes = plt.subplots(*subplots)
    plot_projection(fig, axes)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
