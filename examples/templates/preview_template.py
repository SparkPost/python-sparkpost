from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')
sub_data = {
    'first_name': 'John',
    'last_name': 'Doe'
}
template = sp.transmission.preview('template_id', sub_data)
print template
