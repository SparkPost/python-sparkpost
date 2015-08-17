# Contributing to python-sparkpost

Thanks for taking the time to contribute!

The following is a set of guidelines for contributing to python-sparkpost,
which is hosted in the [SparkPost Organization](https://github.com/sparkpost) on GitHub.
These are just guidelines, not rules, use your best judgment and feel free to
propose changes to this document in a pull request.

## Submitting Issues

* You can create an issue [here](https://github.com/sparkpost/python-sparkpost/issues/new), but
  before doing that please read the notes below on debugging and submitting issues,
  and include as many details as possible with your report.
* Include the version of python-sparkpost you are using.
* Perform a [cursory search](https://github.com/issues?utf8=%E2%9C%93&q=is%3Aissue+user%3Asparkpost+repo%3Apython-sparkpost)
  to see if a similar issue has already been submitted.

## Local development

* Fork the repo
* Clone your fork
* Install virtualenv: ``pip install virtualenv``
* Run ``make install``
* Run ``source venv/bin/activate``
* Write code!

## Testing

Once you are set up for local development:

* Run ``make test`` to test against your current Python environment
* Run ``tox`` to test against multiple Python environments
