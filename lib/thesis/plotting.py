import os
import subprocess
import tempfile

import matplotlib
from matplotlib.backends.backend_pgf import FigureCanvasPgf

GOLDEN_RATIO = (5 ** 0.5 + 1) / 2
TEXTWIDTH = 5.78  # 146.8mm = 5.78in, c.f. preamble.tex


def set_rcparams(size, factor=0.75, subplots=(1, 1)):
    # Set height and width.
    width = TEXTWIDTH
    # Scale height according to golden ratio and number of subplots.
    height = width / GOLDEN_RATIO * subplots[0] / subplots[1]

    if size == 'full' or size is None:
        figsize = (width, height)
    elif size == 'single':
        figsize = (width * factor, height * factor)
    elif type(size) is tuple:
        figsize = size
    else:
        raise ValueError(f'Size "{size}" invalid')
    return {
        "figure.autolayout": True,  # Makes sure the figure is neat & tight.
        "figure.figsize": figsize,
        "figure.dpi": 150,  # Displays figures nicely in notebooks.
        "axes.linewidth": 0.5,  # Matplotlib's current default is 0.8.
        "lines.linewidth": 1.0,
        "lines.markersize": 4,
        "xtick.major.width": 0.5,
        "xtick.minor.width": 0.5,
        "xtick.labelsize": 9,
        "ytick.major.width": 0.5,
        "ytick.minor.width": 0.5,
        "ytick.labelsize": 9,
        "text.usetex": True,  # Use LaTeX to write all text
        "font.family": "serif",  # Use serif rather than sans-serif
        "font.serif": "Latin Modern Roman",
        "font.size": 11,
        "axes.titlesize": 11,  # LaTeX default is 10pt font.
        "axes.labelsize": 9,  # LaTeX default is 10pt font.
        "legend.fontsize": 9,  # Make the legend/label fonts a little smaller
        "legend.frameon": True,  # Remove the black frame around the legend
        "pgf.texsystem": "xelatex",  # Use Xelatex which is TTF font aware
        "pgf.rcfonts": False,  # Use pgf.preamble, ignore Matplotlib RC
        "pgf.preamble": ''.join(
            [
                r'\usepackage{fontspec}',
                r'\usepackage{unicode-math}',
                r'\usepackage{lmodern}',
                r'\setmainfont{Latin Modern Math}',
                r'\setmathfont{Latin Modern Math}',
            ]
        ),
    }


def setup_plotting(size=None):
    matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)
    matplotlib.rcParams.update(set_rcparams(size))


def save_fig(fig, file_name, tight=True):
    """Saves a Matplotlib figure as PDF to the given path and crops it."""

    # Create file name.
    extension = '.pdf'
    if not file_name.endswith(extension):
        file_name += extension

    # Create tmp file for cropping.
    file_name = os.path.abspath(file_name)
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_name = tmp_file.name + extension

    # Save figure
    if tight:
        fig.savefig(tmp_name, bbox_inches='tight')
    else:
        fig.savefig(tmp_name)

    # Crop it.
    subprocess.call('pdfcrop %s %s' % (tmp_name, file_name), shell=True)

    print(f'Saved figure to {file_name}')
