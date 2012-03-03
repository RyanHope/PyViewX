SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = build

ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees -D latex_paper_size=letter $(SPHINXOPTS) .

.PHONY: clean html

egg:
	python setup.py bdist_egg

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

upload:
	python setup.py sdist bdist_egg upload

clean:
	-rm -rf $(BUILDDIR)
	-rm -rf dist
	-rm -rf *.egg-info
	-rm -rf `find . -name *.pyc`