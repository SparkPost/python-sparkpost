Django Email Backend
====================

SparkPost python library comes with an email backend for Django.

Configure Django
----------------

To configure Django to use SparkPost email, put the following configuration in `settings.py` file.

.. code-block:: python

    SPARKPOST_API_KEY = 'API_KEY'
    EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'

Replace *API_KEY* with an actual API key.


Sending an email
----------------

As Django is now configured to use SparkPost's email backend, we can send email simply, as you usually do, using its `send_mail` method.

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
SparkPost will support all Django versions of Django that are within extended support period. Refer to `Django Supported_Version`_.

Current supported versions are:
    * 1.7
    * 1.8
    * 1.9b1


.. _Django Supported_Version: https://www.djangoproject.com/download/#supported-versions


Additional documentation
------------------------

See the `Using SparkPost with Django`_ in support page.

.. _Using SparkPost with Django: https://support.sparkpost.com/customer/en/portal/articles/2169630-using-sparkpost-with-django?b_id=7411

