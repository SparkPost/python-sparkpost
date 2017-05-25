from sparkpost import SparkPost

sp = SparkPost()

response = sp.transmissions.post({
    'options': {
        'sandbox': True,
        'open_tracking': True,
        'click_tracking': True,
    },
    'recipients': 'my_list',
    'content': {
        'from': '"Test User" <test@sparkpostbox.com>',
        'subject': 'Hello from python-sparkpost',
        'text': 'Hello world!',
        'html': '<p>Hello world!</p>',
    },
    'campaign_id': 'python-sparkpost example',
})
