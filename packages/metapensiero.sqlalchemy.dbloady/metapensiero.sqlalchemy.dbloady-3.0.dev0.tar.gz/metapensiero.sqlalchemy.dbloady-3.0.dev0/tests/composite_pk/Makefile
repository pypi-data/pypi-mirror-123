# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Composite PK functional test
# :Created:   lun 14 nov 2016 23:43:35 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021 Lele Gaifax
#

PYVER ?= 3.9
PYTHON3 := python$(PYVER)

.PHONY: test
test: env$(PYVER) testdbloadydb
	env$(PYVER)/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite data.yaml
	env$(PYVER)/bin/python model.py test

env$(PYVER):
	$(PYTHON3) -m venv env$(PYVER)
	env$(PYVER)/bin/pip install --upgrade pip
	env$(PYVER)/bin/pip install sqlalchemy
	env$(PYVER)/bin/pip install -e ../.. .

.PHONY: testdbloadydb
testdbloadydb:
	rm -f /tmp/testdbloady.sqlite
	env$(PYVER)/bin/python model.py setup

.PHONY: clean
clean:
	rm -f /tmp/testdbloady.sqlite

.PHONY: realclean
realclean: clean
	rm -rf env$(PYVER) __pycache__ testdbloady.egg-info
