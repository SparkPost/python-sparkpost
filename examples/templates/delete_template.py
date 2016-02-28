from sparkpost import SparkPost

sp = SparkPost()
result = sp.templates.delete('template_id')
print(result)
