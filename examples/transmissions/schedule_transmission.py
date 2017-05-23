from sparkpost import SparkPost

sp = SparkPost()

response = sp.transmissions.post({
    'options': {
        'sandbox': True,
        'start_time': '2015-11-06T09:10:00-05:00',
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
    'content': {
        'from': '"Test User" <test@sparkpostbox.com>',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
    },
    'campaign_id': 'python-sparkpost example',
})

print(response)
