from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
recipient_list = sp.recipient_lists.get('list_id', True)
print recipient_list
