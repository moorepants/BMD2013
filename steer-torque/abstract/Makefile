FILENAME_BASE = steer-torque-abstract-bmd-2013
BICYCLE_BIB_PATH = /home/moorepants/Research/bicycle-mechanics/Papers/bicycle.bib

pdf:
	python /home/moorepants/bin/generate_sub_bib.py $(FILENAME_BASE).tex $(BICYCLE_BIB_PATH) references.bib
	pdflatex $(FILENAME_BASE)
	bibtex $(FILENAME_BASE)
	pdflatex $(FILENAME_BASE)
	pdflatex $(FILENAME_BASE)

clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *blg)
