from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
results = sp.suppression_list.search(
    From='2015-05-07T00:00:00+0000',
    To='2015-05-07T23:59:59+0000',
    Limit=5
)
print results
