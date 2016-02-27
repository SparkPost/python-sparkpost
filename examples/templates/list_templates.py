from sparkpost import SparkPost

sp = SparkPost()
template_list = sp.templates.list()
print(template_list)
