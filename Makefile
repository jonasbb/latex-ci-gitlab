SVGS=$(wildcard figs/*.svg)
SVGS_TO_PDF=$(SVGS:.svg=.pdf)

ODGS=$(wildcard figs/raw/*.odg)
ODGS_TO_PDF=$(ODGS:figs/raw/%.odg=figs/%.pdf)
FODGS=$(wildcard figs/raw/*.fodg)
FODGS_TO_PDF=$(FODGS:figs/raw/%.fodg=figs/%.pdf)

figs_CONVERTED=$(SVGS_TO_PDF)
figs_CONVERTED+=$(ODGS_TO_PDF)
figs_CONVERTED+=$(FODGS_TO_PDF)

# Crop PDFs to the drawing area and removes empty whitespace or transparent areas
define pdfcrop
	pdfcrop --margin 0 $@ $@
endef

# Use libreoffice to convert ODG graphics into PDFs
define odg_to_pdf
	soffice -env:UserInstallation=file:///tmp/libreoffice-cli/ --convert-to pdf --headless $< --outdir figs/
	$(pdfcrop)
endef

# default target
all: figs citations pdf zip

pdf: *.tex
	latexmk -pdf -pdflatex="pdflatex --shell-escape %O %S" paper.tex

figs: $(figs_CONVERTED)

.PHONY: clean
clean:
	rm -f $(figs_CONVERTED) sources.zip paper.pdf

# convert svg to pdf
figs/%.pdf: figs/%.svg
	inkscape --export-area-drawing --export-type=pdf --export-filename=$@ $<
	$(pdfcrop)

# convert (f)odg to pdf
figs/%.pdf: figs/raw/%.odg
	$(odg_to_pdf)
figs/%.pdf: figs/raw/%.fodg
	$(odg_to_pdf)

.PHONY: citations
citations: $(wildcard *.bib)
# Guard against non-existing bib files
	@if [ "$^" != "" ]; then \
		sed -i 's/^\(\s*month\s*=\s*\)[{]\([^M]..\)[}]/\1\2/g' $^; \
	fi

.PHONY: zip
zip:
	zip -r sources.zip *.tex *.bib *.cls *.bst *.sty figs/*.pdf figs/*.svg
