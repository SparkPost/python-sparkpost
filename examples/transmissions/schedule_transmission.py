from sparkpost import SparkPost

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
    start_time='2015-11-06T09:10:00-05:00',
    campaign='python-sparkpost example',
    metadata={
        'key': 'value',
        'arbitrary': 'values'
    },
    substitution_data={
        'name': 'Example User'
    }
)

print(response)
