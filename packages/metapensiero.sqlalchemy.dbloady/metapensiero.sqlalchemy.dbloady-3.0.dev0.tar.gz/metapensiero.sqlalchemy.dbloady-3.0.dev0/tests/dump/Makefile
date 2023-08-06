# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Dump functional test
# :Created:   gio 10 mar 2016 18:43:53 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2019, 2021 Lele Gaifax
#

PYVER ?= 3.9
PYTHON3 := python$(PYVER)

.PHONY: test
test: env$(PYVER) clean first.dump second.dump
	cmp first.dump second.dump

env$(PYVER):
	$(PYTHON3) -m venv env$(PYVER)
	env$(PYVER)/bin/pip install --upgrade pip
	env$(PYVER)/bin/pip install sqlalchemy
	env$(PYVER)/bin/pip install -e ../.. .

first.dump:
	rm -f /tmp/testdbloady.sqlite
	env$(PYVER)/bin/python model.py setup
	env$(PYVER)/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite data.yaml
	echo ".dump" | sqlite3 /tmp/testdbloady.sqlite > first.dump
	env$(PYVER)/bin/dbdumpy -u sqlite:////tmp/testdbloady.sqlite spec.yaml output.yaml

second.dump:
	rm -f /tmp/testdbloady.sqlite
	env$(PYVER)/bin/python model.py setup
	env$(PYVER)/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite output.yaml
	echo ".dump" | sqlite3 /tmp/testdbloady.sqlite > second.dump

.PHONY: clean
clean:
	rm -f /tmp/testdbloady.sqlite output.yaml first.dump second.dump

.PHONY: realclean
realclean: clean
	rm -rf env$(PYVER) __pycache__ testdbloady.egg-info
