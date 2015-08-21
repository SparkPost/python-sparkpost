from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
template_list = sp.templates.list()
print template_list
