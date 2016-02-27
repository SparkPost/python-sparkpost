from sparkpost import SparkPost

sp = SparkPost()
result = sp.suppression_list.update({
    'email': 'test@test.com',
    'transactional': False,
    'non_transactional': True,
    'description': 'Test description'
})
print(result)
