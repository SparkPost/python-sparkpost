.PHONY: analysis all build clean docs docs-install docs-open install release release-test test venv

all: clean venv install

venv:
	virtualenv venv

install: venv
	. venv/bin/activate; pip install -r dev-requirements.txt
	. venv/bin/activate; pip install -e .

analysis:
	. venv/bin/activate; flake8 sparkpost test

test: analysis
	. venv/bin/activate; py.test --cov-report term-missing --cov-report html --cov sparkpost test/

docs-install:
	. venv/bin/activate; pip install -r docs/requirements.txt

docs:
	. venv/bin/activate; cd docs && make html

docs-open: docs
	. venv/bin/activate; open docs/_build/html/index.html

release: install
	. venv/bin/activate; python setup.py sdist bdist_wheel; twine upload -r pypi dist/*

release-test: install
	. venv/bin/activate; python setup.py sdist bdist_wheel; twine upload -r test dist/*

build: install
	. venv/bin/activate; python setup.py sdist
	. venv/bin/activate; python setup.py bdist_wheel

clean:
	rm -rf venv build dist *.egg-info
