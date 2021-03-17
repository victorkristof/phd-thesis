# Discrete-Choice Mining of Social Processes

This is the repository for my thesis, _Discrete-Choice Mining of Social Processes_.
This repo is based on the [unofficial EPFL thesis template](https://github.com/glederrey/EPFL_thesis_template), and heavily inspired from [Lucas's thesis structure](https://github.com/lucasmaystre/phd-thesis).

## Usage

Install the library (that contains code for plotting):

```
pip install -r requirements.txt
pip install -e lib
```

## Checklist for integrating chapters

While working on my thesis, I wrote a checklist of things to do to integrate a published paper as a thesis chapter.
This checklist is in `chapter-checklist.md`.
It contains snippets of code (mostly Vim commands) to make some repetitive editing easier.

## Plots

Each plot can be generated using the `plot.py` script in the corresponding folder.
In order to use the correct font, you need to make sure **Latin Modern Roman** and **Latin Modern Math** are installed on your system.
On macOS, you can install them by linking the fonts from your Latex distribution:

```
ln -s /usr/local/texlive/2020/texmf-dist/fonts/opentype/public/lm/ "/Users/kristof/Library/Fonts/Latin Modern"
ln -s /usr/local/texlive/2020/texmf-dist/fonts/opentype/public/lm-math/ "/Users/kristof/Library/Fonts/Latin Modern Math"
```

You may need to rebuild the font cache of Matplotlib:

```python
import matplotlib
matplotlib.font_manager._rebuild()
```
