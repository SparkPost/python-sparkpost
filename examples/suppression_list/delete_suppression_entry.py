from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
result = sp.suppression_list.delete('test@test.com')
print result
