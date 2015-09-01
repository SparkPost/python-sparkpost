from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
entry = sp.suppression_list.get('test@test.com')
print entry
