FILENAME_BASE = abstract
BICYCLE_BIB_PATH = /home/moorepants/Research/bicycle-mechanics/Papers/bicycle.bib

pdf:
	python /home/moorepants/bin/generate_sub_bib.py $(FILENAME_BASE).tex $(BICYCLE_BIB_PATH) references.bib
	pdflatex abstract.tex
	bibtex abstract.aux
	pdflatex abstract.tex
	pdflatex abstract.tex

clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *blg)
