from sparkpost import SparkPost

sp = SparkPost()

response = sp.transmissions.send(
    recipient_list='my_list',
    html='<p>Hello world {{name}}</p>',
    text='Hello world {{name}}',
    from_email='test@sparkpostbox.com',
    subject='Example Script',
    description='contrived example',
    custom_headers={
        'X-CUSTOM-HEADER': 'foo bar'
    },
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
