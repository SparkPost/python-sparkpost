Django Email Backend
====================

The SparkPost python library comes with an email backend for Django.

Configure Django
----------------

To configure Django to use SparkPost, put the following configuration in `settings.py` file.

.. code-block:: python

    SPARKPOST_API_KEY = 'API_KEY'
    EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'

Replace *API_KEY* with an actual API key.

You can also use `SPARKPOST_OPTIONS` to set options that will apply to every transmission.
For example:

.. code-block:: python

    SPARKPOST_OPTIONS = {
        'track_opens': False,
        'track_clicks': False,
        'transactional': True,
    }


Sending an email
----------------

Django is now configured to use the SparkPost email backend. You can now send mail using Django's `send_mail` method:

.. code-block:: python

    from django.core.mail import send_mail

    send_mail(
        subject='hello from sparkpost',
        message='Hello Rock stars!'
        from_email='from@yourdomain.com',
        recipient_list=['to@friendsdomain.com'],
        html_message='<p>Hello Rock stars!</p>',
    )


Supported version
-----------------
SparkPost will support all versions of Django that are within extended support period. Refer to `Django Supported_Version`_.

Current supported versions are:
    * 1.7
    * 1.8
    * 1.9b1


.. _Django Supported_Version: https://www.djangoproject.com/download/#supported-versions


Additional documentation
------------------------

See our `Using SparkPost with Django`_ in support article.

.. _Using SparkPost with Django: https://support.sparkpost.com/customer/en/portal/articles/2169630-using-sparkpost-with-django?b_id=7411

