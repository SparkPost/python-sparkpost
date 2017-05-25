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
    response = sp.transmissions.post({
        'recipients': ['john.doe@example.com'],
        'content': {
            'from': 'Testing <test@some-domain-you-havent-configured.com>',
            'subject': 'Testing python-sparkpost exceptions',
            'text': 'Hello world!',
            'html': '<p>Hello world!</p>',
        },
        'campaign_id': 'python-sparkpost example',
    })
except SparkPostAPIException as err:
    # http response status code
    print(err.status)
    # list of formatted errors
    print(err.errors)
    # python requests library response object
    # http://docs.python-requests.org/en/master/api/#requests.Response
    print(err.response.json())
    # you can loop through the errors and extract message, code, description
    for e in err.response.json()['errors']:
        error_template = "{message} Code: {code} Description: {desc} \n"
        print(error_template.format(message=e.get('message', ''),
                                    code=e.get('code', 'none'),
                                    desc=e.get('description', 'none')))
