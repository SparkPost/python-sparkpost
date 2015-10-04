from sparkpost import SparkPost

sp = SparkPost()
recipient_lists = sp.recipient_lists.list()
print recipient_lists
