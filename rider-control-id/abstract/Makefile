FILENAME_BASE = rider-id-abstract-bmd-2013
BICYCLE_BIB_PATH = /home/moorepants/Research/bicycle-mechanics/Papers/bicycle.bib

pdf:
	if [ -a $(BICYCLE_BIB_PATH)];
	then
		python /home/moorepants/bin/generate_sub_bib.py $(FILENAME_BASE).tex $(BICYCLE_BIB_PATH) references.bib
	fi
	pdflatex $(FILENAME_BASE).tex
	bibtex $(FILENAME_BASE).aux
	pdflatex $(FILENAME_BASE).tex
	pdflatex $(FILENAME_BASE).tex

clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *blg)
