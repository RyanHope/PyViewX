SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = build

ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees -D latex_paper_size=letter $(SPHINXOPTS) .

.PHONY: clean html dist

dist:
	python setup.py sdist bdist_egg

upload: dist
	python setup.py sdist bdist_egg upload

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean:
	-rm -rf $(BUILDDIR)
	-rm -rf dist
	-rm -rf *.egg-info
	-rm -rf build
	-rm -rf `find . -name *.pyc`