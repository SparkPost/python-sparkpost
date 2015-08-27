Recipient Lists
=============

Let's use the underlying `recipient_lists API`_ to create a recipient list:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.recipient_lists.create(
        id='UNIQUE_TEST_ID',
        name='Test Recipient list',
        recipients=[
            {
                'address': {
                    'email': 'test1@test.com'
                }
            },
            {
                'address': {
                    'email': 'test2@test.com'
                }
            },
            {
                'address': {
                    'email': 'test3@test.com'
                }
            }
        ]
    )

    print response
    # outputs {u'total_accepted_recipients': 3, u'id': u'UNIQUE_TEST_ID', u'total_rejected_recipients': 0, u'name':'Test Recipient list'}

.. _recipient_lists API: https://www.sparkpost.com/api#/reference/recipient-lists


Retrieve a recipient list
-----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.recipient_lists.get('my-list-id')


List all recipient lists
----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.recipient_lists.list()


API reference
-------------

:doc:`/api/recipient_lists`


Further examples
----------------

See the `python-sparkpost recipient_lists examples`_.

.. _python-sparkpost recipient_lists examples: https://github.com/SparkPost/python-sparkpost/tree/master/examples/recipient_lists


Additional documentation
------------------------

See the `SparkPost Recipient List API Reference`_.

.. _SparkPost Recipient Lists API Reference: https://www.sparkpost.com/api#/reference/recipient_lists
