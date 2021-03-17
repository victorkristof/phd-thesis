#! /bin/sh

for fig in "${@}"; do
    pdfcrop "$fig" tmp.pdf && mv tmp.pdf "$fig"
done
