from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
transmission_list = sp.transmission.list()
print transmission_list
