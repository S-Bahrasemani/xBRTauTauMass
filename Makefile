clean-pyc:
	find brtautau -name "*.pyc" -exec rm {} \;

clean-tilda:
	find brtautau -name "*~" -exec rm {} \;

clean: clean-pyc clean-tilda

clean-training:
	find log -name "*.e*" -exec rm {} \;
	find log -name "*.o*" -exec rm {} \;
	find weights -name "*.root" -exec rm {} \;
	find weights -name "*.xml" -exec rm {} \;
	find weights -name "*.C" -exec rm {} \;

montage:
	@montage -tile 4x5 -geometry 400x400+3+3 plots/*.png montage.pdf
