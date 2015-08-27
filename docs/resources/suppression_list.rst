Suppression List
=============

Let's use the underlying `suppression_list API`_ to create a suppression entry:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.suppression_list.create({
      "email": "test@test.com"
      "transactional": False,
      "non_transactional": True,
      "description": "User requested to not receive any non-transactional emails."
    })

    print response
    # outputs {u'message': u'Recipient successfully created'}

.. _suppression_list API: https://www.sparkpost.com/api#/reference/suppression-list


Get a suppression entry
-----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.suppression_list.get('test@test.com')


List suppression entries
----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.suppression_list.list()


API reference
-------------

:doc:`/api/suppression_list`


Further examples
----------------

See the `python-sparkpost suppression_list examples`_.

.. _python-sparkpost suppression_list examples: https://github.com/SparkPost/python-sparkpost/tree/master/examples/suppression_list


Additional documentation
------------------------

See the `SparkPost Suppression List API Reference`_.

.. _SparkPost Suppression List API Reference: https://www.sparkpost.com/api#/reference/suppression-list
