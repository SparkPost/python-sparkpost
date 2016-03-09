import os

from sparkpost import SparkPost

parent_dir = os.path.dirname(os.path.realpath(__file__))
attachment_path = os.path.abspath(os.path.join(parent_dir, "a-file.txt"))

sp = SparkPost()

response = sp.transmissions.send(
    recipients=[
        'postmaster@example.com',
        'you@me.com',
        {
            'address': {
                'email': 'john.doe@example.com',
                'name': 'John Doe'
            }
        }
    ],
    cc=['carboncopy@example.com'],
    bcc=['blindcarboncopy@example.com'],
    html='<p>Hello {{name}}</p>',
    text='Hello {{name}}',
    from_email='Test User <test@sparkpostbox.com>',
    subject='Example Script',
    description='contrived example',
    custom_headers={
        'X-CUSTOM-HEADER': 'foo bar'
    },
    track_opens=True,
    track_clicks=True,
    attachments=[
        {
            "name": "test.txt",
            "type": "text/plain",
            "filename": attachment_path
        }
    ],
    campaign='sdk example',
    metadata={
        'key': 'value',
        'arbitrary': 'values'
    },
    substitution_data={
        'name': 'Example User'
    },
    reply_to='no-reply@sparkpostmail.com'
)
