# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- HSTORE functional test
# :Created:   gio 22 ott 2015 18:15:12 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016, 2017, 2019, 2021 Lele Gaifax
#

PYVER ?= 3.9
PYTHON3 := python$(PYVER)

.PHONY: test
test: env$(PYVER) testdbloadydb
	env$(PYVER)/bin/dbloady -u postgresql://localhost/testdbloady -s state.yaml data.yaml
	env$(PYVER)/bin/python model.py test_1
	env$(PYVER)/bin/dbloady -u postgresql://localhost/testdbloady -D state.yaml
	env$(PYVER)/bin/python model.py test_2

env$(PYVER):
	$(PYTHON3) -m venv env$(PYVER)
	env$(PYVER)/bin/pip install --upgrade pip
	env$(PYVER)/bin/pip install sqlalchemy psycopg2
	env$(PYVER)/bin/pip install -e ../.. .

.PHONY: testdbloadydb
testdbloadydb:
	dropdb --if-exists testdbloady
	createdb testdbloady
	psql -c "CREATE EXTENSION hstore" testdbloady
	env$(PYVER)/bin/python model.py setup
	rm -f state.yaml

.PHONY: clean
clean:
	dropdb --if-exists testdbloady

.PHONY: realclean
realclean: clean
	rm -rf env$(PYVER) __pycache__ testdbloady.egg-info
