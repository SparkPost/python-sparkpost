from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
recipient_lists = sp.recipient_lists.list()
print recipient_lists
