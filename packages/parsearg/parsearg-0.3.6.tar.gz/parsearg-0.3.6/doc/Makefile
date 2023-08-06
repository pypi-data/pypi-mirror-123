VERSION := $(shell git tag | tail -1)
COMMIT  := $(shell git log | grep commit | head -1 | cut -f2 -d' ') 

SED_SCRIPT  := 's/\\date{\\today}/\\date{\\today\\hspace{0.5cm}Build\: {\\tt version_from_shell (commit_from_shell\\\!\\\!\\\!)}}/g'
SED_SCRIPT  := $(subst version_from_shell,$(VERSION),$(SED_SCRIPT))
SED_SCRIPT  := $(subst commit_from_shell,$(COMMIT),$(SED_SCRIPT))

README:     README.org 
	cp -p $@.tex tmp.tex
	sed --in-place $(SED_SCRIPT) tmp.tex
	# render browser Babel source blocks as HTML
	sed --in-place 's/\]{browser}/\]{html}/g' tmp.tex
	pdflatex -shell-escape tmp.tex
	# bibtex tmp
	pdflatex -shell-escape tmp.tex
	mv tmp.pdf $@.pdf
	# rm -f tmp.tex

parsearg:     parsearg.org 
	cp -p $@.tex tmp.tex
	sed --in-place $(SED_SCRIPT) tmp.tex
	# render browser Babel source blocks as HTML
	sed --in-place 's/\]{browser}/\]{html}/g' tmp.tex
	pdflatex -shell-escape tmp.tex
	# bibtex tmp
	pdflatex -shell-escape tmp.tex
	mv tmp.pdf $@.pdf
	# rm -f tmp.tex

clean:
	rm -f README.aux
	rm -f README.bbl
	rm -f README.blg
	rm -f README.log
	rm -f README.toc
	rm -f README.out
	rm -f parsearg.aux
	rm -f parsearg.bbl
	rm -f parsearg.blg
	rm -f parsearg.log
	rm -f parsearg.toc
	rm -f parsearg.out

scratch:     scratch.tex
	pdflatex -shell-escape $<
