#! /bin/sh

# This script plots the figures given as argument and save them in
# the text/figures/ folder to be used in Latex.
# If no arguments are given, it plots all figures.

# Get absolute path to directory of this script.
BASEDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# Get absolute path to directory of figures for thesis.
FIGDIR="$(cd "$BASEDIR/../text/figures" ; pwd -P)"

# If there are some arguments, use them to plot the figures.
if [ "$#" -gt 0 ]; then
    figures="${@}"
# If there are no arguments, plot all figures.
else
    figures=$(find -X $BASEDIR -maxdepth 1 -mindepth 1 -type d | cut -c 3- | xargs basename -a)
fi

for fig in $figures; do
    echo "Plotting $fig..."
    # Change to the directory the figure.
    cd "$BASEDIR"/"$fig"
    python plot.py --save_as $FIGDIR/$fig.pdf
    cd - &> /dev/null
done
echo "Done."
