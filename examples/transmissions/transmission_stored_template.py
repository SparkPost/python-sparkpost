from sparkpost import SparkPost

sp = SparkPost()

response = sp.transmissions.post({
    'recipients': ['someone@somedomain.com'],
    'template_id': 'my-template-id',
    'use_draft_template': True,
})
