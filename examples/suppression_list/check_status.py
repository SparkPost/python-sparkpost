from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
status = sp.suppression_list.check_status('test@test.com')
print status
