from sparkpost import SparkPost

sp = SparkPost()
response = sp.recipient_lists.create(
    id='UNIQUE_TEST_ID',
    name='Test Recipient list',
    recipients=[
        {
            'address': {
                'email': 'test1@test.com'
            }
        },
        {
            'address': {
                'email': 'test2@test.com'
            }
        },
        {
            'address': {
                'email': 'test3@test.com'
            }
        }
    ]
)
print(response)
