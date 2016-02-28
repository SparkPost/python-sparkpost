from sparkpost import SparkPost

sp = SparkPost()
result = sp.suppression_list.delete('test@test.com')
print(result)
