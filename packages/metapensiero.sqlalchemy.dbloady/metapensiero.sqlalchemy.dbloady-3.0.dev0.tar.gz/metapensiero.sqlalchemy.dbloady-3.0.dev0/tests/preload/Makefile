# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Pre/post scripts test
# :Created:   gio 14 gen 2016 11:28:44 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021 Lele Gaifax
#

PYVER ?= 3.9
PYTHON3 := python$(PYVER)

.PHONY: test
test: env$(PYVER) testdbloadydb
	env$(PYVER)/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite \
	                        -p preload.py -P postload.py data.yaml
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
