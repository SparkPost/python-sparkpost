from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
template = sp.transmission.delete('template_id')
print template
