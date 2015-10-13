from sparkpost import SparkPost

sp = SparkPost()
result = sp.recipient_lists.delete('list_id')
print result
