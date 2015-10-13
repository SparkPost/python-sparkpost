from sparkpost import SparkPost

sp = SparkPost()

response = sp.templates.create(
    id='TEST_ID',
    name='Test Template',
    from_email='test@test.com',
    subject='Test email template!',
    html='<b>This is a test email template!</b>'
)

print response
