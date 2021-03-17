import matplotlib
from matplotlib.backends.backend_pgf import FigureCanvasPgf

WIDTH = 5.78  # textwidth = 146.8mm, c.f. preamble.tex
HEIGHT = 3.0


def set_rcparams(size):
    if size == 'full' or size is None:
        figsize = (WIDTH, HEIGHT)
    elif size == 'single':
        figsize = (WIDTH * 0.75, HEIGHT)
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
        "pgf.rcfonts": False,  # Use pgf.preamble, ignore standard Matplotlib RC
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
    # print("Thesis settings loaded!")
