"""
This example use the pendulum python package, which has a nice API for
datetime/timezone handling. You can use pytz or prepare your own datetimes.
"""
import pendulum
from sparkpost import SparkPost

# create a datetime for two days from now
now = pendulum.now('Europe/Paris')
now = now.add(days=2)

sp = SparkPost()

response = sp.transmissions.post({
    'options': {
        'sandbox': True,
        'start_time': now.to_iso8601_string(),
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
