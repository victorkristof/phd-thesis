#! /bin/sh

figures=../text/figures
for fig in "${@}"; do
    echo "Plotting $fig..."
    python "$fig"/plot.py --save_as $figures/$fig.pdf
done
echo "Done."
