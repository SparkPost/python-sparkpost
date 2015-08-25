Suppression List
=============

Let's use the underlying `suppression_list API`_ to upsert a status:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.suppression_list.upsert({
      "transactional": False,
      "non_transactional": True,
      "description": "User requested to not receive any non-transactional emails."
    })

    print response
    # outputs {u'message': u'Recipient successfully created|updated'}

.. _suppression_list API: https://www.sparkpost.com/api#/reference/suppression-list


Check a Status
-----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.suppression_list.check_status('test@test.com')


Search
----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.suppression_list.search()


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
