import os

from sparkpost import SparkPost

parent_dir = os.path.dirname(os.path.realpath(__file__))
attachment_path = os.path.abspath(os.path.join(parent_dir, "a-file.txt"))

sp = SparkPost()

response = sp.transmissions.post({
    'options': {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
    },
    'recipients': [
        'postmaster@example.com',
        'you@me.com',
        {
            'address': {
                'email': 'john.doe@example.com',
                'name': 'John Doe'
            }
        }
    ],
    'cc': ['carboncopy@example.com'],
    'bcc': ['blindcarboncopy@example.com'],
    'content': {
        'from': '"Test User" <test@sparkpostbox.com>',
        'reply_to': 'no-reply@sparkpostmail.com',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
        'attachments': [
            {
                'name': 'test.txt',
                'type': 'text/plain',
                'filename': attachment_path
            }
        ],
        'headers': {
            'X-CUSTOM-HEADER': 'foo bar'
        },
    },
    'campaign_id': 'python-sparkpost example',
    'metadata': {
        'key': 'value',
        'arbitrary': 'values'
    },
    'substitution_data': {
        'name': 'Example User'
    },
})
