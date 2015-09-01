from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
result = sp.recipient_lists.delete('list_id')
print result
