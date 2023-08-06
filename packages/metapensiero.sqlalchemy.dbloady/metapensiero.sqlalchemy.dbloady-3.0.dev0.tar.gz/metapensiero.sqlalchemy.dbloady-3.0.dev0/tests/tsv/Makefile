# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- TSV functional test
# :Created:   lun 24 giu 2019 18:23:05 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2019, 2021 Lele Gaifax
#

PYVER ?= 3.9
PYTHON3 := python$(PYVER)

.PHONY: test
test: env$(PYVER)
	env$(PYVER)/bin/python test.py

env$(PYVER):
	$(PYTHON3) -m venv env$(PYVER)
	env$(PYVER)/bin/pip install --upgrade pip
	env$(PYVER)/bin/pip install sqlalchemy
	env$(PYVER)/bin/pip install -e ../.. .

.PHONY: clean
clean:

.PHONY: realclean
realclean: clean
	rm -rf env$(PYVER) __pycache__ testdbloady.egg-info
