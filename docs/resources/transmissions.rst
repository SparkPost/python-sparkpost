Transmissions
=============

Here at SparkPost, our messages are known as transmissions. Let's use the underlying `transmissions API`_ to send a friendly test message:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      options: {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
      },
      recipients: ['someone@somedomain.com'],
      content: {
        'from': 'test@sparkpostbox.com',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
      },
    })

    print(response)
    # outputs {u'total_accepted_recipients': 1, u'id': u'47960765679942446', u'total_rejected_recipients': 0}

.. _transmissions API: https://developers.sparkpost.com/api/transmissions.html


Send a transmission
-------------------

Using inline templates and/or recipients
****************************************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      options: {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
      },
      recipients: ['someone@somedomain.com'],
      content: {
        'from': 'test@sparkpostbox.com',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
      },
    })


Including cc, bcc
*****************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      options: {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
      },
      recipients: ['someone@somedomain.com'],
      cc: ['carboncopy@somedomain.com'],
      bcc: ['blindcarboncopy@somedomain.com'],
      content: {
        'from': 'test@sparkpostbox.com',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
      },
    })


Sending an attachment
*********************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      options: {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
      },
      recipients: ['someone@somedomain.com'],
      content: {
        'from': 'test@sparkpostbox.com',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
        'attachments': [
          {
              'name': 'test.txt',
              'type': 'text/plain',
              'filename': '/home/sparkpost/a-file.txt'
          }
        ]
      },
    })


Using substitution data
***********************

.. note::

   Substitution data can be specified at the template, transmission and recipient levels. The order of precedence is as follows: recipient overrides transmission overrides template.

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      options: {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
      },
      recipients: ['someone@somedomain.com'],
      content: {
        'from': 'test@sparkpostbox.com',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello {{name}}!',
        'html': '<p>Hello {{name}}!</p>',
      },
      substitution_data: {
        'name': 'Sparky'
      },
    })


Using a stored template
***********************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      recipients: ['someone@somedomain.com'],
      template_id: 'my-template-id',
    })


Using a stored recipient list
*****************************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmissions.post({
      recipients: 'my-recipient-list',
      template_id: 'my-template-id',
    })


Retrieve a transmission
-----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmissions.get('my-transmission-id')


List all transmissions
----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmissions.get()


API reference
-------------

:doc:`/api/transmissions`


Further examples
----------------

See the `python-sparkpost transmissions examples`_.

.. _python-sparkpost transmissions examples: https://github.com/SparkPost/python-sparkpost/tree/master/examples/transmissions


Additional documentation
------------------------

See the `SparkPost Transmissions API Reference`_.

.. _SparkPost Transmissions API Reference: https://developers.sparkpost.com/api/transmissions.html

