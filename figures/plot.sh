#! /bin/sh

# This script plots the figures given as argument and save them in
# the text/figures/ folder to be used in Latex.
# If no arguments are given, it plots all figures.

BASEDIR=$(dirname "$0")
FIGDIR="$BASEDIR"/../text/figures

# If there are some arguments, use them to plot the figures.
if [ "$#" -gt 0 ]; then
    figures="${@}"
# If there are no arguments, plot all figures.
else
    figures=$(find -X $BASEDIR -maxdepth 1 -mindepth 1 -type d | cut -c 3- | xargs basename -a)
fi

for fig in $figures; do
    echo "Plotting $fig..."
    script="$BASEDIR"/"$fig"/plot.py
    path=$FIGDIR/$fig.pdf
    python $script --save_as $path
done
echo "Done."
