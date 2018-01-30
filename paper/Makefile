texfile = paper
bibfile = references.bib

build:
	pdflatex -interaction=nonstopmode $(texfile).tex
	bibtex $(texfile)
	pdflatex $(texfile).tex
	pdflatex $(texfile).tex

open:
	xdg-open $(texfile).pdf 2>/dev/null >/dev/null &

o: open

deps:
	# There might be more dependencies, but these were the ones I did not have installed by default
	sudo apt install texlive-bibtex-extra pdfgrep
	sudo apt-get install --no-install-recommends texlive-latex-extra

clean:
	rm $(texfile)-blx.bib *.aux *.bcf *.pdf *.log *.bbl *.blg *.out *.run.xml *.synctex.gz || :

edit:
	sensible-editor $(texfile).tex

e: edit

once:
	bibtex $(texfile)
	pdflatex -interaction=nonstopmode $(texfile).tex

buildOnChange:
	while :; do inotifywait $(texfile).tex $(bibfile); make once; done

boc: buildOnChange

check:
	grep -n --color=always -i todo $(texfile).tex || :
	@echo
	pdfgrep -n --color=always \\\?\\\? $(texfile).pdf || :
	@echo
	pdfgrep -n --color=always \!\! $(texfile).pdf || :
	@echo
	pdfgrep -n --color=always \\[[^0-9] $(texfile).pdf || :

