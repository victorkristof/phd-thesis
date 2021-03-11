#! /bin/sh

# Script to lint latex files given as argument.
# Usage: ./lint.sh *.tex

for file in "$@"; do
    echo "Linting $file..."
    latexindent $file > tmp.tex
    mv tmp.tex $file
done
echo "Done"
