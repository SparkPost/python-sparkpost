.. image:: https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg
    :target: https://www.sparkpost.com
    :width: 200px

`Sign up`_ for a SparkPost account and visit our `Developer Hub`_ for even more content.

.. _Sign up: https://app.sparkpost.com/sign-up?src=Dev-Website&sfdcid=70160000000pqBb
.. _Developer Hub: https://developers.sparkpost.com

SparkPost Python API client
===========================

.. image:: https://travis-ci.org/SparkPost/python-sparkpost.svg?branch=master
    :target: https://travis-ci.org/SparkPost/python-sparkpost
    :alt: Build Status

.. image:: https://readthedocs.org/projects/python-sparkpost/badge/?version=latest
    :target: https://python-sparkpost.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/SparkPost/python-sparkpost/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/SparkPost/python-sparkpost?branch=master
    :alt: Coverage Status

.. image:: http://slack.sparkpost.com/badge.svg
    :target: http://slack.sparkpost.com
    :alt: Slack Community

The super-mega-official Python package for using the SparkPost API.


Installation
------------

Install from PyPI using `pip`_:

.. code-block:: bash

    $ pip install sparkpost

.. _pip: http://www.pip-installer.org/en/latest/

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

    print(response)
    # outputs {u'total_accepted_recipients': 1, u'id': u'47960765679942446', u'total_rejected_recipients': 0}

.. _transmissions API: https://www.sparkpost.com/api#/reference/transmissions

Django Integration
------------------
The SparkPost python library comes with an email backend for Django. Put the following configuration in `settings.py` file.

.. code-block:: python

    SPARKPOST_API_KEY = 'API_KEY'
    EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'

Replace *API_KEY* with an actual API key that you've generated in `Get a Key`_ section. Check out the `full documentation`_ on the Django email backend.

.. _full documentation: https://python-sparkpost.readthedocs.io/en/latest/django/backend.html

Using with Google Cloud
-----------------------
There are a few simple modifications necessary to enable the use of the underlying ``requests`` library that python-sparkpost uses. First, add the ``requests`` and ``requests-toolbelt`` to your project's ``requirements.txt``:

.. code-block::

    requests
    requests-toolbelt

Then create or update your ``appengine_config.py`` file to include the following:

.. code-block:: python

    import requests
    import requests_toolbelt.adapters.appengine
    
    requests_toolbelt.adapters.appengine.monkeypatch()

Then deploy your app and you should be able to send using python-sparkpost on Google Cloud.

Documentation
-------------

* Documentation for `python-sparkpost`_
* `SparkPost API Reference`_

.. _python-sparkpost: https://python-sparkpost.readthedocs.io/
.. _SparkPost API Reference: https://www.sparkpost.com/api


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub and make your changes in a branch on your fork
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request. Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/SparkPost/python-sparkpost
.. _AUTHORS: https://github.com/SparkPost/python-sparkpost/blob/master/AUTHORS.rst
