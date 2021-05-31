import os
import subprocess
import tempfile

import matplotlib
from matplotlib.backends.backend_pgf import FigureCanvasPgf

GOLDEN_RATIO = (5 ** 0.5 + 1) / 2
TEXT_WIDTH = 5.78  # 146.8mm = 5.78in, c.f. preamble.tex


def _set_rcparams(size, fraction=0.85, subplots=(1, 1)):
    """Configure Matplotlib to draw figures for my thesis.

    The `size` argument can be a tuple (width, height) or a string indicating
    whether it whether the figure takes the `full` text width or a `fraction`
    of it (in which case the `fraction` can be specified). In both cases, the
    height is automatically determined using the golden ratio.
    """
    if type(size) is tuple:
        figsize = size
    else:
        # Set height and width.
        width = TEXT_WIDTH
        # Scale height according to golden ratio and number of subplots.
        height = width / GOLDEN_RATIO  # * (subplots[0] / subplots[1])

        if size == 'full' or size is None:
            figsize = (width, height)
        elif size == 'fraction':
            figsize = (width * fraction, height * fraction)
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
        "font.serif": "lmodern",
        "font.size": 11,
        "axes.titlesize": 11,  # LaTeX default is 10pt font.
        "axes.labelsize": 9,  # LaTeX default is 10pt font.
        "legend.fontsize": 9,  # Make the legend/label fonts a little smaller
        "legend.frameon": True,  # Remove the black frame around the legend
        "pgf.texsystem": "xelatex",  # Use Xelatex which is TTF font aware
        "pgf.rcfonts": False,  # Use pgf.preamble, ignore Matplotlib RC
        # The thesis's font is Latin Modern, but I cannot make it work properly
        # with Matplotlib (e.g., with `\textsc`). Using the default Computer
        # Modern is good enough, as the visual difference is imperceptible.
        "pgf.preamble": ''.join(
            [
                # r'\usepackage{fontspec}',
                # r'\usepackage{unicode-math}',
                # r'\usepackage{lmodern}',
                # r'\setmainfont{Latin Modern Math}',
                # r'\setmathfont{Latin Modern Math}',
            ]
        ),
    }


def set_aspect_ratio(ax, ratio):
    # Get x and y limits.
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    # Set aspect ratio.
    if ratio == 'golden':
        ax.set_aspect(
            abs((x_right - x_left) / (y_low - y_high)) / GOLDEN_RATIO
        )
    else:
        ax.set_aspect(ratio)


def setup_plotting(size=None, fraction=0.85, subplots=(1, 1)):
    matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)
    matplotlib.rcParams.update(_set_rcparams(size, fraction, subplots))


def save_fig(fig, file_name, tight=True, dpi=None):
    """Saves a Matplotlib figure as PDF to the given path and crops it."""

    # Create file name.
    extension = '.pdf'
    if not file_name.endswith(extension):
        file_name += extension

    # tmp_name = file_name
    # Create tmp file for cropping.
    file_name = os.path.abspath(file_name)
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_name = tmp_file.name + extension

    # Save figure
    if tight:
        fig.tight_layout()
        fig.savefig(tmp_name, dpi=dpi)
    else:
        fig.savefig(tmp_name, dpi=dpi)

    # Crop it.
    subprocess.call(
        'pdfcrop %s %s' % (tmp_name, file_name),
        shell=True,
        stdout=subprocess.DEVNULL,
    )

    print(f'Saved figure to {file_name}')
