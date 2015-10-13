from sparkpost import SparkPost

sp = SparkPost()
sub_data = {
    'first_name': 'John',
    'last_name': 'Doe'
}
template = sp.templates.preview('template_id', sub_data, True)
print template
