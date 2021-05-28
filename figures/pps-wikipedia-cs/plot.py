import fire
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from thesis import save_fig, setup_plotting
from thesis.plotting import TEXT_WIDTH

# I convertd the file frwiki-dot-coldstart.pickle to data.csv using the
# following snippet:

# header = 'n_obs_u,n_obs_a,log_loss'
# with open('pps-wikipedia-cs/data.csv', 'w') as f:
#     f.write(header)
#     f.write('\n')
# with open('pps-wikipedia-cs/data.csv', 'a') as f:
#     for nu, na, ll in zip(obs_u, obs_a, -loss):
#         row = ','.join([str(nu), str(na), f'{ll:.6f}'])
#         f.write(row)
#         f.write('\n')


def load_data():
    return pd.read_csv('data.csv')


def plot_coldstart(data, ax, fig, gridsize=20):
    # Extract data
    loss = -np.array(data['log_loss'])
    obs_u = np.array(data['n_obs_u'])
    obs_a = np.array(data['n_obs_a'])

    perc = np.linspace(0.0, 100.0, num=len(loss))
    # Calling argsort twice essentially gets the (zero-based) ranks for the
    # elements of the list.
    perc_obs_u = perc[np.argsort(np.argsort(obs_u))]
    perc_obs_a = perc[np.argsort(np.argsort(obs_a))]
    img = ax.hexbin(perc_obs_u, perc_obs_a, C=loss, gridsize=gridsize)

    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_aspect('equal')
    ax.set_xlabel('User percentile')
    ax.set_ylabel('Article percentile')
    ax.set_title('Avg. log-likelihood (French Wikipedia)')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.2)
    fig.colorbar(img, cax=cax, orientation='vertical')


def plot(save_as=None):
    width = TEXT_WIDTH * 0.75
    height = width
    setup_plotting(size=(width, height))

    fig, ax = plt.subplots()
    plot_coldstart(load_data(), ax, fig)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
