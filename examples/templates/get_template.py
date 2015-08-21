from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
template = sp.transmission.get('template_id')
print template
