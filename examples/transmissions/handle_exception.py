"""
This script demonstrates how to use the SparkPostAPIException class. This
particular example will yield output similar to the following:

$ python send_transmission_exception.py
400
{u'errors': [{u'message': u'Invalid domain', u'code': u'7001', u'description':
u'Unconfigured Sending Domain <some-domain-you-havent-configured.com> '}]}
['Invalid domain Code: 7001 Description: Unconfigured Sending Domain
<some-domain-you-havent-configured.com>  \n']
"""

from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException

sp = SparkPost()

try:
    response = sp.transmissions.send(
        recipients=['john.doe@example.com'],
        text='Hello there',
        from_email='Testing <test@some-domain-you-havent-configured.com>',
        subject='Testing python-sparkpost exceptions'
    )
except SparkPostAPIException as err:
    # http response status code
    print(err.status)
    # python requests library response object
    # http://docs.python-requests.org/en/master/api/#requests.Response
    print(err.response.json())
    # list of formatted errors
    print(err.errors)
