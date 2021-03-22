PROJECT=thesis

# Define targets that are not related to files and folders.
.PHONY: all clean figures

all: $(PROJECT).tex $(PROJECT).bib
	pdflatex $(PROJECT)
	bibtex $(PROJECT)
	pdflatex $(PROJECT)
	pdflatex $(PROJECT)
	pdflatex $(PROJECT)

compress: $(PROJECT).pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=tmp.pdf $<
	mv tmp.pdf $<

clean:
	latexmk -c
	@rm *.bbl *.brf *.synctex* indent.log

figures:
	@./../figures/plot.sh
