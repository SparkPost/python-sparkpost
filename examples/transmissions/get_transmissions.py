from sparkpost import SparkPost

sp = SparkPost()
transmission_list = sp.transmissions.list()
print(transmission_list)
