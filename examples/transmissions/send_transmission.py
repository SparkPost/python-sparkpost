from sparkpost import SparkPost

sp = SparkPost()

response = sp.transmission.send(
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
    html='<p>Hello world {{name}}</p>',
    text='Hello world {{name}}',
    from_email='test@sparkpostbox.com',
    subject='Example Script',
    description='contrived example',
    custom_headers={
        'X-CUSTOM-HEADER': 'foo bar'
    },
    track_opens=True,
    track_clicks=True,
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
