# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- JSON functional test
# :Created:   mar 08 nov 2016 09:48:18 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021 Lele Gaifax
#

PYVER ?= 3.9
PYTHON3 := python$(PYVER)

.PHONY: test
test: env$(PYVER) testdbloadydb
	env$(PYVER)/bin/dbloady -u postgresql://localhost/testdbloady data.yaml
	env$(PYVER)/bin/python model.py test

env$(PYVER):
	$(PYTHON3) -m venv env$(PYVER)
	env$(PYVER)/bin/pip install --upgrade pip
	env$(PYVER)/bin/pip install sqlalchemy psycopg2
	env$(PYVER)/bin/pip install -e ../.. .

.PHONY: testdbloadydb
testdbloadydb:
	dropdb --if-exists testdbloady
	createdb testdbloady
	env$(PYVER)/bin/python model.py setup

.PHONY: clean
clean:
	dropdb --if-exists testdbloady

.PHONY: realclean
realclean: clean
	rm -rf env$(PYVER) __pycache__ testdbloady.egg-info
