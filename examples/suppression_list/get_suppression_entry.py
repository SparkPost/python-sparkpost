from sparkpost import SparkPost

sp = SparkPost()
entry = sp.suppression_list.get('test@test.com')
print(entry)
