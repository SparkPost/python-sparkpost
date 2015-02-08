from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
trans = sp.transmission.get('transmission_id')
print trans
