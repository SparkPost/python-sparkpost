from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
results = sp.suppression_list.list(
    from_date='2015-05-07T00:00:00+0000',
    to_date='2015-05-07T23:59:59+0000',
    limit=5
)
print results
