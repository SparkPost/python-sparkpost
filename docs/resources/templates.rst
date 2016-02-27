Templates
=============

Let's use the underlying `templates API`_ to create a template:

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    response = sp.templates.create(
        id='TEST_ID',
        name='Test Template',
        from_email='test@test.com',
        subject='Test email template!',
        html='<b>This is a test email template!</b>'
    )

    print(response)
    # outputs {u'id': u'TEST_ID'}

.. _templates API: https://www.sparkpost.com/api#/reference/templates


Retrieve a template
-----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.templates.get('my-template-id')


List all templates
----------------------

.. code-block:: python

    from sparkpost import SparkPost

    sp = SparkPost()

    sp.templates.list()


API reference
-------------

:doc:`/api/templates`


Further examples
----------------

See the `python-sparkpost templates examples`_.

.. _python-sparkpost templates examples: https://github.com/SparkPost/python-sparkpost/tree/master/examples/templates


Additional documentation
------------------------

See the `SparkPost Templates API Reference`_.

.. _SparkPost Templates API Reference: https://www.sparkpost.com/api#/reference/templates
