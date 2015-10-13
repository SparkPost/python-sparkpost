from sparkpost import SparkPost

sp = SparkPost()
transmission = sp.transmission.get('transmission_id')
print transmission
