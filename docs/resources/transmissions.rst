Transmissions
=============

Here at SparkPost, our messages are known as transmissions. Let's use the underlying `transmissions API`_ to send a friendly test message:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.transmission.send(
        recipients=['someone@somedomain.com'],
        html='<p>Hello world</p>',
        from_email='test@sparkpostbox.com',
        subject='Hello from python-sparkpost',
        track_opens=True,
        track_clicks=True
    )

    print response
    # outputs {u'total_accepted_recipients': 1, u'id': u'47960765679942446', u'total_rejected_recipients': 0}

.. _transmissions API: https://www.sparkpost.com/api#/reference/transmissions


Send a transmission
-------------------

There are several ways to send a transmission:

* Using inline templates and/or recipients
* Using a stored template
* Using a stored recipient list


Using inline templates and/or recipients
****************************************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmission.send(
        recipients=['someone@somedomain.com'],
        text="Hello world",
        html='<p>Hello world</p>',
        from_email='test@sparkpostbox.com',
        subject='Hello from python-sparkpost',
        track_opens=True,
        track_clicks=True
    )


Using a stored template
***********************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmission.send(
        recipients=['someone@somedomain.com'],
        template='my-template-id'
    )


Using a stored recipient list
*****************************

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmission.send(
        recipient_list='my-recipient-list',
        template='my-template-id'
    )


Retrieve a transmission
-----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmission.get('my-transmission-id')


List all transmissions
----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.transmission.list()


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

.. _SparkPost Transmissions API Reference: https://www.sparkpost.com/api#/reference/transmissions

