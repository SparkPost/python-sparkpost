from sparkpost import SparkPost

sp = SparkPost()
transmission_list = sp.transmission.list()
print transmission_list
