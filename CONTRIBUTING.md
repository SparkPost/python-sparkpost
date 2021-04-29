# Contributing to python-sparkpost

Transparency is one of our core values, and we encourage developers to contribute and become part of the SparkPost developer community.

The following is a set of guidelines for contributing to python-sparkpost,
which is hosted in the [SparkPost Organization](https://github.com/sparkpost) on GitHub.
These are just guidelines, not rules, use your best judgment and feel free to
propose changes to this document in a pull request.

## Submitting Issues

* You can create an issue [here](https://github.com/sparkpost/python-sparkpost/issues/new), but
  before doing that please read the notes below on debugging and submitting issues,
  and include as many details as possible with your report.
* Include the version of python-sparkpost you are using.
* Perform a [cursory search](https://github.com/SparkPost/python-sparkpost/issues?q=is%3Aissue+is%3Aopen)
  to see if a similar issue has already been submitted.

## Local development

* Fork this repository
* Clone your fork
* Install virtualenv: ``pip install virtualenv``
* Run ``make install``
* Run ``source venv/bin/activate``
* Write code!

## Contribution Steps

### Guidelines

- Provide documentation for any newly added code.
- Provide tests for any newly added code.
- Follow PEP8.

1. Create a new branch named after the issue you’ll be fixing (include the issue number as the branch name, example: Issue in GH is #8 then the branch name should be ISSUE-8))
2. Write corresponding tests and code (only what is needed to satisfy the issue and tests please)
    * Include your tests in the 'test' directory in an appropriate test file
    * Write code to satisfy the tests
3. Ensure automated tests pass
4. Submit a new Pull Request applying your feature/fix branch to the develop branch

## Testing

Once you are set up for local development:

* Run ``make test`` to test against your current Python environment
* Open htmlcov/index.html to view coverage information

### Testing all version combinations

You can also test all the supported Python and dependencies versions with tox:

1. Install tox: ``pip install tox``
2. Run tox: ``tox``

If you do not have Python 2.7, 3.4, and 3.5, you can install them with pyenv:

1. Install [pyenv](https://github.com/yyuu/pyenv)
2. Install the required versions of Python:
    1. ``pyenv install 2.7.11``
    2. ``pyenv install 3.4.4``
    3. ``pyenv install 3.5.1``
3. Set the global versions: ``pyenv global 2.7.11 3.4.4 3.5.1``
4. Run tox: ``tox``

## Releasing

### Increment the library version number
* Update version number in setup.py
* Update version number in sparkpost/__init__.py
* Update CHANGELOG.md to reflect the changes

### To put python-sparkpost on PyPI

* Ensure you have maintainer privileges in PyPI
* Update your ``~/.pypirc`` if necessary to contain your username and password (hint: you can run ``python setup.py register``)
* Run ``make release``, which will create the dists and upload them to PyPI
* Confirm you are able to successfully install the new version by running ``pip install sparkpost``
