from sparkpost import SparkPost

sp = SparkPost()
template = sp.templates.get('template_id')
print template
