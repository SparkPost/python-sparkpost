.PHONY: analysis all build clean docs docs-install install release test venv 

all: clean venv install

venv:
	virtualenv venv

install: venv
	. venv/bin/activate; pip install -r dev-requirements.txt
	. venv/bin/activate; pip install .

analysis:
	. venv/bin/activate; flake8 sparkpost

test: analysis
	. venv/bin/activate; py.test --cov sparkpost test/

docs-install:
	. venv/bin/activate; pip install -r docs/requirements.txt

docs:
	. venv/bin/activate; cd docs && make html

release: install
	. venv/bin/activate; python setup.py sdist upload
	. venv/bin/activate; python setup.py bdist_wheel upload

build: install
	. venv/bin/activate; python setup.py sdist
	. venv/bin/activate; python setup.py bdist_wheel

clean:
	rm -rf venv
