from sparkpost import SparkPost

sp = SparkPost()
recipients = [
    {
        'email': 'test1@test.com',
        'transactional': False,
        'non_transactional': True,
        'description': 'Test description 1'
    },
    {
        'email': 'test2@test.com',
        'transactional': True,
        'non_transactional': True,
        'description': 'Test description 2'
    },
    {
        'email': 'test3@test.com',
        'transactional': True,
        'non_transactional': False,
        'description': 'Test description 3'
    }
]
result = sp.suppression_list.create(recipients)
print(result)
