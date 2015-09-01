from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
result = sp.templates.delete('template_id')
print result
