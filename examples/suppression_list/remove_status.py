from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
result = sp.suppression_list.remove_status('test@test.com')
print result
