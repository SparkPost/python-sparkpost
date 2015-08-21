SparkPost Python API client
===========================

.. image:: https://travis-ci.org/SparkPost/python-sparkpost.svg?branch=master
    :target: https://travis-ci.org/SparkPost/python-sparkpost
    :alt: Build Status

.. image:: https://readthedocs.org/projects/python-sparkpost/badge/?version=latest
    :target: https://readthedocs.org/projects/python-sparkpost/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/SparkPost/python-sparkpost/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/SparkPost/python-sparkpost?branch=master
    :alt: Coverage Status

The super-mega-official Python package for using the SparkPost API.


Installation
------------

Install from PyPI using `pip`_:

.. code-block:: bash

    $ pip install sparkpost

.. _pip: http://www.pip-installer.org/en/latest/

To install a pre-release version (dev, alpha, beta, rc):

.. code-block:: bash

    $ pip install --pre sparkpost

.. _pip: http://www.pip-installer.org/en/latest/


Get a key
---------

Go to `API & SMTP`_ in the SparkPost app and create an API key. We recommend using the ``SPARKPOST_API_KEY`` environment variable:

.. code-block:: python

    from sparkpost import SparkPost
    sp = SparkPost() # uses environment variable

Alternatively, you can pass the API key to the SparkPost class:

.. code-block:: python

    from sparkpost import SparkPost
    sp = SparkPost('YOUR API KEY')

.. _API & SMTP: https://app.sparkpost.com/#/configuration/credentials


Send a message
--------------

Here at SparkPost, our messages are known as transmissions. Let's use the underlying `transmissions API`_ to send a friendly test message:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.send(
        recipients=['someone@somedomain.com'],
        html='<p>Hello world</p>',
        from_email='test@sparkpostbox.com',
        subject='Hello from python-sparkpost'
    )

    print response
    # outputs {u'total_accepted_recipients': 1, u'id': u'47960765679942446', u'total_rejected_recipients': 0}

.. _transmissions API: https://www.sparkpost.com/api#/reference/transmissions


Documentation
-------------

* Documentation for `python-sparkpost`_
* `SparkPost API Reference`_

.. _python-sparkpost: http://readthedocs.org/docs/python-sparkpost
.. _SparkPost API Reference: https://www.sparkpost.com/api


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub and make your changes in a branch on your fork
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request. Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/SparkPost/python-sparkpost
.. _AUTHORS: https://github.com/SparkPost/python-sparkpost/blob/master/AUTHORS.rst
