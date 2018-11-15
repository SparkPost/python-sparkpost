SparkPost Python API client
===========================

The super-mega-official Python package for using the SparkPost API.


Installation
------------

Install from PyPI using `pip`_:

.. code-block:: bash

    $ pip install sparkpost

.. _pip: http://www.pip-installer.org/en/latest/


Authorization
-------------

Go to `API & SMTP`_ in the SparkPost app and create an API key. We recommend using the ``SPARKPOST_API_KEY`` environment variable:

.. code-block:: python

    from sparkpost import SparkPost
    sp = SparkPost() # uses environment variable

Alternatively, you can pass the API key to the SparkPost class:

.. code-block:: python

    from sparkpost import SparkPost
    sp = SparkPost('YOUR API KEY')

For SparkPost EU and Enterprise accounts, pass in a second parameter to set the API host.

.. code-block:: python

    from sparkpost import SparkPost
    sp = SparkPost('YOUR API KEY', 'https://api.eu.sparkpost.com/api')

.. _API & SMTP: https://app.sparkpost.com/account/api-keys


Resources
---------

The following resources are available in python-sparkpost:

.. toctree::
    :glob:
    :maxdepth: 1

    resources/*


API reference
-------------

Auto-generated API reference for python-sparkpost:

.. toctree::
    :maxdepth: 2

    api

Using in Django
---------------

Configure Django to use SparkPost email backend

.. toctree::
    :maxdepth: 2

    django/backend


Additional documentation
------------------------

The underlying SparkPost API is documented at the official `SparkPost API Reference`_.

.. _SparkPost API Reference: https://www.sparkpost.com/api


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub and make your changes in a branch on your fork
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request. Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/SparkPost/python-sparkpost
.. _AUTHORS: https://github.com/SparkPost/python-sparkpost/blob/master/AUTHORS.rst
