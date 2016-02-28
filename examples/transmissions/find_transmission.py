from sparkpost import SparkPost

sp = SparkPost()
transmission = sp.transmissions.get('transmission_id')
print(transmission)
